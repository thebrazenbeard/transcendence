# Human-to-HC Translation

Status: translation architecture.

## Purpose

Translate subject-specific evidence into a candidate HC-compatible representation without pretending that human neuroanatomy and HC software/subsystem boundaries are homologous.

## Required intermediate layer

Use:

`BIOLOGICAL OBSERVATION -> CANDIDATE CAUSAL FUNCTION -> FUNCTIONAL STATE OBJECT -> HC TARGET INTERFACE(S)`

Do not use:

`ANATOMICAL REGION -> HC DIRECTORY`

The latter destroys distributed/multifunctional organization and manufactures certainty.

## Mapping cardinality

Mappings are many-to-many.

One biological mechanism may contribute to memory, affect, salience, self-model, prediction, and conation.

One HC target domain may require evidence distributed across many biological systems and behavioral observations.

## Translation record

A mapping record should preserve:

- translation-record ID;
- source HCSA snapshot;
- biological/behavioral source object IDs;
- source provenance classes;
- candidate causal function;
- evidence strength;
- alternative interpretations;
- target architecture/version;
- target subsystem/interface IDs;
- transformation/model/version;
- output representation;
- uncertainty;
- information discarded/compressed;
- unmapped source state;
- reversibility;
- holdout exposure status;
- reviewer/qualification state.

## Unknown-preserving rule

The translator must be able to emit `UNKNOWN` or `UNMAPPED`.

Forcing every source datum into a target ontology is a data-loss failure.

## Initial HC target hints

These are interface hypotheses, not validated anatomical correspondences:

- autobiographical/semantic/procedural state -> memory + semantics + cognition + relevant skill systems;
- self-concept/continuity -> self identity + memory + chronology;
- preferences/drives/goals -> volitions-conations + affect + salience + cognition;
- interoceptive regulation -> homeostasis-interoception + somatics + affect;
- emotional associations -> affect + memory + salience + social/self models;
- person/relationship models -> Empathy + sociological behaviors + memory + pragmatics;
- language/meaning -> semantics + pragmatics + speech/phonetic systems + memory;
- learned motor/body mappings -> kinesis + adaptable I/O + somatics + memory;
- conflict/cross-domain integration -> resolver + integration-arbitration.

## HC snapshot status

The imported HC tree is a candidate target ontology.

Before a real translation implementation, the project must bind translation records to an exact HC architecture version or commit and explicitly describe any Transcendence-specific extensions.

## Compression accounting

Any dimensionality reduction, abstraction, embedding, model distillation, or state synthesis must record what source information becomes unavailable afterward.

A translator should prefer retaining a pointer to full source evidence rather than treating the compressed output as the source of truth.

## Target evolution

If HC changes, old translations remain reproducible against their original target version.

Migration to a newer target produces a new translation artifact; it does not rewrite historical translation results.

## Validation direction

Eventually, candidate mapping rules should be challenged by:

- perturbation/causal neuroscience where ethically available;
- cross-modal agreement among structural, physiological, and behavioral evidence;
- reconstruction ablation studies;
- held-out subject-specific behavior;
- failure localization by target subsystem.

Until then, mapping claims remain design hypotheses with provenance.
