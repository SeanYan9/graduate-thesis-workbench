# Diagram Generation (Mermaid) — distilled from Agents365-ai/mermaid-skill (MIT)

Text-based diagrams with automatic layout. Use for thesis figures such as the
technical-route diagram (研究技术路线图), algorithm flowcharts, and model
architecture diagrams. Source `.mmd` lives in git; PNG re-renders on demand.

## When to use / when NOT

- **Use**: flowcharts, sequence, state, class/ER, architecture — automatic
  layout is fine and the source stays version-controllable.
- **Do NOT use** (route elsewhere): pixel-precise placement / branded styling
  → drawio; hand-drawn look → excalidraw; strict UML → plantuml.

## Backends (two, auto-fallback)

| Backend | Command | When |
|---|---|---|
| Local `mmdc` | `npm i -g @mermaid-js/mermaid-cli` + `npx puppeteer browsers install chrome-headless-shell` | best quality, offline, Chinese fonts via system fontFamily |
| Kroki API | only curl/python | zero install; PNG/SVG only (no PDF) |

`scripts/render_mermaid.py` probes mmdc → validates with a throwaway export
(a bare `mmdc --version` passes even without Chrome) → falls back to Kroki.

## Workflow (validation-first)

1. Check backend (mmdc + Chrome, else Kroki)
2. Write the `.mmd` to disk (same file each round; no v1/v2)
3. **Validate before export** — render_mermaid.py does a probe export
4. Export PNG (2048 px, white background)
5. **Vision self-check** — read the PNG; fix label clipping (`<br/>` wrap),
   cramped density (split subgraphs / flip TD↔LR), edge spaghetti, low
   contrast (classDef). Max 2 auto rounds; re-validate after every fix.
6. Review loop with the user (minimal `.mmd` edit per request, ≤5 rounds)
7. Report output paths

## Chinese-thesis specifics

- Always set the font in the init block or Chinese renders as boxes:
  ```mermaid
  %%{init: {'theme': 'base', 'themeVariables': {'fontFamily': 'Microsoft YaHei, SimHei, sans-serif', 'primaryColor': '#eef3fb', 'primaryBorderColor': '#2f5597'}}}%%
  ```
- Technical-route diagram style: `flowchart TD`, main phases as top-level
  nodes (research background → theory → modeling → algorithm → validation →
  case study → conclusion), related sub-items grouped in `subgraph` blocks
  (理论/算法 layers), one `classDef` for phases and one for subgraph groups.
- Node text with two lines uses `<br/>`, not `\n`.
- Label special characters (· etc.) are fine unquoted only when simple; wrap
  node labels in double quotes to be safe: `B1["信号控制参数与性能指标<br/>…"]`.
- After export, insert into the DOCX at the correct anchor (body region,
  NOT heading text that also exists in the TOC field).

## Common mistakes

| Mistake | Fix |
|---|---|
| `Could not find Chrome` | Chrome/puppeteer setup problem, NOT a syntax error; install browser or use Kroki |
| Kroki PDF 400 | Kroki does PNG/SVG only for mermaid; use mmdc for PDF |
| Chinese boxes | missing fontFamily in init block |
| Blank/small output | add `-w 2048` |
| Wrong arrow | flowchart `-->`; sequence `->>` request / `-->>` response |
| Subgraph name with spaces | wrap in quotes: `subgraph "My Layer"` |
