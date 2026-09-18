# Transcendence Universal Open + Future-BCI Architecture Amendment

Status: APPROVED IMPLEMENTATION BASELINE

Date: 2026-09-17
Approved by owner in chat: 2026-09-17
Branch: `architecture/consciousness-backup-v1`
Extends: `docs/superpowers/specs/2026-09-17-consciousness-backup-design.md`

## 1. Universal project scope

Transcendence is a universal human-continuity architecture, not a Patrick-specific continuity project and not an identity-bearing archive.

The public repository contains:
- open specifications;
- schemas and interchange formats;
- reference software;
- validation and qualification tooling;
- capture/BCI adapter contracts;
- preservation/recovery protocols;
- reconstruction interfaces;
- threat models and scientific evidence boundaries.

Actual per-person continuity payloads belong in separately controlled private stores. A subject's archive, measurements, memories, relationships, neural recordings, health information, and other continuity-bearing state do not belong in the public architecture repository.

`PUBLIC_ARCHITECTURE != PERSONAL_CONTINUITY_PAYLOAD`

## 2. Access and commons model

The realistic non-negotiable baseline is an open commons:
- free-to-use specifications and formats;
- open-source reference implementations;
- self-hostability;
- exportability;
- provider-neutral archives;
- no single-vendor restore dependency;
- independent validation;
- migration between custodians/providers;
- no architecture feature that requires permission from one company to recover a person's archive.

The aspirational service layer is a genuinely free-to-the-user continuity service. Storage, compute, BCI hardware, clinical acquisition, and future reconstruction may carry real costs, so the architecture does not falsely promise zero-cost infrastructure today.

A public-benefit/free service may be built later, but it must remain an optional deployment of the open architecture rather than the only usable implementation.

`FREE_PUBLIC_SERVICE_GOAL != SINGLE_PROVIDER_DEPENDENCY`

## 3. Stable human-state contract

Transcendence should normalize evidence into a substrate-neutral Human Cognitive State Archive (HCSA), not into one BCI vendor's format or one reconstruction substrate's internal representation.

Acquisition channels are adapters around the archive/state contract:

`behavioral | autobiographical | physiological | digital-life | BCI/neural | connectomic | future unknown channels -> HCSA`

Reconstruction channels likewise consume versioned archive state through target adapters:

`HCSA -> HC Brain | neuromorphic | biological repair | hybrid BCI | emulated neural | future unknown substrate`

HC Brain remains a candidate reference target, not the definition of the person.

## 4. BCI as a first-class future channel

Transcendence explicitly presumes that progressively richer brain-computer interface technology may become available and must be usable without redesigning the archive from scratch.

BCI support is required on both sides:

### Acquisition
A BCI adapter may contribute:
- sparse or dense electrophysiology;
- neural population activity;
- stimulation-response measurements;
- effective-connectivity evidence;
- plasticity/calibration state;
- sensory/motor mappings;
- long-duration longitudinal neural observations;
- future structural, molecular, or other neural state if exposed by later technology.

### Bidirectional calibration
A future bidirectional BCI may support:
- controlled probing;
- closed-loop perturbation;
- causal mapping;
- synthetic-neural co-adaptation;
- calibration between biological and non-biological representations.

### Reconstruction/migration
A sufficiently capable interface may participate in:
- state reinjection;
- synthetic module coupling;
- gradual function transfer;
- overlapping biological/synthetic operation;
- reversible/partially reversible migration experiments.

No particular electrode type, vendor, encoding, implant architecture, sampling rate, or present-day neuroscience theory is canonical.

## 5. Measurement versus interpretation

A BCI measurement is evidence, not its semantic interpretation.

Example:

`RECORDED_PATTERN_X` may be `MEASURED`.

`PATTERN_X_REPRESENTS_MEMORY_Y` is `INFERRED` unless independently established by a stronger method.

Raw source signals should remain preservable alongside normalized and interpreted state whenever lawful and technically feasible.

This permits future science to reinterpret old measurements rather than being trapped by an obsolete decoder.

`NEURAL_SIGNAL != SEMANTIC_MEANING_BY_DEFAULT`

## 6. Continuity operations and lineage

The architecture must represent at least these operations without conflating them:

- `BACKUP` — continuity-bearing state is preserved.
- `RESTORE` — preserved state is instantiated into a functioning target.
- `SUCCESSOR` — a resulting instance derives materially from preserved state while stronger identity continuity remains unestablished.
- `FORK` — two or more descendants continue independently from a shared predecessor state.
- `MIGRATION` — state/function moves between substrates under a controlled handoff.
- `GRADUAL_TRANSFER` — biological and synthetic substrates overlap while function is progressively transferred.

Lineage is a graph, not necessarily one linear "real person" pointer. After a fork, descendants share history to the branch point and then accumulate distinct histories.

## 7. Continuity dimensions

Transcendence tracks distinct continuity dimensions rather than collapsing them into one claim:

- biological continuity;
- autobiographical/informational continuity;
- psychological continuity;
- functional continuity;
- causal/neural continuity where measurable;
- temporal/process continuity;
- phenomenal/subjective continuity.

Evidence for one dimension does not prove another.

`FUNCTIONAL_CONTINUITY != PHENOMENAL_CONTINUITY_PROOF`

## 8. Gradual BCI-mediated migration

Gradual transfer is a first-class research path.

The architecture should support future experiments in which biological neural function and synthetic function coexist, exchange state, calibrate, and progressively shift causal load.

Relevant evidence includes:
- continuity of active state across transitions;
- degree of causal participation by each substrate;
- memory/self-model availability during the transition;
- reversible and irreversible handoff points;
- failure recovery;
- branching/fork events;
- exact chronology.

This path may ultimately provide different continuity evidence than destructive scan-and-reinstantiate methods. The architecture supports the experiment without deciding the metaphysical result in advance.

## 9. Preservation invariant

Whenever technically and legally feasible, preserve:
1. raw evidence;
2. normalized evidence;
3. interpretations;
4. derived continuity state;
5. transformation lineage;
6. conflicts/unknowns;
7. later supersession.

Do not preserve only the newest interpretation.

A future 2050 decoder should be able to revisit a 2035 neural recording without depending on the 2035 interpretation layer.

## 10. Service portability

Any eventual public service must support:
- complete subject export;
- integrity verification;
- encrypted portable archives;
- documented schema/version migrations;
- independent restore testing;
- multiple custodians/replicas;
- no proprietary-only key required to interpret a valid archive;
- no requirement that the original service remain alive.

Service disappearance must not make a valid archive unrecoverable.

## 11. Success direction

Near-term success:
- open continuity data model;
- private per-person archive boundary;
- provenance and temporal lineage;
- present-day capture adapters;
- BCI-neutral adapter contract;
- backup integrity/recovery tooling;
- reconstruction/qualification contracts.

Long-term success:
- increasingly rich BCI capture;
- causal validation;
- substrate adapters;
- gradual-transfer experiments;
- free/public-benefit access where sustainable.

The project must remain useful even if subjective-continuity science remains unresolved.
