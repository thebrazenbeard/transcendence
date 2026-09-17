import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "tools" / "hcsa" / "validate_hcsa.py"

def valid_archive():
    return {
        "schema_id": "TRANSCENDENCE_HCSA_V0",
        "archive_id": "hcsa:synthetic-example",
        "subject_ref": "subject:pseudonymous-example",
        "archive_version": 1,
        "created_at": "2026-09-17T22:30:00Z",
        "records": [
            {
                "record_id": "rec:structural:1",
                "provenance_class": "MEASURED",
                "domain": "STRUCTURAL",
                "temporal_scope": {"instant": "2026-09-17T22:00:00Z"},
                "acquisition": {"method": "synthetic-test", "adapter_id": "adapter:test"},
                "payload_ref": {
                    "media_type": "application/octet-stream",
                    "digest": "sha256:" + "a" * 64,
                    "uri": "artifact://synthetic/structural-1"
                },
                "source_record_ids": [],
                "authority_ref": "authority:subject-controlled"
            }
        ],
        "snapshots": [
            {
                "snapshot_id": "snapshot:1",
                "record_ids": ["rec:structural:1"],
                "created_at": "2026-09-17T22:31:00Z",
                "unknown_coverage": ["effective-connectivity not captured"]
            }
        ],
        "lineage": []
    }

class HCSAValidatorTests(unittest.TestCase):
    def run_validator(self, data):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "archive.json"
            p.write_text(json.dumps(data), encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(SCRIPT), str(p)],
                text=True,
                capture_output=True,
            )

    def assert_invalid(self, data, needle):
        result = self.run_validator(data)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(needle, result.stderr)

    def test_accepts_minimal_measured_archive(self):
        result = self.run_validator(valid_archive())
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)

    def test_rejects_unknown_provenance_class(self):
        data = valid_archive()
        data["records"][0]["provenance_class"] = "MAGIC"
        self.assert_invalid(data, "provenance_class")

    def test_requires_transformation_for_inferred_state(self):
        data = valid_archive()
        data["records"][0]["provenance_class"] = "INFERRED"
        data["records"][0].pop("acquisition")
        self.assert_invalid(data, "transformation")

    def test_rejects_transformation_on_measured_state(self):
        data = valid_archive()
        data["records"][0]["transformation"] = {
            "method_id": "model:test",
            "input_record_ids": [],
            "information_discarded": []
        }
        self.assert_invalid(data, "MEASURED")

    def test_rejects_missing_local_source_record(self):
        data = valid_archive()
        data["records"][0]["source_record_ids"] = ["rec:missing"]
        self.assert_invalid(data, "source_record_ids")

    def test_rejects_self_supersession(self):
        data = valid_archive()
        data["records"][0]["supersedes"] = ["rec:structural:1"]
        self.assert_invalid(data, "supersedes")

    def test_rejects_snapshot_reference_to_missing_record(self):
        data = valid_archive()
        data["snapshots"][0]["record_ids"] = ["rec:missing"]
        self.assert_invalid(data, "snapshots")

    def test_rejects_duplicate_record_ids(self):
        data = valid_archive()
        data["records"].append(copy.deepcopy(data["records"][0]))
        self.assert_invalid(data, "duplicate record_id")

    def test_rejects_unknown_lineage_operation(self):
        data = valid_archive()
        data["lineage"] = [{
            "operation_id": "op:1",
            "operation": "TELEPORT",
            "occurred_at": "2026-09-17T22:32:00Z",
            "parent_snapshot_ids": ["snapshot:1"],
            "child_snapshot_ids": ["snapshot:1"]
        }]
        self.assert_invalid(data, "lineage")

if __name__ == "__main__":
    unittest.main()
