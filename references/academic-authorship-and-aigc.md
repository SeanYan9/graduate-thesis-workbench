# Academic Authorship and AIGC-Risk Review

## Scope

Use this route when the user asks to reduce AIGC risk, remove AI-writing
traces, humanize a thesis, match the author's voice, or review whether prose
sounds templated. The goal is authentic, evidence-bound academic writing. It
is not a detector-bypass procedure and cannot guarantee any detector score.

An AIGC detector result is a noisy style signal, not proof that a person or a
model wrote a passage. Do not use it as the sole basis for authorship,
integrity, or publication decisions. Review clusters of signals together with
the genre, the author's writing history, the source files, and the revision
record.

## Distilled Principles

This reference distills ideas from:

- `AIScientists-Dev/academic-humanizer`: preserve every number, result,
  equation, technical term, and citation; audit before rewriting; match the
  author's voice; keep scholarly register; never evade AI-use disclosure.
- `conorbronsdon/avoid-ai-writing`: separate detect, rewrite, and edit modes;
  treat patterns as signals rather than verdicts; preserve quoted material,
  tables, code, and attributed text; prefer minimal targeted edits; test
  paragraph-to-paragraph dependency.
- `labarba/sciwrite`: improve delivery without changing scientific content;
  audit clutter, verbs, sentence architecture, terminology, numerical
  consistency, and citation integrity.
- `stephenturner/skill-deslop`: remove filler, formulaic contrasts, vague
  attributions, meta-commentary, and inflated stakes while keeping scientific
  formality and domain terminology.
- `blader/humanizer`: use a broad catalog of recurring AI patterns and
  author-sample calibration. Its personality, humor, and casual "soul"
  guidance is not imported into thesis prose.

The source projects are recorded in `references/source-distillation.md`; this
toolkit keeps the workflow and boundaries independent rather than copying their
source files.

## Required Inputs

Before a substantial rewrite, collect what is available:

1. The author's existing draft, notes, calculations, experiment explanations,
   and earlier papers or sections written by the author.
2. The target discipline, university template, language, and chapter role.
3. The claim ledger, evidence map, data manifest, and reference ledger.
4. The section that may be edited and the files that must remain unchanged.

Use `plan/author-voice-profile.md` to record the author's actual sample files,
sentence rhythm, recurring terms, preferred transitions, and legitimate
hedging. Use `plan/ai-assistance-log.md` to record the date, input material,
AI-assisted action, author review, evidence check, and disclosure decision.
Never infer a private voice from a famous author or from generic internet prose.

## Academic Review Modes

| Mode | Use | Output |
|---|---|---|
| `detect` | The author wants diagnosis without rewriting | Signal clusters with locations, false-positive cautions, and priority |
| `revise` | The author wants clearer, more natural academic prose | Minimal evidence-preserving revision plus a change log |
| `voice-calibrate` | An author sample is supplied | Profile comparison and targeted revisions that preserve the author's habits |
| `provenance` | The author needs an integrity record | AI-assistance log, changed-file list, evidence and citation checks |

Default to `detect` before `revise` for a completed section. Do not silently
rewrite a whole chapter when the request identifies only one paragraph or
subsection.

## Audit Sequence

### Pass 1: Authorship and provenance

- Distinguish author-originated text, source quotations, data-derived text,
  AI-assisted drafts, and author-approved revisions.
- Mark passages that have no source, no data, or no author decision behind them.
- Do not present an AI-generated paragraph as the author's research finding.
- Keep the author's substantive decisions visible in notes or the assistance
  log rather than fabricating an anecdote or personal experience.

### Pass 2: Evidence-preserving AI-pattern audit

Flag clusters, not isolated words:

- repeated boilerplate openers such as "近年来" or "随着……发展";
- stacked connective words such as "此外、同时、值得注意的是";
- inflated significance, promotional adjectives, and empty conclusions;
- vague attributions such as "研究表明" without a named source;
- contribution lists that only repeat the abstract;
- synonym cycling for the same defined technical term;
- symmetrical three-part lists used as padding;
- overlong clause chains and repeated paragraph shapes;
- meta-commentary that announces what the paragraph will say;
- formulaic contrasts and mechanically repeated hedging.

The presence of one signal does not establish AI authorship. Keep a legitimate
technical term, transition, passive construction, or repeated keyword when the
discipline or the argument requires it.

### Pass 3: Scholarly register and claim strength

- Keep neutral, precise academic language. Do not add humor, emotional
  reactions, colloquialisms, or first-person life experience.
- Use `we` where the discipline and thesis convention permit it.
- Keep passive voice when the actor is unknown, irrelevant, or standard in the
  Methods section.
- Preserve calibrated verbs such as "表明、提示、与……一致、可能说明".
  Never upgrade them to "证明、证实、保证" without evidence.
- Replace vague importance claims with a concrete gap, number, comparison,
  figure, table, or citation.

### Pass 4: Terminology and structural authenticity

- Repeat the same defined term when it names the same variable or method.
- Keep paragraphs connected by actual reasoning, not by a chain of transition
  words. If paragraph order can be swapped without loss, inspect the argument.
- Prefer specific local details from the author's study, data, model settings,
  or research decisions. Do not invent "human-like" imperfections.
- Vary sentence rhythm only when it follows the logic of the content. Do not
  randomize sentence lengths, punctuation, or word choice.

### Pass 5: Invariant checks

Before delivery, compare the original and revised text:

- numbers, units, sample sizes, equations, variable names, citations, and
  figure/table references are unchanged or explicitly documented;
- no new result, source, mechanism, limitation, or personal experience was
  introduced;
- technical terms and abbreviations remain consistent;
- quoted material, table cells, formulas, captions, and source-attributed text
  were not stylistically rewritten unless the user explicitly authorized it;
- every substantive revision appears in the change log and is available for
  author review.

## Forbidden Shortcuts

Do not:

- promise "AIGC 0%" or any target detector score;
- rewrite solely to fool a specific detector;
- inject typos, random punctuation, fake uncertainty, fake personal details,
  or unnatural colloquialisms;
- use a thesaurus to create artificial vocabulary variation;
- remove citations or weaken a claim merely because its wording is formal;
- convert Chinese academic prose into casual spoken language;
- imitate a named scholar, supervisor, or classmate without the author's own
  permission and sample;
- treat a detector score as evidence that a passage is or is not plagiarized.

## Delivery Contract

Return:

1. The audit mode and the author sample used, if any.
2. Detected signal clusters with locations and a note on possible false
   positives.
3. The revised text or a statement that no edit was made.
4. A concise change log.
5. An invariant report for numbers, citations, equations, and technical terms.
6. Remaining evidence, authorship, disclosure, or formatting risks.

Use `DONE_WITH_CONCERNS` when the prose is usable but no author sample or
revision history was available. Use `NEEDS_EVIDENCE` when a proposed revision
would require an unsupported claim or invented research detail.
