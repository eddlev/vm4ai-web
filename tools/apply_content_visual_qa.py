#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def replace_once(path: Path, old: str, new: str, marker: str) -> bool:
    text = path.read_text(encoding="utf-8")
    if marker in text:
        return False
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one source marker, found {count}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return True


def patch_use_cases() -> bool:
    path = ROOT / "public" / "use-cases.html"
    old = '''      <p class="uc-more">The same structure extends to strategy, operations, and execution. AIR is domain-agnostic by design.</p>
    </div>
  </section>

  <section class="section" style="padding-top:0">'''
    edge = '''      <p class="uc-more">The same structure extends to strategy, operations, and execution. AIR is domain-agnostic by design.</p>
    </div>
  </section>

  <section class="section" id="edge-cases">
    <div class="container">
      <div class="section-head">
        <span class="eyebrow">Edge cases</span>
        <h2>Less obvious uses.</h2>
        <p>AIR becomes especially useful when continuity, evidence, authority, or capability boundaries are harder than the task label itself.</p>
      </div>
      <div class="uc-grid">
        <div class="uc edge-case">
          <div class="k">Rescue</div>
          <h3>Project rescue &amp; archaeology</h3>
          <p>Take over work with conflicting notes, abandoned decisions, partial outputs, or no trustworthy current state. AIR can separate what is still active from what is stale, rebuild an explicit task center, and continue from a bounded current contract.</p>
          <ul><li>state reconstruction</li><li>stale-vs-current separation</li><li>one renewed task center</li></ul>
        </div>
        <div class="uc edge-case">
          <div class="k">Relay</div>
          <h3>Cross-model relay</h3>
          <p>Move a project between compatible models or platforms without treating the old transcript as the project. AIR carries explicit project state through Handoff, then validates and rebinds that state in the receiving session before work continues.</p>
          <ul><li>explicit Handoff state</li><li>receiver validation</li><li>rebind before continuation</li></ul>
        </div>
        <div class="uc edge-case">
          <div class="k">Reconstruction</div>
          <h3>Incident reconstruction</h3>
          <p>When something failed, keep observations, evidence, assumptions, unknowns, and corrective actions separate. AIR gives the investigation a visible working contract so a plausible story does not quietly become the accepted explanation.</p>
          <ul><li>evidence separated from inference</li><li>unknowns stay visible</li><li>corrective actions stay scoped</li></ul>
        </div>
        <div class="uc edge-case">
          <div class="k">Mixed discipline</div>
          <h3>The project that refuses one lane</h3>
          <p>A launch can move through research, positioning, code, documentation, policy, assets, and rollout decisions. AIR can change the capability used for the current step while the same project contract and continuity remain visible.</p>
          <ul><li>step-specific capability</li><li>shared project continuity</li><li>authority does not drift with role</li></ul>
        </div>
        <div class="uc edge-case">
          <div class="k">Challenge</div>
          <h3>Decision stress-testing</h3>
          <p>Use AIR to structure the strongest counter-case, identify which assumptions are carrying the decision, and state what evidence would justify changing course. The framework keeps recommendation, uncertainty, and decision authority distinct.</p>
          <ul><li>strongest counter-case</li><li>reversal triggers</li><li>fact, estimate, judgment separated</li></ul>
        </div>
        <div class="uc edge-case">
          <div class="k">Translation</div>
          <h3>From knowledge to execution</h3>
          <p>Turn standards, research, documentation, or domain guidance into bounded implementation work without pretending that source retrieval alone proves correct application. AIR can carry source constraints into the task, verification, evidence, and delivery path.</p>
          <ul><li>source constraints preserved</li><li>verification stays explicit</li><li>application still has to be evidenced</li></ul>
        </div>
      </div>
    </div>
  </section>

  <section class="section" style="padding-top:0">'''
    return replace_once(path, old, edge, 'id="edge-cases"')


def patch_glossary() -> bool:
    path = ROOT / "public" / "glossary.html"
    text = path.read_text(encoding="utf-8")
    changed = False
    if '<h3>Capability layers</h3>' not in text:
        if text.count('<h3>Grounding layers</h3>') != 1:
            raise SystemExit("glossary: expected exactly one Grounding layers heading")
        text = text.replace('<h3>Grounding layers</h3>', '<h3>Capability layers</h3>', 1)
        changed = True
    executor_marker = '<div class="row"><dt>Executor</dt>'
    if executor_marker not in text:
        method = '<div class="row"><dt>Method Pack</dt><dd>A reusable procedure with explicit execution state, gates, evidence expectations, and handoff state. It does not execute or govern independently of the bound artifact.</dd></div>'
        if text.count(method) != 1:
            raise SystemExit("glossary: expected exactly one Method Pack definition")
        executor = method + '\n          <div class="row"><dt>Executor</dt><dd>A bounded non-agent callable operation that performs one defined action inside the active Orbit 0 contract. It requires the applicable inputs, sources, or tools and produces a bounded output such as an artifact, check, table, transformation, or review. It does not own agency, intent, initiative, or execution authority, and remains subject to the active contract, AIR_GATE, evidence requirements, and tool/source boundaries.</dd></div>'
        text = text.replace(method, executor, 1)
        changed = True
    if changed:
        path.write_text(text, encoding="utf-8")
    return changed


def patch_testing() -> bool:
    path = ROOT / "public" / "testing-and-evidence.html"
    old = '<section class="hero" style="padding-bottom:1.5rem"><div class="container"><span class="eyebrow">How it works · Testing &amp; evidence</span><h1 style="font-size:clamp(2.35rem,1.7rem+2.6vw,3.7rem);margin:1rem 0 1.1rem;max-width:48rem">Test the claim you actually want to make.</h1><p class="sub" style="max-width:45rem">AIR uses different evidence paths for different questions. A behavioral model test, a deterministic release check, human QA and external verification can all be useful — but they do not prove the same thing.</p>'
    new = '<section class="hero hero--page hero--plain"><div class="container"><span class="eyebrow">How it works · Testing &amp; evidence</span><h1 class="page-title">Test the claim you actually want to make.</h1><p class="sub">AIR uses different evidence paths for different questions. A behavioral model test, a deterministic release check, human QA and external verification can all be useful — but they do not prove the same thing.</p>'
    changed = replace_once(path, old, new, 'hero hero--page hero--plain')
    text = path.read_text(encoding="utf-8")
    old_section = '<section class="section" style="padding-top:2rem"><div class="container"><div class="section-head"><span class="eyebrow">Evidence map</span>'
    new_section = '<section class="section section--standard"><div class="container"><div class="section-head"><span class="eyebrow">Evidence map</span>'
    if 'section section--standard' not in text:
        if text.count(old_section) != 1:
            raise SystemExit("testing-and-evidence: expected exactly one first-section spacing override")
        path.write_text(text.replace(old_section, new_section, 1), encoding="utf-8")
        changed = True
    return changed


def patch_css() -> bool:
    path = ROOT / "public" / "air-v2.css"
    text = path.read_text(encoding="utf-8")
    marker = '/* ---------- interior page visual system ---------- */'
    if marker in text:
        return False
    block = r'''

/* ---------- interior page visual system ---------- */
:root{--air-page-title-size:clamp(2.65rem,1.8rem + 3vw,4.5rem);--air-page-title-compact-size:clamp(2.25rem,1.65rem + 2.25vw,3.65rem);--air-page-hero-space:clamp(3.75rem,7vw,5.75rem);--air-section-space:clamp(4rem,7vw,6.5rem);--air-section-space-compact:clamp(2.75rem,5vw,4.25rem)}
.hero--page{padding:var(--air-page-hero-space) 0;border-bottom:1px solid var(--border)}
.hero .page-title{font-size:var(--air-page-title-size);max-width:52rem;margin:1rem 0 1.1rem}
.hero .page-title--compact{font-size:var(--air-page-title-compact-size);max-width:56rem}
.hero--page .sub{max-width:45rem}
.section--standard{padding:var(--air-section-space) 0}
.section--compact{padding:var(--air-section-space-compact) 0}
.hero--patterned{background-color:var(--bg);background-image:linear-gradient(var(--grid) 1px,transparent 1px),linear-gradient(90deg,var(--grid) 1px,transparent 1px);background-size:28px 28px}
.hero--plain{background-image:none}
'''
    path.write_text(text.rstrip() + block + "\n", encoding="utf-8")
    return True


def main() -> int:
    changed = []
    for name, fn in [
        ("public/use-cases.html", patch_use_cases),
        ("public/glossary.html", patch_glossary),
        ("public/testing-and-evidence.html", patch_testing),
        ("public/air-v2.css", patch_css),
    ]:
        if fn():
            changed.append(name)
    print("changed:", ", ".join(changed) if changed else "none")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
