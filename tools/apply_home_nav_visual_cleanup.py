#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "navigation.manifest.json"
PUBLIC = ROOT / "public"
CSS = PUBLIC / "air-v2.css"

ORIENTATION = {
    "how-it-works.html",
    "where-air-fits.html",
    "explore-air.html",
    "get-started.html",
}

PRIMARY_NAV = [
    {"path": "how-it-works.html", "label": "How it works"},
    {"path": "where-air-fits.html", "label": "Where AIR fits"},
    {"path": "explore-air.html", "label": "Explore"},
    {"path": "get-started.html", "label": "Get started"},
]

CLASS_ATTR_RE = re.compile(r'class="([^"]*)"')
H1_RE = re.compile(r'<h1\b([^>]*)>', re.IGNORECASE)
HERO_SECTION_RE = re.compile(
    r'<section\b[^>]*class="[^"]*\bhero\b[^"]*"[^>]*>', re.IGNORECASE
)
MAIN_RE = re.compile(r'<main>.*?</main>', re.IGNORECASE | re.DOTALL)


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
        if declarations:
            replacement = ' style="' + ";".join(declarations) + '"'
        else:
            replacement = ""
        tag = tag[: style_match.start()] + replacement + tag[style_match.end() :]
    return text[: match.start()] + tag + text[match.end() :]


def normalize_hero(text: str, path: str, patterned: bool) -> str:
    matches = list(HERO_SECTION_RE.finditer(text))
    if len(matches) != 1:
        raise SystemExit(f"{path}: expected exactly one hero section, found {len(matches)}")
    match = matches[0]
    tag = match.group(0)
    add = {"hero--patterned" if patterned else "hero--plain"}
    remove = {"hero--plain", "hero--patterned", "brand-field"}
    tag = update_class_attr(tag, add=add, remove=remove)
    return text[: match.start()] + tag + text[match.end() :]


def compact_homepage_main(text: str) -> str:
    matches = list(MAIN_RE.finditer(text))
    if len(matches) != 1:
        raise SystemExit(f"index.html: expected exactly one main element, found {len(matches)}")
    marker = "Structure helps. Evidence still matters."
    if marker in text:
        return text
    main = '''<main>
<section class="hero hero--plain"><div class="container hero-grid"><div><div class="eyebrow">AIR · AI Resource</div><h1 class="page-title">AI work, carried forward.</h1><p class="sub">Continue complex projects across sessions and compatible platforms — without rebuilding the work every time.</p><div class="hero-cta"><a class="btn btn-primary" href="get-started.html">Try AIR</a><a class="btn" href="how-it-works.html">See how it works</a></div><p class="hero-note">Prompt-based framework · host-model governed · compatibility depends on the platform</p></div><div class="hero-art" aria-label="Focused, Fluid and AIR visual system"><div class="hero-art-head"><span>ONE PROJECT</span><span>THREE STATES</span></div><div class="mini-triad"><div class="mini-state"><h3>Focused</h3><div class="mini-v"><div class="task-track"><span class="task-node left"></span><span class="task-node mid"></span><span class="task-node right"></span></div></div></div><div class="mini-state"><h3>Fluid</h3><div class="mini-v"><div class="fluid-mini"><div class="fluid-box alt"><span></span></div><div class="fluid-box"><span></span></div><div class="fluid-box alt"><span></span></div></div></div></div><div class="mini-state"><h3>AIR</h3><div class="mini-v"><div class="air-mini"><div class="project-node past"><span></span></div><b class="arrow">→</b><div class="project-node middle"><span></span></div><b class="arrow">→</b><div class="project-node"><span></span></div></div></div></div></div></div></div></section>
<section class="section"><div class="container"><div class="section-head"><div class="eyebrow">The problem</div><h2>Your project shouldn’t reset with the session.</h2><p>Long AI work creates an ugly choice: stay in an increasingly noisy session, or start fresh and spend time reconstructing work you already did.</p></div><div class="compare-grid"><div class="panel"><div class="panel-label">Without AIR</div><div class="rows"><div class="row"><span class="bullet"></span><span>Long sessions accumulate noise.</span></div><div class="row"><span class="bullet"></span><span>A fresh session means another briefing.</span></div><div class="row"><span class="bullet"></span><span>Decisions disappear into session history.</span></div><div class="row"><span class="bullet"></span><span>Changing platforms breaks continuity.</span></div></div></div><div class="panel air"><div class="panel-label">With AIR</div><div class="rows"><div class="row active"><span class="bullet"></span><span>One active task stays centered.</span></div><div class="row"><span class="bullet"></span><span>Structured handoff captures the current state.</span></div><div class="row"><span class="bullet"></span><span>A new session continues from that state.</span></div><div class="row"><span class="bullet"></span><span>The project can move to another compatible platform.</span></div></div></div></div></div></section>
<section class="section"><div class="container"><div class="section-head"><div class="eyebrow">The AIR system</div><h2>Focused. Fluid. AIR.</h2><p>The same project viewed at three levels: the active task, the continuation point, and the project that persists across sessions and compatible platforms.</p></div><div class="state-grid"><article class="state-card"><h3>Focused</h3><p class="sub">One active task at a time.</p><div class="state-visual"><div class="focused-large"><span class="big-task left"></span><span class="big-task active"></span><span class="big-task right"></span></div></div><p class="state-caption">Focus on one task.</p></article><article class="state-card"><h3>Fluid</h3><p class="sub">Continue, don’t reconstruct.</p><div class="state-visual"><div class="fluid-large"><div class="session-option alt"><span class="state-mark"></span><span>New Session</span></div><div class="session-option"><span class="state-mark"></span><span>Current Session</span></div><div class="session-option alt"><span class="state-mark"></span><span>New Platform</span></div><span class="branch"></span><span class="branch-stem"></span></div></div><p class="state-caption">same project state continues</p></article><article class="state-card"><h3>AIR</h3><p class="sub">Stable across sessions and platforms.</p><div class="state-visual"><div class="air-large"><div class="air-project p1"><span class="state-mark"></span></div><b class="arrow">→</b><div class="air-project p2"><span class="state-mark"></span></div><b class="arrow">→</b><div class="air-project"><span class="state-mark"></span></div></div></div><p class="state-caption">same AIR project persists</p></article></div><div class="state-rule">The container can change. The work keeps its state.</div></div></section>
<section class="section"><div class="container"><div class="section-head"><div class="eyebrow">Continuity</div><h2>Work. Handoff. Continue.</h2><p>AIR carries the explicit working state needed to continue the project instead of asking the next session to reconstruct it from a buried transcript.</p></div><div class="flow"><div class="flow-step"><div class="n">01</div><h3>Work</h3><p>Keep the active task, constraints, decisions and evidence explicit while the project moves forward.</p></div><div class="flow-step"><div class="n">02</div><h3>Handoff</h3><p>Capture the current project state when the session needs to end or the work needs to move.</p></div><div class="flow-step"><div class="n">03</div><h3>Continue</h3><p>Load that state in a new session or compatible platform and resume from the project’s recorded position.</p></div></div><div class="payload continuity-payload"><div><b>Active task</b><span>What is being worked on now.</span></div><div><b>Decisions</b><span>What has already been settled.</span></div><div><b>Constraints</b><span>What the work must respect.</span></div><div><b>Evidence</b><span>What supports the current direction.</span></div><div><b>Approvals</b><span>What the user has authorized.</span></div><div><b>Next step</b><span>Where execution resumes.</span></div></div></div></section>
<section class="section"><div class="container"><div class="section-head"><div class="eyebrow">Trust &amp; boundaries</div><h2>Structure helps. Evidence still matters.</h2><p>AIR is prompt-based and host-model governed. It makes scope, continuity and review boundaries visible, but it does not turn prompt records into independent proof of external events.</p></div><div class="two-grid"><div class="callout"><div class="label">Keep the claim proportional</div><p>Use AIR’s visible records to inspect the working contract. Use the relevant source, tool, test, operator or backend evidence for claims about the world outside the prompt runtime.</p></div><div class="panel"><div class="rows"><div class="row active"><span class="bullet"></span><span>Prompt-based framework, not hidden backend enforcement.</span></div><div class="row"><span class="bullet"></span><span>Host capability and compatibility still matter.</span></div><div class="row"><span class="bullet"></span><span>External claims still require external evidence.</span></div></div><div style="margin-top:1.2rem"><a class="btn" href="testing-and-evidence.html">Testing &amp; Evidence</a></div></div></div></div></section>
<section class="section"><div class="container"><div class="cta-band"><h2>Pick up the project. Not the briefing.</h2><p>Use AIR to carry structured project state into the next session or compatible platform.</p><div class="hero-cta" style="justify-content:center"><a class="btn btn-primary" href="get-started.html">Try AIR</a><a class="btn" href="explore-air.html">Explore AIR</a></div></div></div></section>
</main>'''
    return text[: matches[0].start()] + main + text[matches[0].end() :]


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
        if path == "index.html":
            text = compact_homepage_main(text)
        if path == "where-air-fits.html":
            text = patch_where_air_fits(text)
        text = remove_class_token_everywhere(text, "brand-field")
        text = normalize_h1(text, path)
        text = normalize_hero(text, path, patterned=path in ORIENTATION)
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
