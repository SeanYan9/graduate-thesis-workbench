# Workflow Contract

## 1. Intake Record

Before editing, record:

| Field | Required value |
|---|---|
| Project root | Exact local path |
| Thesis type | Master's thesis, doctoral thesis, capstone, or other |
| Domain | Engineering, computer science, traffic, etc. |
| Language | Chinese, English, or bilingual |
| Output format | DOCX, LaTeX, Markdown, PDF, or mixed |
| Current artifact | Draft chapter, full draft, proposal, paper, or data bundle |
| Target section | Exact chapter, subsection, figure, table, or reference range |
| Evidence status | Available, partial, missing, contradictory |
| Formatting authority | University template, department guide, or user rules |
| Allowed edits | Exact files and folders |

If the project root is not explicit, infer it from the provided file paths and
state the assumption before editing.

## 2. Project Contract

For work beyond one paragraph, keep these files in the project root:

```text
plan/
  project-overview.md
  outline.md
  progress.md
  claim-ledger.md
  evidence-map.md
  task-packets/
figures/
  figure-catalog.md
  data-manifest.md
references/
  reference-ledger.csv
qa/
  audit-report.md
```

The project can use different names when an existing template requires it, but
the same information must remain discoverable.

## 3. Stage Routing

### S0: Scope and structure

Use for title, outline, chapter order, missing sections, or a multi-file edit.

Required actions:

1. Read the existing table of contents and current file structure.
2. Separate fixed architecture from content still to be supplied.
3. Build a chapter-role table: purpose, central claim, inputs, outputs, and
   dependencies.
4. Record what must remain empty or provisional because evidence is not ready.

### S1: Evidence and literature

Use for background, Introduction, Related Work, research gap, and reference
repair.

Required actions:

1. Build an evidence map before prose.
2. Group literature by method family or problem boundary, not by a paper list.
3. Give each paragraph one main message and at least one direct evidence link.
4. Verify reference identity and claim support separately.

### S2: Method and technical chapters

Use for algorithms, models, system architectures, signal-control logic,
mathematical formulations, and implementation details.

Required actions:

1. State inputs, transformations, parameters, constraints, outputs, and
   feedback loops.
2. Define every symbol before use and keep notation stable.
3. Separate established components from the thesis contribution.
4. Link every process box in a diagram to a named operation in the text.

### S3: Results and experiment closure

Use for results, discussion, tables, performance comparisons, ablations,
simulation outputs, field observations, or statistical claims.

Required actions:

1. Inventory raw data, seeds, repetitions, baselines, metrics, and units.
2. Lock the comparison question and unit of analysis.
3. Run strict analysis before writing Results prose.
4. Record allowed wording, limitations, and forbidden stronger claims.

### S4: Figure and table production

Classify every visual as exact-data, conceptual, or mixed before production.
Use `references/figures-and-tables.md`.

### S5: Document integration

Use `DOCX工具` for DOCX modification, OOXML validation, equations, captions,
and rendering. Never treat text extraction alone as proof that a Word document
is correct.

### S6: Final QA

Run the workspace validator, reference reconciliation, visual inspection, and
independent semantic review. Completion is fail-closed.

## 4. Task Packet

For an independent chapter or artifact worker, create:

```markdown
## Task Packet
- Scope:
- Files to read:
- Files allowed to edit:
- Required skills:
- Evidence/data inputs:
- Required artifacts:
- Rejection checks:
- Validation commands:
```

The packet must state the output path and the unresolved gaps. A worker must
return the status, changed paths, evidence gaps, and validation result.
