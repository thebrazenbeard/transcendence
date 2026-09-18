from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping, Sequence


_PROVENANCE = {
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

_NONBIOLOGICAL_SUBSTRATES = {
    "SYNTHETIC",
    "HYBRID",
    "EMULATED",
    "NEUROMORPHIC",
    "UNKNOWN",
}


@dataclass(frozen=True)
class ValidationProblem:
    path: str
    message: str


def validate_hcsa(archive: Mapping) -> list[ValidationProblem]:
    problems: list[ValidationProblem] = []
    if archive.get("schema_version") != "HCSA_V0":
        problems.append(ValidationProblem("schema_version", "expected HCSA_V0"))
    if not str(archive.get("archive_id", "")).strip():
        problems.append(ValidationProblem("archive_id", "archive_id is required"))
    if not str(archive.get("subject_ref", "")).strip():
        problems.append(ValidationProblem("subject_ref", "subject_ref is required"))

    records = archive.get("records")
    if not isinstance(records, Sequence) or isinstance(records, (str, bytes)):
        return problems + [ValidationProblem("records", "records must be an array")]

    by_id: dict[str, Mapping] = {}
    for index, raw in enumerate(records):
        path = f"records[{index}]"
        if not isinstance(raw, Mapping):
            problems.append(ValidationProblem(path, "record must be an object"))
            continue
        record_id = str(raw.get("record_id", "")).strip()
        if not record_id:
            problems.append(ValidationProblem(f"{path}.record_id", "record_id is required"))
            continue
        if record_id in by_id:
            problems.append(ValidationProblem(f"{path}.record_id", "duplicate record_id"))
        by_id[record_id] = raw

        provenance = raw.get("provenance")
        if provenance not in _PROVENANCE:
            problems.append(ValidationProblem(f"{path}.provenance", "unknown provenance class"))

        if not str(raw.get("payload_ref", "")).strip():
            problems.append(ValidationProblem(f"{path}.payload_ref", "payload_ref is required"))

        authority = raw.get("authority")
        if not isinstance(authority, Mapping):
            problems.append(ValidationProblem(f"{path}.authority", "authority object is required"))

        integrity = raw.get("integrity")
        if not isinstance(integrity, Mapping):
            problems.append(ValidationProblem(f"{path}.integrity", "integrity object is required"))
        elif integrity.get("algorithm") != "SHA-256" or len(str(integrity.get("digest", ""))) != 64:
            problems.append(ValidationProblem(f"{path}.integrity", "SHA-256 digest is required"))

    for index, raw in enumerate(records):
        if not isinstance(raw, Mapping):
            continue
        provenance = raw.get("provenance")
        source_ids = raw.get("source_record_ids", [])
        if provenance == "MEASURED" and isinstance(source_ids, Sequence):
            for source_id in source_ids:
                source = by_id.get(str(source_id))
                if source and source.get("provenance") in {
                    "DERIVED",
                    "INFERRED",
                    "INTERPOLATED",
                    "GENERATED",
                    "IMPORTED_REFERENCE",
                }:
                    problems.append(
                        ValidationProblem(
                            f"records[{index}].provenance",
                            "provenance promotion into MEASURED from non-measured source is forbidden",
                        )
                    )
        if isinstance(source_ids, Sequence) and not isinstance(source_ids, (str, bytes)):
            for source_id in source_ids:
                if str(source_id) not in by_id:
                    problems.append(
                        ValidationProblem(
                            f"records[{index}].source_record_ids",
                            f"unknown source record: {source_id}",
                        )
                    )

    snapshots = archive.get("snapshots", [])
    if not isinstance(snapshots, Sequence) or isinstance(snapshots, (str, bytes)):
        problems.append(ValidationProblem("snapshots", "snapshots must be an array"))
    else:
        known = set(by_id)
        for index, snapshot in enumerate(snapshots):
            if not isinstance(snapshot, Mapping):
                problems.append(ValidationProblem(f"snapshots[{index}]", "snapshot must be an object"))
                continue
            if not str(snapshot.get("snapshot_id", "")).strip():
                problems.append(
                    ValidationProblem(f"snapshots[{index}].snapshot_id", "snapshot_id is required")
                )
            for record_id in snapshot.get("record_ids", []):
                if str(record_id) not in known:
                    problems.append(
                        ValidationProblem(
                            f"snapshots[{index}].record_ids",
                            f"unknown record: {record_id}",
                        )
                    )
    return problems


def validate_bci_adapter(manifest: Mapping) -> list[ValidationProblem]:
    problems: list[ValidationProblem] = []
    if manifest.get("schema_version") != "BCI_ADAPTER_V0":
        problems.append(ValidationProblem("schema_version", "expected BCI_ADAPTER_V0"))
    if not str(manifest.get("adapter_id", "")).strip():
        problems.append(ValidationProblem("adapter_id", "adapter_id is required"))
    if not str(manifest.get("adapter_version", "")).strip():
        problems.append(ValidationProblem("adapter_version", "adapter_version is required"))

    direction = manifest.get("direction")
    if direction not in {"ACQUIRE_ONLY", "EFFECT_ONLY", "BIDIRECTIONAL"}:
        problems.append(ValidationProblem("direction", "invalid BCI direction"))

    normalization = manifest.get("normalization")
    if not isinstance(normalization, Mapping) or normalization.get("preserves_raw_reference") is not True:
        problems.append(
            ValidationProblem(
                "normalization.preserves_raw_reference",
                "normalization must preserve a raw measurement reference",
            )
        )

    effects = manifest.get("effect_capabilities", [])
    if not isinstance(effects, Sequence) or isinstance(effects, (str, bytes)):
        problems.append(ValidationProblem("effect_capabilities", "effect_capabilities must be an array"))
        effects = []

    effectful = direction in {"EFFECT_ONLY", "BIDIRECTIONAL"} or bool(effects)
    authority = manifest.get("effect_authority_scope")
    if effectful:
        if not isinstance(authority, Mapping):
            problems.append(
                ValidationProblem(
                    "effect_authority_scope",
                    "effect authority scope is required for effect-capable BCI adapters",
                )
            )
        else:
            allowed = authority.get("allowed_effects")
            if not isinstance(allowed, Sequence) or isinstance(allowed, (str, bytes)):
                problems.append(
                    ValidationProblem(
                        "effect_authority_scope.allowed_effects",
                        "allowed_effects must be an array",
                    )
                )
            else:
                missing = set(map(str, effects)) - set(map(str, allowed))
                if missing:
                    problems.append(
                        ValidationProblem(
                            "effect_authority_scope.allowed_effects",
                            f"effect authority does not cover: {sorted(missing)}",
                        )
                    )
    elif authority not in (None, {}):
        problems.append(
            ValidationProblem(
                "effect_authority_scope",
                "acquire-only adapter should not imply effect authority",
            )
        )

    decoder = manifest.get("decoder")
    if isinstance(decoder, Mapping):
        provenance = decoder.get("interpretation_provenance")
        if provenance in {"MEASURED", "BEHAVIORALLY_OBSERVED", "SELF_REPORTED"}:
            problems.append(
                ValidationProblem(
                    "decoder.interpretation_provenance",
                    "decoder interpretation cannot masquerade as direct measurement/report",
                )
            )

    return problems


def validate_continuity_lineage(lineage: Mapping) -> list[ValidationProblem]:
    problems: list[ValidationProblem] = []
    if lineage.get("schema_version") != "CONTINUITY_LINEAGE_V0":
        problems.append(
            ValidationProblem("schema_version", "expected CONTINUITY_LINEAGE_V0")
        )
    if not str(lineage.get("lineage_id", "")).strip():
        problems.append(ValidationProblem("lineage_id", "lineage_id is required"))

    events = lineage.get("events")
    if not isinstance(events, Sequence) or isinstance(events, (str, bytes)):
        return problems + [ValidationProblem("events", "events must be an array")]

    seen: set[str] = set()
    for index, event in enumerate(events):
        path = f"events[{index}]"
        if not isinstance(event, Mapping):
            problems.append(ValidationProblem(path, "event must be an object"))
            continue
        event_id = str(event.get("event_id", "")).strip()
        if not event_id:
            problems.append(ValidationProblem(f"{path}.event_id", "event_id is required"))
        elif event_id in seen:
            problems.append(ValidationProblem(f"{path}.event_id", "duplicate event_id"))
        seen.add(event_id)

        event_type = event.get("event_type")
        if event_type not in {
            "BACKUP",
            "RESTORE",
            "SUCCESSOR",
            "FORK",
            "MIGRATION",
            "GRADUAL_TRANSFER",
        }:
            problems.append(ValidationProblem(f"{path}.event_type", "invalid event type"))
            continue

        descendants = event.get("descendant_snapshot_ids", [])
        if event_type == "FORK" and len(descendants) < 2:
            problems.append(
                ValidationProblem(
                    f"{path}.descendant_snapshot_ids",
                    "FORK requires at least two descendants",
                )
            )

        substrates = event.get("substrates", [])
        if event_type == "GRADUAL_TRANSFER":
            biological_overlap = False
            nonbiological_overlap = False
            for substrate in substrates:
                if not isinstance(substrate, Mapping):
                    continue
                if substrate.get("role") != "OVERLAPPING_ACTIVE":
                    continue
                if substrate.get("substrate_class") == "BIOLOGICAL":
                    biological_overlap = True
                if substrate.get("substrate_class") in _NONBIOLOGICAL_SUBSTRATES:
                    nonbiological_overlap = True
            if not biological_overlap or not nonbiological_overlap:
                problems.append(
                    ValidationProblem(
                        f"{path}.substrates",
                        "GRADUAL_TRANSFER requires overlapping active biological and non-biological substrates",
                    )
                )

        for claim_index, claim in enumerate(event.get("continuity_claims", [])):
            if not isinstance(claim, Mapping):
                continue
            if claim.get("dimension") == "PHENOMENAL" and claim.get("status") == "SUPPORTED":
                problems.append(
                    ValidationProblem(
                        f"{path}.continuity_claims[{claim_index}]",
                        "V0 does not permit an operational event to assert phenomenal continuity as proven",
                    )
                )

    return problems
