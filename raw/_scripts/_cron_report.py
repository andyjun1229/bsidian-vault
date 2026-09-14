#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cron 日报巡检：检查 raw/ 今日新增、wiki/ 状态、outputs/ 导航。只读，不写。"""
import os

VAULT = "/Users/mac/Documents/Obsidian Vault"
TODAY = "2026-09-09"

# 1. raw/ 中文件名含今天日期的文件
raw_dir = os.path.join(VAULT, "raw")
raw_all = sorted(os.listdir(raw_dir))
raw_md = [f for f in raw_all if f.endswith(".md")]
raw_today = [f for f in raw_md if TODAY in f]
print(f"raw/ 总 md 文件数: {len(raw_md)}")
print(f"raw/ 今日新增: {len(raw_today)}")
for f in raw_today:
    print("  -", f)

# 2. wiki/ 目录状态
wiki_dir = os.path.join(VAULT, "wiki")
if os.path.isdir(wiki_dir):
    wiki_md = [f for f in sorted(os.listdir(wiki_dir)) if f.endswith(".md")]
    wiki_today = [f for f in wiki_md if TODAY in f]
    print()
    print(f"wiki/ 条目数: {len(wiki_md)}")
    print(f"wiki/ 今日更新: {len(wiki_today)}")
    for f in wiki_today:
        print("  -", f)
else:
    print()
    print("wiki/ 目录不存在")

# 3. outputs/ 目录状态
outputs_dir = os.path.join(VAULT, "outputs")
if os.path.isdir(outputs_dir):
    out_all = sorted(os.listdir(outputs_dir))
    print()
    print(f"outputs/ 文件: {len(out_all)}")
    for f in out_all:
        print("  -", f)
else:
    print()
    print("outputs/ 目录不存在")

# 4. you/ 今日新增（也纳入统计）
you_dir = os.path.join(VAULT, "you")
you_md = [f for f in sorted(os.listdir(you_dir)) if f.endswith(".md")]
you_today = [f for f in you_md if TODAY in f]
print()
print(f"you/ 条目数: {len(you_md)}")
print(f"you/ 今日新增: {len(you_today)}")
for f in you_today:
    print("  -", f)
