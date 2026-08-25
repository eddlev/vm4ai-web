#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"

errors: list[str] = []


def require(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


use_cases = (PUBLIC / "use-cases.html").read_text(encoding="utf-8")
glossary = (PUBLIC / "glossary.html").read_text(encoding="utf-8")
testing = (PUBLIC / "testing-and-evidence.html").read_text(encoding="utf-8")
css = (PUBLIC / "air-v2.css").read_text(encoding="utf-8")
manifest = json.loads((ROOT / "navigation.manifest.json").read_text(encoding="utf-8"))

# Approved edge-case block: six entries, no accidental odd card count.
require('id="edge-cases"' in use_cases, "Use Cases is missing the edge-cases section")
require(use_cases.count('class="uc edge-case"') == 6, "Use Cases must contain exactly six edge-case cards")
for title in [
    "Project rescue &amp; archaeology",
    "Cross-model relay",
    "Incident reconstruction",
    "The project that refuses one lane",
    "Decision stress-testing",
    "From knowledge to execution",
]:
    require(title in use_cases, f"Use Cases is missing edge case: {title}")

# Capability-layer ontology and Executor boundary.
require('<h3>Capability layers</h3>' in glossary, "Glossary must use the Capability layers heading")
require('<h3>Grounding layers</h3>' not in glossary, "Glossary still contains the obsolete Grounding layers heading")
require('<dt>Executor</dt>' in glossary, "Glossary is missing Executor")
for phrase in [
    "bounded non-agent callable operation",
    "does not own agency, intent, initiative, or execution authority",
    "AIR_GATE",
]:
    require(phrase in glossary, f"Executor definition is missing required boundary: {phrase}")

# Shared visual tokens/classes.
for token in [
    "--air-page-title-size",
    "--air-page-title-compact-size",
    "--air-page-hero-space",
    "--air-section-space",
    "--air-section-space-compact",
    ".hero--page",
    ".hero .page-title",
    ".section--standard",
    ".section--compact",
    ".hero--patterned",
    ".hero--plain",
]:
    require(token in css, f"air-v2.css is missing visual-system token/class: {token}")

# Testing & Evidence is the first normalized reference/evidence page.
require('class="hero hero--page hero--plain"' in testing, "Testing & Evidence must use the standard plain page hero")
require('<h1 class="page-title">Test the claim you actually want to make.</h1>' in testing, "Testing & Evidence must use the standard page-title class")
require('class="section section--standard"' in testing, "Testing & Evidence first content section must use standard section rhythm")
require('style="padding-bottom:1.5rem"' not in testing, "Testing & Evidence still has the old hero padding override")
require('font-size:clamp(2.35rem,1.7rem+2.6vw,3.7rem)' not in testing, "Testing & Evidence still has the old title-size override")
require('style="padding-top:2rem"' not in testing, "Testing & Evidence still has the old first-section padding override")

# Navigation typography/labels remain title case and unchanged by this batch.
nav = manifest["chrome"]["primary_nav"]
expected = ["How it works", "Use cases", "Where AIR fits", "Docs", "Get started", "Explore"]
actual = [item["label"] for item in nav]
require(actual == expected, f"Primary navigation labels drifted: {actual!r}")
require(all(label != label.upper() for label in actual if len(label) > 4), "Primary navigation must remain title case, not all caps")

if errors:
    print("VISUAL/CONTENT QA: FAIL")
    for error in errors:
        print(f"- {error}")
    raise SystemExit(1)

print("VISUAL/CONTENT QA: PASS")
print("- 6 edge cases")
print("- Capability layers includes Executor")
print("- Testing & Evidence normalized")
print("- visual tokens/classes present")
print("- primary navigation remains title case")
