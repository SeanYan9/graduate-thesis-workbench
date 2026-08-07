# Graduate Thesis Workbench

研究生毕业大论文写作工作台 —— 一个以**证据可追溯**为核心的学术写作 skill，把毕业论文当作由论断（claims）、章节、数据、图表、参考文献和文档结构组成的系统来处理，按请求路由到最小合适的工作流，并在证据或来源缺失时 **fail closed**（拒绝交付）。

适用于中文或中英双语毕业论文的撰写与修改：章节规划与补全、文献综述、论断-引文核验、参考文献修复、DOCX 编辑、数据表格、科学绘图、流程图、架构图、图注、作者风格感知的文稿审校、AIGC 风险审计、交叉引用审计与最终质量检查。

## 触发词

`大论文`、`毕业论文`、`章节补全`、`图表`、`流程图`、`交叉引用`、`参考文献核验`、`AIGC风险`、`AI写作痕迹`、`Word论文`

## 核心原则（Hard Gates）

- 绝不臆造参考文献、DOI 元数据、统计数据、实验结果、样本量、机制、图表数值或来源 URL。
- 计划、假设、mock 值、合成值或视觉占位符不得升级为正文证据；须显式标记并排除在最终论断之外。
- 无证据地图与段落蓝图之前，不写文献驱动型段落；无数据/分析输出/已核验来源之前，不写 Results 或 Discussion 论断。
- 精确数值图必须使用真实数据与可审计的绘图脚本，不得用图像模型绘制坐标轴、数值、基准柱、显著性标记。
- 概念图必须先有 figure brief，明确论断、组件、连接、阅读顺序与来源（provenance）。
- 不承诺任何 AIGC/查重检测分数，不针对检测器优化文本，不伪装 AI 辅助痕迹，不注入伪造错别字、随机标点、虚构个人经历或同义词噪音。
- 未通过工作区验证器与专业检查之前，不得宣称章节/图表/引用集/DOCX 已完成。

## 请求路由

| 请求 | 路由 | 主要产物 |
|---|---|---|
| 大纲、章节顺序、多文件修改 | 项目编排 | `plan/project-overview.md`、`plan/outline.md`、`plan/progress.md` |
| 绪论、引言、相关工作 | 证据驱动写作 | `plan/evidence-map.md`、段落蓝图、论断台账 |
| 方法或系统章节 | 技术章节路由 | 输入-输出流、符号台账、可复现性清单 |
| 结果、讨论、实验收尾 | 先分析后写作 | 分析报告、统计附录、图目录 |
| 精确数据图表 | 数据可视化路由 | 数据清单、脚本、可编辑源、PNG/SVG/PDF |
| 流程图/架构图/机制/概念图 | 图表简报路由 | figure brief、可编辑图表源、渲染预览 |
| 参考文献或交叉引用审计 | 引文核验路由 | 参考文献台账、论断支撑报告、对账报告 |
| 作者风格 / AIGC 风险 / AI 痕迹审校 | 学术真实性路由 | 作者声音画像、只检测不篡改的审计、最小修改报告 |
| Word/DOCX 修改 | DOCX 路由 | 修改后的 DOCX、OOXML 校验、渲染检查 |
| 终稿审计 | 独立 QA 路由 | 审计报告、阻塞项、验证证据 |

## 目录结构

```text
graduate-thesis-workbench/
├── SKILL.md                          # 主文件：路由、硬性门禁、工作流、输出契约
├── agents/
│   └── openai.yaml                   # 接口展示信息（display_name、brand_color 等）
├── references/                       # 按需加载的路由参考文件
│   ├── workflow-contract.md          # 项目设置与任务路由
│   ├── evidence-and-citations.md     # 论断、来源与参考文献
│   ├── figures-and-tables.md         # 可视化与表格产物
│   ├── docx-workflow.md              # Word 文档操作
│   ├── docx-template-style-inheritance.md # 读取并继承用户 Word 模板样式
│   ├── quality-gates.md              # 终稿审计与 fail-closed 规则
│   ├── chinese-thesis-style.md       # 中文学术写作风格默认值
│   ├── academic-authorship-and-aigc.md # 作者身份、AI 痕迹审校、声音校准、披露边界
│   └── source-distillation.md        # 蒸馏来源记录与选择规则
├── scripts/
│   ├── init_thesis_project.py        # 初始化项目契约文件（不覆盖已有文件）
│   ├── validate_thesis_workspace.py  # fail-closed 工作区验证器（支持 --json）
│   ├── docx_style_profile.py         # 只读提取 Word 模板样式与页面设置
│   ├── template_writer.py            # 仅复用模板既有样式写入新内容
│   ├── omml.py                       # 常见 LaTeX 公式转原生 Word OMML
│   └── validate_docx_math.py         # OMML、残留 LaTeX 与重复文本检查
├── LICENSE                           # MIT
└── README.md
```

## 快速开始

### 安装为 skill

将本仓库放入你的 skill 目录（如 `~/.codex/skills/`、`.agents/skills/` 或对应平台的 skill 根目录），保留 `SKILL.md` 作为入口即可被识别。

安装本工具脚本依赖：

```powershell
pip install -r requirements.txt
```

### 初始化一个论文项目

```powershell
python scripts/init_thesis_project.py <project-root> --title "论文标题" --domain "交通工程"
```

该脚本会在项目根目录创建 `plan/`、`figures/`、`references/`、`qa/` 契约文件，**不会覆盖任何已有文件**。

### 验证工作区

```powershell
python scripts/validate_thesis_workspace.py <project-root>
python scripts/validate_thesis_workspace.py <project-root> --json
```

验证器是 fail-closed 的：

- 退出码 `0` = `DONE` 或 `DONE_WITH_CONCERNS`
- 退出码 `1` = 存在阻塞性门禁（`BLOCKED` / `NEEDS_EVIDENCE` / `NEEDS_DATA` / `NEEDS_FORMAT_CHECK`）

它检查：契约文件、论断/证据链接、参考文献核验状态、正文引文对账、正文占位符、表格来源行、figure brief、数据清单、mock 数据泄漏、引用的图表产物是否存在。它**不替代**权威来源核验、统计审查、OOXML 校验与最终渲染页检查。

### 读取模板并按原样写入

当用户已经设置好论文模板时，先读取模板，不修改模板样式：

```powershell
python scripts/docx_style_profile.py "论文初稿.docx" `
  --json "qa/template-style-profile.json" `
  --markdown "qa/template-style-profile.md"
```

然后使用内容 JSON 指定锚点、段落和模板中的既有样式：

```powershell
python scripts/template_writer.py `
  "论文初稿.docx" `
  "chapter-content.json" `
  --output "论文初稿_工作版.docx"
```

脚本会拒绝不存在的样式名，并保持输入文档的 `word/styles.xml`、页眉页脚、
编号和页面设置不变。

### 输入可编辑公式

常见论文公式可以使用 LaTeX 输入，写入后保存为 Word 原生 OMML：

```json
{
  "type": "paragraph",
  "style": "正文",
  "runs": [
    {"text": "饱和度为 "},
    {"latex": "X_p = \\frac{v_p}{c_p}"},
    {"text": "。"}
  ]
}
```

写入后必须运行：

```powershell
python scripts/validate_docx_math.py "论文初稿_工作版.docx" --json
python <DOCX工具>/scripts/office/validate.py "论文初稿_工作版.docx"
```

复杂 LaTeX 命令不支持时脚本会停止并报告，不会把公式降级为图片或斜体普通文本。

## 状态契约

每次非平凡响应必须报告状态：`DONE`、`DONE_WITH_CONCERNS`、`NEEDS_EVIDENCE`、`NEEDS_DATA`、`NEEDS_FORMAT_CHECK` 或 `BLOCKED`，并附上改动文件、消费的证据、受影响的论断/图表、作者身份完整性记录与已运行的验证命令。

## 蒸馏来源

本工具蒸馏了公开仓库的工作流原则（非复制其文件），记录在 [`references/source-distillation.md`](references/source-distillation.md)：

- [Norman-bury/research-writing-skill](https://github.com/Norman-bury/research-writing-skill) — 模块化论文工作流
- [SNL-UCSB/paper-writing-skill](https://github.com/SNL-UCSB/paper-writing-skill) — 论断优先段落架构
- [heyu-233/engineering-figure-agent](https://github.com/heyu-233/engineering-figure-agent) — 图表简报与精确绘图
- [Galaxy-Dawn/claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) — 以人类决策为中心的研究链
- [appautomaton/latex-arxiv-SKILL](https://github.com/appautomaton/latex-arxiv-SKILL) — 审批门控的 LaTeX 工作流
- [Master-cai/Research-Paper-Writing-Skills](https://github.com/Master-cai/Research-Paper-Writing-Skills) — 分节写作与对抗式自审
- [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/writing-plans) — 文件级规划与任务包
- [AIScientists-Dev/academic-humanizer](https://github.com/AIScientists-Dev/academic-humanizer) — 学术声音校准与证据保持编辑
- [conorbronsdon/avoid-ai-writing](https://github.com/conorbronsdon/avoid-ai-writing) — 检测/改写/编辑分离
- [labarba/sciwrite](https://github.com/labarba/sciwrite) — 科学散文审计
- [stephenturner/skill-deslop](https://github.com/stephenturner/skill-deslop) — 去除填充与虚夸语言
- [blader/humanizer](https://github.com/blader/humanizer) — AI 写作模式目录与作者样本校准
- [AllenWang2005/Word-typesetting](https://github.com/AllenWang2005/Word-typesetting) — Word 报告格式审计、LaTeX 转 OMML、公式替换与模板格式门控
- [xuanfengyuju/word-equation-formula](https://github.com/xuanfengyuju/word-equation-formula) — 普通文本公式识别、上下标和希腊字母到 OMML 的离线转换思路
- [nihole/md2docx](https://github.com/nihole/md2docx) — 以既有 Word 模板为排版权威，将外部内容插入目标文档的流程

拒绝采纳以规避检测器为主要承诺、未经独立验证的降率主张，或建议伪造错误/随机噪声/欺骗性作者信号的工具。

## 许可

[MIT](LICENSE) © 2026 graduate-thesis-workbench contributors
