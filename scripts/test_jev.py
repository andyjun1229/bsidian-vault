#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jev 首测：用 self-interview 第一层过关判据做分类任务
判据（来自 self-interview skill）：一条访谈回答是否包含具体细节（时间/地点/人物/数字）
  - 具体细节 = 过关（可深挖的事实）
  - 笼统感受 = 不过关（需要追问）

测试集：2026-09-17 轻巧与能量对谈的真实回答（含糊和具体都有）
用法：export JEV_API_KEY=你的key && python3 scripts/test_jev.py
      可选对比：export GLM_API_KEY=xxx && python3 scripts/test_jev.py --compare
API 格式说明：Jev 经 Vercel AI Gateway 接入，OpenAI 兼容格式。
  若实际接入后端点/模型名不同，改下面两个常量即可。
"""

import os
import re
import sys
import time
import json
import urllib.request

JEV_BASE = "https://ai-gateway.vercel.ai/v1/chat/completions"  # 若官网直连换成官方端点
JEV_MODEL = "typesafe/jev"  # 若模型名不同按文档改

SYSTEM = (
    "你是一个二分类判断器。判断用户给出的访谈回答是否包含具体细节"
    "（具体时间、地点、人物、数字、事件）。只输出 JSON："
    '{"verdict":"具体"|"笼统","confidence":0.0到1.0}。不输出任何其他文字。'
)

CASES = [
    # (回答, 人工标注) —— 人工标注用于算准确率
    ("在这个地方工作，想到与这些我不喜欢的人一起共事我就皱眉头，会产生非常多负面能量", "笼统"),
    ("被质疑，他说了非常过分的话，几乎等同于侮辱自尊，我当时那一刻非常难受", "笼统"),
    ("部队里说错话，领导把我骂懵了，我是一番好心，在他那里就是冒犯了他", "具体"),
    ("给一个老板开车时走错路，他当着很多外人的场骂我非常难听的话", "具体"),
    ("我就是坐着难受", "笼统"),
    ("跟一个朋友聊AI与化工领域合作做一个知识库的想法，我讲思路他接话", "具体"),
    ("我另一个朋友找我帮他设计产品图，还问我产品方面的意见", "具体"),
    ("我自我消解了，没有那么多在意了，心智更成熟了", "笼统"),
]


def call(base, model, key, text):
    body = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": text},
        ],
    }).encode()
    req = urllib.request.Request(base, data=body, headers={
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    })
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read())
    ms = int((time.time() - t0) * 1000)
    content = data["choices"][0]["message"]["content"]
    return content, ms


def run(name, base, model, key):
    print(f"\n===== {name} =====")
    ok, total, total_ms = 0, 0, 0
    for text, label in CASES:
        try:
            out, ms = call(base, model, key, text)
            total_ms += ms
            total += 1
            m = re.search(r'"verdict"\s*:\s*"([^"]+)"', out)
            verdict = m.group(1) if m else out[:20]
            c = re.search(r'"confidence"\s*:\s*([\d.]+)', out)
            conf = c.group(1) if c else "?"
            hit = "✓" if verdict == label else "✗"
            if verdict == label:
                ok += 1
            print(f"{hit} {verdict}(置信{conf}) {ms}ms | {text[:28]}…")
        except Exception as e:
            print(f"✗ 错误 {str(e)[:60]} | {text[:28]}…")
    if total:
        print(f"准确率 {ok}/{total}，平均耗时 {total_ms//total}ms")


if __name__ == "__main__":
    jev_key = os.environ.get("JEV_API_KEY")
    if not jev_key:
        print("用法：export JEV_API_KEY=你的key && python3 scripts/test_jev.py")
        print("key 获取：① typesafe.ai 点 Join Waitlist；② Vercel AI Marketplace（GitHub 一键登录）搜 jev")
        raise SystemExit(1)
    run("Jev", JEV_BASE, JEV_MODEL, jev_key)
    glm_key = os.environ.get("GLM_API_KEY")
    if glm_key:
        run("GLM-5.3-Flash 对比", "https://open.bigmodel.cn/api/paas/v4/chat/completions",
            "glm-5.3-flash", glm_key)
