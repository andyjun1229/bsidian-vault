#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A 组修复：链接: [x](y) -> 链接: "[x](y)"，然后全量校验"""
import os, re, yaml

VAULT = "/Users/mac/Documents/Obsidian Vault"
you_dir = os.path.join(VAULT, "you")

MD_LINK = re.compile(r"^(链接)\s*:\s*(\[[^\]]*\]\([^)]*\))\s*$")

fixed = []
for f in sorted(os.listdir(you_dir)):
    if not f.endswith(".md"):
        continue
    path = os.path.join(you_dir, f)
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    lines = content.splitlines()
    changed = False
    for i in range(1, min(len(lines), 40)):
        m = MD_LINK.match(lines[i])
        if m:
            lines[i] = f"{m.group(1)}: \"{m.group(2)}\""
            changed = True
    if changed:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + ("\n" if content.endswith("\n") else ""))
        fixed.append(f)

print(f"A) 修复 markdown 链接值: {len(fixed)} 个文件")

def frontmatter_end(lines):
    for i in range(1, min(len(lines), 40)):
        if lines[i].strip() == "---":
            return i
    return None

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
    print("✅ 全部 you/ 文件 frontmatter 合法且 type/status 齐全")
