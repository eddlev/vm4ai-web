#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
MANIFEST = ROOT / "navigation.manifest.json"
CSS = PUBLIC / "air-v2.css"

EXPECTED_NAV = [
    {"path": "how-it-works.html", "label": "How it works"},
    {"path": "where-air-fits.html", "label": "Where AIR fits"},
    {"path": "explore-air.html", "label": "Explore"},
    {"path": "get-started.html", "label": "Get started"},
]
ORIENTATION = {
    "how-it-works.html",
    "where-air-fits.html",
    "explore-air.html",
    "get-started.html",
}

H1_RE = re.compile(r'<h1\b([^>]*)>', re.IGNORECASE)
HERO_RE = re.compile(r'<section\b[^>]*class="([^"]*\bhero\b[^"]*)"[^>]*>', re.IGNORECASE)
MAIN_RE = re.compile(r'<main>(.*?)</main>', re.IGNORECASE | re.DOTALL)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def classes_from_attrs(attrs: str) -> set[str]:
    match = re.search(r'class="([^"]*)"', attrs)
    return set(match.group(1).split()) if match else set()


def main() -> int:
    errors: list[str] = []
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))

    if manifest["chrome"]["primary_nav"] != EXPECTED_NAV:
        fail(errors, "primary navigation does not match the approved four-item contract")

    product_paths = {str(item["path"]) for item in manifest["chrome"]["footer"]["Product"]}
    for required in {"air-docs.html", "use-cases.html"}:
        if required not in product_paths:
            fail(errors, f"{required} must remain discoverable in the footer")

    pages = [str(entry["path"]) for entry in manifest["pages"] if str(entry["path"]) != "404.html"]
    patterned: set[str] = set()
    for path in pages:
        text = (PUBLIC / path).read_text(encoding="utf-8")
        if "brand-field" in text:
            fail(errors, f"{path}: legacy brand-field texture class remains")

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

        hero = list(HERO_RE.finditer(text))
        if len(hero) != 1:
            fail(errors, f"{path}: expected exactly one hero section, found {len(hero)}")
        else:
            classes = set(hero[0].group(1).split())
            if path in ORIENTATION:
                if "hero--patterned" not in classes or "hero--plain" in classes:
                    fail(errors, f"{path}: orientation hero is not patterned")
                else:
                    patterned.add(path)
            else:
                if "hero--plain" not in classes or "hero--patterned" in classes:
                    fail(errors, f"{path}: non-orientation hero is not plain")

    if patterned != ORIENTATION:
        fail(errors, f"patterned hero set is {sorted(patterned)}, expected {sorted(ORIENTATION)}")

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
        ".hero--patterned{",
        ".hero--plain{",
    ]
    for marker in required_css:
        if marker not in css:
            fail(errors, f"air-v2.css: missing {marker}")
    if "--air-page-title-compact-size" in css or ".page-title--compact" in css:
        fail(errors, "air-v2.css: compact page-title variant still exists")

    if errors:
        print("home/nav visual cleanup validation: FAIL", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"home/nav visual cleanup validation: PASS ({len(pages)} content pages)")
    print("primary nav: How it works | Where AIR fits | Explore | Get started")
    print("patterned heroes: " + ", ".join(sorted(ORIENTATION)))
    print("homepage sections: 6")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
