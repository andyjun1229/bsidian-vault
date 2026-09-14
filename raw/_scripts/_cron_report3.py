#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""只读普查：you/ 所有文件的 frontmatter 结构问题"""
import os, re

VAULT = "/Users/mac/Documents/Obsidian Vault"
you_dir = os.path.join(VAULT, "you")

glued = []      # status: xxx--- 粘连
unterminated = []  # 首个 --- 后没有第二个 ---
both_ok = 0

for f in sorted(os.listdir(you_dir)):
    if not f.endswith(".md"):
        continue
    path = os.path.join(you_dir, f)
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        unterminated.append((f, "no-open"))
        continue
    # 找闭合
    close_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            close_idx = i
            break
    has_glued = any(re.match(r"^status:\s*\S+---\s*$", ln) for ln in lines[:20])
    if has_glued:
        glued.append((f, close_idx is None))
    if close_idx is None:
        unterminated.append((f, "no-close"))
    else:
        both_ok += 1

print(f"结构正常: {both_ok}")
print(f"status 粘连 '---': {len(glued)}  (其中无闭合行: {sum(1 for _, c in glued if not c)})")
for f, c in glued[:10]:
    print(f"  - {f}  close={'有' if c else '无'}")
print(f"frontmatter 未闭合: {len(unterminated)}")
for f, kind in unterminated[:10]:
    print(f"  - {f}  ({kind})")
