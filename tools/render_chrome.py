#!/usr/bin/env python3
"""Render canonical vm4ai.com header/footer into static public HTML.

The deployed site remains plain static HTML. This tool owns only the global
<header class="site-header"> and <footer class="site-footer"> regions.
Everything outside those two regions must remain byte-for-byte unchanged.
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "navigation.manifest.json"
HEADER_TEMPLATE = ROOT / "chrome" / "header.html"
FOOTER_TEMPLATE = ROOT / "chrome" / "footer.html"

HEADER_RE = re.compile(
    r'<header\b[^>]*class=["\'][^"\']*\bsite-header\b[^"\']*["\'][^>]*>.*?</header>',
    re.IGNORECASE | re.DOTALL,
)
FOOTER_RE = re.compile(
    r'<footer\b[^>]*class=["\'][^"\']*\bsite-footer\b[^"\']*["\'][^>]*>.*?</footer>',
    re.IGNORECASE | re.DOTALL,
)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def render_links(items: list[dict], current: str | None = None, indent: str = "      ") -> str:
    lines: list[str] = []
    for item in items:
        path = str(item["path"])
        label = html.escape(str(item["label"]))
        attrs = ""
        if current is not None and path == current:
            attrs = ' class="active" aria-current="page"'
        lines.append(f'{indent}<a href="{html.escape(path, quote=True)}"{attrs}>{label}</a>')
    return "\n".join(lines)


def render_legal(items: list[dict]) -> str:
    links = [
        f'<a class="legal" href="{html.escape(str(item["path"]), quote=True)}">{html.escape(str(item["label"]))}</a>'
        for item in items
    ]
    return " · ".join(links)


def render_header(template: str, manifest: dict, current: str) -> str:
    if template.count("{{PRIMARY_NAV}}") != 1:
        raise RuntimeError("chrome/header.html must contain exactly one {{PRIMARY_NAV}} placeholder")
    return template.replace(
        "{{PRIMARY_NAV}}",
        render_links(manifest["chrome"]["primary_nav"], current=current, indent="      "),
    )


def render_footer(template: str, manifest: dict) -> str:
    footer = manifest["chrome"]["footer"]
    replacements = {
        "{{FOOTER_PRODUCT}}": render_links(footer["Product"], indent="        "),
        "{{FOOTER_EVIDENCE}}": render_links(footer["Evidence"], indent="        "),
        "{{FOOTER_MORE}}": render_links(footer["More"], indent="        "),
        "{{FOOTER_LEGAL}}": render_legal(footer["Legal"]),
    }
    out = template
    for marker, value in replacements.items():
        if out.count(marker) != 1:
            raise RuntimeError(f"chrome/footer.html must contain exactly one {marker} placeholder")
        out = out.replace(marker, value)
    return out


def exactly_one(pattern: re.Pattern[str], text: str, label: str, path: str) -> re.Match[str]:
    matches = list(pattern.finditer(text))
    if len(matches) != 1:
        raise RuntimeError(f"{path}: expected exactly one {label}, found {len(matches)}")
    return matches[0]


def skeleton(text: str, path: str) -> str:
    exactly_one(HEADER_RE, text, "site-header", path)
    exactly_one(FOOTER_RE, text, "site-footer", path)
    text = HEADER_RE.sub("{{SHARED_HEADER}}", text, count=1)
    text = FOOTER_RE.sub("{{SHARED_FOOTER}}", text, count=1)
    return text


def render_page(source: str, path: str, header: str, footer: str) -> str:
    exactly_one(HEADER_RE, source, "site-header", path)
    exactly_one(FOOTER_RE, source, "site-footer", path)
    rendered = HEADER_RE.sub(lambda _: header, source, count=1)
    rendered = FOOTER_RE.sub(lambda _: footer, rendered, count=1)
    if skeleton(source, path) != skeleton(rendered, path):
        raise RuntimeError(f"{path}: non-chrome page content changed during render")
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true", help="rewrite registered public HTML with canonical chrome")
    mode.add_argument("--check", action="store_true", help="fail if registered public HTML is not already canonical")
    args = parser.parse_args()

    manifest = load_json(MANIFEST)
    public = ROOT / manifest["site"]["public_root"]
    header_template = HEADER_TEMPLATE.read_text(encoding="utf-8").strip()
    footer = render_footer(FOOTER_TEMPLATE.read_text(encoding="utf-8").strip(), manifest)

    changed: list[str] = []
    for entry in manifest["pages"]:
        path = str(entry["path"])
        file_path = public / path
        if not file_path.is_file():
            raise RuntimeError(f"registered page missing: {file_path}")
        source = file_path.read_text(encoding="utf-8")
        header = render_header(header_template, manifest, current=path)
        rendered = render_page(source, path, header, footer)
        if rendered != source:
            changed.append(path)
            if args.write:
                file_path.write_text(rendered, encoding="utf-8")

    if args.check and changed:
        print("shared chrome is stale on:")
        for path in changed:
            print(f"- {path}")
        return 1

    if args.write:
        print(f"shared chrome rendered: {len(changed)} page(s) changed")
    else:
        print(f"shared chrome check: PASS ({len(manifest['pages'])} registered page(s))")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"shared chrome render failed: {exc}", file=sys.stderr)
        sys.exit(1)
