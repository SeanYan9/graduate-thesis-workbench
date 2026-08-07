# DOCX Workflow

Use `DOCX工具` for document operations. This workbench supplies routing and
quality gates; it does not replace the DOCX tool's OOXML, equation, revision,
comment, or rendering scripts. When a user provides a formatted Word file,
also read `docx-template-style-inheritance.md`.

## Safe Edit Sequence

1. Preserve the original input file.
2. Run `scripts/docx_style_profile.py` against the input and preserve the
   resulting style profile as an audit artifact.
3. Apply a narrowly scoped edit to a copy under the project root using only
   styles that already exist in the input document.
4. Compare `word/styles.xml` before and after the content insertion.
5. Validate native OMML with `scripts/validate_docx_math.py` when formulas or
   quantity symbols are present.
6. Validate OOXML relationships and content types.
7. Render the output to PDF or page images.
8. Inspect headings, page breaks, headers, footers, equations, captions,
   tables, fonts, hyperlinks, and figure placement.
9. Report the output path and the validation evidence.

## Thesis-Specific Checks

- heading levels match the approved outline;
- chapter, section, figure, table, equation, appendix, and reference numbering
  is stable;
- captions are attached to the correct object;
- table notes keep `注:` and `数据来源:` on separate lines when required;
- formulas remain native equations or preserve the source format;
- formula conversion is in-place, with no visible LaTeX or duplicate plain
  text remaining;
- user-defined template styles remain unchanged and newly inserted content
  uses existing style names;
- Chinese punctuation, spaces, fonts, and mixed Chinese-English terms are
  consistent;
- tracked changes and comments are intentionally retained or accepted;
- no source file is silently overwritten.

Text extraction is necessary for content checks but insufficient for layout
verification. A document is not complete until the rendered pages are checked.
