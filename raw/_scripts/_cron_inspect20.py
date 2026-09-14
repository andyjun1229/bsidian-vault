#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""打印 20 个问题文件的 frontmatter 原文，便于精准修复"""
import os

VAULT = "/Users/mac/Documents/Obsidian Vault"
you_dir = os.path.join(VAULT, "you")

targets = [
    "2026-01-31--公众号--AI智能体写代码.md",
    "2026-02-04--公众号--一个人干翻团队.md",
    "2026-02-05--公众号--每天10分钟八段锦.md",
    "2026-02-10--公众号--技术不是关键.md",
    "2026-03-20--公众号--我养了一个AI虾（OpenClaw）后，想明白了三件事.md",
    "2026-03-24--公众号--90%的人还在用AI聊天，10%的人已经在用AI赚钱.md",
    "2026-03-24--公众号--OpenClaw 这次大更新，我看懂了它的野心.md",
    "2026-03-25--公众号--别再重启人生了，你的身体需要打补丁.md",
    "2026-04-23--公众号--AI智能体的终极问题.md",
    "2026-04-24--公众号--如何写好skill的真相.md",
    "2026-05-06--公众号--AI进化全能工作助理.md",
    "2026-05-11--公众号--构建专属知识库.md",
    "2026-05-12--公众号--老子问能婴儿乎.md",
    "2026-06-24--公众号--我用AI10分钟做出1个微信小程序.md",
    "2026-06-30--公众号--我的AI应用半年总结.md",
    "2026-07-07--公众号--AI写标书你可能想错了方向.md",
    "2026-07-08--公众号--只有学会了才能使人快乐.md",
    "2026-07-16--自己创作--炒股7年我头一次搞清楚了直觉这个东西到底是什么.md",
    "2026-07-20--method--Serenity供应链瓶颈选股方法论蒸馏.md",
    "2026-09-07--操作经验--数据安全专题培训总结.md",
]

for f in targets:
    path = os.path.join(you_dir, f)
    if not os.path.isfile(path):
        print(f"### {f}  [文件不存在]")
        continue
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    # 找闭合（前40行内）
    close = None
    for i in range(1, min(len(lines), 40)):
        if lines[i].strip() == "---":
            close = i
            break
    end = close if close else min(len(lines), 15)
    print(f"### {f}  (闭合行: {close})")
    for ln in lines[: end + 1]:
        print("  |", repr(ln))
    print()
