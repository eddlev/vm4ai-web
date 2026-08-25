#!/usr/bin/env python3
"""Apply and verify the approved AIR website positioning update.

The script is intentionally narrow and idempotent. It updates only the public
surfaces approved for the SDD/category-positioning work and fails if expected
anchors disappear instead of guessing around changed site structure.
"""
from __future__ import annotations

import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if new in text:
        return
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one replacement anchor, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def insert_before_once(path: Path, marker: str, addition: str, sentinel: str) -> None:
    text = path.read_text(encoding="utf-8")
    if sentinel in text:
        return
    count = text.count(marker)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one insertion anchor, found {count}")
    path.write_text(text.replace(marker, addition + marker, 1), encoding="utf-8")


def where_air_fits_page() -> str:
    return '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Where AIR fits — SDD, agents and governed execution</title>
<meta name="description" content="Where AIR fits relative to raw AI chat, spec-driven development, coding-agent environments and autonomous agent runtimes — and why AIR is a governed project runtime rather than another agent layer.">
<meta name="theme-color" content="#1A1613">
<link rel="icon" type="image/svg+xml" href="favicon.svg">
<link rel="icon" href="/favicon.ico" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="canonical" href="https://vm4ai.com/where-air-fits.html">
<meta property="og:type" content="website">
<meta property="og:site_name" content="AIR by VM4AI">
<meta property="og:title" content="Where AIR fits — AIR by VM4AI">
<meta property="og:description" content="SDD, coding agents, agent runtimes and governed execution occupy different layers. See where AIR sits.">
<meta property="og:url" content="https://vm4ai.com/where-air-fits.html">
<meta property="og:image" content="https://vm4ai.com/og-image.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="Where AIR fits — AIR by VM4AI">
<meta name="twitter:description" content="SDD, coding agents, agent runtimes and governed execution occupy different layers. See where AIR sits.">
<meta name="twitter:image" content="https://vm4ai.com/og-image.png">
<link rel="stylesheet" href="air-v2.css">
<style>
.landscape{display:grid;gap:1rem}.land-row{display:grid;grid-template-columns:1.05fr 1.45fr 1.45fr;gap:1rem;padding:1.15rem 1.2rem;border:1px solid var(--border);border-radius:14px;background:var(--surface)}
.land-row strong{font-weight:600}.land-row span{color:var(--muted)}.land-head{background:transparent;border-style:dashed;font-family:var(--font-mono);font-size:.75rem;letter-spacing:.06em;text-transform:uppercase;color:var(--subtle)}
.axis-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}.axis-card{border:1px solid var(--border);border-radius:16px;padding:1.4rem;background:var(--surface)}.axis-card.air{border-color:var(--brass);background:color-mix(in srgb,var(--brass) 7%,var(--surface))}.axis-card .k{font-family:var(--font-mono);font-size:.72rem;letter-spacing:.08em;text-transform:uppercase;color:var(--brass)}.axis-card p{color:var(--muted);margin:.55rem 0 0}
.source-note{font-size:.9rem;color:var(--muted)}
@media(max-width:760px){.land-row{grid-template-columns:1fr}.land-head{display:none}.axis-grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<header class="site-header"><div class="container nav-row"><a class="brand" href="index.html"><svg class="mark air-eye" viewBox="0 0 64 64" aria-hidden="true"><rect x="9.5" y="9.5" width="45" height="45" rx="13" stroke-width="5"/><circle class="air-pupil" cx="32" cy="32" r="8.5"/></svg>AIR <span class="by">by VM4AI</span></a><nav class="nav" id="nav" aria-label="Primary"><a href="how-it-works.html">How it works</a><a href="air-docs.html">Docs</a><a href="get-started.html">Get started</a><a href="use-cases.html">Use cases</a><a href="about.html">About</a><a href="blog.html">Blog</a></nav><div class="nav-actions"><a class="btn" href="https://github.com/eddlev/vm4ai-air-kit" target="_blank" rel="noopener"><span class="github-label">GitHub</span></a><button class="icon-btn" data-theme-toggle aria-label="Toggle light or dark theme"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg></button><button class="icon-btn menu-btn" data-menu-toggle aria-label="Open menu"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 6h18M3 12h18M3 18h18"/></svg></button></div></div></header>
<main>
<section class="hero brand-field"><div class="container"><div class="eyebrow">The landscape</div><h1>Where AIR fits.</h1><p class="sub">Spec-driven development, coding agents, autonomous agent runtimes, and governed AI work solve overlapping problems at different layers. AIR is not trying to collapse them into one category.</p><div class="hero-cta"><a class="btn btn-primary" href="how-it-works.html#spec-driven">See AIR's execution model</a><a class="btn" href="get-started.html">Try AIR</a></div></div></section>
<section class="section"><div class="container"><div class="section-head"><div class="eyebrow">Different layers</div><h2>Similar words. Different jobs.</h2><p>These are architectural categories, not a feature-scoreboard. Individual products can span more than one row.</p></div><div class="landscape"><div class="land-row land-head"><strong>Category</strong><span>Primary job</span><span>Typical execution model</span></div><div class="land-row"><strong>Raw AI chat</strong><span>General interaction and one-session assistance.</span><span>Conversational model behavior with state largely carried in the current context.</span></div><div class="land-row"><strong>SDD harness</strong><span>Turn a software specification into an implementation workflow.</span><span>Structured spec, plan and task artifacts consumed by a coding agent or development environment.</span></div><div class="land-row"><strong>Agentic engineering environment</strong><span>Build and modify software through increasingly autonomous execution.</span><span>One or more coding agents use tools, repositories, tests, permissions and development-state machinery.</span></div><div class="land-row"><strong>Agent runtime</strong><span>Sustain long-horizon work, tool use, delegation and recovery.</span><span>Stateful agent loops, often with coordinators or parallel sub-agents.</span></div><div class="land-row" style="border-color:var(--brass)"><strong>AIR</strong><span>Govern sustained AI work: task state, specification, evidence, approvals, review and continuity.</span><span>One bound active task supplies execution authority; non-agent capability layers shape work inside that contract.</span></div></div></div></section>
<section class="section" style="padding-top:0"><div class="container"><div class="section-head"><div class="eyebrow">AIR's position</div><h2>Governed execution without requiring autonomous agency.</h2><p>AIR can structure work performed by a capable host model without turning capability layers into independent agents.</p></div><div class="axis-grid"><div class="axis-card"><div class="k">Specification</div><h3>Define what must be true</h3><p>For software, behavior and verification are specified before material implementation where the task requires it. Other domains use the verification abstraction that fits the work.</p></div><div class="axis-card"><div class="k">Authority</div><h3>Keep one execution center</h3><p>The bound Orbit 0 artifact is the sole positive execution authority. Specialists, methods and executors do not inherit project authority merely because they are available.</p></div><div class="axis-card"><div class="k">Evidence</div><h3>Keep claims proportional</h3><p>AIR distinguishes declared prompt-layer state from source, tool, operator and backend evidence. Passing a conversational checkpoint is not treated as proof of an external event.</p></div><div class="axis-card air"><div class="k">Continuity</div><h3>Carry governed state forward</h3><p>Handoff serializes explicit project state for validation and rebinding in another compatible session instead of relying on hidden memory or transcript reconstruction.</p></div></div></div></section>
<section class="section" style="padding-top:0"><div class="container"><div class="section-head"><div class="eyebrow">Software</div><h2>SDD is a native fit — not AIR's whole category.</h2><p>For behavior-bearing development work, AIR's sequence is specification-first: resolve intent, define observable behavior and planned verification, test specification adequacy, generate under the active contract, execute verification, and reconcile the result back to the original intent. AIR applies the same discipline beyond code using domain-appropriate evidence and verification.</p></div><div class="callout"><div class="label">A useful shorthand</div><p><strong>AIR for software:</strong> spec-driven development. <strong>AIR as a system:</strong> specification-driven governed execution for sustained professional AI work.</p></div></div></section>
<section class="section" style="padding-top:0"><div class="container"><div class="section-head"><div class="eyebrow">Examples, not equivalence</div><h2>Products can overlap these layers.</h2><p>The examples below are useful reference points, not claims that the products are interchangeable or directly benchmark-comparable.</p></div><div class="cards"><a class="card" href="https://github.com/github/spec-kit" target="_blank" rel="noopener"><div class="k">SDD harness</div><h3>GitHub Spec Kit</h3><p>A specification-driven software-development harness built around structured development artifacts and coding-agent execution.</p><span class="go">Primary source →</span></a><a class="card" href="https://kiro.dev/" target="_blank" rel="noopener"><div class="k">Agentic engineering</div><h3>Kiro</h3><p>An agentic engineering environment that turns specifications into requirements, design, tasks and implementation.</p><span class="go">Primary source →</span></a><a class="card" href="https://github.com/ApodexAI/FrontierAgent" target="_blank" rel="noopener"><div class="k">Agent runtime</div><h3>FrontierAgent</h3><p>A stateful agent runtime with coordinator, task-board, sandbox, approvals, recovery and bounded sub-agent execution.</p><span class="go">Primary source →</span></a><a class="card" href="https://github.com/eddlev/vm4ai-air-kit" target="_blank" rel="noopener"><div class="k">Governed project runtime</div><h3>AIR</h3><p>A prompt-based project runtime centered on one bound active task, explicit governance records, evidence boundaries and portable Handoff state.</p><span class="go">Inspect AIR →</span></a></div><p class="source-note" style="margin-top:1.2rem">Category descriptions are intentionally conservative. They describe publicly documented architecture and positioning, not independent performance rankings.</p></div></section>
<section class="section" style="padding-top:0"><div class="container"><div class="cta-band"><h2>Use the layer you actually need.</h2><p>If the problem is sustained AI work that must stay scoped, reviewable and portable, AIR supplies the governing project layer without requiring a new chat workspace or autonomous-agent stack.</p><div class="hero-cta" style="justify-content:center"><a class="btn btn-primary" href="get-started.html">Try AIR</a><a class="btn" href="use-cases.html">See use cases</a></div></div></div></section>
</main>
<footer class="site-footer"><div class="container"><div class="foot-grid"><div class="foot-brand"><a class="brand" href="index.html"><svg class="mark" viewBox="0 0 64 64" aria-hidden="true"><rect x="9.5" y="9.5" width="45" height="45" rx="13" stroke-width="5"/><circle cx="32" cy="32" r="8.5"/></svg> AIR <span class="by">by VM4AI</span></a><p>AI work, carried forward. A prompt-based framework for focused work, structured continuity and compatible-platform handoff.</p></div><div class="foot-col"><h4>Product</h4><a href="how-it-works.html">How it works</a><a href="air-docs.html">Documentation</a><a href="get-started.html">Get started</a><a href="use-cases.html">Use cases</a><a href="where-air-fits.html">Where AIR fits</a><a href="blog.html">Blog</a><a href="glossary.html">Glossary</a></div><div class="foot-col"><h4>More</h4><a href="about.html">About</a><a href="services.html">Services</a><a href="https://github.com/eddlev/air-brand" target="_blank" rel="noopener">Brand kit</a></div><div class="foot-col"><h4>Connect</h4><a href="https://github.com/eddlev/vm4ai-air-kit" target="_blank" rel="noopener">GitHub</a><a href="https://github.com/sponsors/eddlev" target="_blank" rel="noopener">Sponsor</a><a href="https://github.com/eddlev/vm4ai-air-kit/discussions" target="_blank" rel="noopener">Support</a></div></div><div class="foot-bottom"><span>© 2026 VM4AI · Apache-2.0 (code) · <a class="legal" href="privacy.html">Privacy</a> · <a class="legal" href="terms.html">Terms</a></span><a class="made" href="made-with-air.html"><svg class="mark" viewBox="0 0 64 64" aria-hidden="true"><rect x="9.5" y="9.5" width="45" height="45" rx="13" stroke-width="5"/><circle cx="32" cy="32" r="8.5"/></svg> Made with AIR</a></div></div></footer>
<script src="air-v2.js"></script>
</body>
</html>'''


def apply_patch() -> None:
    how = PUBLIC / "how-it-works.html"
    use = PUBLIC / "use-cases.html"
    glossary = PUBLIC / "glossary.html"
    index = PUBLIC / "index.html"

    how_marker = '''  <section class="section" style="padding-top:0">\n    <div class="container">\n      <div class="section-head">\n        <span class="eyebrow">Evidence</span>'''
    how_addition = '''  <section class="section" id="spec-driven" style="padding-top:0">\n    <div class="container">\n      <div class="section-head">\n        <span class="eyebrow">Spec-driven development</span>\n        <h2>Spec-driven for software. Governed execution beyond it.</h2>\n        <p>For behavior-bearing software work, AIR defines intended observable behavior and planned verification before code generation, then asks whether the planned verification could all pass while the intended behavior is still materially wrong.</p>\n      </div>\n      <div class="cards">\n        <div class="card"><div class="k">01 · Specify behavior</div><h3>Define the observable result</h3><p>The behavior specification states what the implementation must do without unnecessarily choosing its private internal structure.</p></div>\n        <div class="card"><div class="k">02 · Design verification</div><h3>Plan how the claim will be checked</h3><p>The verification specification defines the acceptance, invariant, unit, integration, regression, security, fixture, property, or other checks that fit the work.</p></div>\n        <div class="card"><div class="k">03 · Test adequacy</div><h3>Ask whether the spec can miss the point</h3><p>AIR checks whether every planned verification could pass while a material part of the intended behavior is still wrong. If so, implementation stays review-gated.</p></div>\n        <div class="card"><div class="k">04 · Execute + reconcile</div><h3>Build under the contract, then return to intent</h3><p>After implementation and verification, AIR reconciles observed behavior back to the original intent, behavior specification, and current acceptance criteria.</p></div>\n      </div>\n      <div class="callout" style="margin-top:1.2rem"><div class="label">AIR is broader than SDD</div><p>Software uses behavior and verification specifications. Research can use source quality and triangulation; analysis can use scenarios, criteria and counterexamples; documents can use requirements and source fidelity; design can use user-visible outcomes and human evaluation. <a href="where-air-fits.html">See where AIR fits →</a></p></div>\n    </div>\n  </section>\n\n'''
    insert_before_once(how, how_marker, how_addition, 'id="spec-driven"')

    old_dev = '''          <p>Research, build, debug, and review against a roadmap instead of a vibe. AIR scopes the work, executes one active step at a time, and keeps the contract visible — so generated code is traceable, not mysterious.</p>\n          <ul><li>roadmap-first execution</li><li>active-step artifacts</li><li>gates before delivery</li></ul>'''
    new_dev = '''          <p>Research, design, build, debug, and review against an explicit specification instead of a vibe. For behavior-bearing changes, AIR defines intended behavior and verification before code generation, checks whether the verification is adequate, then executes and reconciles the result back to the original intent.</p>\n          <ul><li>specification before implementation</li><li>verification designed up front</li><li>adequacy + delivery gates</li></ul>'''
    replace_once(use, old_dev, new_dev)

    gloss_marker = '''      <div class="defgroup">\n        <h3>Onboarding — the Q-codes</h3>'''
    gloss_addition = '''      <div class="defgroup">\n        <h3>Specification-driven work</h3>\n        <dl class="deflist gloss">\n          <div class="row"><dt>Spec-Driven Development (SDD)</dt><dd>A software-development approach where an explicit specification defines what should be built before material implementation, and implementation is checked against that specification. AIR supports SDD natively for software work without reducing the whole framework to a coding-only workflow.</dd></div>\n          <div class="row"><dt>Specification-First Verification (SFV)</dt><dd>AIR's proportional discipline for defining what outcome is intended and what evidence would justify saying it succeeded before material execution. Coding can use a dedicated SFV Method Pack, but the underlying verification discipline also applies outside software.</dd></div>\n          <div class="row"><dt><code>behavior_specification</code></dt><dd>For behavior-bearing coding work, the intended observable or contractual result that implementation must satisfy, without unnecessarily choosing private implementation details.</dd></div>\n          <div class="row"><dt><code>verification_specification</code></dt><dd>The planned observations, tests, source comparisons, evaluations, or reviews — plus expected results and evidence classes — that will be used to judge whether the intended outcome was achieved.</dd></div>\n          <div class="row"><dt><code>specification_adequacy_state</code></dt><dd>The gate that asks a hard question before execution: could all planned verification pass while the thing AIR and the user actually intend is still materially wrong?</dd></div>\n        </dl>\n      </div>\n\n'''
    insert_before_once(glossary, gloss_marker, gloss_addition, 'Spec-Driven Development (SDD)')

    index_old = '''<a class="card" href="about.html#principles"><div class="k">Trust</div><h3>Principles</h3><p>Prompt-compiled, evidence-aware, human judgment kept in the loop.</p><span class="go">Read the stance →</span></a></div></div></section>'''
    index_new = '''<a class="card" href="about.html#principles"><div class="k">Trust</div><h3>Principles</h3><p>Prompt-compiled, evidence-aware, human judgment kept in the loop.</p><span class="go">Read the stance →</span></a></div><p style="margin:1.2rem 0 0;font-family:var(--font-mono);font-size:.84rem"><a href="where-air-fits.html">Where AIR fits → SDD, coding agents, agent runtimes, and governed execution</a></p></div></section>'''
    replace_once(index, index_old, index_new)

    page = PUBLIC / "where-air-fits.html"
    desired = where_air_fits_page()
    if not page.exists() or page.read_text(encoding="utf-8") != desired:
        page.write_text(desired, encoding="utf-8")


def check_contract() -> None:
    how = (PUBLIC / "how-it-works.html").read_text(encoding="utf-8")
    use = (PUBLIC / "use-cases.html").read_text(encoding="utf-8")
    glossary = (PUBLIC / "glossary.html").read_text(encoding="utf-8")
    started = (PUBLIC / "get-started.html").read_text(encoding="utf-8")
    index = (PUBLIC / "index.html").read_text(encoding="utf-8")

    required = {
        "how-it-works SDD section": 'id="spec-driven"' in how,
        "use-cases specification language": "specification before implementation" in use,
        "glossary SDD definition": "Spec-Driven Development (SDD)" in glossary,
        "where-air-fits page": (PUBLIC / "where-air-fits.html").exists(),
        "homepage discovery link": "Where AIR fits → SDD" in index,
        "canonical modifier 1": "air -o on" in glossary,
        "canonical modifier 2": "air -o -min" in glossary,
        "canonical modifier 3": "air -t on" in glossary,
        "canonical modifier 4": "air -t off" in glossary,
        "no universal 200k requirement": "200k" not in started.lower(),
        "handoff revalidation language": "validates and rebinds" in started,
        "hidden reasoning boundary": "not hidden chain-of-thought" in started,
    }
    failed = [name for name, ok in required.items() if not ok]
    if failed:
        raise SystemExit("AIR public contract check failed: " + "; ".join(failed))

    forbidden_modifiers = ["air status", "air object off", "air quiet", "air immersive", "air lanes", "air patch"]
    joined = "\n".join([glossary, started, how])
    found = [term for term in forbidden_modifiers if term in joined.lower()]
    if found:
        raise SystemExit("Legacy modifier language found in current reference surfaces: " + ", ".join(found))

    print("AIR public contract check: PASS")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="apply the approved positioning patch")
    parser.add_argument("--check", action="store_true", help="validate the resulting public contract")
    args = parser.parse_args()
    if not args.apply and not args.check:
        parser.error("choose --apply and/or --check")
    if args.apply:
        apply_patch()
    if args.check:
        check_contract()


if __name__ == "__main__":
    main()
