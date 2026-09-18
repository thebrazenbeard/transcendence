import json
import unittest

from transcendence_core.integrity import (
    build_manifest,
    canonical_json_bytes,
    sha256_bytes,
    validate_portable_path,
    verify_manifest,
)
from transcendence_core.validation import (
    ValidationProblem,
    validate_bci_adapter,
    validate_continuity_lineage,
    validate_hcsa,
)


def authority(**overrides):
    value = {
        "storage": True,
        "read": True,
        "research": False,
        "training": False,
        "interpretation": True,
        "reconstruction": False,
        "activation": False,
        "replication": False,
        "disclosure": False,
    }
    value.update(overrides)
    return value


class HcsaValidationTests(unittest.TestCase):
    def test_valid_synthetic_archive(self):
        archive = {
            "schema_version": "HCSA_V0",
            "archive_id": "synthetic-person-001",
            "subject_ref": "synthetic://person/001",
            "created_at": "2026-09-17T20:00:00Z",
            "records": [
                {
                    "record_id": "raw-1",
                    "provenance": "MEASURED",
                    "source_record_ids": [],
                    "capture_method": "synthetic-fixture",
                    "captured_at": "2026-09-17T19:00:00Z",
                    "biological_interval": None,
                    "scope": "synthetic-neural-signal",
                    "payload_ref": "objects/raw-1.bin",
                    "representation": "application/octet-stream",
                    "units": None,
                    "uncertainty": 0.1,
                    "model_version": None,
                    "supersedes": None,
                    "privacy_class": "PRIVATE",
                    "authority": authority(),
                    "integrity": {"algorithm": "SHA-256", "digest": "a" * 64},
                },
                {
                    "record_id": "inferred-1",
                    "provenance": "INFERRED",
                    "source_record_ids": ["raw-1"],
                    "capture_method": None,
                    "captured_at": "2026-09-17T19:01:00Z",
                    "biological_interval": None,
                    "scope": "synthetic-interpretation",
                    "payload_ref": "objects/inferred-1.json",
                    "representation": "application/json",
                    "units": None,
                    "uncertainty": 0.4,
                    "model_version": "fixture-decoder-v1",
                    "supersedes": None,
                    "privacy_class": "PRIVATE",
                    "authority": authority(),
                    "integrity": {"algorithm": "SHA-256", "digest": "b" * 64},
                },
            ],
            "snapshots": [
                {
                    "snapshot_id": "snap-1",
                    "cutoff_at": "2026-09-17T19:02:00Z",
                    "record_ids": ["raw-1", "inferred-1"],
                    "unresolved_conflicts": [],
                    "unknowns": ["phenomenal-continuity"],
                }
            ],
        }
        self.assertEqual(validate_hcsa(archive), [])

    def test_generated_source_cannot_be_relabelled_measured(self):
        archive = {
            "schema_version": "HCSA_V0",
            "archive_id": "synthetic-person-001",
            "subject_ref": "synthetic://person/001",
            "created_at": "2026-09-17T20:00:00Z",
            "records": [
                {
                    "record_id": "generated-1",
                    "provenance": "GENERATED",
                    "source_record_ids": [],
                    "captured_at": "2026-09-17T19:00:00Z",
                    "payload_ref": "objects/generated.json",
                    "privacy_class": "PRIVATE",
                    "authority": authority(),
                    "integrity": {"algorithm": "SHA-256", "digest": "a" * 64},
                },
                {
                    "record_id": "fake-measured",
                    "provenance": "MEASURED",
                    "source_record_ids": ["generated-1"],
                    "captured_at": "2026-09-17T19:01:00Z",
                    "payload_ref": "objects/fake.bin",
                    "privacy_class": "PRIVATE",
                    "authority": authority(),
                    "integrity": {"algorithm": "SHA-256", "digest": "b" * 64},
                },
            ],
            "snapshots": [],
        }
        problems = validate_hcsa(archive)
        self.assertTrue(any("provenance promotion" in p.message for p in problems))


class BciValidationTests(unittest.TestCase):
    def test_read_only_adapter_needs_no_effect_authority(self):
        manifest = {
            "schema_version": "BCI_ADAPTER_V0",
            "adapter_id": "synthetic-readonly",
            "adapter_version": "0.0.1",
            "direction": "ACQUIRE_ONLY",
            "modalities": ["synthetic-electrophysiology"],
            "raw_representation": "application/x.synthetic-signal",
            "normalization": {"version": "v1", "preserves_raw_reference": True},
            "decoder": {
                "version": "synthetic-decoder-v1",
                "interpretation_provenance": "INFERRED",
            },
            "uncertainty_model": "synthetic",
            "effect_capabilities": [],
            "effect_authority_scope": None,
        }
        self.assertEqual(validate_bci_adapter(manifest), [])

    def test_effect_capable_adapter_requires_authority_scope(self):
        manifest = {
            "schema_version": "BCI_ADAPTER_V0",
            "adapter_id": "synthetic-bidir",
            "adapter_version": "0.0.1",
            "direction": "BIDIRECTIONAL",
            "modalities": ["synthetic-electrophysiology"],
            "raw_representation": "application/x.synthetic-signal",
            "normalization": {"version": "v1", "preserves_raw_reference": True},
            "uncertainty_model": "synthetic",
            "effect_capabilities": ["synthetic-stimulation"],
            "effect_authority_scope": None,
        }
        problems = validate_bci_adapter(manifest)
        self.assertTrue(any("effect authority" in p.message for p in problems))


class LineageValidationTests(unittest.TestCase):
    def test_fork_requires_multiple_descendants(self):
        lineage = {
            "schema_version": "CONTINUITY_LINEAGE_V0",
            "lineage_id": "synthetic-lineage",
            "events": [
                {
                    "event_id": "fork-1",
                    "event_type": "FORK",
                    "occurred_at": "2026-09-17T20:00:00Z",
                    "predecessor_snapshot_ids": ["snap-0"],
                    "descendant_snapshot_ids": ["snap-1"],
                    "substrates": [],
                    "evidence_refs": [],
                    "continuity_claims": [],
                    "unresolved_questions": [],
                }
            ],
        }
        problems = validate_continuity_lineage(lineage)
        self.assertTrue(any("at least two descendants" in p.message for p in problems))

    def test_gradual_transfer_requires_overlapping_biological_and_nonbiological_substrates(self):
        lineage = {
            "schema_version": "CONTINUITY_LINEAGE_V0",
            "lineage_id": "synthetic-lineage",
            "events": [
                {
                    "event_id": "gradual-1",
                    "event_type": "GRADUAL_TRANSFER",
                    "occurred_at": "2026-09-17T20:00:00Z",
                    "predecessor_snapshot_ids": ["snap-0"],
                    "descendant_snapshot_ids": ["snap-1"],
                    "substrates": [
                        {
                            "substrate_id": "bio",
                            "substrate_class": "BIOLOGICAL",
                            "role": "OVERLAPPING_ACTIVE",
                            "interval": "t0/t1",
                        },
                        {
                            "substrate_id": "synthetic",
                            "substrate_class": "SYNTHETIC",
                            "role": "OVERLAPPING_ACTIVE",
                            "interval": "t0/t1",
                        },
                    ],
                    "evidence_refs": ["synthetic-evidence"],
                    "continuity_claims": [
                        {
                            "dimension": "PHENOMENAL",
                            "status": "UNKNOWN",
                            "evidence_refs": [],
                        }
                    ],
                    "unresolved_questions": ["phenomenal-continuity"],
                }
            ],
        }
        self.assertEqual(validate_continuity_lineage(lineage), [])


class IntegrityTests(unittest.TestCase):
    def test_canonical_hash_is_key_order_stable(self):
        a = canonical_json_bytes({"b": 2, "a": 1})
        b = canonical_json_bytes({"a": 1, "b": 2})
        self.assertEqual(a, b)
        self.assertEqual(sha256_bytes(a), sha256_bytes(b))

    def test_manifest_detects_tampering(self):
        files = {
            "objects/a.json": b'{"synthetic":true}',
            "objects/b.bin": b"abc",
        }
        manifest = build_manifest(
            archive_id="synthetic-person-001",
            files=files,
            created_at="2026-09-17T20:00:00Z",
        )
        self.assertEqual(verify_manifest(manifest, files), [])
        tampered = dict(files)
        tampered["objects/b.bin"] = b"abd"
        self.assertTrue(verify_manifest(manifest, tampered))

    def test_portable_paths_reject_traversal(self):
        for bad in ("../secret", "/absolute", "a/../../b", "C:\\private\\x"):
            with self.assertRaises(ValueError):
                validate_portable_path(bad)


if __name__ == "__main__":
    unittest.main()
