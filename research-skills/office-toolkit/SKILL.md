---
name: office-toolkit
description: "处理 Office 文档（Word/Excel/PPT/PDF）的技能。当用户要求读取、创建、编辑 Word 文档（.docx）、Excel 表格（.xlsx/.csv）、PPT（.pptx）或 PDF 时使用。基于 python-docx、openpyxl、python-pptx、pypdf 库。Requires: python-docx, openpyxl, python-pptx, pypdf, pandoc, LibreOffice（验证用）。"
metadata: {"openclaw":{"emoji":"📄","requires":{"anyBins":[]}}}
---

# office-toolkit

处理 Office 文档：Word（.docx）、Excel（.xlsx/.csv）、PPT（.pptx）、PDF。

## 环境要求

```bash
pip install --break-system-packages python-docx openpyxl python-pptx pypdf
sudo apt install libreoffice-writer libreoffice-calc libreoffice-impress pandoc
```

## 快速参考

| 任务 | 库/命令 |
|------|---------|
| 读 Word | `python-docx` / `pandoc -t markdown` / `unzip` + XML iterparse（大型文件） |
| 创建/编辑 Word | `python-docx`（优先），`pandoc`（markdown→DOCX，更可靠） |
| 读 Excel | `openpyxl` 或 `pandas` |
| 创建/编辑 Excel | `openpyxl` |
| 读 PPT | `python-pptx` |
| 创建/编辑 PPT | `python-pptx` |
| 读 PDF | `pypdf` 或 `pandoc` |
| PDF 格式验证 | LibreOffice `soffice` |
| PDF 转图片 | `pdftoppm` (poppler-utils) |

---

## Word (.docx)

### 读取

**首选方法：** python-docx（适合正常大小的文件）
```python
from docx import Document
doc = Document('file.docx')
for para in doc.paragraphs:
    print(para.text)
```

**备选方法：** pandoc（带格式提取，包括修订痕迹）
```python
import subprocess
result = subprocess.run(['pandoc', '--track-changes=all', 'file.docx', '-t', 'markdown'], 
    capture_output=True, text=True)
print(result.stdout)
```

**兜底方法：unzip + XML iterparse（适用于大型/损坏的 .docx 文件）**

当 `python-docx` 超时（document.xml > 200KB）或 ZIP 结构损坏时使用此方法。流式解析避免将整个 XML 树加载到内存中：

```bash
# 第一步：解压 docx（实际是 ZIP 文件）
unzip -o file.docx -d /tmp/extracted/

# 第二步：用 Python iterparse 流式提取文本
python3 << 'PYEOF'
import xml.etree.ElementTree as ET

w_ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
t_tag = w_ns + 't'
p_tag = w_ns + 'p'

text_lines = []
context = ET.iterparse('/tmp/extracted/word/document.xml', events=('end',))

current_para = []
for event, elem in context:
    if elem.tag == t_tag and elem.text:
        current_para.append(elem.text)
    elif elem.tag == p_tag:
        line = ''.join(current_para).strip()
        if line:
            text_lines.append(line)
        current_para = []
    elem.clear()  # 释放内存

full_text = '\n'.join(text_lines)
print(full_text[:80000])  # 预览前 80000 字符
print(f'\n\n=== Total chars: {len(full_text)} ===')
PYEOF
```

**排查清单（当所有方法均失败时）：**
1. 用 `unzip -l file.docx 2>&1 | head -30` 检查 ZIP 结构
2. 检查 `word/document.xml` 大小 — 若超过 500KB，使用 iterparse
3. 若 ZIP 条目损坏（NULL），用 `zip -FF` 尝试修复
4. 对于包含嵌入图片和表格的大型文档，iterparse 是最可靠的选择

### 创建
```python
from docx import Document
from docx.shared import Pt, Inches

doc = Document()
# 标题
doc.add_heading('文档标题', 0)

# 段落
p = doc.add_paragraph('正文内容')
p.runs[0].bold = True  # 加粗
p.runs[0].font.size = Pt(12)
p.runs[0].font.name = 'Arial'

# 引用
doc.add_paragraph('引用内容', style='Intense Quote')

# 表格
table = doc.add_table(rows=2, cols=3)
table.style = 'Light Grid Accent 1'
table.rows[0].cells[0].text = '表头1'
table.rows[0].cells[1].text = '表头2'

doc.save('output.docx')
```

### Markdown 转 DOCX（推荐 pandoc）

当需要将 markdown 文件转换为 DOCX 时，使用 pandoc 比 python-docx 更可靠——pandoc 原生处理 markdown，自动转换标题层级、表格、代码块、列表等结构。

```bash
pandoc input.md -o output.docx --from markdown
```

**Pitfall — `--reference-doc` 陷阱**：不要使用 `--reference-doc=/dev/null`，会触发 `pandoc: Data.Binary.Get.runGet at position 0: not enough bytes` 错误。若不需要自定义模板，直接省略该参数。

**python-docx 可靠性问题**：`pip install --break-system-packages python-docx` 后可能因 lxml 的 `etree` 导入失败而无法使用。此时 pandoc 是更可靠的替代方案。

### 编辑现有文档
1. 解压 → 修改 XML → 重新打包（推荐用 python-docx 直接修改）
2. 复杂格式建议用 LibreOffice 打开编辑

---

## Excel (.xlsx)

### 读取
```python
import openpyxl
wb = openpyxl.load_workbook('file.xlsx')
ws = wb.active
for row in ws.iter_rows(values_only=True):
    print(row)
```

### 创建/编辑
```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

wb = openpyxl.Workbook()
ws = wb.active
ws.title = '数据'

# 写入
ws['A1'] = '姓名'
ws['B1'] = '年龄'
ws['A2'] = '张三'
ws['B2'] = 25

# 格式化
header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
ws['A1'].fill = header_fill
ws['A1'].font = Font(color='FFFFFF', bold=True)
ws['A1'].alignment = Alignment(horizontal='center')

# 保存
wb.save('output.xlsx')
```

### 格式化规则（财务场景）
- 蓝色字体：硬编码输入值
- 黑色字体：公式/计算
- 绿色字体：同文件内链接
- 红色字体：外部链接
- 黄色背景：需要关注的假设

---

## PowerPoint (.pptx)

### 读取

**首选方法：** python-pptx
```python
from pptx import Presentation
prs = Presentation('file.pptx')
for slide in prs.slides:
    for shape in slide.shapes:
        if hasattr(shape, 'text') and shape.text.strip():
            print(shape.text.strip())
```

**兜底方法：unzip + XML 解析（适用于 execute_code 沙箱或 python-pptx 不可用时）**

`execute_code` 运行在独立沙箱中，没有 python-pptx。`delegate_task` 子 agent 的 Python 环境也可能缺少该库。此时直接用 `unzip` + XML 提取文本——PPTX 本质是 ZIP 包，每页幻灯片为 `ppt/slides/slideN.xml`：

```bash
unzip -o file.pptx -d /tmp/pptx_extracted/ >/dev/null 2>&1
find /tmp/pptx_extracted/ppt/slides -name "slide*.xml" | sort -V | while read f; do
    echo "=== $(basename $f) ==="
    python3 -c "
import xml.etree.ElementTree as ET
tree = ET.parse('$f')
for t in tree.iter():
    if t.tag.endswith('}t') and t.text:
        print(t.text, end=' ')
print()
"
done
```

**Pitfall**: 该方法只提取纯文本，不保留排版、表格结构、图片。若需表格数据，需额外解析 `<a:graphicFrame>` 内的 `<a:t>` 元素。

### 创建
```python
from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()
prs.slide_width = Inches(10)
prs.slide_height = Inches(7.5)

# 使用空白布局
slide = prs.slides.add_slide(prs.slide_layouts[6])
title = slide.shapes.title
subtitle = slide.placeholders[1]
title.text = '演示标题'
subtitle.text = '副标题'

prs.save('output.pptx')
```

### 设计原则
- **颜色方案**：选一个大胆的配色，主色占60-70%，1-2个辅助色，1个尖锐强调色
- **不要默认蓝色**：根据主题选配色
- **深浅对比**：标题页用深色背景，结论页用浅色背景（"三明治"结构）
- **排版留白**：不要堆满，留呼吸空间

---

## PDF

### 读取
```python
from pypdf import PdfReader
reader = PdfReader('file.pdf')
print(f'页数: {len(reader.pages)}')
for page in reader.pages:
    print(page.extract_text())
```

### 合并
```python
from pypdf import PdfWriter, PdfReader
writer = PdfWriter()
for pdf_file in ['doc1.pdf', 'doc2.pdf']:
    reader = PdfReader(pdf_file)
    for page in reader.pages:
        writer.add_page(page)
with open('merged.pdf', 'wb') as f:
    writer.write(f)
```

### 分割
```python
reader = PdfReader('input.pdf')
for i, page in enumerate(reader.pages):
    writer = PdfWriter()
    writer.add_page(page)
    with open(f'page_{i+1}.pdf', 'wb') as f:
        writer.write(f)
```

### 旋转
```python
page = reader.pages[0]
page.rotate(90)  # 顺时针90度
```

---

## 依赖安装（当前环境状态）

| 依赖 | 状态 |
|------|------|
| python-docx | ✅ 已安装 |
| openpyxl | ✅ 已安装 |
| python-pptx | ✅ 已安装 |
| pypdf | ✅ 已安装 |
| pandoc | ✅ 已安装 |
| LibreOffice | ✅ 已安装 |

---

## 常见问题

### python-docx 在 conda 环境中无法导入

症状：`pip install --break-system-packages python-docx` 成功后，`import docx` 仍然报 `ModuleNotFoundError`。

原因：`--break-system-packages` 将包安装到系统 Python 的 site-packages（如 `/usr/local/lib/python3.12/dist-packages`），而非 conda 环境的 site-packages。激活 conda 环境后 `python3` 指向 conda 的 Python，无法找到系统路径下的包。

排查：
```bash
pip show python-docx | grep Location
python3 -c "import sys; print('\n'.join(sys.path))"
```

修复（按优先级）：
1. 在 conda 环境内安装：`eval "$(conda shell.bash hook)" && conda activate agent-venv && pip install python-docx`
2. 运行时添加系统路径：`python3 -c "import sys; sys.path.insert(0, '/usr/local/lib/python3.12/dist-packages'); import docx"`
3. 兜底：用 `pandoc -t plain` 或 `unzip + XML iterparse` 替代 python-docx

### execute_code / delegate_task 中的 python-docx

`execute_code` 运行在独立沙箱中，`delegate_task` 子 agent 有各自的 Python 环境。这些环境可能找不到系统安装的 python-docx。

推荐模式：`delegate_task` 时在 brief 中指定使用 `pandoc` 或 `unzip + XML iterparse` 读取 DOCX，避免依赖 python-docx。如需使用，在 brief 中提供 `sys.path.insert` 的修复代码。

---

## Agent Rules

- 创建文件前先确保目录可写
- 复杂文档先尝试 python-docx 等库，库无法处理再用 LibreOffice
- **读取大型 .docx（document.xml > 200KB）：** python-docx 可能超时。使用 `unzip` + XML iterparse 兜底方法
- 对于文本提取，优先使用 Python 库方法，若失败再尝试 LibreOffice
- PDF 读取优先用 `pypdf`，文字提取效果差时用 `pandoc`
- Excel 格式化参照财务规范（蓝/黑/绿/红字体 + 黄色背景）
- LibreOffice 路径：`soffice` 或 `libreoffice`（已安装）
- 收到文件路径时，先检查文件是否存在：`pathlib.Path(path).exists()`
