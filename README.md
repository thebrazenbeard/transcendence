# Transcendence

Transcendence is a research and engineering project about **backing up enough of a particular human's cognitive organization to support a future attempt at reconstruction in a non-biological substrate**.

It does not assume that current neuroscience can do this, that a connectome is a complete person, or that a convincing digital replica proves subjective survival.

The central question is:

> **What information must survive for a particular human mind to be reconstructable, and what evidence would justify claims about the fidelity and continuity of that reconstruction?**

## Architectural posture

Transcendence uses an information-conservative pipeline:

`BIOLOGICAL HUMAN -> CAPTURE -> ARCHIVE -> INTERPRET -> TRANSLATE -> RECONSTRUCT -> QUALIFY`

Each stage creates a new provenance-bearing artifact. Later interpretation may annotate or supersede earlier conclusions, but it must not rewrite raw evidence into something it was not.

Foundational claim limits:

`BEHAVIORAL_EQUIVALENCE != PERSONAL_CONTINUITY`

`CONNECTOME_CAPTURE != COMPLETE_PERSON_CAPTURE`

`FUNCTIONAL_RECONSTRUCTION != SUBJECTIVE_CONTINUITY_PROOF`

`HC_COMPATIBILITY != SUCCESSFUL_HUMAN_REINSTANTIATION`

## Imported Hyperconnectome Brain material

This repository was seeded with a substantial snapshot of the Hyperconnectome Brain (HC) architecture. In Transcendence, that material is a **candidate target substrate and reference ontology** for reconstruction research.

It is not evidence that HC can currently instantiate a human mind.

The imported subsystem tree supplies useful target domains—memory, cognition, affect, self-modeling, conation, semantics, social modeling, salience, interoception, arbitration, embodiment, and related functions. Transcendence adds the missing human-capture and translation layers.

The mapping is explicitly many-to-many. Biological anatomy must not be assigned one-to-one to HC folders.

Original copied root documents are preserved under `docs/imported-hc/`. See `docs/imported-hc/PROVENANCE.md`.

## Core Transcendence documents

- `docs/transcendence/ARCHITECTURE.md` — six-stage project architecture and stage-boundary invariants.
- `docs/transcendence/HUMAN_COGNITIVE_STATE_ARCHIVE.md` — Human Cognitive State Archive (HCSA), provenance, chronology, lineage, and durability.
- `docs/transcendence/CAPTURE_LAYERS.md` — structural, effective-connectivity, molecular, dynamic, embodied, cognitive, and longitudinal capture domains.
- `docs/transcendence/HUMAN_TO_HC_TRANSLATION.md` — rules for mapping biological evidence through candidate functions into HC-compatible representations.
- `docs/transcendence/RECONSTRUCTION_AND_QUALIFICATION.md` — reconstruction metadata, holdout testing, fidelity dimensions, and claim ladder.
- `docs/transcendence/CONTINUITY_BOUNDARIES.md` — behavioral, functional, causal, temporal, and subjective-continuity distinctions.
- `docs/transcendence/THREAT_MODEL.md` — epistemic, technical, security, governance, and impersonation failure modes.
- `docs/transcendence/RESEARCH_QUESTIONS.md` — unresolved scientific and engineering frontiers.
- `docs/transcendence/SOURCE_INDEX.md` — source-to-claim ledger and explicit non-claims.

The design source is `docs/superpowers/specs/2026-09-17-consciousness-backup-design.md`.

## Human Cognitive State Archive

The core durable subject artifact is the **Human Cognitive State Archive (HCSA)**.

An HCSA is not a "consciousness file." It is a provenance-preserving archive of biological measurements, dynamic state, cognitive evidence, longitudinal observations, interpretations, unknowns, and reconstruction lineage.

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
2. preserve increasingly rich biological state as measurement technology improves;
3. permit terminal or destructive high-resolution capture as an additional evidence regime without treating it as continuity proof;
4. preserve raw evidence so future science can reinterpret it;
5. translate through explicit candidate causal functions instead of direct brain-region-to-software-module analogies;
6. test reconstructed systems using hidden subject-specific holdouts and mechanistic lineage, not conversational resemblance alone.

The repository should remain useful even if the HC target architecture changes. The HCSA and its raw evidence must therefore be more durable than any particular reconstruction model.

## Scientific status

This project is speculative engineering constrained by real neuroscience.

Current connectomics, cell atlases, engram research, physiology, and neurotechnology can inform what information might matter. They do **not** currently establish a sufficient recipe for human consciousness backup or an empirical test for first-person continuity after destructive reconstruction.

Where a claim depends on current science, use `docs/transcendence/SOURCE_INDEX.md` and preserve the distinction among documented evidence, project inference, hypothesis, dispute, and unknown.

## Governance

Transcendence governance is defined in the root `WARDEN.md`.

The HC `WARDEN.md` copied into the initial repository is preserved as provenance under `docs/imported-hc/WARDEN_ORIGINAL.md`; it does not silently govern this project.
