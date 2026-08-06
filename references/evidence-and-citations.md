# Evidence and Citation Contract

## Claim Ledger

Create one row for each substantive claim:

| ID | Claim | Type | Evidence IDs | Allowed wording | Forbidden wording | Status |
|---|---|---|---|---|---|---|
| C-001 | ... | literature / observed / computed / inferred | E-001 | ... | ... | verified |

Use these statuses:

- `verified`: the source or data directly supports the wording.
- `supported`: evidence supports the claim with a stated condition or scope.
- `observed`: the artifact shows the pattern, but interpretation remains limited.
- `inferred`: a reasoned interpretation that must be labeled as such.
- `needs-evidence`: do not promote into final manuscript prose.
- `placeholder`: planning-only and forbidden in submission output.

## Evidence Map

Use one row per source or data artifact:

| Evidence ID | Source/data | Type | Exact finding | Claim slot | Location | Risk |
|---|---|---|---|---|---|---|

`Location` must be a DOI landing page, section, page, table, figure, dataset
path, script output, or user-provided file location. A source title alone is
not enough for a specific claim.

## Reference Verification Order

Verify in this order, selecting the sources available for the document type:

1. DOI and publisher record.
2. Crossref metadata.
3. arXiv, IEEE Xplore, ACM Digital Library, or official repository.
4. CNKI, WanFang, university repository, or government source for Chinese
   journals, theses, and official statistics.
5. Semantic Scholar or another scholarly index for discovery and cross-check.

Never generate a final reference entry from memory. If the item cannot be
uniquely identified, keep it in the ledger as `unverifiable` and use
`[待核验文献]` outside the final manuscript.

## Field-Level Checks

Compare:

- authors and author order;
- exact title and key technical terms;
- year, volume, issue, and pages or article number;
- venue or issuing organization;
- DOI, URL, arXiv ID, or repository identifier;
- publication type: journal, conference, report, thesis, standard, or web page.

Report critical mismatches separately from warnings. A real paper with the
wrong DOI is still an invalid reference.

## Claim-Level Checks

For every citation attached to a concrete statement:

1. Locate the relevant passage, table, figure, or official statistic.
2. Confirm the source supports the sentence's direction, condition, unit, and
   scope.
3. Weaken or split the sentence if the source only supports part of it.
4. Preserve the distinction between source fact, author observation, and
   author inference.

## Reconciliation

After edits:

- every in-text citation appears in the reference list;
- every reference-list entry is used or explicitly marked as background;
- numbering follows first appearance when the style requires it;
- duplicate works are merged;
- the same author-year collision has a stable disambiguation;
- DOI and URL fields remain attached to the correct work;
- citations in figure captions, table notes, appendices, and footnotes are
  included in the audit.

## Official Statistics

For government data, record the agency, release title, release date, statistic
definition, unit, retrieval date, and URL. Do not replace an official source
with a news summary when the official publication is available.
