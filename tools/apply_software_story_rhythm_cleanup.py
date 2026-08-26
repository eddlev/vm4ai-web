#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"


def replace_state(text: str, old: str, new: str, label: str) -> tuple[str, bool]:
    if old in text:
        return text.replace(old, new, 1), True
    if new in text:
        return text, False
    raise SystemExit(f"{label}: neither old nor normalized state found")


def restore_section(text: str, eyebrow: str, page: str) -> tuple[str, bool]:
    old = f'<section class="section" style="padding-top:0"><div class="container"><div class="section-head"><div class="eyebrow">{eyebrow}</div>'
    new = f'<section class="section"><div class="container"><div class="section-head"><div class="eyebrow">{eyebrow}</div>'
    return replace_state(text, old, new, f"{page}: {eyebrow}")


def patch_where(text: str) -> tuple[str, bool]:
    changed = False
    for label in ["AIR's position", "Go deeper", "Examples, not equivalence"]:
        text, did = restore_section(text, label, "where-air-fits.html")
        changed |= did
    return text, changed


def patch_development(text: str) -> tuple[str, bool]:
    changed = False
    for label in ["A typical AIR development path", "Good fit", "Probably overkill"]:
        text, did = restore_section(text, label, "air-for-development.html")
        changed |= did
    old = '<section class="section" style="padding-top:0"><div class="container"><div class="cards">'
    new = '<section class="section"><div class="container"><div class="cards">'
    text, did = replace_state(text, old, new, "air-for-development.html: bottom cards")
    changed |= did
    return text, changed


def patch_sdd(text: str) -> tuple[str, bool]:
    changed = False
    for label in ["AIR sequence", "What AIR adds", "Beyond code"]:
        text, did = restore_section(text, label, "spec-driven-development.html")
        changed |= did

    old_boundary = '<section class="section" style="padding-top:0"><div class="container"><div class="callout"><div class="label">Assurance boundary</div>'
    new_boundary = '<section class="section"><div class="container"><div class="callout"><div class="label">Assurance boundary</div>'
    text, did = replace_state(text, old_boundary, new_boundary, "spec-driven-development.html: Assurance boundary")
    changed |= did

    old_refs = '<p class="refs" style="margin-top:1rem">External category references: <a href="https://github.com/github/spec-kit" target="_blank" rel="noopener">GitHub Spec Kit</a> and <a href="https://kiro.dev/" target="_blank" rel="noopener">Kiro</a>. AIR source: <a href="https://github.com/eddlev/vm4ai-air-kit" target="_blank" rel="noopener">vm4ai-air-kit</a>.</p>'
    new_refs = '<div class="split" style="margin-top:1rem"><div class="plain"><h3>Category references</h3><p><a href="https://github.com/github/spec-kit" target="_blank" rel="noopener">GitHub Spec Kit</a> · <a href="https://kiro.dev/" target="_blank" rel="noopener">Kiro</a></p></div><div class="plain"><h3>AIR source</h3><p><a href="https://github.com/eddlev/vm4ai-air-kit" target="_blank" rel="noopener">vm4ai-air-kit</a></p></div></div>'
    text, did = replace_state(text, old_refs, new_refs, "spec-driven-development.html: reference boxes")
    changed |= did

    if '.refs{font-size:.92rem;color:var(--muted)}' in text:
        text = text.replace('.refs{font-size:.92rem;color:var(--muted)}', '', 1)
        changed = True
    return text, changed


def patch_sfv(text: str) -> tuple[str, bool]:
    changed = False
    for label in ["Core records", "Execution path", "Not code-only", "Boundaries"]:
        text, did = restore_section(text, label, "specification-first-verification.html")
        changed |= did

    pattern = re.compile(
        r'\n<section class="section" style="padding-top:0"><div class="container"><div class="callout"><div class="label">In the current AIR Kit</div>.*?</div></section>\n(?=</main>)',
        re.DOTALL,
    )
    if pattern.search(text):
        text = pattern.sub('\n', text, count=1)
        changed = True
    elif "In the current AIR Kit" in text or "AIR Kit repository" in text:
        raise SystemExit("specification-first-verification.html: current-kit block is in an unexpected state")
    return text, changed


PATCHES = {
    "where-air-fits.html": patch_where,
    "air-for-development.html": patch_development,
    "spec-driven-development.html": patch_sdd,
    "specification-first-verification.html": patch_sfv,
}


def validate_file(name: str, text: str) -> list[str]:
    errors: list[str] = []
    required_labels = {
        "where-air-fits.html": ["AIR's position", "Go deeper", "Examples, not equivalence"],
        "air-for-development.html": ["A typical AIR development path", "Good fit", "Probably overkill"],
        "spec-driven-development.html": ["AIR sequence", "What AIR adds", "Beyond code"],
        "specification-first-verification.html": ["Core records", "Execution path", "Not code-only", "Boundaries"],
    }[name]
    for label in required_labels:
        bad = f'<section class="section" style="padding-top:0"><div class="container"><div class="section-head"><div class="eyebrow">{label}</div>'
        good = f'<section class="section"><div class="container"><div class="section-head"><div class="eyebrow">{label}</div>'
        if bad in text or good not in text:
            errors.append(f"{name}: {label} is not on canonical section padding")

    if name == "air-for-development.html":
        if '<section class="section"><div class="container"><div class="cards">' not in text:
            errors.append(f"{name}: bottom cards do not have canonical section padding")
    elif name == "spec-driven-development.html":
        if '<section class="section"><div class="container"><div class="callout"><div class="label">Assurance boundary</div>' not in text:
            errors.append(f"{name}: Assurance boundary does not have canonical section padding")
        for marker in ["Category references", "AIR source", "GitHub Spec Kit", "Kiro", "vm4ai-air-kit"]:
            if marker not in text:
                errors.append(f"{name}: missing reference-box marker {marker}")
        if 'class="refs"' in text or "External category references:" in text:
            errors.append(f"{name}: loose reference line remains")
    elif name == "specification-first-verification.html":
        for forbidden in ["In the current AIR Kit", "AIR Kit repository"]:
            if forbidden in text:
                errors.append(f"{name}: removed current-kit/source content remains: {forbidden}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.write == args.check:
        raise SystemExit("choose exactly one of --write or --check")

    changed_files: list[str] = []
    all_errors: list[str] = []
    for name, patch in PATCHES.items():
        path = PUBLIC / name
        current = path.read_text(encoding="utf-8")
        normalized, changed = patch(current)
        if args.write and changed:
            path.write_text(normalized, encoding="utf-8")
            changed_files.append(name)
        check_text = normalized if args.write else current
        all_errors.extend(validate_file(name, check_text))

    if all_errors:
        for error in all_errors:
            print(f"- {error}")
        return 1

    if args.check:
        print("software-story rhythm validation: PASS (4 pages)")
    else:
        print(f"software-story rhythm cleanup: {len(changed_files)} page(s) changed")
        for name in changed_files:
            print(f"- {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
