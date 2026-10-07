#!/usr/bin/env python3
"""Import a Medium post into this Hugo site as a markdown file.

The Medium post page itself is behind Cloudflare, so this fetches the
author's RSS feed instead, finds the item matching the URL, converts its
HTML to markdown (no em dashes) and writes content/posts/<slug>.md with the
front matter used by the site.

Usage:
    python3 tools/medium_import.py <medium-post-url> [options]

Example:
    python3 tools/medium_import.py \\
        "https://medium.com/@tacherasasi/some-post-deadbeef1234"
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"
)
CONTENT_NS = "{http://purl.org/rss/1.0/modules/content/}encoded"
REPO_ROOT = Path(__file__).resolve().parents[1]
SLUG_RE = re.compile(r"^[A-Za-z0-9._-]+$")
URL_RE = re.compile(r"https?://[^\s<>()\[\]]+")


def de_em_dash(text: str) -> str:
    text = text.replace(" \u2014 ", ", ")
    return text.replace("\u2014", ", ")


def linkify(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        url = match.group(0).rstrip(".,;:!?")
        return f"[{url}]({url}){match.group(0)[len(url):]}"

    return URL_RE.sub(repl, text)


def guess_language(code: str) -> str:
    if re.search(
        r"^package\s+\w+|:=|\bfunc\s+\w+\(|\[\]byte|\bchan\b|\bdefer\b|^\s*go\s+[\w.]+\(|^\s*io\.",
        code,
        re.M,
    ):
        return "go"
    if re.search(r"\bfn\s+\w+\(", code) and re.search(r"\bconst\b|\bvar\b|\bpub\b", code):
        return "zig"
    if re.search(r"\bfn\s+\w+\(", code) and re.search(r"\blet\s+mut\b|\bimpl\s+\w+|\bpub\s+fn\b", code):
        return "rust"
    if re.search(r"^\s*#include\s*<", code, re.M):
        return "c"
    if re.search(r"\bdef\s+\w+\(|^\s*import\s+\w+", code, re.M):
        return "python"
    if re.search(
        r"\binterface\s+\w+|\)\s*=>|\bexport\s+(const|function|interface)\b|:\s*(string|number|boolean)\b",
        code,
    ):
        return "ts"
    return ""


class MarkdownConverter(HTMLParser):
    SKIP = {"script", "style", "iframe"}
    BOLD = {"strong", "b"}
    ITALIC = {"em", "i"}

    def __init__(self, lang_override: str = "") -> None:
        super().__init__(convert_charrefs=True)
        self.lang_override = lang_override
        self.parts: list[str] = []
        self.link_stack: list[str] = []
        self.skip_depth = 0
        self.li_depth = 0
        self.list_stack: list[list] = []
        self.in_pre = False
        self.pre_lang = ""
        self.pre_buf: list[str] = []

    def emit(self, text: str) -> None:
        self.parts.append(text)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k: (v or "") for k, v in attrs}
        if tag in self.SKIP:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if self.in_pre:
            if tag == "br":
                self.pre_buf.append("\n")
            elif tag == "code":
                cls = attr.get("class", "")
                if cls.startswith("language-"):
                    self.pre_lang = cls[len("language-"):]
            return

        if tag == "pre":
            self.in_pre = True
            self.pre_lang = ""
            self.pre_buf = []
        elif tag == "p":
            if self.li_depth == 0:
                self.emit("\n\n")
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.emit("\n\n" + "#" * int(tag[1]) + " ")
        elif tag in self.BOLD:
            self.emit("**")
        elif tag in self.ITALIC:
            self.emit("*")
        elif tag == "a":
            self.emit("[")
            self.link_stack.append(attr.get("href", ""))
        elif tag == "img":
            src = attr.get("src", "")
            if src and "medium.com/_/stat" not in src:
                self.emit(f"![{attr.get('alt', '')}]({src})")
        elif tag == "figure":
            self.emit("\n\n")
        elif tag == "br":
            self.emit("  \n")
        elif tag == "blockquote":
            self.emit("\n\n> ")
        elif tag == "hr":
            self.emit("\n\n---\n\n")
        elif tag in ("ul", "ol"):
            self.list_stack.append([tag, 0])
            self.emit("\n")
        elif tag == "li":
            if not self.list_stack:
                self.list_stack.append(["ul", 0])
            entry = self.list_stack[-1]
            entry[1] += 1
            indent = "  " * len(self.list_stack)
            marker = f"{entry[1]}. " if entry[0] == "ol" else "* "
            self.emit(indent + marker)
            self.li_depth += 1
        elif tag == "code":
            self.emit("`")

    def handle_endtag(self, tag: str) -> None:
        if tag in self.SKIP:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if self.skip_depth:
            return
        if self.in_pre:
            if tag == "pre":
                code = "".join(self.pre_buf).strip("\n")
                lang = self.pre_lang or self.lang_override or guess_language(code)
                self.emit(f"\n\n```{lang}\n{code}\n```\n\n")
                self.in_pre = False
                self.pre_lang = ""
                self.pre_buf = []
            return

        if tag == "p":
            if self.li_depth == 0:
                self.emit("\n\n")
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self.emit("\n\n")
        elif tag in self.BOLD:
            self.emit("**")
        elif tag in self.ITALIC:
            self.emit("*")
        elif tag == "a":
            href = self.link_stack.pop() if self.link_stack else ""
            self.emit(f"]({href})")
        elif tag == "figure":
            self.emit("\n\n")
        elif tag == "blockquote":
            self.emit("\n\n")
        elif tag in ("ul", "ol"):
            if self.list_stack:
                self.list_stack.pop()
            self.emit("\n")
        elif tag == "li":
            self.li_depth = max(0, self.li_depth - 1)
            self.emit("\n")
        elif tag == "code":
            self.emit("`")

    def handle_data(self, data: str) -> None:
        if self.skip_depth:
            return
        if self.in_pre:
            self.pre_buf.append(data)
            return
        text = data.replace("\u00a0", " ").replace("\n", " ")
        text = de_em_dash(text)
        if not self.link_stack:
            text = linkify(text)
        self.emit(text)


def collapse_blank_lines(markdown: str) -> str:
    lines, out, in_code, blanks = markdown.split("\n"), [], False, 0
    for line in lines:
        if line.lstrip().startswith("```"):
            in_code = not in_code
        if not in_code and not line.strip():
            blanks += 1
            if blanks > 1:
                continue
        else:
            blanks = 0
        out.append(line)
    return "\n".join(out)


def to_markdown(fragment: str, lang_override: str = "") -> str:
    conv = MarkdownConverter(lang_override)
    conv.feed(fragment)
    conv.close()
    markdown = de_em_dash(collapse_blank_lines("".join(conv.parts)))
    return markdown.strip() + "\n"


def truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    cut = text[:limit]
    if " " in cut:
        cut = cut.rsplit(" ", 1)[0]
    return cut.rstrip() + "..."


def derive_summary(markdown: str) -> str:
    for line in markdown.splitlines():
        line = line.strip()
        if not line or line.startswith("![") or line.startswith("#"):
            continue
        line = URL_RE.sub(lambda m: m.group(0), line)
        line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
        line = line.replace("**", "").replace("*", "")
        return truncate(line, 200)
    return ""


def parse_medium_url(raw: str) -> tuple[str, str]:
    parsed = urlparse(raw)
    if not parsed.hostname or not parsed.hostname.endswith("medium.com"):
        raise SystemExit(f"not a medium.com URL: {raw}")
    parts = [p for p in parsed.path.split("/") if p]
    for i, part in enumerate(parts):
        if part.startswith("@") and i + 1 < len(parts):
            slug = parts[i + 1]
            if not SLUG_RE.match(slug):
                raise SystemExit(f"unsupported slug in URL: {slug}")
            return part[1:], slug
    raise SystemExit(
        "could not find @handle/slug in URL; "
        "use the canonical https://medium.com/@user/<slug> form"
    )


def fetch(url: str, timeout: float) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/rss+xml, application/xml, text/xml, */*",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def find_item(items: list[ET.Element], slug: str) -> ET.Element | None:
    for item in items:
        link = item.findtext("link") or ""
        path = [p for p in urlparse(link).path.split("/") if p]
        if path and path[-1] == slug:
            return item
    return None


def parse_date(pub_date: str | None) -> date:
    if pub_date:
        try:
            return parsedate_to_datetime(pub_date).date()
        except (TypeError, ValueError):
            pass
    return date.today()


def yaml_string(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="medium_import",
        description="Convert a Medium post into a Hugo markdown file.",
    )
    parser.add_argument("url", help="canonical Medium post URL")
    parser.add_argument(
        "-o",
        "--out",
        default=str(REPO_ROOT / "content" / "posts"),
        help="output directory (default: content/posts)",
    )
    parser.add_argument(
        "--summary",
        default="",
        help="front matter summary (default: first paragraph, truncated)",
    )
    parser.add_argument(
        "--tags",
        default="",
        help="comma-separated tags (default: RSS categories)",
    )
    parser.add_argument("--feed", default="", help="override the RSS feed URL")
    parser.add_argument(
        "--lang",
        default="",
        help="force the fenced-code language (default: guess from the code)",
    )
    parser.add_argument("--force", action="store_true", help="overwrite if the file exists")
    parser.add_argument("--timeout", type=float, default=30.0, help="HTTP timeout in seconds")
    args = parser.parse_args()

    handle, slug = parse_medium_url(args.url)
    feed_url = args.feed or f"https://medium.com/feed/@{handle}"

    try:
        feed_xml = fetch(feed_url, args.timeout)
    except OSError as err:
        raise SystemExit(f"failed to fetch {feed_url}: {err}")

    try:
        root = ET.fromstring(feed_xml)
    except ET.ParseError as err:
        raise SystemExit(f"failed to parse RSS feed: {err}")

    item = find_item(list(root.iter("item")), slug)
    if item is None:
        raise SystemExit(
            f"post {slug!r} not found in {feed_url} "
            "(the RSS feed only lists recent posts)"
        )

    title = item.findtext("title") or slug
    link = item.findtext("link") or args.url
    content = item.findtext(CONTENT_NS) or ""
    md = to_markdown(content, args.lang)

    summary = args.summary or derive_summary(md) or title
    tags = [t.strip() for t in args.tags.split(",") if t.strip()]
    if not tags:
        tags = [c.text.strip() for c in item.findall("category") if c.text and c.text.strip()]

    post_id = slug.rsplit("-", 1)[-1] if "-" in slug else ""

    out = (
        "---\n"
        f"title: {yaml_string(title)}\n"
        f"date: {parse_date(item.findtext('pubDate')).isoformat()}\n"
        f"summary: {yaml_string(summary)}\n"
        "draft: false\n"
        f"medium: {yaml_string(link)}\n"
        f"tags: [{', '.join(yaml_string(t) for t in tags)}]\n"
        "---\n\n"
        f"{md}"
    )
    if post_id:
        out += (
            "\n"
            f"![](https://medium.com/_/stat?event=post.clientViewed"
            f"&referrerSource=full_rss&postId={post_id})\n"
        )
    out += f"\n---\n\n*Originally published on [Medium]({link}).*\n"

    if "\u2014" in out:
        raise SystemExit("refusing to write: em dash survived conversion")

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)
    dst = out_dir / f"{slug}.md"
    if dst.exists() and not args.force:
        raise SystemExit(f"{dst} already exists (use --force to overwrite)")

    dst.write_text(out, encoding="utf-8")
    print(dst)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
