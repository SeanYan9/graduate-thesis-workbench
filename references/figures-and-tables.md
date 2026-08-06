# Figures and Tables Contract

## Figure Brief

Create a brief before drawing:

```markdown
# Figure F-01
- Section:
- Claim supported:
- Reader question:
- Artifact type: exact-data | conceptual | mixed
- Archetype: comparison | process | architecture | mechanism | taxonomy | deployment
- Reading order:
- Required nodes/series:
- Required relationships:
- Data source:
- Provenance: original | reproduced | adapted | external
- Backend:
- Output formats:
- Caption takeaway:
- Acceptance checks:
```

The figure serves one reader question. Do not use a visual to decorate a weak
claim or to hide missing evidence.

## Exact-Data Figures

Use a real data file and a reproducible script. The data manifest must include:

| Figure | Data file | Real/mock | Source | Transformations | Script | Outputs |
|---|---|---|---|---|---|---|

Rules:

- `mock_` and `synthetic_` files are planning-only.
- State the unit of analysis, denominator, metric direction, sample size, and
  error-bar basis.
- Preserve the raw data, transformation code, and output path.
- Prefer PNG plus SVG or PDF. Use the thesis template's width and resolution.
- Use plots for exact values. Do not ask an image model to draw axes, numbers,
  benchmark bars, significance marks, or measured geometry.
- Check labels, units, legends, color meaning, limits, annotations, rounding,
  and caption claims against the data.

## Conceptual Figures and Flowcharts

Use an editable vector or text source as the primary artifact:

- Mermaid for simple process maps and feedback loops;
- Graphviz for directed graphs and dependency structures;
- TikZ for publication-controlled LaTeX diagrams;
- draw.io, PowerPoint, or another editable vector tool when required by the
  university template.

Use image generation only as a draft or for a non-quantitative concept
illustration. Replace text-heavy final diagrams with an editable source.

For each diagram, validate:

- every node names a real component, operation, or state;
- every arrow has a defined direction and relationship;
- branches, merges, loops, and control/data paths are explicit;
- the visual emphasis matches the thesis contribution;
- no unsupported mechanism or causal relation was added;
- the caption states the takeaway, not merely the inventory of boxes;
- all terms and abbreviations are defined in the chapter.

## Tables

Before formatting a table, lock:

- comparison question and row/column meaning;
- unit and denominator;
- decimal precision and rounding rule;
- sample size and uncertainty representation;
- missing-value policy;
- source and data provenance;
- whether the table is main text, appendix, or supplementary.

For data tables, keep a machine-readable source file whenever possible. For
each table in the manuscript, include a caption and, when data are external or
compiled, a separate `数据来源:` line after the `注:` line.

## Visual QA

Inspect at the final page size:

- clipping, overlap, blank margins, missing glyphs, and unreadable labels;
- axis and legend order;
- table splits and repeated headers;
- consistent numbering and in-text references;
- color meaning in grayscale or color-blind viewing;
- caption-to-figure and figure-to-data agreement.
