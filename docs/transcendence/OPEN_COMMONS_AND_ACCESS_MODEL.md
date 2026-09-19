# Open Commons and Access Model

Status: architecture contract.

## Purpose

Transcendence is intended for everyone, not for one person's private continuity project.

The public architecture is a commons. Personal continuity data is not.

## Public architecture

The public repository may contain:
- specifications;
- schemas;
- interoperability profiles;
- reference implementations;
- capture/BCI adapter interfaces;
- archive tooling;
- integrity and recovery tooling;
- reconstruction interfaces;
- qualification suites;
- threat models;
- scientific source ledgers.

It must not contain a person's private continuity payload merely because that payload conforms to the architecture.

## Private subject stores

Each person's Human Cognitive State Archive belongs in a separate private subject-controlled store or equivalent private custody surface.

The architecture should support:
- one or more custodians;
- encrypted replication;
- offline copies;
- self-hosting;
- export/import;
- provider migration;
- independent integrity verification;
- independent restore testing.

A provider may host an archive without becoming the owner of its meaning, the sole recovery path, or the authority to reconstruct the subject.

## Free-to-use baseline

The realistic baseline target is:
- open specification;
- open formats;
- open-source reference stack;
- no mandatory proprietary provider;
- no mandatory subscription to decode a valid archive;
- no contractual lock-in as a technical requirement.

Hardware, clinical acquisition, storage, bandwidth, compute, and future BCI procedures may still have real-world costs.

## Free public service goal

A genuinely free-to-the-user continuity service is a long-term public-benefit goal.

Such a service should be treated as one deployment of the commons architecture, not the architecture itself.

If that service ceases to exist, valid subject archives should remain portable and recoverable elsewhere.

## Portability invariant

`SERVICE_FAILURE != ARCHIVE_DEATH`

A valid archive should be independently interpretable from open schemas and should support migration to another custodian or future implementation.

## Governance boundary

Possession of a subject archive does not imply permission to:
- inspect every field;
- train models on it;
- reconstruct the subject;
- activate a reconstruction;
- fork/replicate the subject;
- publish or sell the archive;
- change retention/destruction policy.

Authority is separately represented and subject-controlled where law and technology permit.
