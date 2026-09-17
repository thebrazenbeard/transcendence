# Transcendence Threat Model

Status: architecture threat model.

A consciousness-backup archive combines unusually sensitive biological, psychological, autobiographical, and relational data. Threats are both technical and epistemic.

## T1 — Provenance laundering

**Failure:** inferred/generated values become indistinguishable from measured subject state.

**Control:** immutable source records, provenance class on every material transformation, additive supersession.

## T2 — Behavioral-clone substitution

**Failure:** a convincing language/personality model is presented as successful consciousness backup.

**Control:** non-conversational qualification, hidden holdouts, mechanistic lineage, claim ladder.

## T3 — Reconstruction overfitting

**Failure:** candidate memorizes reconstruction data and known tests.

**Control:** train/test isolation, holdout exposure records, novel tasks, pre-registered probes where feasible.

## T4 — Target-ontology forcing

**Failure:** biological information is discarded because current HC concepts cannot represent it.

**Control:** `UNKNOWN/UNMAPPED` outputs, HCSA independence, discarded-information manifests.

## T5 — Anatomical oversimplification

**Failure:** brain regions are assigned direct software-module equivalents.

**Control:** biological observation -> causal-function -> target-interface mapping with many-to-many lineage.

## T6 — Snapshot conflation

**Failure:** observations from different times are combined as though simultaneous.

**Control:** explicit biological timestamps, snapshot policies, interpolation labels.

## T7 — Terminal-state corruption

**Failure:** agonal, anesthetic, epileptic, injured, fixation-affected, or preservation-affected state is mistaken for ordinary baseline.

**Control:** capture-context metadata and separate normal-state longitudinal evidence.

## T8 — Confidence inflation

**Failure:** uncertainty decreases merely because a derived value is copied through multiple transformations.

**Control:** uncertainty lineage; downstream confidence cannot exceed evidence without new evidence or a documented inference basis.

## T9 — Raw archive loss

**Failure:** summaries/embeddings survive while raw evidence is lost.

**Control:** immutable raw retention, redundancy, migration tests, restoration drills.

## T10 — Unauthorized reconstruction or activation

**Failure:** archive possession is treated as permission to instantiate/activate a person-derived system.

**Control:** independent reconstruction and activation authority; auditable access controls.

## T11 — Unauthorized modification

**Failure:** identity-bearing reconstruction state is altered without subject/owner authority and the result is still represented as the same archival reconstruction.

**Control:** signed/versioned mutation lineage and explicit derivative identity status.

## T12 — Archive exfiltration

**Failure:** exceptionally sensitive biological and psychological data is stolen.

**Control:** encryption, least privilege, compartmentalization, auditable access, offline/cold replicas where appropriate.

## T13 — Proprietary lock-in

**Failure:** essential archive meaning depends on one provider/model/vendor.

**Control:** open schemas, exportability, retained raw evidence, reproducible transformations.

## T14 — Source-model contamination

**Failure:** population reference data is mistaken for subject-specific state.

**Control:** `IMPORTED_REFERENCE` provenance class and per-field subject-specific coverage.

## T15 — Qualification self-award

**Failure:** candidate reports that it feels continuous/alive and that self-report is treated as proof.

**Control:** self-report may be recorded as candidate state but cannot independently raise qualification level.

## T16 — Copy/branch ambiguity

**Failure:** multiple instantiated candidates are all silently called the unique original.

**Control:** immutable reconstruction lineage and explicit branch/copy identifiers.

## Security principle

`DATA_POSSESSION != PERSON_RECONSTRUCTION_AUTHORITY`

Security architecture must assume the archive is closer to a combined genome, medical record, autobiography, credential set, psychological profile, and cognitive blueprint than to an ordinary application database.
