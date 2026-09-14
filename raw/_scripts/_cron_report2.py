#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""只读巡检：30 天 stale 检查 + outputs/index.md 头部 + wiki 条目清单"""
import os, time

VAULT = "/Users/mac/Documents/Obsidian Vault"
you_dir = os.path.join(VAULT, "you")
now = time.time()

# 1. 30 天未动的 method/article（非 stale 状态）
stale_candidates = []
for f in sorted(os.listdir(you_dir)):
    if not f.endswith(".md"):
        continue
    path = os.path.join(you_dir, f)
    days = int((now - os.path.getmtime(path)) / 86400)
    if days > 30:
        try:
            with open(path, encoding="utf-8") as fh:
                head = fh.read(600)
        except Exception:
            continue
        ftype = status = ""
        for line in head.splitlines():
            if line.startswith("type:"):
                ftype = line.split(":", 1)[1].strip()
            elif line.startswith("status:"):
                status = line.split(":", 1)[1].strip()
        if ftype in ("method", "article") and status not in ("stale", ""):
            stale_candidates.append((f, ftype, status, days))

print(f"30天未修改的 method/article（未标 stale）: {len(stale_candidates)}")
for f, t, s, d in stale_candidates[:15]:
    print(f"  - {f}  (type={t}, status={s}, {d}天)")

# 2. outputs/index.md 前 40 行
idx = os.path.join(VAULT, "outputs", "index.md")
print()
print("=== outputs/index.md 头部 ===")
if os.path.isfile(idx):
    with open(idx, encoding="utf-8") as fh:
        for i, line in enumerate(fh):
            if i >= 40:
                break
            print(line.rstrip())
else:
    print("文件不存在！")

# 3. wiki 条目清单
wiki_dir = os.path.join(VAULT, "wiki")
print()
print("=== wiki/ 条目 ===")
for f in sorted(os.listdir(wiki_dir)):
    if f.endswith(".md"):
        print(" -", f)
