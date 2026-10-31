> **License:** Source-visible, **not open source**. Original material is proprietary. Private noncommercial evaluation, research, and security review are permitted only as specified in [LICENSE](LICENSE). Commercial use, redistribution, hosted services, and public derivatives require separate written permission; see [COMMERCIAL_LICENSE.md](COMMERCIAL_LICENSE.md). Third-party material retains its own licenses.

# Transcendence — modular cognitive architecture and reference controls

Transcendence is a reusable **cognitive-architecture specification and executable reference-kernel research project**. It divides a proposed cognitive system into independently governed capabilities—memory, attention, evidence, reasoning, affect, identity, routing, behavior, I/O, and effect control—and supplies a small Python implementation to test selected cross-cutting invariants.

Its deliverables today are architecture and conformance contracts, plus a bounded, standard-library reference kernel. **It is not an installed cognitive runtime, a trained model, a working virtual person, or a complete host authorization service.** Integrators can study the contracts and execute the reference tests before deciding which components to implement in their own environment.

## What is implemented

| Component | Available now | Important limit |
| --- | --- | --- |
| [Architecture and subsystem specifications](docs/REPOSITORY_MAP.md) | Contracts for cognitive organs, evidence, routing, memory, representation, and protected effects | Most named subsystems are designs, not runnable services |
| [In-memory reference kernel](runtime/reference_kernel/hc_kernel.py) | Typed observed/derived/predicted evidence, scoped current-memory projection, explicit routing, modeled authority grants and effect-state receipts | Tests operate on caller-supplied records and grant fixtures; they do not authenticate external subjects |
| [Durable reference kernel](runtime/reference_kernel/durable_kernel.py) | JSONL append journal, hash-linked records, reconstruction, read-only inspection, and recovery-epoch fencing | Hash continuity is not a signature/MAC; a writer able to rewrite and rehash the entire journal is outside its protection |
| [Reference-kernel tests](runtime/reference_kernel/test_hc_kernel.py) and [durability tests](runtime/reference_kernel/test_durable_kernel.py) | Executable checks for state distinctions, duplicate-request suppression, restart/recovery behavior, and damaged-journal rejection | Passing test cases does not establish multi-host deployment, tamper-resistant custody, or emergent cognition |
| [Conformance specification](specs/HC_CONFORMANCE_SUITE_V1.yaml) | Declared test and evidence expectations for a broader implementation | A specification is not proof that every runtime path conforms |

The reference-kernel code is self-contained Python using the standard library. Other planned areas remain predominantly documents: cognition and integration, current/deep memory, salience and affect, semantics and pragmatics, speech/I/O, kinesis, somatics, identity, and learning. Their directory READMEs and the [repository map](docs/REPOSITORY_MAP.md) explain the intended boundaries.

## Verify the executable slice

From a clone of this repository, with Python 3.12 (the version used in this README audit):

```bash
cd runtime/reference_kernel
python3 -m unittest -v test_hc_kernel.py test_durable_kernel.py
cd ../..
python3 -m unittest discover -s tests -v
```

The first command exercises the kernel's modelled authority, evidence, memory, effect, journal, and recovery behaviors. The second checks repository workspace-startup safety. These commands do **not** install a model, start a server, contact an external provider, change permissions, or perform a real-world action.

At the source revision audited for this README, the local Python 3.12 runs passed **12 in-memory**, **14 durable-kernel**, and **3 workspace-startup** tests. Those counts are local test evidence, not external security certification or host deployment qualification.

## Architecture navigation

- [Runtime model](docs/runtime/HYPERCONNECTOME_RUNTIME_MODEL.md) — how states, routes, and evidence are intended to connect.
- [Plasticity and state governance](docs/runtime/PLASTICITY_AND_STATE_GOVERNANCE.md) — boundaries on learning and state change.
- [Cross-system integration contract](docs/architecture/CROSS_SYSTEM_INTEGRATION_CONTRACT.md) — proposed consumption and delegation boundaries.
- [Reference-kernel guide](runtime/reference_kernel/README.md) — the original in-memory vertical-slice scope and its limits.
- [Implementation status](docs/runtime/REFERENCE_KERNEL_IMPLEMENTATION_STATUS.md) and [qualification notes](docs/qualification/MINIMAL_REFERENCE_KERNEL_VERTICAL_SLICE_2026-09-10_R2.md) — historical evidence cuts. The implementation-status note predates the current durable-journal module; inspect current source and tests for the actual executable surface.
- [Authority and effect governance](basic%20operating%20instructions/AUTHORITY_CONSENT_AND_EFFECT_GOVERNANCE.md) — requirements for protected actions.

## Integration and security boundaries

**A model's claim is not host authority.** The embedded host must authenticate actors, bind each model provider/adapter and runtime instance to a stable subject, independently establish current scoped consent, and authorize each protected effect at its execution boundary. No permission, consent, history, or identity from one model adapter transfers automatically to another. This project specifies aspects of that architecture but does **not** implement a coherent issuer and verifier for immutable provider bindings or a production authorization service.

The in-memory reference `AuthorityGrant` is a modeled fixture with basis and scope; it cannot certify that a real actor granted permission. The durable journal detects some corruption and ordering failures but is **not** independently authenticated or protected against an adversary with arbitrary write access. In-flight effects after recovery require reconciliation, not replay. Passing a kernel test therefore means only that its narrowly asserted behavior was observed in the tested process.

Source-level workspace safety checks also guard against a previously removed concealed VS Code `folderOpen` task and executable content disguised as a font. They test the current tracked tree—not older checkouts, extensions, installed hosts, or user-level editor configuration. Do not execute historical removed payloads. See the [workspace safety tests](tests/test_workspace_startup_safety.py).

## Maturity and reuse

**Status: research architecture with executable control-reference slices.** There is no complete temporal hypergraph executor, organ scheduler, distributed coalition runtime, trained language model, authenticated multi-provider host, physical embodiment interface, or end-to-end cognitive deployment in this repository. Reuse the documented interfaces as an evaluation/design reference; implement and qualify real service, process-isolation, identity, consent, provider, storage, and effect controls separately.

Contributions follow [CONTRIBUTING.md](CONTRIBUTING.md) and [CLA.md](CLA.md). Public source visibility does not grant an unrestricted software redistribution or model-training license.
