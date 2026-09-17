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


class TranscendenceCoreTests(unittest.TestCase):
    def test_canonical_hash_is_key_order_stable(self):
        self.assertEqual(sha256_json({"b": 2, "a": 1}), sha256_json({"a": 1, "b": 2}))
        self.assertEqual(canonical_json_bytes({"b": 2, "a": 1}), b'{"a":1,"b":2}')

    def test_valid_synthetic_hcsa(self):
        doc = {
            "schema_version": "HCSA-V0",
            "archive_id": "synthetic-subject-001",
            "records": [{
                "record_id": "rec-1",
                "archive_id": "synthetic-subject-001",
                "provenance_class": "MEASURED",
                "source_artifact_ids": ["synthetic-signal-1"],
                "observed_at": "2040-01-01T00:00:00Z",
                "payload_ref": "objects/aa/record.bin",
                "privacy_classification": "PRIVATE_SUBJECT",
                "authority_scope": {"storage": True, "research": False},
                "integrity_digest": "0" * 64,
                "provenance_history": [],
            }],
        }
        validate_hcsa(doc)

    def test_generated_evidence_cannot_be_promoted_to_measured(self):
        doc = {
            "schema_version": "HCSA-V0",
            "archive_id": "synthetic",
            "records": [{
                "record_id": "rec-1",
                "archive_id": "synthetic",
                "provenance_class": "MEASURED",
                "source_artifact_ids": [],
                "observed_at": "2040-01-01T00:00:00Z",
                "payload_ref": "objects/1",
                "privacy_classification": "PRIVATE_SUBJECT",
                "authority_scope": {},
                "integrity_digest": "0" * 64,
                "provenance_history": [{"from": "GENERATED", "to": "MEASURED"}],
            }],
        }
        with self.assertRaises(ValidationError):
            validate_hcsa(doc)

    def test_read_only_bci_adapter(self):
        validate_bci_adapter({
            "schema_version": "BCI-ADAPTER-V0",
            "adapter_id": "synthetic-eeg",
            "adapter_version": "0.1",
            "direction": "ACQUIRE",
            "modalities": ["electrophysiology"],
            "raw_representation": "application/octet-stream",
        })

    def test_effect_bci_requires_authority_scope(self):
        with self.assertRaises(ValidationError):
            validate_bci_adapter({
                "schema_version": "BCI-ADAPTER-V0",
                "adapter_id": "synthetic-bidir",
                "adapter_version": "0.1",
                "direction": "BIDIRECTIONAL",
                "modalities": ["electrophysiology", "stimulation"],
                "raw_representation": "application/octet-stream",
                "effect_capabilities": ["synthetic-stimulation"],
            })

    def test_fork_requires_multiple_descendants(self):
        base = {
            "schema_version": "CONTINUITY-LINEAGE-V0",
            "events": [{
                "event_id": "event-1",
                "event_type": "FORK",
                "occurred_at": "2040-01-01T00:00:00Z",
                "predecessor_snapshot_ids": ["snap-0"],
                "descendant_snapshot_ids": ["snap-1"],
                "substrates": ["synthetic-a"],
                "continuity_claims": {},
            }],
        }
        with self.assertRaises(ValidationError):
            validate_lineage(base)

    def test_gradual_transfer_requires_multiple_substrates_and_keeps_phenomenal_unknown(self):
        valid = {
            "schema_version": "CONTINUITY-LINEAGE-V0",
            "events": [{
                "event_id": "event-1",
                "event_type": "GRADUAL_TRANSFER",
                "occurred_at": "2040-01-01T00:00:00Z",
                "predecessor_snapshot_ids": ["snap-0"],
                "descendant_snapshot_ids": ["snap-1"],
                "substrates": ["biological", "synthetic"],
                "continuity_claims": {
                    "TEMPORAL_PROCESS": {"status": "SUPPORTED", "evidence_refs": ["ev-1"]},
                    "PHENOMENAL_SUBJECTIVE": {"status": "UNKNOWN", "evidence_refs": []},
                },
            }],
        }
        validate_lineage(valid)
        invalid = json.loads(json.dumps(valid))
        invalid["events"][0]["continuity_claims"]["PHENOMENAL_SUBJECTIVE"]["status"] = "PROVEN"
        with self.assertRaises(ValidationError):
            validate_lineage(invalid)

    def test_integrity_manifest_detects_tampering(self):
        files = {"objects/a.bin": b"abc", "metadata/archive.json": b"{}"}
        manifest = build_integrity_manifest(files)
        ok, errors = verify_integrity_manifest(files, manifest)
        self.assertTrue(ok, errors)
        tampered = dict(files)
        tampered["objects/a.bin"] = b"abcd"
        ok, errors = verify_integrity_manifest(tampered, manifest)
        self.assertFalse(ok)
        self.assertTrue(any("digest mismatch" in item for item in errors))

    def test_portability_rejects_path_traversal(self):
        with self.assertRaises(ValidationError):
            validate_portable_path("../private")
        with self.assertRaises(ValidationError):
            validate_portable_path("/absolute")
        with self.assertRaises(ValidationError):
            validate_portable_path("..\\private")


if __name__ == "__main__":
    unittest.main()
