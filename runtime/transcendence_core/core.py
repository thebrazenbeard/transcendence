from __future__ import annotations

import hashlib
import json
from pathlib import PurePosixPath
from typing import Any, Mapping


PROVENANCE_CLASSES = {
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

LINEAGE_EVENT_TYPES = {
    "BACKUP",
    "RESTORE",
    "SUCCESSOR",
    "FORK",
    "MIGRATION",
    "GRADUAL_TRANSFER",
}

CONTINUITY_DIMENSIONS = {
    "BIOLOGICAL",
    "AUTOBIOGRAPHICAL_INFORMATIONAL",
    "PSYCHOLOGICAL",
    "FUNCTIONAL",
    "CAUSAL_NEURAL",
    "TEMPORAL_PROCESS",
    "PHENOMENAL_SUBJECTIVE",
}

AUTHORITY_FIELDS = {
    "storage",
    "read",
    "research",
    "training",
    "interpretation",
    "reconstruction",
    "activation",
    "replication",
    "disclosure",
}

PRIVACY_CLASSES = {
    "PUBLIC",
    "PRIVATE_SUBJECT",
    "SENSITIVE_SUBJECT",
    "RESTRICTED_SUBJECT",
}

NONBIOLOGICAL_SUBSTRATES = {
    "SYNTHETIC",
    "HYBRID",
    "EMULATED",
    "NEUROMORPHIC",
    "UNKNOWN",
}


class ValidationError(ValueError):
    pass


def canonical_json_bytes(value: Any) -> bytes:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json_bytes(value)).hexdigest()


def validate_hcsa(document: Mapping[str, Any]) -> None:
    archive_id = _required_text(document, "archive_id")
    if _required_text(document, "schema_version") != "HCSA-V0":
        raise ValidationError("unsupported HCSA schema_version")
    _required_text(document, "subject_ref")
    _required_text(document, "created_at")

    records = document.get("records")
    if not isinstance(records, list):
        raise ValidationError("records must be a list")

    seen: set[str] = set()
    records_by_id: dict[str, Mapping[str, Any]] = {}
    for record in records:
        if not isinstance(record, Mapping):
            raise ValidationError("record must be an object")
        record_id = _required_text(record, "record_id")
        if record_id in seen:
            raise ValidationError(f"duplicate record_id: {record_id}")
        seen.add(record_id)
        records_by_id[record_id] = record

        if _required_text(record, "archive_id") != archive_id:
            raise ValidationError("record archive_id mismatch")
        provenance = _required_text(record, "provenance_class")
        if provenance not in PROVENANCE_CLASSES:
            raise ValidationError(f"unknown provenance class: {provenance}")
        _required_text(record, "observed_at")
        _required_text(record, "payload_ref")

        privacy = _required_text(record, "privacy_classification")
        if privacy not in PRIVACY_CLASSES:
            raise ValidationError(f"unknown privacy_classification: {privacy}")

        digest = _required_text(record, "integrity_digest")
        if len(digest) != 64 or any(ch not in "0123456789abcdef" for ch in digest):
            raise ValidationError("integrity_digest must be lowercase SHA-256 hex")

        sources = record.get("source_artifact_ids")
        if not isinstance(sources, list):
            raise ValidationError("source_artifact_ids must be a list")

        authority = record.get("authority_scope")
        if not isinstance(authority, Mapping):
            raise ValidationError("authority_scope must be an object")
        missing_authority = AUTHORITY_FIELDS - set(authority)
        if missing_authority:
            raise ValidationError(
                f"authority_scope missing fields: {sorted(missing_authority)}"
            )
        for key in AUTHORITY_FIELDS:
            if not isinstance(authority.get(key), bool):
                raise ValidationError(f"authority_scope.{key} must be boolean")

        history = record.get("provenance_history", [])
        if not isinstance(history, list):
            raise ValidationError("provenance_history must be a list")
        if provenance == "MEASURED":
            for item in history:
                if isinstance(item, Mapping) and item.get("from") == "GENERATED":
                    raise ValidationError("generated evidence cannot be relabeled measured")

        transform = record.get("transformation")
        if provenance in {"DERIVED", "INFERRED", "INTERPOLATED", "GENERATED"}:
            if not isinstance(transform, Mapping):
                raise ValidationError(f"{provenance} record requires transformation metadata")
            if not isinstance(transform.get("input_record_ids"), list):
                raise ValidationError("transformation input_record_ids must be a list")
            _required_text(transform, "method_version")
        elif transform is not None and not isinstance(transform, Mapping):
            raise ValidationError("transformation must be an object or null")

    for record_id, record in records_by_id.items():
        transform = record.get("transformation")
        if not isinstance(transform, Mapping):
            continue
        input_ids = transform.get("input_record_ids", [])
        for input_id in input_ids:
            source = records_by_id.get(str(input_id))
            if source is None:
                raise ValidationError(
                    f"record {record_id} transformation references unknown record {input_id}"
                )
            if (
                record.get("provenance_class") == "MEASURED"
                and source.get("provenance_class")
                in {"DERIVED", "INFERRED", "INTERPOLATED", "GENERATED", "IMPORTED_REFERENCE"}
            ):
                raise ValidationError(
                    "non-measured evidence cannot be promoted into MEASURED through transformation"
                )

    transformation_inputs: dict[str, tuple[str, ...]] = {}
    for record_id, record in records_by_id.items():
        transform = record.get("transformation")
        if isinstance(transform, Mapping):
            transformation_inputs[record_id] = tuple(
                str(input_id) for input_id in transform.get("input_record_ids", [])
            )

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit_provenance(record_id: str) -> None:
        if record_id in visiting:
            raise ValidationError("transformation provenance cycle detected")
        if record_id in visited:
            return
        visiting.add(record_id)
        for input_id in transformation_inputs.get(record_id, ()):
            visit_provenance(input_id)
        visiting.remove(record_id)
        visited.add(record_id)

    for record_id in records_by_id:
        visit_provenance(record_id)

    snapshots = document.get("snapshots")
    if not isinstance(snapshots, list):
        raise ValidationError("snapshots must be a list")
    snapshot_ids: set[str] = set()
    for snapshot in snapshots:
        if not isinstance(snapshot, Mapping):
            raise ValidationError("snapshot must be an object")
        snapshot_id = _required_text(snapshot, "snapshot_id")
        if snapshot_id in snapshot_ids:
            raise ValidationError(f"duplicate snapshot_id: {snapshot_id}")
        snapshot_ids.add(snapshot_id)
        _required_text(snapshot, "cutoff_at")
        record_ids = snapshot.get("record_ids")
        if not isinstance(record_ids, list):
            raise ValidationError("snapshot record_ids must be a list")
        for record_id in record_ids:
            if str(record_id) not in records_by_id:
                raise ValidationError(f"snapshot references unknown record: {record_id}")
        if not isinstance(snapshot.get("unresolved_conflicts"), list):
            raise ValidationError("snapshot unresolved_conflicts must be a list")
        if not isinstance(snapshot.get("unknowns"), list):
            raise ValidationError("snapshot unknowns must be a list")


def validate_bci_adapter(document: Mapping[str, Any]) -> None:
    if _required_text(document, "schema_version") != "BCI-ADAPTER-V0":
        raise ValidationError("unsupported BCI adapter schema_version")
    _required_text(document, "adapter_id")
    _required_text(document, "adapter_version")
    direction = _required_text(document, "direction")
    if direction not in {"ACQUIRE", "EFFECT", "BIDIRECTIONAL"}:
        raise ValidationError("invalid BCI direction")

    modalities = document.get("modalities")
    if not isinstance(modalities, list) or not modalities:
        raise ValidationError("BCI adapter requires at least one modality")
    _required_text(document, "raw_representation")
    _required_text(document, "uncertainty_model")

    normalization = document.get("normalization")
    if not isinstance(normalization, Mapping):
        raise ValidationError("BCI adapter requires normalization metadata")
    _required_text(normalization, "version")
    if normalization.get("preserves_raw_reference") is not True:
        raise ValidationError("normalization must preserve raw measurement reference")

    decoder = document.get("decoder")
    if decoder is not None:
        if not isinstance(decoder, Mapping):
            raise ValidationError("decoder must be an object or null")
        _required_text(decoder, "version")
        decoder_provenance = _required_text(decoder, "interpretation_provenance")
        if decoder_provenance not in {
            "DERIVED",
            "INFERRED",
            "INTERPOLATED",
            "GENERATED",
            "UNKNOWN",
        }:
            raise ValidationError("decoder interpretation cannot masquerade as measured evidence")

    effects = document.get("effect_capabilities")
    if not isinstance(effects, list):
        raise ValidationError("effect_capabilities must be a list")
    if direction == "ACQUIRE" and effects:
        raise ValidationError(
            "ACQUIRE adapter cannot declare effect_capabilities"
        )
    if direction in {"EFFECT", "BIDIRECTIONAL"} and not effects:
        raise ValidationError(
            "effect-capable adapter requires at least one effect capability"
        )

    authority = document.get("effect_authority_scope")
    if direction in {"EFFECT", "BIDIRECTIONAL"} or effects:
        if not isinstance(authority, Mapping) or not authority:
            raise ValidationError("effect-capable BCI adapter requires effect_authority_scope")
        _required_text(authority, "scope_id")
        allowed_effects = authority.get("allowed_effects")
        if not isinstance(allowed_effects, list):
            raise ValidationError("effect_authority_scope.allowed_effects must be a list")
        missing = set(map(str, effects)) - set(map(str, allowed_effects))
        if missing:
            raise ValidationError(
                f"effect_authority_scope does not cover effects: {sorted(missing)}"
            )
    elif authority not in (None, {}):
        raise ValidationError("acquire-only adapter must not imply effect authority")


def validate_lineage(document: Mapping[str, Any]) -> None:
    if _required_text(document, "schema_version") != "CONTINUITY-LINEAGE-V0":
        raise ValidationError("unsupported continuity lineage schema_version")
    _required_text(document, "lineage_id")
    events = document.get("events")
    if not isinstance(events, list):
        raise ValidationError("events must be a list")

    seen: set[str] = set()
    lineage_edges: dict[str, set[str]] = {}
    for event in events:
        if not isinstance(event, Mapping):
            raise ValidationError("lineage event must be an object")
        event_id = _required_text(event, "event_id")
        if event_id in seen:
            raise ValidationError(f"duplicate event_id: {event_id}")
        seen.add(event_id)

        event_type = _required_text(event, "event_type")
        if event_type not in LINEAGE_EVENT_TYPES:
            raise ValidationError(f"invalid lineage event type: {event_type}")
        _required_text(event, "occurred_at")

        predecessors = event.get("predecessor_snapshot_ids")
        descendants = event.get("descendant_snapshot_ids")
        if not isinstance(predecessors, list) or not isinstance(descendants, list):
            raise ValidationError("lineage event requires predecessor/descendant lists")
        if not predecessors or not descendants:
            raise ValidationError(
                "lineage event requires non-empty predecessor and descendant sets"
            )
        predecessor_ids = tuple(str(item) for item in predecessors)
        descendant_ids = tuple(str(item) for item in descendants)
        if len(set(predecessor_ids)) != len(predecessor_ids):
            raise ValidationError("lineage predecessor_snapshot_ids must be unique")
        if len(set(descendant_ids)) != len(descendant_ids):
            raise ValidationError("lineage descendant_snapshot_ids must be unique")
        if set(predecessor_ids) & set(descendant_ids):
            raise ValidationError("lineage event cannot descend to its own predecessor")
        if event_type == "FORK" and len(descendant_ids) < 2:
            raise ValidationError("FORK requires at least two descendants")
        for predecessor_id in predecessor_ids:
            lineage_edges.setdefault(predecessor_id, set()).update(descendant_ids)

        substrates = event.get("substrates")
        if not isinstance(substrates, list):
            raise ValidationError("lineage event requires substrate metadata")
        biological_overlap = False
        nonbiological_overlap = False
        for substrate in substrates:
            if not isinstance(substrate, Mapping):
                raise ValidationError("substrate participation must be an object")
            _required_text(substrate, "substrate_id")
            substrate_class = _required_text(substrate, "substrate_class")
            role = _required_text(substrate, "role")
            if role == "OVERLAPPING_ACTIVE":
                if substrate_class == "BIOLOGICAL":
                    biological_overlap = True
                if substrate_class in NONBIOLOGICAL_SUBSTRATES:
                    nonbiological_overlap = True

        if event_type == "GRADUAL_TRANSFER":
            if not biological_overlap or not nonbiological_overlap:
                raise ValidationError(
                    "GRADUAL_TRANSFER requires overlapping active biological and non-biological substrates"
                )

        refs = event.get("evidence_refs")
        if not isinstance(refs, list):
            raise ValidationError("lineage event evidence_refs must be a list")
        if not isinstance(event.get("unresolved_questions"), list):
            raise ValidationError("lineage event unresolved_questions must be a list")

        claims = event.get("continuity_claims")
        if not isinstance(claims, Mapping):
            raise ValidationError("continuity_claims must be an object")
        for dimension, claim in claims.items():
            if dimension not in CONTINUITY_DIMENSIONS:
                raise ValidationError(f"unknown continuity dimension: {dimension}")
            if not isinstance(claim, Mapping):
                raise ValidationError("continuity claim must be an object")
            status = _required_text(claim, "status")
            if dimension == "PHENOMENAL_SUBJECTIVE" and status not in {
                "UNKNOWN",
                "UNESTABLISHED",
            }:
                raise ValidationError(
                    "V0 phenomenal continuity must remain UNKNOWN/UNESTABLISHED"
                )
            claim_refs = claim.get("evidence_refs")
            if not isinstance(claim_refs, list):
                raise ValidationError("continuity claim evidence_refs must be a list")

    visiting_snapshots: set[str] = set()
    visited_snapshots: set[str] = set()

    def visit_snapshot(snapshot_id: str) -> None:
        if snapshot_id in visiting_snapshots:
            raise ValidationError("continuity lineage snapshot cycle detected")
        if snapshot_id in visited_snapshots:
            return
        visiting_snapshots.add(snapshot_id)
        for descendant_id in lineage_edges.get(snapshot_id, set()):
            visit_snapshot(descendant_id)
        visiting_snapshots.remove(snapshot_id)
        visited_snapshots.add(snapshot_id)

    all_snapshot_ids = set(lineage_edges)
    for descendants in lineage_edges.values():
        all_snapshot_ids.update(descendants)
    for snapshot_id in all_snapshot_ids:
        visit_snapshot(snapshot_id)


def validate_portable_path(path: str) -> str:
    if not path or "\\" in path or ":" in path:
        raise ValidationError("portable path must use non-empty POSIX relative syntax")
    p = PurePosixPath(path)
    if p.is_absolute() or any(part in {"", ".", ".."} for part in p.parts):
        raise ValidationError("portable path traversal/absolute path rejected")
    return str(p)


def build_integrity_manifest(files: Mapping[str, bytes]) -> dict[str, Any]:
    entries = []
    for path in sorted(files):
        safe = validate_portable_path(path)
        payload = files[path]
        if not isinstance(payload, (bytes, bytearray)):
            raise TypeError("manifest file payloads must be bytes")
        entries.append(
            {
                "path": safe,
                "sha256": hashlib.sha256(bytes(payload)).hexdigest(),
                "bytes": len(payload),
            }
        )
    manifest = {"schema_version": "HCSA-INTEGRITY-V0", "entries": entries}
    manifest["manifest_sha256"] = sha256_json(entries)
    return manifest


def verify_integrity_manifest(
    files: Mapping[str, bytes],
    manifest: Mapping[str, Any],
) -> tuple[bool, tuple[str, ...]]:
    errors: list[str] = []
    if manifest.get("schema_version") != "HCSA-INTEGRITY-V0":
        errors.append("unsupported manifest schema_version")
    entries = manifest.get("entries")
    if not isinstance(entries, list):
        return False, tuple(errors + ["entries must be a list"])

    try:
        expected_manifest_digest = sha256_json(entries)
    except (TypeError, ValueError):
        return False, tuple(errors + ["manifest entries are not canonical-json compatible"])
    if manifest.get("manifest_sha256") != expected_manifest_digest:
        errors.append("manifest digest mismatch")

    declared_paths: set[str] = set()
    for entry in entries:
        if not isinstance(entry, Mapping):
            errors.append("invalid manifest entry")
            continue
        try:
            path = validate_portable_path(str(entry["path"]))
        except (KeyError, ValidationError) as exc:
            errors.append(str(exc))
            continue
        declared_paths.add(path)
        payload = files.get(path)
        if payload is None:
            errors.append(f"missing file: {path}")
            continue
        digest = hashlib.sha256(bytes(payload)).hexdigest()
        if digest != entry.get("sha256"):
            errors.append(f"digest mismatch: {path}")
        if len(payload) != entry.get("bytes"):
            errors.append(f"size mismatch: {path}")

    safe_actual_paths: set[str] = set()
    for path in files:
        try:
            safe_actual_paths.add(validate_portable_path(path))
        except ValidationError as exc:
            errors.append(f"invalid supplied path {path!r}: {exc}")
    undeclared = sorted(safe_actual_paths - declared_paths)
    errors.extend(f"undeclared file: {path}" for path in undeclared)
    return not errors, tuple(errors)


def _required_text(mapping: Mapping[str, Any], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{key} is required")
    return value
