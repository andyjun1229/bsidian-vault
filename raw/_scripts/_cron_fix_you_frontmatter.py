#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""you/ frontmatter 批量修复：
1) 备份 you/ 到 /tmp/you-backup-YYYYMMDD
2) 修复粘连行: `status: xxx---` -> `status: xxx` + 换行 + `---`（type 同理）
3) 用 yaml.safe_load 权威校验每个文件
"""
import os, re, shutil, sys, datetime

VAULT = "/Users/mac/Documents/Obsidian Vault"
you_dir = os.path.join(VAULT, "you")
today = datetime.date.today().strftime("%Y%m%d")
backup_dir = f"/tmp/you-backup-{today}"

# 1. 备份
if os.path.isdir(backup_dir):
    shutil.rmtree(backup_dir)
shutil.copytree(you_dir, backup_dir)
print(f"备份完成: {backup_dir} ({len(os.listdir(backup_dir))} 个文件)")

GLUE = re.compile(r"^(type|status):\s*(\S+?)---\s*$")

fixed = []
for f in sorted(os.listdir(you_dir)):
    if not f.endswith(".md"):
        continue
    path = os.path.join(you_dir, f)
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    lines = content.splitlines()
    changed = False
    out = []
    for i, ln in enumerate(lines):
        m = GLUE.match(ln)
        if m:
            out.append(f"{m.group(1)}: {m.group(2)}")
            out.append("---")
            changed = True
        else:
            out.append(ln)
    if changed:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write("\n".join(out) + ("\n" if content.endswith("\n") else ""))
        fixed.append(f)

print(f"修复粘连行: {len(fixed)} 个文件")

# 3. 权威校验
import yaml

ok, bad = [], []
for f in sorted(os.listdir(you_dir)):
    if not f.endswith(".md"):
        continue
    path = os.path.join(you_dir, f)
    with open(path, encoding="utf-8") as fh:
        content = fh.read()
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        bad.append((f, "无 frontmatter 开头"))
        continue
    close = None
    for i in range(1, min(len(lines), 40)):
        if lines[i].strip() == "---":
            close = i
            break
    if close is None:
        bad.append((f, "frontmatter 未闭合"))
        continue
    try:
        meta = yaml.safe_load("\n".join(lines[1:close]))
        if not isinstance(meta, dict):
            bad.append((f, "frontmatter 不是映射"))
            continue
        missing = [k for k in ("type", "status") if k not in meta]
        if missing:
            bad.append((f, f"缺少字段: {missing}"))
        else:
            ok.append(f)
    except Exception as e:
        bad.append((f, f"YAML解析失败: {str(e)[:60]}"))

print()
print(f"校验通过: {len(ok)} / {len(ok) + len(bad)}")
if bad:
    print(f"仍有问题: {len(bad)}")
    for f, why in bad[:20]:
        print(f"  - {f}  ({why})")
else:
    print("✅ 全部 you/ 文件 frontmatter 结构合法，type/status 齐全")
