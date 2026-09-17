import json
import re
import sys
from pathlib import Path

SCHEMA_ID = "TRANSCENDENCE_HCSA_V0"
PROVENANCE = {
    "MEASURED",
    "BEHAVIORALLY_OBSERVED",
    "SELF_REPORTED",
    "DERIVED",
    "INFERRED",
    "INTERPOLATED",
    "GENERATED",
    "IMPORTED_REFERENCE",
    "UNKNOWN",
}
TRANSFORMED = {"DERIVED", "INFERRED", "INTERPOLATED", "GENERATED"}
DIRECT = {"MEASURED", "BEHAVIORALLY_OBSERVED", "SELF_REPORTED", "IMPORTED_REFERENCE"}
DOMAINS = {
    "STRUCTURAL",
    "EFFECTIVE_CONNECTIVITY",
    "CELLULAR_MOLECULAR",
    "DYNAMIC_NEURAL",
    "EMBODIED_REGULATORY",
    "COGNITIVE_PHENOTYPE",
    "LONGITUDINAL_SHADOW",
    "BCI_RAW",
    "BCI_NORMALIZED",
    "OTHER",
}
LINEAGE_OPS = {
    "BACKUP",
    "RESTORE",
    "SUCCESSOR",
    "FORK",
    "MIGRATION",
    "GRADUAL_TRANSFER",
}
SHA256 = re.compile(r"^sha256:[0-9a-f]{64}$")

def nonempty(value):
    return isinstance(value, str) and bool(value.strip())

def _validate_payload_ref(payload, prefix, errors):
    if not isinstance(payload, dict):
        errors.append(f"{prefix}.payload_ref must be an object")
        return
    if not nonempty(payload.get("media_type")):
        errors.append(f"{prefix}.payload_ref.media_type must be a non-empty string")
    if not isinstance(payload.get("digest"), str) or not SHA256.fullmatch(payload["digest"]):
        errors.append(f"{prefix}.payload_ref.digest must be sha256:<64 lowercase hex>")
    if "uri" in payload and not nonempty(payload.get("uri")):
        errors.append(f"{prefix}.payload_ref.uri must be a non-empty string when present")

def _validate_transformation(transformation, prefix, record_ids, errors):
    if not isinstance(transformation, dict):
        errors.append(f"{prefix}.transformation must be an object")
        return
    if not nonempty(transformation.get("method_id")):
        errors.append(f"{prefix}.transformation.method_id must be a non-empty string")
    inputs = transformation.get("input_record_ids")
    if not isinstance(inputs, list):
        errors.append(f"{prefix}.transformation.input_record_ids must be a list")
    else:
        for rid in inputs:
            if rid not in record_ids:
                errors.append(f"{prefix}.transformation.input_record_ids references missing record {rid!r}")
    discarded = transformation.get("information_discarded")
    if not isinstance(discarded, list):
        errors.append(f"{prefix}.transformation.information_discarded must be a list")

def validate_hcsa(data):
    errors = []
    if data.get("schema_id") != SCHEMA_ID:
        errors.append(f"schema_id must equal {SCHEMA_ID}")
    for field in ("archive_id", "subject_ref", "created_at"):
        if not nonempty(data.get(field)):
            errors.append(f"{field} must be a non-empty string")
    if not isinstance(data.get("archive_version"), int) or data["archive_version"] < 1:
        errors.append("archive_version must be an integer >= 1")

    records = data.get("records")
    if not isinstance(records, list) or not records:
        errors.append("records must be a non-empty list")
        records = []

    ids = []
    for record in records:
        if isinstance(record, dict):
            ids.append(record.get("record_id"))
    seen = set()
    record_ids = set()
    for rid in ids:
        if not nonempty(rid):
            continue
        if rid in seen:
            errors.append(f"duplicate record_id {rid!r}")
        seen.add(rid)
        record_ids.add(rid)

    for i, record in enumerate(records):
        prefix = f"records[{i}]"
        if not isinstance(record, dict):
            errors.append(f"{prefix} must be an object")
            continue
        rid = record.get("record_id")
        if not nonempty(rid):
            errors.append(f"{prefix}.record_id must be a non-empty string")

        provenance = record.get("provenance_class")
        if provenance not in PROVENANCE:
            errors.append(f"{prefix}.provenance_class is invalid: {provenance!r}")

        domain = record.get("domain")
        if domain not in DOMAINS:
            errors.append(f"{prefix}.domain is invalid: {domain!r}")

        temporal = record.get("temporal_scope")
        if not isinstance(temporal, dict) or not any(
            nonempty(temporal.get(k)) for k in ("instant", "start", "end")
        ):
            errors.append(f"{prefix}.temporal_scope must contain instant, start, or end")

        _validate_payload_ref(record.get("payload_ref"), prefix, errors)

        sources = record.get("source_record_ids")
        if not isinstance(sources, list):
            errors.append(f"{prefix}.source_record_ids must be a list")
        else:
            for source in sources:
                if source not in record_ids:
                    errors.append(f"{prefix}.source_record_ids references missing record {source!r}")

        supersedes = record.get("supersedes", [])
        if not isinstance(supersedes, list):
            errors.append(f"{prefix}.supersedes must be a list")
        else:
            for prior in supersedes:
                if prior == rid:
                    errors.append(f"{prefix}.supersedes cannot reference its own record_id")
                elif prior not in record_ids:
                    errors.append(f"{prefix}.supersedes references missing record {prior!r}")

        if provenance in TRANSFORMED:
            _validate_transformation(record.get("transformation"), prefix, record_ids, errors)
        elif provenance == "MEASURED" and "transformation" in record:
            errors.append(f"{prefix}: MEASURED state must not carry a transformation; use DERIVED for transformed measurements")

        if provenance in DIRECT:
            acquisition = record.get("acquisition")
            if not isinstance(acquisition, dict) or not nonempty(acquisition.get("method")):
                errors.append(f"{prefix}.acquisition.method is required for {provenance}")

        if not nonempty(record.get("authority_ref")):
            errors.append(f"{prefix}.authority_ref must be a non-empty string")

    snapshots = data.get("snapshots")
    if not isinstance(snapshots, list) or not snapshots:
        errors.append("snapshots must be a non-empty list")
        snapshots = []
    snapshot_ids = set()
    for i, snapshot in enumerate(snapshots):
        prefix = f"snapshots[{i}]"
        if not isinstance(snapshot, dict):
            errors.append(f"{prefix} must be an object")
            continue
        sid = snapshot.get("snapshot_id")
        if not nonempty(sid):
            errors.append(f"{prefix}.snapshot_id must be a non-empty string")
        elif sid in snapshot_ids:
            errors.append(f"duplicate snapshot_id {sid!r}")
        else:
            snapshot_ids.add(sid)
        refs = snapshot.get("record_ids")
        if not isinstance(refs, list) or not refs:
            errors.append(f"{prefix}.record_ids must be a non-empty list")
        else:
            for rid in refs:
                if rid not in record_ids:
                    errors.append(f"{prefix}.record_ids references missing record {rid!r}")
        if not nonempty(snapshot.get("created_at")):
            errors.append(f"{prefix}.created_at must be a non-empty string")
        if not isinstance(snapshot.get("unknown_coverage"), list):
            errors.append(f"{prefix}.unknown_coverage must be a list")

    lineage = data.get("lineage")
    if not isinstance(lineage, list):
        errors.append("lineage must be a list")
        lineage = []
    op_ids = set()
    for i, op in enumerate(lineage):
        prefix = f"lineage[{i}]"
        if not isinstance(op, dict):
            errors.append(f"{prefix} must be an object")
            continue
        oid = op.get("operation_id")
        if not nonempty(oid):
            errors.append(f"{prefix}.operation_id must be a non-empty string")
        elif oid in op_ids:
            errors.append(f"duplicate lineage operation_id {oid!r}")
        else:
            op_ids.add(oid)
        if op.get("operation") not in LINEAGE_OPS:
            errors.append(f"{prefix}.operation is invalid: {op.get('operation')!r}")
        if not nonempty(op.get("occurred_at")):
            errors.append(f"{prefix}.occurred_at must be a non-empty string")
        for field in ("parent_snapshot_ids", "child_snapshot_ids"):
            refs = op.get(field)
            if not isinstance(refs, list):
                errors.append(f"{prefix}.{field} must be a list")
                continue
            for sid in refs:
                if sid not in snapshot_ids:
                    errors.append(f"{prefix}.{field} references missing snapshot {sid!r}")

    return errors

def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("usage: validate_hcsa.py <archive.json>", file=sys.stderr)
        return 2
    try:
        data = json.loads(Path(argv[0]).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"archive: {exc}", file=sys.stderr)
        return 2
    errors = validate_hcsa(data)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("VALID")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
