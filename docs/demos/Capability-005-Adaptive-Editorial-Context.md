# Capability 5 Demo - Adaptive Editorial Context

## Status

Architecture baseline established.

Implementation demonstration will be completed before Capability 5
is considered Done.

## 1. Problem

The earlier workflow prototype represented article creation as an
ordered sequence.

That model could not fully support:

- natural mixed input,
- rapid first-pass creation,
- changes of direction,
- focused revision,
- expired source URLs,
- paywalled Author-supplied material,
- portable resumption,
- or Author-controlled project memory.

## 2. What Changed

Capability 5 establishes:

- the Adaptive Editorial Context as the system kernel,
- Editorial Contributions as interpreted events,
- versioned editorial components,
- multidimensional readiness,
- dependency-aware revision,
- durable source context,
- Editorial Integrity as a first-class component,
- and Portable Editorial Projects.

## 3. Why It Matters

The Studio can follow the Author's creative process without turning
article development into a form or wizard.

It can preserve context while allowing the Author to:

- add another source,
- revise perspective,
- change the thesis,
- revise only the conclusion,
- replace only the Hero Visual,
- or resume the project later.

It can also preserve the editorial value of a source when the
original URL later expires or becomes inaccessible.

## 4. Architecture Demonstration

```text
Author Contribution
        │
        ▼
Intent and Event Interpretation
        │
        ▼
Adaptive Editorial Context
├── Inputs
├── Sources
├── Durable Source Context
├── Evidence
├── Perspective
├── Thesis
├── Article
├── Hero Visual
├── Integrity
├── Readiness
└── Revision History
        │
        ├───────────────┐
        ▼               ▼
First Article Package   Focused Revision
        │               │
        └───────┬───────┘
                ▼
      Portable Editorial Project
```

## 5. Intended Author Demonstration

**Author**

> Here is a URL. I disagree with its conclusion because the real
> problem is operational accountability.

**Studio interpretation**

- Source supplied
- Topic inferred
- Author perspective supplied
- Research may be required
- Candidate thesis can be proposed

**Author**

> I copied this paragraph from a paywalled article. The important
> part is the statistic and the author's conclusion.

**Studio behaviour**

- Record known citation metadata
- Preserve a concise source summary
- Preserve the statistic used
- Preserve the Author's reaction
- Retain only the minimum necessary excerpt
- Record that future independent access may be limited

**Author**

> Now write the article.

**Studio behaviour**

- Use the accumulated Editorial Context
- Produce the first article package
- Include a 720 × 425 Hero Visual
- Preserve evidence provenance

**Author**

> Keep the article, but change the Hero Visual.

**Studio behaviour**

- Preserve the article
- Revise only the Hero Visual component
- Record the decision and new version

## 6. Portable Resume Demonstration

The Author saves:

```text
Ramrattan-Editorial-Project_Operational-Accountability-in-AI_2026.08.01v01.md
```

The Author decides where the file is stored.

The Product does not ask for or depend on the storage path.

Later, the Author chooses:

> Resume an Existing Editorial Project

The Studio restores:

- project identity,
- current thesis,
- Author perspective,
- durable source summaries,
- evidence used,
- article context,
- Hero Visual context,
- optional publication URLs,
- integrity state,
- and next actions.

## 7. Acceptance Criteria

Architecture baseline:

- [x] Adaptive Editorial Context defined
- [x] Portable Editorial Project defined
- [x] VCM filename standard defined
- [x] 255-character filename maximum defined
- [x] Resume behaviour defined
- [x] No external path dependency
- [x] Expired URL resilience defined
- [x] Paywalled excerpt handling defined
- [x] Editorial Integrity defined
- [x] Capability Definition of Done defined
- [x] Capability Demo standard introduced

Implementation:

- [ ] Context model implemented
- [ ] Component versioning implemented
- [ ] VCM filename generation implemented
- [ ] Markdown serialization implemented
- [ ] Resume validation implemented
- [ ] Durable source context implemented
- [ ] Integrity state implemented
- [ ] Behavioural tests passing

## 8. What We Learned

The product does not need to know where the Author stores their
files.

A few kilobytes of well-structured, Author-owned context can
preserve enough knowledge to resume an article project.

The durable value of a source is not merely its URL.

The project should preserve the claims, evidence, metadata,
interpretation, and editorial significance required to understand
the work later.

## 9. What Comes Next

Implement the Adaptive Editorial Context and Portable Editorial
Project model in Python.

The first implementation should remain independent of article and
image-generation providers.
