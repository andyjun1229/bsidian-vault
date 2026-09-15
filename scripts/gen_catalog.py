"""
从 you/ 的 frontmatter 自动生成 outputs/__catalog.md 目录文件。
只读取 frontmatter，不读正文，速度很快。
递归扫描 you/ 及其子目录（如 you/灵感/），跳过 _ 开头的文件和隐藏目录。

用法: python3 ~/Documents/bsidian-vault/scripts/gen_catalog.py
"""

import os
import datetime

VAULT = os.path.expanduser("~/Documents/bsidian-vault")
YOU_DIR = os.path.join(VAULT, "you")
OUTPUTS_DIR = os.path.join(VAULT, "outputs")
CATALOG = os.path.join(OUTPUTS_DIR, "__catalog.md")


def read_frontmatter(path):
    """Read YAML frontmatter from a markdown file."""
    fm = {}
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    if not content.startswith("---"):
        return fm, content

    end = content.find("---", 3)
    if end == -1:
        return fm, content

    fm_text = content[3:end].strip()
    body = content[end + 3 :].strip()

    for line in fm_text.split("\n"):
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip().lower()
            val = val.strip().strip('"').strip("'")
            fm[key] = val

    return fm, body


def get_first_heading(body):
    """Extract the first # heading from body."""
    for line in body.split("\n"):
        line = line.strip()
        if line.startswith("# ") and not line.startswith("##"):
            return line[2:].strip()
    return ""


entries = []

for root, dirs, files in os.walk(YOU_DIR):
    dirs[:] = sorted(d for d in dirs if not d.startswith("."))
    for filename in sorted(files):
        if not filename.endswith(".md") or filename.startswith("_"):
            continue

        path = os.path.join(root, filename)
        rel = os.path.relpath(path, VAULT)  # 例: you/灵感/xxx.md
        fm, body = read_frontmatter(path)
        title = get_first_heading(body) or filename.replace(".md", "")

        filetype = fm.get("type", "?")
        status = fm.get("status", "?")

        # Status indicator
        if status == "evergreen":
            status_icon = "🌲"
        elif status == "growing":
            status_icon = "🌱"
        elif status == "sprouting":
            status_icon = "🌰"
        elif status == "stale":
            status_icon = "🥀"
        else:
            status_icon = "❓"

        entries.append((filetype, status, status_icon, title, rel))

# Group by type
type_order = ["article", "method", "experience", "note", "prd", "story", "archive", "draft"]
type_labels = {
    "article": "文章",
    "method": "方法论/框架",
    "experience": "操作经验",
    "note": "笔记/想法",
    "prd": "产品文档/方案",
    "story": "回忆录",
    "archive": "归档",
    "draft": "草稿/待补素材",
}

lines = []
lines.append("---")
lines.append("自动生成时间: " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
lines.append("来源: you/ 目录 frontmatter（含子目录）")
lines.append("---")
lines.append("")
lines.append("# 📚 知识库总目录")
lines.append("")
lines.append(f"共 {len(entries)} 条。🌲 = 成熟观点  🌱 = 正在成长  🌰 = 初稿  🥀 = 过时")
lines.append("")

for t in type_order:
    group = [e for e in entries if e[0] == t]
    if not group:
        continue
    label = type_labels.get(t, t)
    lines.append(f"## {label} ({len(group)})")
    lines.append("")
    for _, status, icon, title, rel in group:
        link = f"[[{rel}]]"
        lines.append(f"- {icon} {link} — {title}" if status != "growing" else f"- {icon} {link}")
    lines.append("")

# Also add "unknown type" group
unknown = [e for e in entries if e[0] not in type_order]
if unknown:
    lines.append(f"## 未分类 ({len(unknown)})")
    lines.append("")
    for _, status, icon, title, rel in unknown:
        lines.append(f"- {icon} [[{rel}]]")
    lines.append("")


with open(CATALOG, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"✅ 已生成: {CATALOG}")
print(f"   共 {len(entries)} 条，{len(type_order)} 个分类")
