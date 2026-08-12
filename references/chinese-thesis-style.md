# Chinese Thesis Style Defaults

Use project-specific instructions first. When no conflicting university
template rule exists, use these defaults for the current Chinese thesis:

- Keep the prose academic but plain. Alternate short and long sentences so
  paragraph lengths visibly vary; uniform paragraph sizes read as AI-written.
- Avoid mechanical connectors such as “首先”“其次”“最后”“综上” when paragraph
  structure already carries the relation.
- Remove unnecessary quotation marks and em dashes; use “、” where an em dash
  or enumeration would otherwise appear. No filler words; keep academic tone.
- Express results directly. Do not wrap results in unnecessary parentheses;
  state “平均延误为 65.34 s” rather than “平均延误（65.34 s）”.
- Prefer continuous paragraphs over bullet-like enumeration in manuscript body.
  Fold layered “从理论层面看 / 从算法层面看 / …” or “文献梳理部分 / 模型构建
  部分 / …” enumerations into one flowing paragraph instead of parallel leads.
- Keep terminology stable across chapters, captions, tables, and references.
- State uncertainty and limitations directly instead of using vague confidence.
- Do not use anti-AI polishing to erase technical conditions, citations, units,
  or scope boundaries.
- Thesis body must never reference process artifacts: do not write “小论文”,
  “开题报告”, “Supporting Materials”, “支撑材料/补充材料”, “投稿材料”, or
  “前期算法研究”. Content from those sources is either pasted in as formal
  text or paraphrased; the manuscript cites only published literature [n].

## Chapter thickness & benchmark-mirroring (proven 2026-08-12)

When the user feels chapters 1-2 are too thin, mirror a published master
thesis on the same topic (e.g. 孔思园, 短连线交叉口自适应信号配时):

- Theory chapter: expand each parameter/concept individually (definition,
  symbol, engineering effect, e.g. cycle length, green split, effective green,
  saturation flow rate), not one summary paragraph. Add a dedicated overview
  section for emission models (COPERT/MOBILE/MOVES/IVE/CMEM principles) when
  emissions are in scope. End the chapter with 本章小结.
- Literature review: name specific authors with their method and citation
  ("栗红强基于交通强度提出周期时长优化模型[48]") instead of blanket
  group citations ([2-5] ...). Keep prose continuous, no (1)(2)(3) bullets
  unless the template demands them.
- Introduction: open the background with hard data; add a technical-route
  diagram (matplotlib, SimHei font) under 1.3 研究内容和技术路线.
- When inserting headings/pictures programmatically, anchor on body text
  (i > 90) or unique body phrases, never on heading text that also exists in
  the TOC field (1.3 研究内容和方法 appears both in TOC and body).
