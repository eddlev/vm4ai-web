#!/usr/bin/env python3
"""Render contextual parent links for vm4ai.com secondary/deep pages.

Parent relationships live in navigation.manifest.json under `context_back`.
The deployed site remains static HTML. This renderer is idempotent and fails
closed when a mapped page cannot accept the canonical back-link placement.
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

BLOCK_RE = re.compile(
    r"<!-- CONTEXT_BACK_START -->.*?<!-- CONTEXT_BACK_END -->",
    re.IGNORECASE | re.DOTALL,
)
LEGACY_BACKLINK_RE = re.compile(
    r"\s*<a\b[^>]*class=[\"'][^\"']*\bbacklink\b[^\"']*[\"'][^>]*>.*?</a>\s*",
    re.IGNORECASE | re.DOTALL,
)
HERO_CONTAINER_RE = re.compile(
    r"(<section\b[^>]*class=[\"'][^\"']*\bhero\b[^\"']*[\"'][^>]*>\s*"
    r"<div\b[^>]*class=[\"'][^\"']*\bcontainer\b[^\"']*[\"'][^>]*>)",
    re.IGNORECASE | re.DOTALL,
)
ARTICLE_RE = re.compile(
    r"(<article\b[^>]*class=[\"'][^\"']*\barticle\b[^\"']*[\"'][^>]*>)",
    re.IGNORECASE | re.DOTALL,
)
SECTION_CONTAINER_RE = re.compile(
    r"(<main\b[^>]*>\s*<section\b[^>]*>\s*"
    r"<div\b[^>]*class=[\"'][^\"']*\bcontainer\b[^\"']*[\"'][^>]*>)",
    re.IGNORECASE | re.DOTALL,
)

OLD_ASSURANCE = "Governed does not mean magically guaranteed."
NEW_ASSURANCE = "Governed does not mean guaranteed."


def load_manifest() -> dict:
    with MANIFEST.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def validate_parent_map(manifest: dict) -> tuple[dict[str, str], dict[str, str]]:
    pages = manifest.get("pages")
    if not isinstance(pages, list):
        raise RuntimeError("navigation.manifest.json must contain a pages list")
    labels = {str(entry["path"]): str(entry["label"]) for entry in pages}
    parents = manifest.get("context_back", {})
    if not isinstance(parents, dict):
        raise RuntimeError("navigation.manifest.json context_back must be an object")

    clean: dict[str, str] = {}
    for child, parent in parents.items():
        child = str(child)
        parent = str(parent)
        if child not in labels:
            raise RuntimeError(f"context_back child is not registered: {child}")
        if parent not in labels:
            raise RuntimeError(f"context_back parent is not registered: {parent}")
        if child == parent:
            raise RuntimeError(f"context_back self-parent is invalid: {child}")
        clean[child] = parent

    for start in clean:
        seen: set[str] = set()
        current = start
        while current in clean:
            if current in seen:
                raise RuntimeError(f"context_back cycle detected from {start}")
            seen.add(current)
            current = clean[current]

    return clean, labels


def back_block(parent: str, label: str) -> str:
    return (
        "<!-- CONTEXT_BACK_START -->\n"
        f'<a class="context-back" href="{html.escape(parent, quote=True)}">'
        f'← {html.escape(label)}</a>\n'
        "<!-- CONTEXT_BACK_END -->"
    )


def insert_block(source: str, block: str, path: str) -> str:
    for pattern in (HERO_CONTAINER_RE, ARTICLE_RE, SECTION_CONTAINER_RE):
        match = pattern.search(source)
        if match:
            return source[: match.end()] + "\n" + block + "\n" + source[match.end() :]
    raise RuntimeError(f"{path}: no supported contextual-back insertion point found")


def transform(source: str, path: str, parents: dict[str, str], labels: dict[str, str]) -> str:
    rendered = source
    blocks = list(BLOCK_RE.finditer(rendered))
    if len(blocks) > 1:
        raise RuntimeError(f"{path}: expected at most one contextual back block, found {len(blocks)}")

    if path in parents:
        rendered = LEGACY_BACKLINK_RE.sub("\n", rendered)
        parent = parents[path]
        canonical = back_block(parent, labels[parent])
        if blocks:
            rendered = BLOCK_RE.sub(canonical, rendered, count=1)
        else:
            rendered = insert_block(rendered, canonical, path)
    elif blocks:
        rendered = BLOCK_RE.sub("", rendered, count=1)

    if path == "how-it-works.html":
        if OLD_ASSURANCE in rendered:
            rendered = rendered.replace(OLD_ASSURANCE, NEW_ASSURANCE, 1)
        elif NEW_ASSURANCE not in rendered:
            raise RuntimeError("how-it-works.html: assurance heading not found")

    expected = 1 if path in parents else 0
    actual = rendered.count("<!-- CONTEXT_BACK_START -->")
    if actual != expected:
        raise RuntimeError(f"{path}: expected {expected} contextual back block(s), found {actual}")
    return rendered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()

    manifest = load_manifest()
    parents, labels = validate_parent_map(manifest)
    public = ROOT / manifest["site"]["public_root"]

    changed: list[str] = []
    for entry in manifest["pages"]:
        path = str(entry["path"])
        file_path = public / path
        if not file_path.is_file():
            raise RuntimeError(f"registered page missing: {path}")
        source = file_path.read_text(encoding="utf-8")
        rendered = transform(source, path, parents, labels)
        if rendered != source:
            changed.append(path)
            if args.write:
                file_path.write_text(rendered, encoding="utf-8")

    if args.check and changed:
        print("contextual navigation is stale on:")
        for path in changed:
            print(f"- {path}")
        return 1

    if args.write:
        print(f"contextual navigation rendered: {len(changed)} page(s) changed")
    else:
        print(f"contextual navigation check: PASS ({len(parents)} mapped page(s))")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"contextual navigation render failed: {exc}", file=sys.stderr)
        sys.exit(1)
