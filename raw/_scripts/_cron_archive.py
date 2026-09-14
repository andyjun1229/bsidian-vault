#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把本次 cron 产生的临时巡检/修复脚本归档到 raw/_scripts/（不删除）"""
import os, shutil

VAULT = "/Users/mac/Documents/Obsidian Vault"
raw = os.path.join(VAULT, "raw")
dst = os.path.join(raw, "_scripts")
os.makedirs(dst, exist_ok=True)

moved = []
for f in os.listdir(raw):
    if f.startswith("_cron_") and f.endswith(".py"):
        shutil.move(os.path.join(raw, f), os.path.join(dst, f))
        moved.append(f)

print(f"归档 {len(moved)} 个脚本 -> raw/_scripts/")
for f in sorted(moved):
    print("  -", f)
print()
print("raw/ 根目录剩余脚本:", [f for f in os.listdir(raw) if f.startswith("_")])
