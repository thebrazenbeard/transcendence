# Transcendence

Transcendence is a universal, open research and engineering project for **preserving enough human continuity-bearing state to support future reconstruction, migration, and increasingly capable brain-computer-interface integration across substrates**.

It is not a Patrick-specific continuity archive. The public repository defines architecture, protocols, schemas, reference tooling, qualification methods, and evidence boundaries. Actual per-person continuity payloads belong in separately controlled private stores.

The long-term public-interest goal is to make continuity preservation genuinely available to everyone for free. The realistic non-negotiable baseline is an open commons: free-to-use specifications, open formats, open-source reference implementations, self-hostability, exportability, and no mandatory vendor dependency.

Transcendence does not assume that current neuroscience can already accomplish human consciousness backup, that a connectome is a complete person, or that a convincing digital replica proves subjective survival.

The central question is:

> **What information must survive for a particular human mind to be reconstructable or migratable, and what evidence would justify claims about fidelity and continuity?**

## Architectural posture

Transcendence uses an information-conservative pipeline:

`BIOLOGICAL HUMAN -> CAPTURE -> ARCHIVE -> INTERPRET -> TRANSLATE -> RECONSTRUCT / MIGRATE -> QUALIFY`

Each stage creates a new provenance-bearing artifact. Later interpretation may annotate or supersede earlier conclusions, but it must not rewrite raw evidence into something it was not.

Foundational claim limits:

`BEHAVIORAL_EQUIVALENCE != PERSONAL_CONTINUITY`

`CONNECTOME_CAPTURE != COMPLETE_PERSON_CAPTURE`

`FUNCTIONAL_RECONSTRUCTION != SUBJECTIVE_CONTINUITY_PROOF`

`HC_COMPATIBILITY != SUCCESSFUL_HUMAN_REINSTANTIATION`

`SERVICE_FAILURE != ARCHIVE_DEATH`

`NEURAL_SIGNAL != SEMANTIC_MEANING_BY_DEFAULT`

## Universal open architecture, private personal state

The public repo may contain the architecture and tools needed to capture, preserve, validate, export, migrate, reconstruct, and study continuity-bearing state.

It must not become the storage location for actual people's private memories, neural recordings, relationships, medical data, identity-bearing state, or personal archives.

Each person's Human Cognitive State Archive (HCSA) belongs in a separate private subject-controlled store or equivalent custody surface.

The architecture should support:
- encrypted portable archives;
- self-hosting;
- multiple independent custodians/replicas;
- offline recovery;
- open schema migration;
- independent integrity verification;
- independent restore testing;
- complete subject export;
- provider migration without loss of meaning.

A future free public-benefit service is encouraged, but it must remain one deployment of the architecture rather than the only path to preserve or recover a person.

See `docs/transcendence/OPEN_COMMONS_AND_ACCESS_MODEL.md`.

## Future BCI is a first-class channel

Transcendence explicitly assumes that brain-computer interfaces may become progressively richer and should be usable without redesigning the continuity architecture.

BCI is an adapter boundary around the substrate-neutral HCSA, not the definition of the person.

Future BCI channels may contribute:
- electrophysiology and population activity;
- stimulation/response evidence;
- effective-connectivity measurements;
- plasticity/calibration state;
- longitudinal neural observations;
- sensorimotor mappings;
- richer structural, molecular, or other state exposed by future technology.

Bidirectional BCI may eventually support causal probing, synthetic-neural co-adaptation, state reinjection, overlapping biological/synthetic operation, and gradual substrate migration.

Raw BCI measurements should remain preservable alongside normalized and interpreted state whenever lawful and technically feasible so later science can reinterpret earlier recordings.

See `docs/transcendence/BCI_AND_CONTINUITY_MIGRATION.md`.

## Continuity operations

Transcendence distinguishes operations that are often incorrectly collapsed into "uploading":

- `BACKUP` — continuity-bearing state is preserved.
- `RESTORE` — preserved state is instantiated.
- `SUCCESSOR` — a resulting instance materially derives from preserved state without assuming stronger identity continuity.
- `FORK` — multiple descendants continue from a shared predecessor.
- `MIGRATION` — state/function moves across substrates under controlled handoff.
- `GRADUAL_TRANSFER` — biological and synthetic substrates overlap while function is progressively transferred.

Continuity is therefore represented as lineage, potentially a branching graph rather than one linear "real person" pointer.

Behavioral, informational/autobiographical, psychological, functional, causal/neural, temporal/process, biological, and subjective/phenomenal continuity remain distinct claim dimensions.

## Imported Hyperconnectome Brain material

This repository was seeded with a substantial snapshot of the Hyperconnectome Brain (HC) architecture. In Transcendence, that material is a **candidate target substrate and reference ontology** for reconstruction research.

It is not evidence that HC can currently instantiate a human mind.

The imported subsystem tree supplies useful target domains—memory, cognition, affect, self-modeling, conation, semantics, social modeling, salience, interoception, arbitration, embodiment, and related functions. Transcendence adds the missing human-capture, preservation, continuity, BCI, translation, migration, and qualification layers.

The mapping is explicitly many-to-many. Biological anatomy must not be assigned one-to-one to HC folders.

Original copied root documents are preserved under `docs/imported-hc/`. See `docs/imported-hc/PROVENANCE.md`.

## Core Transcendence documents

- `docs/transcendence/ARCHITECTURE.md` — six-stage project architecture and stage-boundary invariants.
- `docs/transcendence/HUMAN_COGNITIVE_STATE_ARCHIVE.md` — HCSA provenance, chronology, lineage, and durability.
- `docs/transcendence/CAPTURE_LAYERS.md` — structural, effective-connectivity, molecular, dynamic, embodied, cognitive, and longitudinal capture domains.
- `docs/transcendence/OPEN_COMMONS_AND_ACCESS_MODEL.md` — universal/open architecture, private per-person stores, portability, and free-service goal.
- `docs/transcendence/BCI_AND_CONTINUITY_MIGRATION.md` — future BCI adapter model and gradual biological/synthetic migration.
- `docs/transcendence/HUMAN_TO_HC_TRANSLATION.md` — mapping biological evidence through candidate functions into HC-compatible representations.
- `docs/transcendence/RECONSTRUCTION_AND_QUALIFICATION.md` — reconstruction metadata, holdout testing, fidelity dimensions, and claim ladder.
- `docs/transcendence/CONTINUITY_BOUNDARIES.md` — behavioral, functional, causal, temporal, and subjective-continuity distinctions.
- `docs/transcendence/THREAT_MODEL.md` — epistemic, technical, security, governance, and impersonation failure modes.
- `docs/transcendence/RESEARCH_QUESTIONS.md` — unresolved scientific and engineering frontiers.
- `docs/transcendence/SOURCE_INDEX.md` — source-to-claim ledger and explicit non-claims.

The base design source is `docs/superpowers/specs/2026-09-17-consciousness-backup-design.md`, extended by `docs/superpowers/specs/2026-09-17-universal-open-bci-amendment.md`.

## Implemented V0 reference contracts

Draft PR #1 now includes executable, substrate-neutral V0 reference material:

- `specs/transcendence/hcsa-v0.schema.json` — HCSA envelope/evidence record contract;
- `specs/transcendence/bci-adapter-v0.schema.json` — acquisition/effect/bidirectional BCI adapter contract;
- `specs/transcendence/continuity-lineage-v0.schema.json` — BACKUP / RESTORE / SUCCESSOR / FORK / MIGRATION / GRADUAL_TRANSFER lineage;
- `specs/transcendence/integrity-manifest-v0.schema.json` — portable integrity manifest;
- `runtime/transcendence_core/core.py` — canonical JSON hashing, semantic validation, path-safe portability, and integrity verification;
- `runtime/transcendence_core/test_core.py` — synthetic-only regression tests.

The reference implementation intentionally contains no real person's continuity payload and performs no BCI hardware I/O, capture, reconstruction, activation, or migration.

## Human Cognitive State Archive

The core durable subject artifact is the **Human Cognitive State Archive (HCSA)**.

An HCSA is not a "consciousness file." It is a provenance-preserving archive of biological measurements, dynamic state, cognitive evidence, longitudinal observations, interpretations, unknowns, and reconstruction/migration lineage.

Subject-state provenance must remain visible. At minimum, material values distinguish:

- `MEASURED`
- `BEHAVIORALLY_OBSERVED`
- `SELF_REPORTED`
- `DERIVED`
- `INFERRED`
- `INTERPOLATED`
- `GENERATED`
- `IMPORTED_REFERENCE`
- `UNKNOWN`

A future model may estimate missing state, but generated state never becomes measured history merely because it is plausible.

`PLAUSIBLE_FILL != OBSERVED_PERSON_STATE`

## Research direction

Transcendence deliberately pursues a hybrid strategy:

1. accumulate a longitudinal cognitive/behavioral shadow while the person is alive;
2. preserve increasingly rich biological and neural state as measurement technology improves;
3. use future BCI as a first-class acquisition and bidirectional calibration channel;
4. preserve raw evidence so future science can reinterpret it;
5. permit terminal/destructive high-resolution capture as an additional evidence regime without treating it as continuity proof;
6. support non-destructive gradual BCI-mediated migration as a separate research path;
7. translate through explicit candidate causal functions instead of direct brain-region-to-software-module analogies;
8. test reconstructed or migrated systems using hidden subject-specific holdouts, causal evidence, lineage, and exact chronology rather than conversational resemblance alone.

The repository should remain useful even if HC changes or is replaced. The HCSA and its raw evidence must therefore be more durable than any particular reconstruction model.

## Scientific status

This project is speculative engineering constrained by real neuroscience.

Current connectomics, cell atlases, engram research, physiology, and neurotechnology can inform what information might matter. They do **not** currently establish a sufficient recipe for human consciousness backup or an empirical test for first-person continuity after destructive reconstruction or substrate migration.

Where a claim depends on current science, use `docs/transcendence/SOURCE_INDEX.md` and preserve the distinction among documented evidence, project inference, hypothesis, dispute, and unknown.

## Governance

Transcendence governance is defined in the root `WARDEN.md`.

The HC `WARDEN.md` copied into the initial repository is preserved as provenance under `docs/imported-hc/WARDEN_ORIGINAL.md`; it does not silently govern this project.
