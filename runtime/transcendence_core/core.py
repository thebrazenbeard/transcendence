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
    records = document.get("records")
    if not isinstance(records, list):
        raise ValidationError("records must be a list")

    seen: set[str] = set()
    for record in records:
        if not isinstance(record, Mapping):
            raise ValidationError("record must be an object")
        record_id = _required_text(record, "record_id")
        if record_id in seen:
            raise ValidationError(f"duplicate record_id: {record_id}")
        seen.add(record_id)
        if _required_text(record, "archive_id") != archive_id:
            raise ValidationError("record archive_id mismatch")
        provenance = _required_text(record, "provenance_class")
        if provenance not in PROVENANCE_CLASSES:
            raise ValidationError(f"unknown provenance class: {provenance}")
        _required_text(record, "observed_at")
        _required_text(record, "payload_ref")
        _required_text(record, "privacy_classification")
        _required_text(record, "integrity_digest")

        sources = record.get("source_artifact_ids")
        if not isinstance(sources, list):
            raise ValidationError("source_artifact_ids must be a list")

        authority = record.get("authority_scope")
        if not isinstance(authority, Mapping):
            raise ValidationError("authority_scope must be an object")

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
    if "semantic_interpretation" in document and "decoder_version" not in document:
        raise ValidationError("semantic interpretation requires decoder_version")
    if direction in {"EFFECT", "BIDIRECTIONAL"}:
        effects = document.get("effect_capabilities")
        if not isinstance(effects, list) or not effects:
            raise ValidationError("effect-capable BCI adapter requires effect_capabilities")
        authority = document.get("effect_authority_scope")
        if not isinstance(authority, Mapping) or not authority:
            raise ValidationError("effect-capable BCI adapter requires effect_authority_scope")


def validate_lineage(document: Mapping[str, Any]) -> None:
    if _required_text(document, "schema_version") != "CONTINUITY-LINEAGE-V0":
        raise ValidationError("unsupported continuity lineage schema_version")
    events = document.get("events")
    if not isinstance(events, list):
        raise ValidationError("events must be a list")

    seen: set[str] = set()
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
        if event_type == "FORK" and len(descendants) < 2:
            raise ValidationError("FORK requires at least two descendants")
        substrates = event.get("substrates")
        if not isinstance(substrates, list) or not substrates:
            raise ValidationError("lineage event requires substrate metadata")
        if event_type == "GRADUAL_TRANSFER" and len(set(map(str, substrates))) < 2:
            raise ValidationError("GRADUAL_TRANSFER requires overlapping/multiple substrates")
        claims = event.get("continuity_claims", {})
        if not isinstance(claims, Mapping):
            raise ValidationError("continuity_claims must be an object")
        for dimension, claim in claims.items():
            if dimension not in CONTINUITY_DIMENSIONS:
                raise ValidationError(f"unknown continuity dimension: {dimension}")
            if not isinstance(claim, Mapping):
                raise ValidationError("continuity claim must be an object")
            status = _required_text(claim, "status")
            if dimension == "PHENOMENAL_SUBJECTIVE" and status not in {"UNKNOWN", "UNESTABLISHED"}:
                raise ValidationError("V0 phenomenal continuity must remain UNKNOWN/UNESTABLISHED")
            refs = claim.get("evidence_refs")
            if not isinstance(refs, list):
                raise ValidationError("continuity claim evidence_refs must be a list")


def validate_portable_path(path: str) -> str:
    if not path or "\\" in path:
        raise ValidationError("portable path must use non-empty POSIX syntax")
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
        entries.append({
            "path": safe,
            "sha256": hashlib.sha256(bytes(payload)).hexdigest(),
            "bytes": len(payload),
        })
    manifest = {"schema_version": "HCSA-INTEGRITY-V0", "entries": entries}
    manifest["manifest_sha256"] = sha256_json(entries)
    return manifest


def verify_integrity_manifest(files: Mapping[str, bytes], manifest: Mapping[str, Any]) -> tuple[bool, tuple[str, ...]]:
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

    undeclared = sorted(set(files) - declared_paths)
    errors.extend(f"undeclared file: {path}" for path in undeclared)
    return not errors, tuple(errors)


def _required_text(mapping: Mapping[str, Any], key: str) -> str:
    value = mapping.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{key} is required")
    return value
