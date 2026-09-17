# HCSA V0 Machine Contract

Status: reference implementation / experimental schema.

## Purpose

HCSA V0 is the first machine-readable Human Cognitive State Archive contract in Transcendence.

It exists to make the project's evidence discipline executable without pretending that V0 captures a complete person.

`VALID_HCSA_V0 != COMPLETE_CONSCIOUSNESS_BACKUP`

## Files

- `schemas/hcsa-v0.schema.json` — JSON Schema shape contract.
- `tools/hcsa/validate_hcsa.py` — dependency-free semantic validator.
- `tools/hcsa/test_validate_hcsa.py` — validator regression tests.
- `examples/hcsa/minimal-valid-v0.json` — synthetic non-person example.

## Public/private boundary

The schema is public.

Actual subject archives are private continuity payloads and do not belong in this public repository.

The example archive is deliberately synthetic.

## Core object types

### Archive

The root binds records, snapshots, and continuity-lineage operations to one pseudonymous `subject_ref`.

V0 does not define legal identity, identity proofing, or custody policy.

### Record

A record represents one material state/evidence object.

Required fields include:

- `record_id`
- `provenance_class`
- `domain`
- `temporal_scope`
- `payload_ref`
- `source_record_ids`
- `authority_ref`

Large payloads are referenced by digest/URI rather than embedded into the manifest.

### Snapshot

A snapshot names a reproducible set of archive records and explicitly lists known unknown coverage.

### Lineage operation

V0 recognizes:

- `BACKUP`
- `RESTORE`
- `SUCCESSOR`
- `FORK`
- `MIGRATION`
- `GRADUAL_TRANSFER`

This records provenance/continuity operations without claiming metaphysical identity.

## Provenance rules enforced by the reference validator

Allowed classes are exactly:

- `MEASURED`
- `BEHAVIORALLY_OBSERVED`
- `SELF_REPORTED`
- `DERIVED`
- `INFERRED`
- `INTERPOLATED`
- `GENERATED`
- `IMPORTED_REFERENCE`
- `UNKNOWN`

`DERIVED`, `INFERRED`, `INTERPOLATED`, and `GENERATED` require a transformation record.

`MEASURED` must not carry a transformation. If a measurement is normalized, decoded, embedded, compressed, or otherwise transformed, preserve the raw measured record and create a derived record.

That enforces:

`TRANSFORMED_MEASUREMENT != RAW_MEASUREMENT`

## Reference integrity

The semantic validator additionally checks constraints that ordinary JSON Schema cannot conveniently express:

- record IDs are unique;
- local source references resolve;
- a record cannot supersede itself;
- superseded record IDs resolve;
- snapshot record references resolve;
- snapshot IDs are unique;
- lineage operation IDs are unique;
- lineage snapshot references resolve;
- lineage operation kind is recognized.

## BCI compatibility

Raw BCI evidence may use domain `BCI_RAW` with `MEASURED` provenance.

Decoded/normalized BCI evidence should normally become a distinct `BCI_NORMALIZED` record with `DERIVED` or `INFERRED` provenance and a transformation lineage back to raw records.

`NEURAL_SIGNAL != SEMANTIC_MEANING_BY_DEFAULT`

## Payload integrity

V0 payload references use a mandatory SHA-256 digest string:

`sha256:<64 lowercase hex>`

The reference validator checks syntax only. It does not fetch the payload or recompute its digest.

A later archive-integrity tool should independently verify referenced payload bytes.

## Authority boundary

Every record contains `authority_ref`, but V0 does not yet define the authority-object schema.

This is deliberate: subject/custodian/reconstruction/activation permissions remain a separate contract.

`ARCHIVE_RECORD_VALIDITY != RECONSTRUCTION_AUTHORITY`

## V0 limitations

V0 does not yet standardize:

- cryptographic signatures;
- encrypted payload packaging;
- distributed custody;
- consent/authority object structure;
- petabyte/exabyte chunk manifests;
- ontology identifiers below broad domains;
- coordinate systems for neural anatomy;
- uncertainty mathematics;
- conflict objects;
- BCI adapter schema;
- translation-to-HC schema;
- reconstruction manifests;
- qualification result schema.

Those are follow-on contracts. V0's purpose is the smallest honest archive spine onto which they can attach.
