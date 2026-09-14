#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复剩余 20 个文件的 frontmatter YAML 错误：
A) 链接: [x](y)  -> 链接: "[x](y)"（加引号）
B) 全角冒号行首处 -> ASCII ": "
C) @ 开头标量 -> 加双引号
然后全量 yaml 校验
"""
import os, re, yaml

VAULT = "/Users/mac/Documents/Obsidian Vault"
you_dir = os.path.join(VAULT, "you")

MD_LINK = re.compile(r"^(链接|链接：)\s*(\[[^\]]*\]\([^)]*\))\s*$")

def frontmatter_end(lines):
    for i in range(1, min(len(lines), 40)):
        if lines[i].strip() == "---":
            return i
    return None

fixed_a, fixed_b, fixed_c = [], [], []

for f in sorted(os.listdir(you_dir)):
    if not f.endswith(".md"):
        continue
    path = os.path.join(you_dir, f)
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    lines = content.splitlines()
    end = frontmatter_end(lines)
    changed = False
    for i in range(1, end if end else len(lines)):
        ln = lines[i]
        # A) markdown 链接值加引号
        m = MD_LINK.match(ln)
        if m:
            lines[i] = f"{m.group(1)}: \"{m.group(2)}\""
            fixed_a.append(f)
            changed = True
            continue
        # B) 全角冒号（仅第一处，即键分隔符）
        if "：" in ln:
            lines[i] = ln.replace("：", ": ", 1)
            fixed_b.append(f)
            changed = True
            continue
        # C) 序列项里 @ 开头的标量
        if re.match(r"^\s*-\s+[A-Za-z/]+:\s*@.*\)\s*$", ln) and not ln.lstrip("- ").startswith('"'):
            indent = ln[: len(ln) - len(ln.lstrip())]
            lines[i] = f'{indent}- "{ln.strip()[2:]}"'
            fixed_c.append(f)
            changed = True
    if changed:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + ("\n" if content.endswith("\n") else ""))

print(f"A) markdown链接加引号: {len(set(fixed_a))} 个文件")
print(f"B) 全角冒号修正:     {len(set(fixed_b))} 个文件")
print(f"C) @标量加引号:      {len(set(fixed_c))} 个文件")

# 全量权威校验
ok, bad = [], []
for f in sorted(os.listdir(you_dir)):
    if not f.endswith(".md"):
        continue
    path = os.path.join(you_dir, f)
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    if not lines or lines[0].strip() != "---":
        bad.append((f, "无 frontmatter 开头"))
        continue
    end = frontmatter_end(lines)
    if end is None:
        bad.append((f, "frontmatter 未闭合"))
        continue
    try:
        meta = yaml.safe_load("\n".join(lines[1:end]))
        if not isinstance(meta, dict):
            bad.append((f, "frontmatter 不是映射"))
            continue
        missing = [k for k in ("type", "status") if k not in meta]
        if missing:
            bad.append((f, f"缺少字段: {missing}"))
        else:
            ok.append(f)
    except Exception as e:
        bad.append((f, f"YAML失败: {str(e)[:50]}"))

print()
print(f"校验通过: {len(ok)} / {len(ok) + len(bad)}")
if bad:
    print(f"仍有问题: {len(bad)}")
    for f, why in bad:
        print(f"  - {f}  ({why})")
else:
    print("✅ 全部 166 个 you/ 文件 frontmatter 合法且 type/status 齐全")
