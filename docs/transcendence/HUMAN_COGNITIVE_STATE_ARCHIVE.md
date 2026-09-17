# Human Cognitive State Archive (HCSA)

Status: archive architecture.

## Definition

A Human Cognitive State Archive is a durable, versioned, provenance-preserving container for evidence and derived state relevant to reconstructing a particular human's cognitive organization.

An HCSA is not a declaration that consciousness has been captured.

## Design goals

An archive should:

- preserve raw evidence whenever feasible;
- retain subject/time/capture context;
- distinguish measurement from inference and synthesis;
- permit future reinterpretation under improved science;
- support temporal rather than fictitious single-snapshot state;
- retain discarded-information records for lossy transformations;
- remain independent of one vendor, model, or target substrate;
- preserve access/consent/authority metadata separately from possession.

## Provenance classes

### MEASURED

Directly acquired physical/biological measurement from the subject or specimen.

### BEHAVIORALLY_OBSERVED

Demonstrated through task performance or externally observed behavior.

### SELF_REPORTED

Reported by the subject through introspection, testimony, preference statement, autobiographical report, or similar channel.

### DERIVED

Computed deterministically from source inputs by a specified transformation.

### INFERRED

Estimated from evidence using a model, hypothesis, or probabilistic procedure.

### INTERPOLATED

Estimated between measured temporal/spatial states under an explicit method.

### GENERATED

Created to fill missing information without direct subject evidence sufficient to classify it as inferred or interpolated.

### IMPORTED_REFERENCE

Taken from a population atlas, reference model, general theory, or other non-subject-specific source.

### UNKNOWN

Not established by available evidence.

## Provenance invariant

`GENERATED -> MEASURED` is forbidden.

A generated value may later be independently measured and superseded by a new measured record. The original generated record remains history.

## Minimum record fields

A material archive object should be able to represent:

- stable object/record ID;
- subject/archive ID;
- provenance class;
- source artifact IDs;
- capture/observation method;
- biological timestamp or temporal interval;
- archive-ingest timestamp;
- anatomical/functional scope when known;
- value/payload;
- units/representation;
- uncertainty or confidence;
- acquisition artifacts/known confounds;
- transformation/model version if derived;
- supersedes/superseded-by lineage;
- privacy/security classification;
- authority/consent scope;
- integrity digest.

## Temporal semantics

Measurements from different times are not a single simultaneous brain.

The archive should distinguish at least:

- stable structural state;
- slowly changing structural/plastic state;
- learned state;
- transient cognitive state;
- current regulatory/interoceptive state;
- developmental trajectory;
- pathology/injury trajectory;
- medication/anesthesia/intoxication state where material;
- pre-terminal and terminal perturbation;
- preservation/fixation artifact;
- capture-induced artifact.

Where simultaneous state is inferred from asynchronous measurements, that synthesis must be labeled as inference/interpolation rather than measurement.

## Snapshot model

An HCSA snapshot is a reproducible view over archive state at a specified version/time policy.

A snapshot should record:

- archive root/version;
- inclusion rules;
- cutoff time;
- accepted supersession policy;
- evidence classes included;
- model-derived layers included;
- unresolved conflicts;
- unknown coverage.

A reconstruction consumes a named snapshot, not "the archive" generically.

## Transformation lineage

Every transformation should identify:

- exact inputs;
- transformation code/model/version;
- parameters;
- output;
- uncertainty introduced;
- information discarded;
- whether the transformation is reversible;
- whether qualification holdouts were visible to the transformer.

## Contradiction model

Conflicting evidence is preserved.

For example, a self-reported preference may conflict with repeated behavioral choices. Neither source is deleted. An interpretation may weigh them, but it must preserve the disagreement and provenance.

## Durability

Future implementation should support:

- content-addressed immutable raw evidence;
- cryptographic integrity checks;
- open versioned schemas;
- redundant geographically separated copies;
- format migration with retained originals;
- reproducible transformation manifests;
- encryption and subject-level access controls;
- no sole dependency on one proprietary provider;
- recovery testing.

## Authority separation

Archive possession does not imply authority to reconstruct.

At minimum, future policy should represent distinct permissions for:

- storage;
- read access;
- research use;
- model training;
- interpretation;
- reconstruction;
- activation;
- modification;
- replication;
- disclosure;
- transfer;
- deletion/retention change.

`DATA_POSSESSION != PERSON_RECONSTRUCTION_AUTHORITY`

## Archive claim ceiling

An HCSA can be evaluated for coverage, integrity, provenance quality, and reproducibility.

It cannot by its existence prove that it contains every state required for consciousness or personal continuity.
