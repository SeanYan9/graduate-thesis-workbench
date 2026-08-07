# DOCX 模板样式继承工作流

## 目标

用户提供的 Word 模板、论文初稿或格式样章是排版权威。写入新内容时读取其中已经存在的样式、页面设置和段落结构，直接复用这些定义，不擅自修改 `word/styles.xml`、页边距、页眉页脚、编号体系或分节设置。

## 安全边界

- 先复制输入 DOCX，再对副本操作。
- 使用 `scripts/docx_style_profile.py` 读取样式画像，记录样式名、样式 ID、字体、字号、段落缩进、间距、使用次数和页面设置。
- 使用 `scripts/template_writer.py` 写入新内容。脚本只允许使用模板中已经存在的样式名，找不到样式时直接失败。
- 不根据默认样式名称猜测用户格式。中文模板可能使用自定义名称、中文名称或学校模板内部样式 ID。
- 写入前后比较 `word/styles.xml` 的哈希或字节内容，确保样式定义没有被脚本改写。
- 模板中没有的样式需要由作者在 Word 中补充，不能由写入器静默创建。

## 样式画像

```powershell
python scripts/docx_style_profile.py `
  "模板.docx" `
  --json "qa/template-style-profile.json" `
  --markdown "qa/template-style-profile.md"
```

画像至少记录：

- 段落、字符和表格样式名称及 ID；
- 字体、东亚字体、字号、粗体、斜体、颜色；
- 左右缩进、首行缩进、段前段后、行距和孤行控制；
- 页面大小、页边距、页眉页脚距离；
- 样式在正文、表格、页眉和页脚中的使用次数。

样式画像只是读取结果，不是新的格式规范。后续写作必须以用户模板为准。

## 内容写入

内容规格使用 JSON，写入器在锚点段落之后插入新段落：

```json
{
  "anchor": "第二章 相关理论基础",
  "blocks": [
    {
      "type": "heading",
      "style": "用户模板中的标题样式",
      "text": "2.1 交通信号控制的基本参数以及性能指标"
    },
    {
      "type": "paragraph",
      "style": "用户模板中的正文样式",
      "runs": [
        {"text": "饱和度由式 "},
        {"latex": "X_p = \\frac{v_p}{c_p}"},
        {"text": " 计算。"}
      ]
    },
    {
      "type": "formula",
      "style": "用户模板中的公式样式",
      "latex": "X_p = \\frac{v_p}{c_p}",
      "number": "(2-1)"
    }
  ]
}
```

执行：

```powershell
python scripts/template_writer.py `
  "论文初稿.docx" `
  "chapter-2-content.json" `
  --output "论文初稿_工作版.docx"
```

写入器支持 `heading`、`paragraph` 和 `formula` 三类块。段落中的 `runs` 可以交替放入普通文字和 LaTeX 公式，公式不会被追加到段尾。

## 公式规则

- 普通文本中的数学表达式先用 LaTeX 表达，再转为原生 Word OMML。
- 支持变量、上下标、分式、根式、常见希腊字母、关系运算符、求和与乘积等常见论文公式。
- 变量使用数学斜体，单位、函数名、解释性下标和运算符使用正体。
- 复杂或暂不支持的 LaTeX 命令必须报错，不得退化成斜体普通文本。
- 显示公式编号使用单独编号字符串，公式主体居中、编号右对齐。
- 转换后必须检查 `m:oMath` 或 `m:oMathPara`，并确认原始 LaTeX 和重复的普通文本已经消失。

```powershell
python scripts/validate_docx_math.py `
  "论文初稿_工作版.docx" `
  --json
```

## 交付门禁

模板继承通过的最低条件：

1. 模板样式定义未被修改；
2. 所有写入块使用的样式均存在于模板；
3. 公式以 OMML 保存，不是图片或普通文本；
4. 公式转换没有残留 LaTeX、占位符或重复文本；
5. OOXML 校验通过；
6. 在 Microsoft Word 中打开后由作者检查分页、字体、公式基线和编号位置。
