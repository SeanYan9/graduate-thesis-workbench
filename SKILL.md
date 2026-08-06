---
name: graduate-thesis-workbench
description: Use when revising or filling a Chinese or bilingual graduate thesis, including chapter planning and drafting, literature review, claim-citation verification, reference repair, DOCX editing, data tables, scientific plots, flowcharts, architecture diagrams, figure captions, authorship-aware prose review, AIGC-risk audit, cross-reference audits, or final thesis QA. Trigger on 大论文, 毕业论文, 章节补全, 图表, 流程图, 交叉引用, 参考文献核验, AIGC风险, AI写作痕迹, or Word论文.
---

# Graduate Thesis Workbench

## Purpose

Treat a graduate thesis as an evidence-traceable system of claims, chapters,
data, figures, tables, references, and document structure. Route each request
to the smallest appropriate workflow, keep manuscript prose separate from
planning notes, and fail closed when evidence or provenance is missing.

## Hard Gates

- Do not invent references, DOI metadata, statistics, experiment results,
  sample sizes, mechanisms, figure values, table values, or source URLs.
- Do not promote a plan, hypothesis, mock value, synthetic value, or visual
  placeholder into manuscript evidence. Mark it explicitly and keep it out of
  final claims.
- Do not write a literature-driven paragraph until an evidence map and
  paragraph blueprint exist.
- Do not write a Results or Discussion claim until the relevant data,
  analysis output, or verified source is available.
- Do not create an exact-value plot with an image model. Use real data and an
  auditable plotting script.
- Do not create a conceptual diagram without a figure brief that names the
  claim, components, connections, reading order, and provenance.
- Do not promise a specific AIGC or detector score, optimize text against a
  detector as if it were an authorship test, or disguise AI assistance.
- Do not inject fake typos, random punctuation, artificial personal stories,
  unsupported first-person experience, synonym noise, or deliberate factual
  awkwardness to simulate human authorship.
- Do not rewrite academic prose in a casual, humorous, promotional, or
  personality-heavy voice. Match the author's supplied writing sample and the
  discipline's register instead.
- Do not change numbers, results, equations, defined technical terms, or
  citations during an authorship or AI-pattern pass.
- Treat AI-writing patterns as review signals, not proof of authorship. Use
  clusters, genre context, the author's own samples, and provenance records.
- Do not claim a chapter, figure, table, citation set, or DOCX is complete
  until the workspace validator and required specialist checks pass.
- Keep unresolved issues in a machine-readable ledger. Use `BLOCKED`,
  `NEEDS_EVIDENCE`, `NEEDS_DATA`, or `NEEDS_FORMAT_CHECK` instead of hiding
  uncertainty in polished prose.

## Route the Request

| Request | Required route | Primary artifacts |
|---|---|---|
| Outline, chapter order, multi-file revision | Project orchestration | `plan/project-overview.md`, `plan/outline.md`, `plan/progress.md` |
| Background, Introduction, Related Work | Evidence-driven writing | `plan/evidence-map.md`, paragraph blueprints, claim ledger |
| Method or system chapter | Technical chapter route | input-output flow, notation ledger, reproducibility checklist |
| Results, Discussion, experiment closure | Results analysis first | analysis report, statistics appendix, figure catalog |
| Exact data figure or table | Data visualization route | data manifest, script, editable source, PNG/SVG/PDF |
| Flowchart, architecture, mechanism, conceptual diagram | Figure brief route | figure brief, editable diagram source, rendered preview |
| Reference list or cross-citation audit | Citation verification route | reference ledger, claim-support report, reconciliation report |
| Authorship, AIGC-risk, or AI-pattern review | Academic authenticity route | author voice profile, detect-only audit, minimal revision report |
| Word/DOCX modification | DOCX route | changed DOCX, OOXML validation, rendered inspection |
| Final thesis audit | Independent QA route | audit report, blockers, verification evidence |

Load only the reference file needed for the selected route:

- `references/workflow-contract.md` for project setup and task routing.
- `references/evidence-and-citations.md` for claims, sources, and references.
- `references/figures-and-tables.md` for visual and tabular artifacts.
- `references/docx-workflow.md` for Word document operations.
- `references/quality-gates.md` for final audits and fail-closed rules.
- `references/chinese-thesis-style.md` when editing the user's Chinese prose.
- `references/academic-authorship-and-aigc.md` for authorship integrity,
  AI-pattern review, voice calibration, and disclosure boundaries.
- `references/source-distillation.md` when explaining provenance or updating
  this toolkit.

## Operating Workflow

1. **Intake**
   - Identify the project root, thesis type, target template, current chapter,
     file format, existing outline, source pool, data availability, and
     requested output path.
   - Inventory DOCX, PDF, Markdown, LaTeX, image, spreadsheet, CSV, JSON,
     BibTeX, and reference-list inputs before editing.
   - Read the current outline and document structure before proposing prose.

2. **Establish the project contract**
   - Create or update `plan/project-overview.md`, `plan/outline.md`, and
     `plan/progress.md` for any task touching more than one paragraph.
   - Create `plan/claim-ledger.md` for substantive claims and
     `plan/evidence-map.md` for literature-driven sections.
   - Create `figures/figure-catalog.md` and `figures/data-manifest.md` when
     figures, tables, simulations, or experimental data are involved.
   - Record the exact files allowed to change and the unresolved gaps.
   - When prose is generated or substantially rewritten, request an author
     writing sample when available and record its path in
     `plan/author-voice-profile.md`.

3. **Build before polishing**
   - Write a one-sentence purpose for the chapter or artifact.
   - Build paragraph roles, claim-evidence links, and figure/table roles.
   - Draft topic sentences or captions first, then write the surrounding prose.
   - Keep user instructions, revision notes, and placeholders out of manuscript
     paragraphs.
   - Distinguish author-originated text, AI-assisted draft text, and
     author-approved revision in `plan/ai-assistance-log.md`.

4. **Verify at the source boundary**
   - Verify each citation's existence and bibliographic fields before adding it.
   - Verify that the cited source supports the exact claim, not merely the topic.
   - Trace each reported value from source data through transformations to the
     final paragraph, table, or figure.
   - Reconcile in-text citations, reference list, figure/table numbering, units,
     values, sample sizes, and captions after every substantive edit.

5. **Review independently**
   - Run the mechanical validator.
   - Run a separate semantic review focused on unsupported claims, missing
     definitions, causal overreach, stale cross-references, and visual
     misrepresentation.
   - Render final DOCX/PDF outputs and inspect page breaks, fonts, equations,
     captions, tables, figures, hyperlinks, and blank pages.
   - For an authorship pass, run detection before rewriting, apply only
     evidence-preserving edits, compare against the author's sample, and obtain
     author review of substantive changes. Report signals and changes, never
     an alleged detector score.
   - Report exact commands and outputs before using completion language.

## Local Validation Commands

Use the bundled scripts from the skill directory:

```powershell
python scripts/init_thesis_project.py <project-root>
python scripts/validate_thesis_workspace.py <project-root>
python scripts/validate_thesis_workspace.py <project-root> --json
```

The initializer creates the project contract without overwriting existing
files. The validator is fail-closed: exit code `0` means `DONE` or
`DONE_WITH_CONCERNS`; exit code `1` means a required gate is blocked. It checks
the contract files, claim/evidence links, reference verification status,
in-text citation reconciliation, manuscript placeholders, table source lines,
figure briefs, data manifests, mock-data leakage, and referenced figure
artifacts. It does not replace canonical-source checks, statistical review,
OOXML validation, or final rendered-page inspection.

## Academic Authorship Gate

Load `references/academic-authorship-and-aigc.md` whenever the user mentions
AIGC rate, AI writing traces, humanization, de-AI editing, voice matching, or
natural academic prose.

Use this route to make the thesis more specific, evidence-bound, and
consistent with the author's own writing. It is not a detector-bypass route.
Require an author sample when available, preserve the author's technical
vocabulary, audit before editing, make minimal targeted changes, and keep an
authorship log. For Chinese academic prose, prefer plain precise sentences and
the user's established transitions. Do not add casualness, emotional language,
invented imperfections, or fake individual experiences.

## Specialist Skill Routing

Use existing skills instead of duplicating their implementation:

- **Required for literature search:** `nature-academic-search` or another
  available academic search skill.
- **Required for reference verification:** `nature-ref-verifier`; use
  Crossref, DOI, publisher, arXiv, IEEE, CNKI, or WanFang as appropriate.
- **Required for scientific plots:** `nature-figure` or `publication-chart-skill`.
- **Required for strict experiment analysis:** `nature-statistics`,
  `results-analysis`, or the available domain-specific analysis skill.
- **Required for DOCX:** `DOCX工具`; preserve styles and validate OOXML.
- **Useful for prose structure:** `research-paper-writing`, `nature-writing`,
  and `writing-plans`.
- **Optional final prose pass:** `humanizer`, only after evidence and meaning
  are locked. Use its pattern catalog only; do not apply its personality,
  humor, colloquialism, or "soul injection" guidance to a thesis. It must not
  weaken technical precision or remove citations.

## Output Contract

Every non-trivial response must state:

- **Status:** `DONE`, `DONE_WITH_CONCERNS`, `NEEDS_EVIDENCE`, `NEEDS_DATA`,
  `NEEDS_FORMAT_CHECK`, or `BLOCKED`.
- **Changed or produced files:** exact paths.
- **Evidence consumed:** source IDs, data files, scripts, or user materials.
- **Claims affected:** supported, weakened, revised, or deferred.
- **Figures/tables affected:** purpose, provenance, data status, and output paths.
- **Authorship integrity:** author sample used, provenance record, substantive
  edits requiring author review, and disclosure decision.
- **Verification run:** commands and the relevant pass/fail lines.
- **Remaining risk:** unresolved facts, formatting, source, or interpretation gaps.

## Stop Conditions

Stop writing and return a blocker report when:

- a source cannot be uniquely identified or the claim cannot be checked;
- exact numeric data is absent, contradictory, or not traceable;
- the figure type, unit, denominator, error-bar basis, or comparison unit is
  unresolved;
- a diagram would introduce a mechanism or relationship not supported by the
  thesis;
- a DOCX edit would overwrite the source or alter unknown OOXML structures;
- the final render exposes clipping, missing glyphs, broken numbering, or
  unreadable visual content.

## Common Failure Modes

| Failure | Required correction |
|---|---|
| "待核验" references written as final references | Keep a provisional ledger row and verify before insertion |
| Mock data used in a Results sentence | Rename it `mock_` or `synthetic_`, mark planning-only, and block promotion |
| Figure generated before its claim is clear | Return to the figure brief and claim ledger |
| A real paper cited for an unsupported sentence | Downgrade or split the claim and find direct evidence |
| Table note omits a source line | Add separate `注:` and `数据来源:` lines |
| Chapter reads like a list of source summaries | Synthesize by theme, limitation, and bridge to the research gap |
| DOCX appears correct in text extraction but breaks visually | Render to PDF/images and inspect the actual pages |
| User asks for an "AIGC 0%" guarantee | Explain that detector scores are unstable signals, then perform authorship-aware, evidence-preserving review |
| Humanizer replaces technical terms or adds fabricated lived experience | Restore the author's terminology and flag the unsupported additions |
