#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "navigation.manifest.json"
PUBLIC = ROOT / "public"
CSS = PUBLIC / "air-v2.css"

PRIMARY_NAV = [
    {"path": "how-it-works.html", "label": "How it works"},
    {"path": "where-air-fits.html", "label": "Where AIR fits"},
    {"path": "explore-air.html", "label": "Explore"},
    {"path": "get-started.html", "label": "Get started"},
]

CLASS_ATTR_RE = re.compile(r'class="([^"]*)"')
H1_RE = re.compile(r'<h1\b([^>]*)>', re.IGNORECASE)


def update_class_attr(tag: str, add: set[str] | None = None, remove: set[str] | None = None) -> str:
    add = add or set()
    remove = remove or set()
    match = CLASS_ATTR_RE.search(tag)
    if match:
        classes = [c for c in match.group(1).split() if c not in remove]
        for item in add:
            if item not in classes:
                classes.append(item)
        value = " ".join(classes)
        return tag[: match.start()] + f'class="{value}"' + tag[match.end() :]
    if not add:
        return tag
    insert = " " + f'class="{" ".join(sorted(add))}"'
    return tag[:-1] + insert + ">"


def remove_class_token_everywhere(text: str, token: str) -> str:
    def repl(match: re.Match[str]) -> str:
        classes = [c for c in match.group(1).split() if c != token]
        return f'class="{" ".join(classes)}"'
    return CLASS_ATTR_RE.sub(repl, text)


def normalize_h1(text: str, path: str) -> str:
    matches = list(H1_RE.finditer(text))
    if len(matches) != 1:
        raise SystemExit(f"{path}: expected exactly one h1, found {len(matches)}")
    match = matches[0]
    tag = match.group(0)
    tag = update_class_attr(tag, add={"page-title"}, remove={"page-title--compact"})
    style_match = re.search(r'\sstyle="([^"]*)"', tag)
    if style_match:
        declarations = []
        for raw in style_match.group(1).split(";"):
            raw = raw.strip()
            if not raw:
                continue
            if raw.split(":", 1)[0].strip().lower() == "font-size":
                continue
            declarations.append(raw)
        replacement = (' style="' + ";".join(declarations) + '"') if declarations else ""
        tag = tag[: style_match.start()] + replacement + tag[style_match.end() :]
    return text[: match.start()] + tag + text[match.end() :]


def patch_where_air_fits(text: str) -> str:
    marker = '<div class="cards"><a class="card" href="spec-driven-development.html">'
    replacement = '<div class="cards cards--three"><a class="card" href="spec-driven-development.html">'
    if replacement in text:
        return text
    if text.count(marker) != 1:
        raise SystemExit(f"where-air-fits.html: expected exactly one software-card grid marker, found {text.count(marker)}")
    return text.replace(marker, replacement, 1)


def patch_css() -> bool:
    text = CSS.read_text(encoding="utf-8")
    original = text
    text = text.replace(
        ".hero h1{font-size:clamp(3.1rem,6.7vw,6.3rem);max-width:720px;margin:.8rem 0 1rem}",
        ".hero h1{font-size:var(--air-page-title-size);max-width:720px;margin:.8rem 0 1rem}",
    )
    text = text.replace(
        ":root{--air-page-title-size:clamp(2.65rem,1.8rem + 3vw,4.5rem);--air-page-title-compact-size:clamp(2.25rem,1.65rem + 2.25vw,3.65rem);--air-page-hero-space:clamp(3.75rem,7vw,5.75rem);--air-section-space:clamp(4rem,7vw,6.5rem);--air-section-space-compact:clamp(2.75rem,5vw,4.25rem)}",
        ":root{--air-page-title-size:clamp(2.65rem,1.8rem + 3vw,4.5rem);--air-page-hero-space:clamp(3.75rem,7vw,5.75rem);--air-section-space:clamp(4rem,7vw,6.5rem);--air-section-space-compact:clamp(2.75rem,5vw,4.25rem)}",
    )
    text = text.replace(
        ".hero .page-title{font-size:var(--air-page-title-size);max-width:52rem;margin:1rem 0 1.1rem}",
        ".page-title{font-size:var(--air-page-title-size);max-width:52rem;margin:1rem 0 1.1rem}",
    )
    text = re.sub(r'\n?\.hero \.page-title--compact\{[^}]*\}', "", text)
    text = re.sub(r'\n?\.hero--patterned\{[^}]*\}', "", text)
    text = re.sub(r'\n?\.hero--plain\{[^}]*\}', "", text)
    addon_marker = "/* ---------- orientation cleanup ---------- */"
    if addon_marker not in text:
        text = text.rstrip() + '''\n\n/* ---------- orientation cleanup ---------- */
.cards--three{grid-template-columns:repeat(3,minmax(0,1fr));gap:clamp(1rem,2vw,1.5rem)}
.continuity-payload{margin-top:2rem}
@media(max-width:840px){.cards--three{grid-template-columns:1fr}}
''' + "\n"
    if text != original:
        CSS.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    changed: list[str] = []

    if manifest["chrome"]["primary_nav"] != PRIMARY_NAV:
        manifest["chrome"]["primary_nav"] = PRIMARY_NAV
        MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        changed.append("navigation.manifest.json")

    registered = [str(entry["path"]) for entry in manifest["pages"] if str(entry["path"]) != "404.html"]
    for path in registered:
        file_path = PUBLIC / path
        text = file_path.read_text(encoding="utf-8")
        original = text
        if path == "where-air-fits.html":
            text = patch_where_air_fits(text)
        for token in ("brand-field", "hero--patterned", "hero--plain"):
            text = remove_class_token_everywhere(text, token)
        text = normalize_h1(text, path)
        if text != original:
            file_path.write_text(text, encoding="utf-8")
            changed.append(f"public/{path}")

    if patch_css():
        changed.append("public/air-v2.css")

    print("changed:")
    for path in changed:
        print(f"- {path}")
    if not changed:
        print("- none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
