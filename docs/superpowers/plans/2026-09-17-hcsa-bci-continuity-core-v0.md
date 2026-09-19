# Transcendence Implementation Plan — HCSA / BCI / Continuity Core V0

Date: 2026-09-17
Branch: `architecture/consciousness-backup-v1`
Status: IMPLEMENTATION AUTHORIZED ON DRAFT PR #1

## Goal

Create the first executable, substrate-neutral continuity-data contracts and reference tooling without storing any real person's continuity payload in this public repository.

## Scope

Implement:
- HCSA envelope and record schemas;
- BCI adapter manifest schema;
- continuity-lineage schema;
- integrity manifest schema;
- pure-Python reference validation and canonical hashing;
- portable manifest generation/verification;
- synthetic fixtures and tests only.

Do not implement:
- real human capture;
- medical/clinical workflows;
- actual BCI hardware I/O;
- neural decoding claims;
- reconstruction/activation;
- migration of a real person;
- subjective-continuity claims;
- private subject-data ingestion.

## Task 1 — HCSA core schemas

Add machine-readable schemas for:
- archive envelope;
- evidence record;
- transformation lineage;
- snapshot descriptor.

Requirements:
- substrate neutral;
- provenance enum preserved;
- raw/source references distinct from inferred/generated fields;
- privacy classification represented;
- authority/consent metadata represented independently from possession;
- digest/integrity fields explicit;
- no requirement for HC Brain target fields.

## Task 2 — BCI adapter contract

Add a versioned adapter manifest describing:
- adapter identity/version;
- acquisition/effect direction;
- modalities;
- spatial/temporal resolution metadata;
- calibration method;
- raw representation;
- decoder/normalizer version;
- uncertainty;
- effect/stimulation capabilities;
- safety/authority ceiling;
- subject-state context.

Measurement and semantic interpretation must be separate.

## Task 3 — Continuity lineage schema

Represent:
- BACKUP
- RESTORE
- SUCCESSOR
- FORK
- MIGRATION
- GRADUAL_TRANSFER

Each event binds:
- predecessor snapshot(s);
- descendant snapshot(s);
- chronology;
- substrate(s);
- evidence refs;
- continuity-dimension claims;
- unresolved/unknown dimensions.

No event type silently implies phenomenal continuity.

## Task 4 — Integrity + portability tooling

Add stdlib reference code for:
- canonical JSON encoding;
- SHA-256 object digest;
- manifest creation;
- manifest verification;
- path-safe portable archive inventory;
- schema/version discovery.

No cryptographic identity/signature claim beyond ordinary SHA-256 integrity in V0.

## Task 5 — Validation reference

Add a lightweight validator that enforces the most important semantic invariants in addition to JSON shape:
- generated evidence cannot be relabeled measured;
- archive ID / record ID required;
- lineage event predecessor/descendant rules;
- FORK requires multiple descendants;
- GRADUAL_TRANSFER records overlapping substrate participation metadata;
- BCI effects require an explicit effect-authority scope;
- decoder interpretation never replaces raw measurement provenance.

## Task 6 — Synthetic fixtures + tests

Use only fictional/synthetic data.

Tests cover:
- valid HCSA archive;
- invalid provenance promotion;
- valid read-only BCI adapter;
- invalid effect-capable adapter without authority ceiling;
- valid FORK;
- invalid single-descendant FORK;
- valid GRADUAL_TRANSFER;
- canonical hash stability;
- manifest detects tampering;
- export inventory rejects path traversal.

## Completion gate

Implementation remains on draft PR #1.

Before calling this slice complete:
1. all reference tests pass on exact PR head;
2. imported HC reference-kernel tests still pass;
3. no real person-specific payload is present;
4. README/docs point to the implemented contracts;
5. no implementation text claims current human consciousness capture/reconstruction/migration capability.
