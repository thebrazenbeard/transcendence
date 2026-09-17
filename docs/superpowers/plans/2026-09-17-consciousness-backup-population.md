# Transcendence Architecture Population Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the imported HC Brain snapshot into a coherent Transcendence research repository for evidence-preserving human cognitive-state capture, translation, reconstruction, and qualification.

**Architecture:** Preserve the copied HC material as a candidate target substrate and provenance-bearing reference. Add a separate Transcendence documentation layer that owns the human-capture problem, keeps raw evidence distinct from interpretation and generated state, maps human state to HC only through explicit many-to-many functional mappings, and constrains reconstruction claims through independent qualification.

**Tech Stack:** Markdown documentation, Git/GitHub provenance, existing HC reference architecture.

**Spec:** `docs/superpowers/specs/2026-09-17-consciousness-backup-design.md`

## Global Constraints

- `BEHAVIORAL_EQUIVALENCE != PERSONAL_CONTINUITY`
- `CONNECTOME_CAPTURE != COMPLETE_PERSON_CAPTURE`
- `FUNCTIONAL_RECONSTRUCTION != SUBJECTIVE_CONTINUITY_PROOF`
- `HC_COMPATIBILITY != SUCCESSFUL_HUMAN_REINSTANTIATION`
- Do not silently convert inferred/generated state into measured subject state.
- Do not map biological anatomy one-to-one to HC folders.
- Imported HC material remains a candidate reconstruction substrate/reference ontology, not feasibility proof.
- Preserve source provenance and unknowns.
- Root governance must not silently inherit copied HC governance.

---

### Task 1: Preserve imported HC root provenance and establish repository identity

**Files:**
- Create: `docs/imported-hc/README_ORIGINAL.md`
- Create: `docs/imported-hc/WARDEN_ORIGINAL.md`
- Create: `docs/imported-hc/PROVENANCE.md`
- Modify: `README.md`
- Modify: `WARDEN.md`

**Interfaces:**
- Consumes: imported HC snapshot at `main@68e7a794d6134e8319121404f31062288dc8d6a3`.
- Produces: explicit Transcendence identity and non-destructive imported-HC provenance boundary.

- [ ] **Step 1:** Copy the original root README and WARDEN verbatim into `docs/imported-hc/`.
- [ ] **Step 2:** Write `PROVENANCE.md` describing what is known, unknown, imported, and native.
- [ ] **Step 3:** Replace root README with the Transcendence mission, architecture pipeline, claim ceiling, and navigation.
- [ ] **Step 4:** Replace root WARDEN with Transcendence-specific governance that preserves Patrick's owner authority and explicitly leaves project-specific wardenship unassigned unless later established.
- [ ] **Step 5:** Verify the original root texts remain recoverable byte-for-byte from the preserved files.

### Task 2: Split the design into durable architecture documents

**Files:**
- Create: `docs/transcendence/ARCHITECTURE.md`
- Create: `docs/transcendence/HUMAN_COGNITIVE_STATE_ARCHIVE.md`
- Create: `docs/transcendence/CAPTURE_LAYERS.md`
- Create: `docs/transcendence/HUMAN_TO_HC_TRANSLATION.md`

**Interfaces:**
- Consumes: approved design specification.
- Produces: canonical documentation for Capture -> Archive -> Interpret -> Translate.

- [ ] **Step 1:** Define the six-stage pipeline and stage-boundary invariants.
- [ ] **Step 2:** Define HCSA provenance classes, temporal semantics, lineage, unknown-state handling, and durability requirements.
- [ ] **Step 3:** Define structural, effective-connectivity, molecular, dynamic, embodied, cognitive-phenotype, and longitudinal-shadow capture layers.
- [ ] **Step 4:** Define many-to-many biological observation -> candidate causal function -> HC target mapping with retained discarded-information records.
- [ ] **Step 5:** Cross-check every mapping rule against the no-anatomy-shortcut constraint.

### Task 3: Define reconstruction, continuity, qualification, and threat boundaries

**Files:**
- Create: `docs/transcendence/RECONSTRUCTION_AND_QUALIFICATION.md`
- Create: `docs/transcendence/CONTINUITY_BOUNDARIES.md`
- Create: `docs/transcendence/THREAT_MODEL.md`

**Interfaces:**
- Consumes: HCSA and translation records.
- Produces: conservative reconstruction metadata, holdout testing model, claim ladder, continuity boundary, and security/epistemic threats.

- [ ] **Step 1:** Define reconstruction-candidate metadata and immutable lineage.
- [ ] **Step 2:** Define held-out subject-specific tests and contamination/exposure lineage.
- [ ] **Step 3:** Define structural/state/autobiographical/semantic/procedural/value/affective/conative/self/social/cognitive-style qualification dimensions.
- [ ] **Step 4:** Define the claim ladder through `CONTINUITY_PRESERVATION_CANDIDATE`, keeping `SUBJECTIVE_CONTINUITY` UNKNOWN absent a future empirical criterion.
- [ ] **Step 5:** Enumerate provenance laundering, overfitting, target forcing, snapshot conflation, terminal-state corruption, behavioral-clone substitution, confidence inflation, archive loss, unauthorized reconstruction, and proprietary lock-in.

### Task 4: Establish research frontier and source ledger

**Files:**
- Create: `docs/transcendence/RESEARCH_QUESTIONS.md`
- Create: `docs/transcendence/SOURCE_INDEX.md`

**Interfaces:**
- Consumes: current neuroscience sources and architecture unknowns.
- Produces: explicit unknowns/falsifiable questions and source-to-claim provenance.

- [ ] **Step 1:** Record unresolved minimum-sufficient-state, dynamics, molecular-state, causal-inference, translation, and continuity questions.
- [ ] **Step 2:** Record source metadata and exact architectural conclusions each source supports.
- [ ] **Step 3:** Record what each source does not establish, especially consciousness-backup feasibility or subjective continuity.
- [ ] **Step 4:** Verify source claims against primary/high-authority publications.

### Task 5: Repository-level verification

**Files:**
- Review all files changed by Tasks 1-4.

**Interfaces:**
- Consumes: completed documentation surface.
- Produces: reviewable architecture cut with explicit claim limits.

- [ ] **Step 1:** Verify required files exist and root README links resolve textually.
- [ ] **Step 2:** Search for forbidden implication patterns: connectome=sufficient person, HC=validated human reconstruction, behavioral match=continuity proof.
- [ ] **Step 3:** Verify every provenance class in the design spec is represented in HCSA documentation.
- [ ] **Step 4:** Verify original README and WARDEN are preserved in `docs/imported-hc/`.
- [ ] **Step 5:** Refresh draft PR #1 with exact implementation scope and remaining unknowns.
