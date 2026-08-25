#!/usr/bin/env python3
"""Validate vm4ai.com navigation and internal-link integrity.

Standard-library only. The public site stays static and deployment keeps its
zero-build Cloudflare Pages model; this script is a development/release check,
not a runtime dependency.
"""
from __future__ import annotations

import argparse
import json
import posixpath
import sys
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlparse

REPO_ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO_ROOT / "navigation.manifest.json"


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[str] = []
        self.primary_nav: list[tuple[str, str]] = []
        self.footer_links: list[str] = []
        self._nav_depth = 0
        self._footer_depth = 0
        self._active_anchor: dict[str, object] | None = None

    @staticmethod
    def _attrs(attrs: list[tuple[str, str | None]]) -> dict[str, str]:
        return {k: (v or "") for k, v in attrs}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        a = self._attrs(attrs)
        classes = set(a.get("class", "").split())
        if tag == "nav" and ("nav" in classes or a.get("aria-label", "").lower() == "primary"):
            self._nav_depth += 1
        elif self._nav_depth:
            self._nav_depth += 1

        if tag == "footer" and "site-footer" in classes:
            self._footer_depth += 1
        elif self._footer_depth:
            self._footer_depth += 1

        if tag == "a" and "href" in a:
            href = a["href"].strip()
            self.links.append(href)
            if self._footer_depth:
                self.footer_links.append(href)
            if self._nav_depth:
                self._active_anchor = {"href": href, "text": []}

    def handle_data(self, data: str) -> None:
        if self._active_anchor is not None:
            text = self._active_anchor["text"]
            assert isinstance(text, list)
            text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._active_anchor is not None:
            href = str(self._active_anchor["href"])
            pieces = self._active_anchor["text"]
            assert isinstance(pieces, list)
            label = " ".join("".join(pieces).split())
            self.primary_nav.append((href, label))
            self._active_anchor = None

        if self._nav_depth:
            self._nav_depth -= 1
        if self._footer_depth:
            self._footer_depth -= 1


def load_manifest() -> dict:
    with MANIFEST_PATH.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def page_path_from_url(url: str, base_url: str, homepage: str) -> str | None:
    parsed = urlparse(url)
    if parsed.scheme and parsed.scheme not in {"http", "https"}:
        return None
    base = urlparse(base_url)
    if parsed.netloc and parsed.netloc != base.netloc:
        return None
    path = unquote(parsed.path or "")
    if path in {"", "/"}:
        return homepage
    return path.lstrip("/")


def local_target(source: str, href: str, base_url: str, homepage: str, ignored_schemes: set[str]) -> str | None:
    href = href.strip()
    if not href or href.startswith("#"):
        return None
    parsed = urlparse(href)
    if parsed.scheme in ignored_schemes:
        return None
    if parsed.scheme in {"http", "https"} or parsed.netloc:
        return page_path_from_url(href, base_url, homepage)
    raw_path = unquote(parsed.path)
    if raw_path in {"", "/"}:
        return homepage if raw_path == "/" else source
    if raw_path.startswith("/"):
        return posixpath.normpath(raw_path.lstrip("/"))
    source_dir = posixpath.dirname(source)
    return posixpath.normpath(posixpath.join(source_dir, raw_path))


def read_sitemap(path: Path, base_url: str, homepage: str) -> set[str]:
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    root = ET.parse(path).getroot()
    out: set[str] = set()
    for loc in root.findall("sm:url/sm:loc", ns):
        if not loc.text:
            continue
        page = page_path_from_url(loc.text.strip(), base_url, homepage)
        if page is not None:
            out.add(page)
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict-chrome", action="store_true", help="treat target primary-nav/footer drift as errors")
    args = parser.parse_args()

    manifest = load_manifest()
    site = manifest["site"]
    validation = manifest["validation"]
    public = REPO_ROOT / site["public_root"]
    homepage = site["homepage"]
    base_url = site["base_url"]
    ignored_schemes = set(validation.get("ignored_href_schemes", []))

    errors: list[str] = []
    warnings: list[str] = []

    page_entries = manifest["pages"]
    registered = {p["path"]: p for p in page_entries}
    if len(registered) != len(page_entries):
        errors.append("navigation.manifest.json contains duplicate page paths")

    # Every top-level HTML page is either registered or deliberately removed.
    actual_html = {p.name for p in public.glob("*.html") if p.is_file()}
    registered_html = set(registered)
    if validation.get("require_all_top_level_html_registered", False):
        for path in sorted(actual_html - registered_html):
            errors.append(f"unregistered public HTML page: {path}")
        for path in sorted(registered_html - actual_html):
            errors.append(f"manifest page does not exist: public/{path}")

    # Manifest navigation and journey references must resolve to registered pages.
    for item in manifest["chrome"]["primary_nav"]:
        if item["path"] not in registered:
            errors.append(f"primary_nav references unregistered page: {item['path']}")
    for group, items in manifest["chrome"]["footer"].items():
        for item in items:
            if item["path"] not in registered:
                errors.append(f"footer group {group!r} references unregistered page: {item['path']}")
    for journey, paths in manifest["journeys"].items():
        for path in paths:
            if path not in registered:
                errors.append(f"journey {journey!r} references unregistered page: {path}")

    # Sitemap must match the manifest's explicit sitemap policy.
    if validation.get("require_sitemap_exact_for_registered_pages", False):
        sitemap_actual = read_sitemap(public / site["sitemap"], base_url, homepage)
        sitemap_expected = {p["path"] for p in page_entries if p.get("sitemap", False)}
        for path in sorted(sitemap_expected - sitemap_actual):
            errors.append(f"registered sitemap page missing from sitemap.xml: {path}")
        for path in sorted(sitemap_actual - sitemap_expected):
            errors.append(f"sitemap.xml contains page not marked sitemap=true: {path}")

    # Parse every registered HTML page once.
    parsed_pages: dict[str, PageParser] = {}
    for path in sorted(registered_html & actual_html):
        p = PageParser()
        p.feed((public / path).read_text(encoding="utf-8"))
        parsed_pages[path] = p

    inbound_sources: dict[str, set[str]] = defaultdict(set)
    broken: list[tuple[str, str, str]] = []

    for source, parsed in parsed_pages.items():
        for href in parsed.links:
            target = local_target(source, href, base_url, homepage, ignored_schemes)
            if target is None:
                continue
            target_path = public / target
            if validation.get("require_internal_href_targets_exist", False) and not target_path.exists():
                broken.append((source, href, target))
                continue
            if target in registered and target != source:
                inbound_sources[target].add(source)

    for source, href, target in broken:
        errors.append(f"broken internal href in {source}: {href!r} -> {target}")

    if validation.get("require_minimum_inbound_links", False):
        for path, entry in registered.items():
            minimum = int(entry.get("min_inbound", 0))
            actual = len(inbound_sources.get(path, set()))
            if actual < minimum:
                errors.append(f"insufficient inbound discovery for {path}: {actual} unique source page(s), minimum {minimum}")

    # Shared chrome is intentionally a target contract until the refactor lands.
    target_primary = [(i["path"], i["label"]) for i in manifest["chrome"]["primary_nav"]]
    primary_signatures: Counter[tuple[tuple[str, str], ...]] = Counter()
    footer_signatures: Counter[tuple[str, ...]] = Counter()
    target_footer_paths = {
        item["path"]
        for items in manifest["chrome"]["footer"].values()
        for item in items
    }

    for source, parsed in parsed_pages.items():
        primary = tuple(
            (local_target(source, href, base_url, homepage, ignored_schemes) or href, label)
            for href, label in parsed.primary_nav
        )
        if primary:
            primary_signatures[primary] += 1

        footer_internal = []
        for href in parsed.footer_links:
            target = local_target(source, href, base_url, homepage, ignored_schemes)
            if target in registered:
                footer_internal.append(target)
        if footer_internal:
            footer_signatures[tuple(dict.fromkeys(footer_internal))] += 1

    chrome_issues: list[str] = []
    if len(primary_signatures) > 1:
        chrome_issues.append(f"primary navigation currently has {len(primary_signatures)} distinct signatures across pages")
    elif primary_signatures:
        current_primary = list(next(iter(primary_signatures)))
        if current_primary != target_primary:
            chrome_issues.append("current primary navigation differs from navigation.manifest.json target")

    if len(footer_signatures) > 1:
        chrome_issues.append(f"footer navigation currently has {len(footer_signatures)} distinct internal-link signatures across pages")

    for source, parsed in parsed_pages.items():
        footer_targets = {
            local_target(source, href, base_url, homepage, ignored_schemes)
            for href in parsed.footer_links
        }
        missing = sorted(target_footer_paths - footer_targets)
        if missing:
            # One aggregate message per signature is enough; avoid flooding output.
            warnings.append(f"{source}: footer is missing target-contract links: {', '.join(missing)}")

    if chrome_issues:
        if args.strict_chrome or validation.get("chrome_mode") == "error":
            errors.extend(chrome_issues)
        else:
            warnings.extend(chrome_issues)

    print(f"registered pages: {len(registered)}")
    print(f"public HTML pages: {len(actual_html)}")
    print(f"errors: {len(errors)}")
    print(f"warnings: {len(warnings)}")

    if warnings:
        print("\nWARNINGS")
        for item in warnings:
            print(f"- {item}")

    if errors:
        print("\nERRORS")
        for item in errors:
            print(f"- {item}")
        return 1

    print("\nVM4AI navigation validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
