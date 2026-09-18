import json
import unittest

from core import (
    ValidationError,
    build_integrity_manifest,
    canonical_json_bytes,
    sha256_json,
    validate_bci_adapter,
    validate_hcsa,
    validate_lineage,
    validate_portable_path,
    verify_integrity_manifest,
)


def authority_scope(**overrides):
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


class TranscendenceCoreTests(unittest.TestCase):
    def test_canonical_hash_is_key_order_stable(self):
        self.assertEqual(sha256_json({"b": 2, "a": 1}), sha256_json({"a": 1, "b": 2}))
        self.assertEqual(canonical_json_bytes({"b": 2, "a": 1}), b'{"a":1,"b":2}')

    def test_valid_synthetic_hcsa_with_snapshot(self):
        doc = {
            "schema_version": "HCSA-V0",
            "archive_id": "synthetic-subject-001",
            "subject_ref": "synthetic://subject/001",
            "created_at": "2040-01-01T00:00:00Z",
            "records": [
                {
                    "record_id": "rec-1",
                    "archive_id": "synthetic-subject-001",
                    "provenance_class": "MEASURED",
                    "source_artifact_ids": ["synthetic-signal-1"],
                    "observed_at": "2040-01-01T00:00:00Z",
                    "capture_method": "synthetic-fixture",
                    "biological_interval": None,
                    "scope": "synthetic-neural-signal",
                    "payload_ref": "objects/aa/record.bin",
                    "representation": "application/octet-stream",
                    "units": None,
                    "uncertainty": 0.1,
                    "model_version": None,
                    "privacy_classification": "PRIVATE_SUBJECT",
                    "authority_scope": authority_scope(),
                    "integrity_digest": "0" * 64,
                    "provenance_history": [],
                    "transformation": None,
                    "supersedes": None,
                },
                {
                    "record_id": "rec-2",
                    "archive_id": "synthetic-subject-001",
                    "provenance_class": "INFERRED",
                    "source_artifact_ids": ["synthetic-signal-1"],
                    "observed_at": "2040-01-01T00:01:00Z",
                    "payload_ref": "objects/aa/inferred.json",
                    "privacy_classification": "PRIVATE_SUBJECT",
                    "authority_scope": authority_scope(),
                    "integrity_digest": "1" * 64,
                    "provenance_history": [],
                    "transformation": {
                        "input_record_ids": ["rec-1"],
                        "method_version": "synthetic-decoder-v1",
                        "information_discarded": None,
                    },
                    "supersedes": None,
                },
            ],
            "snapshots": [
                {
                    "snapshot_id": "snap-1",
                    "cutoff_at": "2040-01-01T00:02:00Z",
                    "record_ids": ["rec-1", "rec-2"],
                    "unresolved_conflicts": [],
                    "unknowns": ["phenomenal-continuity"],
                }
            ],
        }
        validate_hcsa(doc)

    def test_generated_evidence_cannot_be_promoted_to_measured(self):
        doc = {
            "schema_version": "HCSA-V0",
            "archive_id": "synthetic",
            "subject_ref": "synthetic://subject/001",
            "created_at": "2040-01-01T00:00:00Z",
            "records": [
                {
                    "record_id": "rec-1",
                    "archive_id": "synthetic",
                    "provenance_class": "MEASURED",
                    "source_artifact_ids": [],
                    "observed_at": "2040-01-01T00:00:00Z",
                    "payload_ref": "objects/1",
                    "privacy_classification": "PRIVATE_SUBJECT",
                    "authority_scope": authority_scope(),
                    "integrity_digest": "0" * 64,
                    "provenance_history": [{"from": "GENERATED", "to": "MEASURED"}],
                }
            ],
            "snapshots": [],
        }
        with self.assertRaises(ValidationError):
            validate_hcsa(doc)

    def test_transformation_cannot_promote_generated_record_to_measured(self):
        doc = {
            "schema_version": "HCSA-V0",
            "archive_id": "synthetic",
            "subject_ref": "synthetic://subject/001",
            "created_at": "2040-01-01T00:00:00Z",
            "records": [
                {
                    "record_id": "gen-1",
                    "archive_id": "synthetic",
                    "provenance_class": "GENERATED",
                    "source_artifact_ids": [],
                    "observed_at": "2040-01-01T00:00:00Z",
                    "payload_ref": "objects/gen",
                    "privacy_classification": "PRIVATE_SUBJECT",
                    "authority_scope": authority_scope(),
                    "integrity_digest": "0" * 64,
                    "provenance_history": [],
                    "transformation": {
                        "input_record_ids": [],
                        "method_version": "fixture-v1",
                        "information_discarded": None,
                    },
                },
                {
                    "record_id": "fake-measured",
                    "archive_id": "synthetic",
                    "provenance_class": "MEASURED",
                    "source_artifact_ids": [],
                    "observed_at": "2040-01-01T00:01:00Z",
                    "payload_ref": "objects/fake",
                    "privacy_classification": "PRIVATE_SUBJECT",
                    "authority_scope": authority_scope(),
                    "integrity_digest": "1" * 64,
                    "provenance_history": [],
                    "transformation": {
                        "input_record_ids": ["gen-1"],
                        "method_version": "fixture-v1",
                        "information_discarded": None,
                    },
                },
            ],
            "snapshots": [],
        }
        with self.assertRaises(ValidationError):
            validate_hcsa(doc)

    def test_read_only_bci_adapter_preserves_raw_reference(self):
        validate_bci_adapter(
            {
                "schema_version": "BCI-ADAPTER-V0",
                "adapter_id": "synthetic-eeg",
                "adapter_version": "0.1",
                "direction": "ACQUIRE",
                "modalities": ["electrophysiology"],
                "raw_representation": "application/octet-stream",
                "normalization": {"version": "v1", "preserves_raw_reference": True},
                "decoder": {
                    "version": "fixture-decoder-v1",
                    "interpretation_provenance": "INFERRED",
                },
                "uncertainty_model": "synthetic",
                "effect_capabilities": [],
                "effect_authority_scope": None,
                "subject_state_context": None,
            }
        )

    def test_decoder_interpretation_cannot_claim_measured_provenance(self):
        with self.assertRaises(ValidationError):
            validate_bci_adapter(
                {
                    "schema_version": "BCI-ADAPTER-V0",
                    "adapter_id": "synthetic-eeg",
                    "adapter_version": "0.1",
                    "direction": "ACQUIRE",
                    "modalities": ["electrophysiology"],
                    "raw_representation": "application/octet-stream",
                    "normalization": {"version": "v1", "preserves_raw_reference": True},
                    "decoder": {
                        "version": "fixture-decoder-v1",
                        "interpretation_provenance": "MEASURED",
                    },
                    "uncertainty_model": "synthetic",
                    "effect_capabilities": [],
                    "effect_authority_scope": None,
                    "subject_state_context": None,
                }
            )

    def test_effect_bci_requires_scoped_effect_authority(self):
        with self.assertRaises(ValidationError):
            validate_bci_adapter(
                {
                    "schema_version": "BCI-ADAPTER-V0",
                    "adapter_id": "synthetic-bidir",
                    "adapter_version": "0.1",
                    "direction": "BIDIRECTIONAL",
                    "modalities": ["electrophysiology", "stimulation"],
                    "raw_representation": "application/octet-stream",
                    "normalization": {"version": "v1", "preserves_raw_reference": True},
                    "decoder": None,
                    "uncertainty_model": "synthetic",
                    "effect_capabilities": ["synthetic-stimulation"],
                    "effect_authority_scope": None,
                    "subject_state_context": None,
                }
            )

    def test_fork_requires_multiple_descendants(self):
        base = {
            "schema_version": "CONTINUITY-LINEAGE-V0",
            "lineage_id": "synthetic-lineage",
            "events": [
                {
                    "event_id": "event-1",
                    "event_type": "FORK",
                    "occurred_at": "2040-01-01T00:00:00Z",
                    "predecessor_snapshot_ids": ["snap-0"],
                    "descendant_snapshot_ids": ["snap-1"],
                    "substrates": [],
                    "evidence_refs": [],
                    "continuity_claims": {},
                    "unresolved_questions": [],
                }
            ],
        }
        with self.assertRaises(ValidationError):
            validate_lineage(base)

    def test_gradual_transfer_requires_biological_and_nonbiological_overlap(self):
        valid = {
            "schema_version": "CONTINUITY-LINEAGE-V0",
            "lineage_id": "synthetic-lineage",
            "events": [
                {
                    "event_id": "event-1",
                    "event_type": "GRADUAL_TRANSFER",
                    "occurred_at": "2040-01-01T00:00:00Z",
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
                    "continuity_claims": {
                        "TEMPORAL_PROCESS": {
                            "status": "SUPPORTED",
                            "evidence_refs": ["synthetic-evidence"],
                        },
                        "PHENOMENAL_SUBJECTIVE": {
                            "status": "UNKNOWN",
                            "evidence_refs": [],
                        },
                    },
                    "unresolved_questions": ["phenomenal-continuity"],
                }
            ],
        }
        validate_lineage(valid)
        invalid = json.loads(json.dumps(valid))
        invalid["events"][0]["substrates"][1]["role"] = "TARGET"
        with self.assertRaises(ValidationError):
            validate_lineage(invalid)

    def test_phenomenal_continuity_cannot_be_promoted_to_proven_in_v0(self):
        lineage = {
            "schema_version": "CONTINUITY-LINEAGE-V0",
            "lineage_id": "synthetic-lineage",
            "events": [
                {
                    "event_id": "restore-1",
                    "event_type": "RESTORE",
                    "occurred_at": "2040-01-01T00:00:00Z",
                    "predecessor_snapshot_ids": ["snap-0"],
                    "descendant_snapshot_ids": ["snap-1"],
                    "substrates": [
                        {
                            "substrate_id": "synthetic",
                            "substrate_class": "SYNTHETIC",
                            "role": "TARGET",
                            "interval": None,
                        }
                    ],
                    "evidence_refs": [],
                    "continuity_claims": {
                        "PHENOMENAL_SUBJECTIVE": {
                            "status": "SUPPORTED",
                            "evidence_refs": [],
                        }
                    },
                    "unresolved_questions": [],
                }
            ],
        }
        with self.assertRaises(ValidationError):
            validate_lineage(lineage)

    def test_integrity_manifest_detects_tampering_and_unmanifested_files(self):
        files = {"objects/a.bin": b"abc", "metadata/archive.json": b"{}"}
        manifest = build_integrity_manifest(files)
        ok, errors = verify_integrity_manifest(files, manifest)
        self.assertTrue(ok, errors)

        tampered = dict(files)
        tampered["objects/a.bin"] = b"abcd"
        ok, errors = verify_integrity_manifest(tampered, manifest)
        self.assertFalse(ok)
        self.assertTrue(any("digest mismatch" in item for item in errors))

        extra = dict(files)
        extra["objects/unlisted.bin"] = b"x"
        ok, errors = verify_integrity_manifest(extra, manifest)
        self.assertFalse(ok)
        self.assertTrue(any("undeclared file" in item for item in errors))

    def test_portability_rejects_path_traversal_and_platform_paths(self):
        for bad in ("../private", "/absolute", "..\\private", "C:\\private\\x"):
            with self.assertRaises(ValidationError):
                validate_portable_path(bad)


if __name__ == "__main__":
    unittest.main()
