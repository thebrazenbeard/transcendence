# BCI and Continuity Migration

Status: architecture contract.

## Design premise

Transcendence assumes that brain-computer interface technology may eventually become substantially more capable than current systems.

The project does not depend on one forecast about when that happens, nor on one vendor or neural encoding.

BCI is treated as an interchangeable evidence/effect interface around the substrate-neutral HCSA.

## Adapter boundary

A BCI adapter declares:
- device/interface identity;
- acquisition modality;
- spatial/temporal resolution;
- coverage;
- calibration method;
- biological state/context;
- raw data representation;
- normalization/decoder version;
- uncertainty;
- stimulation/effect capabilities where applicable;
- safety/authority limits;
- exact transformation lineage.

Raw measurement and semantic interpretation remain separate objects.

## Acquisition modes

The architecture supports progressively richer BCI input such as:
- neural activity recordings;
- population dynamics;
- stimulation/response data;
- functional/effective connectivity evidence;
- sensorimotor mappings;
- longitudinal plasticity measurements;
- closed-loop calibration data;
- future structural/molecular measurements exposed through advanced interfaces.

Unknown future modalities can be added through versioned adapters without changing the identity of the archive.

## Bidirectional use

Future bidirectional BCI may support causal investigation and calibration by coupling measurements with bounded stimulation/effects.

A stimulation command is an effect request with explicit authority and safety scope. Its successful execution does not by itself establish semantic meaning or personal continuity.

## Gradual transfer

Gradual biological-to-synthetic transfer is a first-class migration path.

A migration lineage may record:
- biological modules/functions participating at each time;
- synthetic modules/functions participating at each time;
- shared/overlapping causal operation;
- state synchronization;
- handoff boundaries;
- rollback/reversibility;
- subject-reported continuity where available;
- behavioral/functional measurements;
- neural/causal measurements;
- forks or divergent descendants;
- failures/gaps.

The architecture should support mixed biological/synthetic operation rather than assuming reconstruction must happen after biological cessation.

## Continuity evidence

Gradual transfer can produce evidence about temporal/process and causal continuity that a destructive scan cannot.

It still must not silently become proof of phenomenal continuity.

`CONTINUOUS_CAUSAL_HANDOFF != PROVEN_CONTINUOUS_SUBJECTIVITY`

## Raw signal preservation

When lawful and technically feasible, retain raw neural recordings in addition to decoded state.

A later decoder may reinterpret earlier observations.

`OLD_DECODER_ERROR != PERMANENT_ARCHIVE_ERROR`

## Target independence

BCI-mediated migration may target:
- HC Brain;
- neuromorphic hardware;
- hybrid biological/synthetic systems;
- emulated neural systems;
- repaired/reconstructed biological tissue;
- future unknown substrates.

The HCSA and continuity-lineage model must remain valid across those targets.
