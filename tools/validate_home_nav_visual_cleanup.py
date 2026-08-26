#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
MANIFEST = ROOT / "navigation.manifest.json"
CSS = PUBLIC / "air-v2.css"
VISUAL_CONTRACT = PUBLIC / "air-visual-contract.css"
VISUAL_CONTRACT_LINK = '<link rel="stylesheet" href="air-visual-contract.css">'

EXPECTED_NAV = [
    {"path": "how-it-works.html", "label": "How it works"},
    {"path": "where-air-fits.html", "label": "Where AIR fits"},
    {"path": "explore-air.html", "label": "Explore"},
    {"path": "get-started.html", "label": "Get started"},
    {"path": "about.html", "label": "About"},
]
EXPECTED_NAV_SIGNATURE = [(item["path"], item["label"]) for item in EXPECTED_NAV]

H1_RE = re.compile(r'<h1\b([^>]*)>', re.IGNORECASE)
MAIN_RE = re.compile(r'<main>(.*?)</main>', re.IGNORECASE | re.DOTALL)
NAV_RE = re.compile(r'<nav\b[^>]*\bid=["\']nav["\'][^>]*>(.*?)</nav>', re.IGNORECASE | re.DOTALL)
NAV_LINK_RE = re.compile(r'<a\b[^>]*href="([^"]+)"[^>]*>(.*?)</a>', re.IGNORECASE | re.DOTALL)
FOOT_GRID_MARKUP_RE = re.compile(r'<(?:div|section)\b[^>]*class="[^"]*\bfoot-grid\b[^"]*"', re.IGNORECASE)
TAG_RE = re.compile(r'<[^>]+>')


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def classes_from_attrs(attrs: str) -> set[str]:
    match = re.search(r'class="([^"]*)"', attrs)
    return set(match.group(1).split()) if match else set()


def nav_signature(text: str, path: str, errors: list[str]) -> list[tuple[str, str]] | None:
    matches = list(NAV_RE.finditer(text))
    if len(matches) != 1:
        fail(errors, f"{path}: expected exactly one primary nav, found {len(matches)}")
        return None
    signature: list[tuple[str, str]] = []
    for href, raw_label in NAV_LINK_RE.findall(matches[0].group(1)):
        label = html.unescape(TAG_RE.sub("", raw_label))
        label = " ".join(label.split())
        signature.append((href, label))
    return signature


def main() -> int:
    errors: list[str] = []
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if manifest["chrome"]["primary_nav"] != EXPECTED_NAV:
        fail(errors, "primary navigation does not match the approved five-item contract")

    footer = manifest["chrome"]["footer"]
    if set(footer) != {"Legal"}:
        fail(errors, "footer contract must be compact and contain only the Legal group")
    else:
        legal_paths = {str(item["path"]) for item in footer["Legal"]}
        if legal_paths != {"privacy.html", "terms.html"}:
            fail(errors, "compact footer Legal group must contain Privacy and Terms")

    explore = (PUBLIC / "explore-air.html").read_text(encoding="utf-8")
    for required in {"air-docs.html", "use-cases.html"}:
        if f'href="{required}"' not in explore:
            fail(errors, f"{required} must remain discoverable from Explore")

    registered_pages = [str(entry["path"]) for entry in manifest["pages"]]
    content_pages = [path for path in registered_pages if path != "404.html"]

    for path in registered_pages:
        text = (PUBLIC / path).read_text(encoding="utf-8")

        signature = nav_signature(text, path, errors)
        if signature is not None and signature != EXPECTED_NAV_SIGNATURE:
            fail(errors, f"{path}: primary nav differs from canonical five-item sequence: {signature!r}")

        if VISUAL_CONTRACT_LINK + "\n</head>" not in text:
            fail(errors, f"{path}: shared visual contract is not loaded last in the head")

        if text.count('class="btn github-btn"') != 1:
            fail(errors, f"{path}: canonical github-btn control missing or duplicated")
        if FOOT_GRID_MARKUP_RE.search(text):
            fail(errors, f"{path}: obsolete multi-column footer markup remains")
        if text.count('class="foot-bottom"') != 1:
            fail(errors, f"{path}: compact foot-bottom missing or duplicated")
        for required_footer_marker in [
            'class="legal" href="privacy.html"',
            'class="legal" href="terms.html"',
            'class="made" href="made-with-air.html"',
        ]:
            if required_footer_marker not in text:
                fail(errors, f"{path}: compact footer missing {required_footer_marker}")

    for path in content_pages:
        text = (PUBLIC / path).read_text(encoding="utf-8")
        if "brand-field" in text:
            fail(errors, f"{path}: legacy brand-field texture class remains")
        for obsolete in ("hero--patterned", "hero--plain"):
            if obsolete in text:
                fail(errors, f"{path}: obsolete {obsolete} texture semantic remains")

        h1 = list(H1_RE.finditer(text))
        if len(h1) != 1:
            fail(errors, f"{path}: expected exactly one h1, found {len(h1)}")
        else:
            attrs = h1[0].group(1)
            classes = classes_from_attrs(attrs)
            if "page-title" not in classes:
                fail(errors, f"{path}: h1 is missing page-title")
            if "page-title--compact" in classes:
                fail(errors, f"{path}: compact title variant remains")
            style = re.search(r'style="([^"]*)"', attrs)
            if style and re.search(r'(^|;)\s*font-size\s*:', style.group(1), re.IGNORECASE):
                fail(errors, f"{path}: h1 still has an inline font-size")

    index = (PUBLIC / "index.html").read_text(encoding="utf-8")
    main_match = MAIN_RE.search(index)
    if not main_match:
        fail(errors, "index.html: main element missing")
    else:
        section_count = len(re.findall(r'<section\b', main_match.group(1), re.IGNORECASE))
        if section_count != 6:
            fail(errors, f"index.html: expected 6 main sections after reduction, found {section_count}")

    for required in [
        "Your project shouldn’t reset with the session.",
        "Focused. Fluid. AIR.",
        "Work. Handoff. Continue.",
        "Structure helps. Evidence still matters.",
        "Pick up the project. Not the briefing.",
    ]:
        if required not in index:
            fail(errors, f"index.html: missing retained landing-page section: {required}")

    for removed in [
        "Not another AI workspace",
        "What gets carried forward",
        "Dive deeper into AIR’s structure.",
        "AIR costs you something.",
        "The evidence is in the work.",
    ]:
        if removed in index:
            fail(errors, f"index.html: removed/redundant section still present: {removed}")

    where = (PUBLIC / "where-air-fits.html").read_text(encoding="utf-8")
    if '<div class="cards cards--three"><a class="card" href="spec-driven-development.html">' not in where:
        fail(errors, "where-air-fits.html: software-story cards are not using the three-column variant")

    css = CSS.read_text(encoding="utf-8")
    required_css = [
        "--air-page-title-size:clamp(2.65rem,1.8rem + 3vw,4.5rem)",
        ".hero h1{font-size:var(--air-page-title-size)",
        ".page-title{font-size:var(--air-page-title-size)",
        ".cards--three{grid-template-columns:repeat(3,minmax(0,1fr))",
    ]
    for marker in required_css:
        if marker not in css:
            fail(errors, f"air-v2.css: missing {marker}")
    if "--air-page-title-compact-size" in css or ".page-title--compact" in css:
        fail(errors, "air-v2.css: compact page-title variant still exists")
    if ".hero--patterned{" in css or ".hero--plain{" in css:
        fail(errors, "air-v2.css: obsolete hero texture variants remain")

    contract = VISUAL_CONTRACT.read_text(encoding="utf-8")
    for marker in [
        "--air-page-title-size:clamp(2.65rem,1.8rem + 3vw,4.5rem)",
        ".page-title,.hero h1.page-title{font-size:var(--air-page-title-size)!important}",
        "background-image:radial-gradient(rgba(201,162,39,.05) 1px,transparent 1.4px)!important",
        "background-size:26px 26px!important",
        "background-attachment:fixed!important",
        ".hero{background-color:transparent!important;background-image:none!important}",
        ".site-header .nav{gap:4px!important}",
        ".site-header .nav a{",
        "font:500 .91rem/1 'Space Grotesk',system-ui,sans-serif!important",
        "color:var(--muted,#A99E91)!important",
        ".site-header .nav a[aria-current=\"page\"]{",
        ".site-header .github-btn{",
        ".site-footer .foot-grid{display:none!important}",
        ".site-footer .foot-bottom{",
    ]:
        if marker not in contract:
            fail(errors, f"air-visual-contract.css: missing {marker}")
    if ".hero--patterned" in contract or ".hero--plain" in contract:
        fail(errors, "air-visual-contract.css: obsolete hero texture semantics remain")

    if errors:
        print("home/nav visual cleanup validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"home/nav visual cleanup validation: PASS ({len(registered_pages)} registered pages)")
    print("primary nav: How it works | Where AIR fits | Explore | Get started | About")
    print("primary nav visual: canonical landing-page typography/spacing/colors")
    print("global canvas texture: Showcase-style radial pattern")
    print("header GitHub control: canonical landing-page button")
    print("footer: compact Legal + Made with AIR")
    print("deep discovery: Explore")
    print("shared visual contract: loaded last on every registered page")
    print("homepage sections: 6")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
