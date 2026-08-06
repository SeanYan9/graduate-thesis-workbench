# DOCX Workflow

Use `DOCX工具` for document operations. This workbench supplies routing and
quality gates; it does not replace the DOCX tool's OOXML, equation, revision,
comment, or rendering scripts.

## Safe Edit Sequence

1. Preserve the original input file.
2. Extract or inspect the document structure and styles.
3. Apply a narrowly scoped edit to a copy under the project root.
4. Validate OOXML relationships and content types.
5. Render the output to PDF or page images.
6. Inspect headings, page breaks, headers, footers, equations, captions,
   tables, fonts, hyperlinks, and figure placement.
7. Report the output path and the validation evidence.

## Thesis-Specific Checks

- heading levels match the approved outline;
- chapter, section, figure, table, equation, appendix, and reference numbering
  is stable;
- captions are attached to the correct object;
- table notes keep `注:` and `数据来源:` on separate lines when required;
- formulas remain native equations or preserve the source format;
- Chinese punctuation, spaces, fonts, and mixed Chinese-English terms are
  consistent;
- tracked changes and comments are intentionally retained or accepted;
- no source file is silently overwritten.

Text extraction is necessary for content checks but insufficient for layout
verification. A document is not complete until the rendered pages are checked.
