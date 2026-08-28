#!/usr/bin/env python3
"""Check all raw/ files for proper frontmatter."""
import os, yaml

raw_dir = "/Users/mac/Documents/Obsidian Vault/raw"
issues = []
for f in sorted(os.listdir(raw_dir)):
    if not f.endswith(".md"):
        continue
    fpath = os.path.join(raw_dir, f)
    size = os.path.getsize(fpath)
    if size == 0:
        issues.append(f"  {f}: EMPTY FILE")
        continue
    with open(fpath, "r", encoding="utf-8") as fh:
        content = fh.read()
    if not content.startswith("---"):
        issues.append(f"  {f}: MISSING frontmatter")
        continue
    end = content.find("---", 3)
    if end == -1:
        issues.append(f"  {f}: INCOMPLETE frontmatter")
        continue
    fm_text = content[3:end].strip()
    try:
        fm = yaml.safe_load(fm_text)
        if fm is None:
            issues.append(f"  {f}: empty frontmatter dict")
        else:
            for key in ["来源", "时间", "平台"]:
                if key not in fm:
                    issues.append(f"  {f}: missing field \"{key}\"")
    except Exception as e:
        issues.append(f"  {f}: YAML error - {e}")

if issues:
    print("Issues found:")
    for i in issues:
        print(i)
else:
    print("All raw/ files have proper frontmatter ✓")
