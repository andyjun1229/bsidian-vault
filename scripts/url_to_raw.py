#!/usr/bin/env python3
"""将文章链接抓取为 raw 层原始素材。"""

from __future__ import annotations

import argparse
import datetime as dt
import html
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


IGNORED_TAGS = {"script", "style", "noscript", "svg"}


class TextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._chunks: list[str] = []
        self._ignore_depth = 0

    def handle_starttag(self, tag: str, attrs):
        if tag in IGNORED_TAGS:
            self._ignore_depth += 1
        if tag in {"p", "div", "section", "article", "br", "li", "h1", "h2", "h3", "h4", "h5", "h6"}:
            self._chunks.append("\n")

    def handle_endtag(self, tag: str):
        if tag in IGNORED_TAGS and self._ignore_depth > 0:
            self._ignore_depth -= 1
        if tag in {"p", "div", "section", "article", "li"}:
            self._chunks.append("\n")

    def handle_data(self, data: str):
        if self._ignore_depth:
            return
        text = data.strip()
        if text:
            self._chunks.append(text)
            self._chunks.append("\n")

    def get_text(self) -> str:
        text = "".join(self._chunks)
        text = html.unescape(text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()


def detect_platform(domain: str) -> str:
    d = domain.lower()
    if "mp.weixin.qq.com" in d:
        return "公众号"
    if "x.com" in d or "twitter.com" in d:
        return "推特/X"
    if "zhihu.com" in d:
        return "知乎"
    if "bilibili.com" in d:
        return "B站"
    return "网页"


def detect_category(platform: str, explicit: str | None) -> str:
    if explicit:
        return explicit
    if platform in {"公众号", "推特/X", "知乎", "B站"}:
        return platform
    return "网页"


def clean_name(s: str, fallback: str = "未命名文章") -> str:
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"[\\/:*?\"<>|]", "-", s)
    s = s.replace("\u3000", " ")
    s = s.strip(" .")
    return s or fallback


def parse_html_meta(page_html: str) -> dict[str, str]:
    meta: dict[str, str] = {}

    def pick(pattern: str) -> str | None:
        m = re.search(pattern, page_html, flags=re.IGNORECASE | re.DOTALL)
        if not m:
            return None
        return html.unescape(m.group(1)).strip()

    title = pick(r"<meta[^>]+property=[\"']og:title[\"'][^>]+content=[\"'](.*?)[\"']")
    if not title:
        title = pick(r"<title[^>]*>(.*?)</title>")
    if title:
        meta["title"] = title

    author = pick(r"<meta[^>]+name=[\"']author[\"'][^>]+content=[\"'](.*?)[\"']")
    if author:
        meta["author"] = author

    pub = pick(r"<meta[^>]+(?:property|name)=[\"'](?:article:published_time|publishdate|pubdate|date)[\"'][^>]+content=[\"'](.*?)[\"']")
    if pub:
        meta["published_time"] = pub

    site = pick(r"<meta[^>]+property=[\"']og:site_name[\"'][^>]+content=[\"'](.*?)[\"']")
    if site:
        meta["site_name"] = site

    return meta


def parse_date(text: str | None) -> str | None:
    if not text:
        return None
    m = re.search(r"(20\d{2})[-/年](\d{1,2})[-/月](\d{1,2})", text)
    if not m:
        return None
    y, mo, d = m.groups()
    try:
        return dt.date(int(y), int(mo), int(d)).strftime("%Y-%m-%d")
    except ValueError:
        return None


def fetch_html(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        raw = resp.read()
        ctype = resp.headers.get("Content-Type", "")
    charset_match = re.search(r"charset=([\w-]+)", ctype, flags=re.IGNORECASE)
    charset = charset_match.group(1) if charset_match else "utf-8"
    try:
        return raw.decode(charset, errors="replace")
    except LookupError:
        return raw.decode("utf-8", errors="replace")


def extract_text(page_html: str) -> str:
    parser = TextExtractor()
    parser.feed(page_html)
    text = parser.get_text()
    lines = [re.sub(r"\s+", " ", ln).strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]
    return "\n\n".join(lines)


def find_existing_by_url(raw_dir: Path, url: str) -> Path | None:
    for f in raw_dir.glob("*.md"):
        try:
            head = f.read_text(encoding="utf-8", errors="ignore")[:5000]
        except Exception:
            continue
        if f"链接：{url}" in head or f"链接: {url}" in head:
            return f
    return None


def unique_path(raw_dir: Path, base_name: str) -> Path:
    candidate = raw_dir / f"{base_name}.md"
    if not candidate.exists():
        return candidate
    i = 2
    while True:
        candidate = raw_dir / f"{base_name}-{i}.md"
        if not candidate.exists():
            return candidate
        i += 1


def build_markdown(
    title: str,
    source_name: str,
    url: str,
    date_str: str,
    platform: str,
    content: str,
    author: str | None,
) -> str:
    fetched = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    body = content if content else "（正文抓取失败，请手动补充）"
    author_line = f"作者：{author}\n" if author else ""
    return (
        "---\n"
        f"来源：{source_name}\n"
        f"链接：{url}\n"
        f"时间：{date_str}\n"
        f"平台：{platform}\n"
        f"抓取时间：{fetched}\n"
        "---\n\n"
        f"# {title}\n\n"
        "## 摘要\n\n"
        "（自动抓取，建议二次清理）\n\n"
        "## 原文正文\n\n"
        f"{body}\n\n"
        "## 备注\n\n"
        f"- 自动录入来源链接\n- {author_line}".rstrip()
        + "\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description="输入文章链接，自动写入 raw 原始素材")
    ap.add_argument("url", help="文章链接")
    ap.add_argument("--vault", default=str(Path(__file__).resolve().parents[1]), help="Obsidian Vault 根目录")
    ap.add_argument("--category", default=None, help="来源分类（默认自动推断）")
    ap.add_argument("--title", default=None, help="手动覆盖标题")
    ap.add_argument("--date", default=None, help="手动覆盖日期，格式 YYYY-MM-DD")
    ap.add_argument("--dry-run", action="store_true", help="仅打印结果，不落盘")
    args = ap.parse_args()

    url = args.url.strip()
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme not in {"http", "https", "file"}:
        print("[ERROR] 只支持 http/https/file 链接", file=sys.stderr)
        return 2

    vault = Path(args.vault).expanduser().resolve()
    raw_dir = vault / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

    existing = find_existing_by_url(raw_dir, url)
    if existing:
        print(f"[SKIP] 已存在同链接素材: {existing}")
        return 0

    try:
        page_html = fetch_html(url)
    except urllib.error.URLError as e:
        print(f"[ERROR] 抓取失败: {e}", file=sys.stderr)
        return 1

    meta = parse_html_meta(page_html)
    text = extract_text(page_html)

    domain = parsed.netloc or "local-file"
    platform = detect_platform(domain)
    category = detect_category(platform, args.category)

    title = clean_name(args.title or meta.get("title") or "未命名文章")
    source_name = meta.get("site_name") or domain

    date_str = args.date or parse_date(meta.get("published_time")) or dt.date.today().strftime("%Y-%m-%d")
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        print("[ERROR] --date 格式必须是 YYYY-MM-DD", file=sys.stderr)
        return 2

    base_name = f"{date_str}--{category}--{title}"
    out_path = unique_path(raw_dir, clean_name(base_name, fallback=f"{date_str}--{category}--未命名文章"))

    md = build_markdown(
        title=title,
        source_name=source_name,
        url=url,
        date_str=date_str,
        platform=platform,
        content=text,
        author=meta.get("author"),
    )

    if args.dry_run:
        print(f"[DRY-RUN] 将写入: {out_path}")
        print(md[:1000])
        return 0

    out_path.write_text(md, encoding="utf-8")
    print(f"[OK] 已写入: {out_path}")
    print(f"[INFO] 正文长度: {len(text)} 字符")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
