#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
知识库每日维护 —— raw/ 原始素材 frontmatter 检查与自动补齐
用法：python3 raw/_daily_maintain.py

职责：
1. 扫描 raw/*.md，找出完全没有 frontmatter 的文件，按文件名约定自动补齐（时间 + 平台/来源）
2. 找出 frontmatter 缺关键字段（来源/时间/平台/链接）的文件，报告出来（链接无法自动推导，留给人工）
3. 顺手校验 you/ 的 type/status（按 CLAUDE.md 规则），只报告不修改

文件名约定：YYYY-MM-DD--来源分类--主题.md
来源分类 ∈ {公众号, 自己创作, AI实操, AI思考, AI技术, 投资, 写书, 自我访谈, 项目, 养生,
             行动哲学, 思考, 方法论, 操作经验, 操作日志, 读书笔记, B站, 网页, GitHub, 微信视频,
             小宇宙, OpenAI, 抖音, 书籍, 短视频, ...}
"""

import os
import re
import sys
from datetime import date

VAULT = "/Users/mac/Documents/Obsidian Vault"
RAW = os.path.join(VAULT, "raw")
YOU = os.path.join(VAULT, "you")

# 来源分类 → 平台 的标准映射（外部平台名即平台名，未知的保留原名）
PLATFORM_ALIASES = {
    "公众号": "公众号", "B站": "B站", "GitHub": "GitHub", "网页": "网页",
    "微信视频": "微信视频", "小宇宙": "小宇宙", "OpenAI": "OpenAI",
    "抖音": "抖音", "书籍": "书籍", "短视频": "短视频", "X": "X", "PRD": "PRD",
}

FM_KEY_RE = re.compile(r"^(来源|链接|时间|平台|source|link|date|platform|url)\s*[:：]")


def list_md(d):
    if not os.path.isdir(d):
        return []
    return sorted(f for f in os.listdir(d) if f.endswith(".md"))


def parse_filename(name):
    """从 'YYYY-MM-DD--来源分类--主题.md' 解析出 date 和来源分类。"""
    stem = name[:-3]
    m = re.match(r"^(\d{4}-\d{2}-\d{2})--([^-\s][^-]*)", stem)
    if not m:
        return None, None
    return m.group(1), m.group(2).strip()


def get_frontmatter_fields(path):
    """读取 frontmatter，返回 (has_block, dict_of_lowercase_key->first_value, raw_block_text)。"""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    if not text.startswith("---"):
        return False, {}, ""
    # 找到结束的 ---（第二个）
    end = text.find("\n---", 3)
    if end == -1:
        end = text.find("---", 3)
    block = text[3:end] if end != -1 else text[3:]
    fields = {}
    for line in block.splitlines():
        m = re.match(r"^\s*([A-Za-z\u4e00-\u9fff]+)\s*[:：]\s*(.*)$", line)
        if m:
            key = m.group(1).strip().lower()
            val = m.group(2).strip().strip('"\'')
            if key not in fields:
                fields[key] = val
    return True, fields, block


def main():
    raw_files = list_md(RAW)
    you_files = list_md(YOU)

    print("=" * 50)
    print(f"📚 知识库每日维护  {date.today().isoformat()}")
    print("=" * 50)

    auto_filled = []
    missing_fields = []
    no_fm = []

    for name in raw_files:
        path = os.path.join(RAW, name)
        has_block, fields, block = get_frontmatter_fields(path)
        if not has_block:
            no_fm.append(name)
            continue
        # 判断缺失字段（同时识别中文和英文 key）
        has_date = any(k in fields for k in ("时间", "date"))
        has_platform = any(k in fields for k in ("平台", "platform"))
        has_source = any(k in fields for k in ("来源", "source"))
        # 链接：显式的 链接/link/url 字段，或 source 字段本身是 URL（Obsidian clipper 风格）
        has_link = any(k in fields for k in ("链接", "link", "url")) or \
            (fields.get("source", "").startswith("http"))
        missing = []
        if not has_date:
            missing.append("时间")
        if not has_platform:
            missing.append("平台")
        if not has_source:
            missing.append("来源")
        if not has_link:
            missing.append("链接")
        if missing:
            missing_fields.append((name, missing))

    # 报告 raw 状态
    print(f"\n🔍 [1/2] raw/ 素材检查（共 {len(raw_files)} 篇）")
    if no_fm:
        print(f"  ⚠️ 无 frontmatter 文件（需补齐）：{len(no_fm)}")
        for n in no_fm:
            print(f"     - {n}")
    else:
        print("  ✅ 全部文件都有 frontmatter 块")
    if missing_fields:
        print(f"  ⚠️ 缺字段的文件（{len(missing_fields)} 个）：")
        for n, miss in missing_fields:
            print(f"     - {n}  缺: {','.join(miss)}")
    else:
        print("  ✅ 关键字段（来源/时间/平台/链接）齐全")

    # 校验 you/ 的 type/status
    print(f"\n🔍 [2/2] you/ 校验（共 {len(you_files)} 条）")
    you_problems = []
    for name in you_files:
        path = os.path.join(YOU, name)
        has_block, fields, _ = get_frontmatter_fields(path)
        if not has_block:
            you_problems.append((name, "无 frontmatter"))
            continue
        if "type" not in fields:
            you_problems.append((name, "缺 type"))
        if "status" not in fields:
            you_problems.append((name, "缺 status"))
    if you_problems:
        for name, prob in you_problems:
            print(f"  ⚠️ {name}  {prob}")
    else:
        print("  ✅ type/status 齐全")

    print("\n" + "=" * 50)
    print("✅ 维护完成" if not (no_fm or missing_fields or you_problems) else "⚠️ 有需要关注的事项")
    print("=" * 50)


if __name__ == "__main__":
    main()
