#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复后重算：30天未动的 method/article（status 正确解析）+ __catalog 计数核对"""
import os, time, yaml, re

VAULT = "/Users/mac/Documents/Obsidian Vault"
you_dir = os.path.join(VAULT, "you")
now = time.time()

def frontmatter_end(lines):
    for i in range(1, min(len(lines), 40)):
        if lines[i].strip() == "---":
            return i
    return None

stale_cand = []
status_dist = {}
for f in sorted(os.listdir(you_dir)):
    if not f.endswith(".md"):
        continue
    path = os.path.join(you_dir, f)
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    end = frontmatter_end(lines)
    meta = yaml.safe_load("\n".join(lines[1:end])) or {}
    st = meta.get("status", "?")
    status_dist[st] = status_dist.get(st, 0) + 1
    days = int((now - os.path.getmtime(path)) / 86400)
    if meta.get("type") in ("method", "article") and st != "stale" and days > 30:
        stale_cand.append((f, days))

print("status 分布:", status_dist)
print(f"30天未动的 method/article（未标 stale）: {len(stale_cand)}")
for f, d in stale_cand[:8]:
    print(f"  - {f} ({d}天)")
if len(stale_cand) > 8:
    print(f"  ... 等共 {len(stale_cand)} 个")

# __catalog.md 声称的条数
cat = os.path.join(VAULT, "outputs", "__catalog.md")
with open(cat, encoding="utf-8") as fh:
    head = fh.read(800)
m = re.search(r"(\d+)\s*条", head)
print()
print(f"__catalog.md 声称条数: {m.group(1) if m else '未找到'}")
print("__catalog.md 头部:")
for ln in head.splitlines()[:10]:
    print("  |", ln)
