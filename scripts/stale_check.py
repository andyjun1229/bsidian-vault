#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
30 天遗忘扫描 —— CLAUDE.md 遗忘规则的自动化执行
用法：python3 scripts/stale_check.py [--days 30]

规则（来自 CLAUDE.md v6.1）：
- you/ 里 30 天没修改的 method/article 文件 → 建议标记 stale
- 不删除，只报告（stale 可随时复活）

输出：适合 cronjob/周巡检直接引用的清单
"""

import os
import re
import sys
import time

VAULT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
YOU = os.path.join(VAULT, "you")

FM_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)


def get_fm_field(fm_text, key):
    m = re.search(rf"^{key}\s*:\s*(.+)$", fm_text, re.MULTILINE)
    return m.group(1).strip().strip("[]\"'") if m else None


def scan(days=30):
    now = time.time()
    cutoff = now - days * 86400
    results = []
    if not os.path.isdir(YOU):
        print("you/ 目录不存在")
        return results
    for f in sorted(os.listdir(YOU)):
        if not f.endswith(".md"):
            continue
        path = os.path.join(YOU, f)
        mtime = os.path.getmtime(path)
        if mtime >= cutoff:
            continue  # 30 天内改过，跳过
        try:
            head = open(path, encoding="utf-8", errors="ignore").read(2000)
        except Exception:
            continue
        fm = FM_RE.match(head)
        ftype = get_fm_field(fm.group(1), "type") if fm else None
        status = get_fm_field(fm.group(1), "status") if fm else None
        # 只关注 method/article；已经是 stale 的不再报
        if ftype in ("method", "article") and status != "stale":
            days_old = int((now - mtime) / 86400)
            results.append((f, ftype, status, days_old))
    return results


if __name__ == "__main__":
    days = 30
    if "--days" in sys.argv:
        days = int(sys.argv[sys.argv.index("--days") + 1])
    stale_candidates = scan(days)
    if not stale_candidates:
        print(f"✅ 30 天遗忘扫描：you/ 里没有超过 {days} 天未修改的 method/article")
    else:
        print(f"⚠️ 30 天遗忘扫描：以下 {len(stale_candidates)} 个文件超过 {days} 天未修改，建议标记 stale 或复活加工：")
        for name, ftype, status, d in stale_candidates:
            print(f"  - you/{name}（type: {ftype}, status: {status}, {d} 天未动）")
