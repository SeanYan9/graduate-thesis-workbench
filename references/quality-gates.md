# Quality Gates

## Gate A: Structural

- Required chapter files exist.
- The outline and chapter headings agree.
- No unexpected chapter or missing required chapter exists.
- Section numbering, figure numbering, table numbering, and equation numbering
  are unique and monotonic where required.
- The table of contents and lists of figures/tables can be regenerated.

## Gate B: Evidence

- Every major claim has a claim-ledger row.
- Every literature claim has a verified source or an explicit blocker.
- Every results claim points to a data or analysis artifact.
- The text does not contain process notes, user instructions, or unresolved
  template language.

## Gate C: Numerical

- The same value has one unit and one rounding rule across abstract, body,
  table, figure, conclusion, and appendix.
- Percentages have a visible denominator.
- Mean, standard deviation, confidence interval, p-value, effect size, and
  sample size are not mixed or silently omitted.
- Error bars and significance markers have an explicit definition.
- Causal language does not exceed the design.

## Gate D: Visual

- Every figure/table has a purpose, caption, provenance, and in-text reference.
- Exact-data figures have a data manifest, script, and reproducible output.
- Conceptual figures have an editable source and a thesis-supported graph.
- Figure and table values agree with the source artifacts.
- The rendered output is readable at final document size.

## Gate E: Reference

- In-text citations and bibliography reconcile in both directions.
- Reference metadata matches canonical sources.
- DOI/URL, author order, year, venue, volume, issue, pages or article number
  are checked.
- Claims are checked against source content, not just bibliographic identity.

## Gate F: DOCX/PDF

- The output opens successfully.
- OOXML validation passes.
- Rendering produces the expected page count or an explained change.
- No clipping, blank pages, missing glyphs, broken equations, displaced
  captions, unreadable tables, or stale hyperlinks remain.

## Completion Language

Use:

- `DONE` only when all applicable gates pass.
- `DONE_WITH_CONCERNS` when the artifact is usable but a non-blocking risk is
  documented.
- `NEEDS_EVIDENCE`, `NEEDS_DATA`, `NEEDS_FORMAT_CHECK`, or `BLOCKED` when a
  gate prevents a reliable final result.

Never substitute "看起来正确", "应该完成", or "大致没有问题" for evidence.
