# Source Distillation Record

This toolkit distills workflow principles from public repositories. It does
not copy their source files, prompts, code, private materials, or branding.
The local implementation keeps its own contracts and attribution record.

## Selected Sources

| Source | Distilled contribution |
|---|---|
| https://github.com/Norman-bury/research-writing-skill | Modular thesis workflow: project planning, evidence-driven writing, chapter gates, figures, statistics, verification, and staged review |
| https://github.com/SNL-UCSB/paper-writing-skill | Claim-first paragraph architecture, topic-sentence scaffolding, rhetorical moves, figure synthesis, and independent red-team review |
| https://github.com/heyu-233/engineering-figure-agent | Figure brief, image/plot/mixed routing, exact plots from numeric data, editable specifications, provenance and high-resolution checks |
| https://github.com/Galaxy-Dawn/claude-scholar | Human-decision-centered research chain: problem, evidence, experiment, analysis, claim, writing, citation verification, publication charts and tables |
| https://github.com/appautomaton/latex-arxiv-SKILL | Approval-gated LaTeX workflow, issue tracking, citation verification, rhythm refinement, and compile-as-proof discipline |
| https://github.com/Master-cai/Research-Paper-Writing-Skills | Section-specific academic writing, paragraph flow, claim-evidence alignment, visual quality, and adversarial self-review |
| https://github.com/obra/superpowers/tree/main/skills/writing-plans | File-level planning, task packets, testable steps, and explicit verification before implementation |
| https://github.com/AIScientists-Dev/academic-humanizer | Academic voice calibration, evidence-preserving edits, scholarly register, and disclosure-aware human review |
| https://github.com/conorbronsdon/avoid-ai-writing | Detect/rewrite/edit separation, signal clustering, minimal edits, and preservation of quoted or structured content |
| https://github.com/labarba/sciwrite | Scientific prose audits for clarity, sentence architecture, terminology, numerical consistency, and citation integrity |
| https://github.com/stephenturner/skill-deslop | Removal of filler, vague attribution, formulaic structure, and inflated scientific language |
| https://github.com/blader/humanizer | Broad AI-writing pattern catalog and author-sample calibration, restricted here to academic-safe pattern review |
| https://github.com/AllenWang2005/Word-typesetting | Word report formatting workflow, native OMML formula replacement, template-aware document checks, and fail-closed formatting audits |
| https://github.com/xuanfengyuju/word-equation-formula | Offline tokenize-merge-build approach for converting plain-text subscripts, superscripts, Greek letters, and operators into editable OMML |
| https://github.com/nihole/md2docx | Template-as-authority document generation: insert converted content into an existing Word template while preserving its styles and structural settings |

## Selection Rules

- Prefer repositories with an actual `SKILL.md`, executable scripts, schemas,
  tests, or concrete artifacts over marketing-only repositories.
- Prefer explicit evidence, data, provenance, and failure handling.
- Keep distinct responsibilities modular. Do not merge planning, prose,
  numerical plotting, and document packaging into one undifferentiated rule.
- Treat repository descriptions and stars as discovery signals, not proof of
  quality. The local workflow must still validate every output.
- Reject tools whose primary promise is detector evasion, whose reported
  detection-rate reduction is not independently verified, or whose workflow
  recommends fabricated errors, random noise, or deceptive authorship signals.
- Do not copy external repository code or branding into this toolkit. Distill
  the workflow and reimplement only the smallest functions needed for the
  thesis DOCX route. Preserve source attribution in this record.

## Local Integrations

The workbench can route to these already available local skills:

- `nature-academic-search`
- `nature-ref-verifier`
- `nature-writing`
- `nature-figure`
- `nature-statistics`
- `DOCX工具`
- `research-paper-writing`
- `writing-plans`
- `humanizer`

The DOCX route now also includes local implementations of:

- read-only template style profiling;
- style-validated content insertion after an explicit anchor;
- common LaTeX to native OMML conversion;
- residual-LaTeX, duplicate-text, and native-OMML validation.

Use them only when their trigger and artifact contract match the task.

## Excluded From the Core Workflow

- `redbaronyyyyy-eng/humanizer-zh-academic`: its stated objective is to reduce
  detector scores and its numerical effectiveness claim is not a sufficient
  basis for an academic integrity rule.
- Broad casual-writing humanizers: personality injection, humor, invented
  first-person experience, and colloquial rewrites are inappropriate for a
  thesis unless the author's own discipline and sample explicitly require them.
