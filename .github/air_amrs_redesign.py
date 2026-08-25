from pathlib import Path
import re

path = Path('public/how-it-works.html')
text = path.read_text(encoding='utf-8')
original = text


def block(src, start, end):
    a = src.index(start)
    b = src.index(end, a) + len(end)
    return src[a:b]

header_before = block(text, '<header class="site-header">', '</header>')
footer_before = block(text, '<footer class="site-footer">', '</footer>')

new_css = r'''.amrs-note{max-width:50rem;margin:.8rem 0 0;color:var(--subtle);font-size:.84rem;line-height:1.55}
.amrs{position:relative;display:flex;flex-direction:column;gap:.7rem;max-width:58rem;margin:1.6rem 0 0;padding-left:2.8rem}
.amrs::before{content:"";position:absolute;left:1rem;top:1.35rem;bottom:1.35rem;width:2px;background:linear-gradient(to bottom,var(--ember-ink),color-mix(in srgb,var(--brass) 50%,var(--border)),var(--brass))}
.amrs-stage{position:relative;border:1px solid var(--border);border-radius:14px;background:var(--surface);box-shadow:var(--card-shadow);overflow:visible;transition:border-color .2s,background .2s}
.amrs-stage::before{content:"";position:absolute;left:-2.28rem;top:1.45rem;width:14px;height:14px;border-radius:50%;box-sizing:border-box;background:var(--bg);border:3px solid color-mix(in srgb,var(--brass) 72%,var(--border));z-index:2}
.amrs-stage.floor{border-left:3px solid var(--ember-ink)}
.amrs-stage.floor::before{border-color:var(--ember-ink);background:color-mix(in srgb,var(--ember) 18%,var(--bg))}
.amrs-stage.top{border-left:3px solid var(--brass);background:color-mix(in srgb,var(--brass) 5%,var(--surface))}
.amrs-stage.top::before{border-color:var(--brass);background:var(--brass)}
.amrs-stage[open]{border-color:var(--border-strong)}
.amrs-stage summary{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:1rem;align-items:start;padding:1rem 1.15rem;cursor:pointer;list-style:none}
.amrs-stage summary::-webkit-details-marker{display:none}
.amrs-stage summary:focus-visible{outline:2px solid var(--brass);outline-offset:3px;border-radius:12px}
.amrs-titleline{display:flex;align-items:baseline;gap:.7rem;flex-wrap:wrap}
.amrs-n{font-family:var(--font-mono);font-size:.74rem;color:var(--brass);white-space:nowrap;letter-spacing:.02em}
.amrs-title{font-size:1rem;font-weight:600;color:var(--text)}
.amrs-analogue{font-family:var(--font-mono);font-size:.69rem;color:var(--subtle);margin-top:.28rem}
.amrs-summary-copy{color:var(--muted);font-size:.88rem;line-height:1.5;margin:.42rem 0 0;max-width:48rem}
.amrs-status{display:inline-block;margin-top:.55rem;padding:.22rem .45rem;border:1px solid var(--border-strong);border-radius:6px;font-family:var(--font-mono);font-size:.64rem;letter-spacing:.05em;color:var(--subtle);background:var(--surface-2)}
.amrs-stage.floor .amrs-status{border-color:color-mix(in srgb,var(--ember) 50%,var(--border));color:var(--ember-ink)}
.amrs-stage.top .amrs-status{border-color:color-mix(in srgb,var(--brass) 65%,var(--border));color:var(--brass)}
.amrs-toggle{display:grid;place-items:center;width:30px;height:30px;border:1px solid var(--border-strong);border-radius:8px;color:var(--brass);font-family:var(--font-mono);font-size:1rem;line-height:1;background:var(--surface-2);margin-top:.05rem}
.amrs-toggle::before{content:"+"}
.amrs-stage[open] .amrs-toggle::before{content:"−"}
.amrs-detail{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;border-top:1px solid var(--border);padding:1rem 1.15rem 1.2rem}
.amrs-detail-block{min-width:0;padding:.85rem .9rem;border:1px solid color-mix(in srgb,var(--border) 82%,transparent);border-radius:10px;background:color-mix(in srgb,var(--surface-2) 72%,transparent)}
.amrs-detail-block h4{margin:0 0 .4rem;font-family:var(--font-mono);font-size:.68rem;letter-spacing:.07em;text-transform:uppercase;color:var(--brass);font-weight:500}
.amrs-detail-block p{margin:0;color:var(--muted);font-size:.86rem;line-height:1.55}
.amrs-foot{color:var(--muted);max-width:50rem;margin:1.1rem 0 0;font-size:.92rem}
@media (max-width:720px){
  .amrs{padding-left:2.3rem}
  .amrs::before{left:.75rem}
  .amrs-stage::before{left:-1.93rem}
  .amrs-stage summary{padding:.9rem 1rem}
  .amrs-detail{grid-template-columns:1fr;padding:.9rem 1rem 1rem}
}'''

css_pattern = re.compile(r'\.amrs\{.*?\.amrs-foot\{[^}]*\}', re.S)
text, css_count = css_pattern.subn(new_css, text, count=1)
if css_count != 1:
    raise SystemExit(f'Expected one AMRS CSS block, replaced {css_count}')

new_section = '''  <section class="section" id="amrs" style="padding-top:0">
    <div class="container">
      <div class="section-head">
        <span class="eyebrow">Readiness</span>
        <h2>How mature is your project?</h2>
        <p class="sub" style="max-width:50rem">AIR tracks project maturity from <strong>problem framing to production approval</strong>. Each AMRS stage defines what exists, what AIR may claim, and what still has to be earned.</p>
        <p class="amrs-note"><strong>AMRS-0 → AMRS-6.</strong> Expand any stage to see its claim boundaries, readiness requirements, and a familiar product-development analogue. Product analogues are orientation only: terms such as PoC, MVP, beta, and release candidate vary between organizations; AMRS remains AIR's operative readiness model.</p>
      </div>

      <div class="amrs" aria-label="AIR Maturity Readiness Scale from AMRS-0 to AMRS-6">
        <details class="amrs-stage floor">
          <summary>
            <div>
              <div class="amrs-titleline"><span class="amrs-n">AMRS-0</span><span class="amrs-title">Problem framing</span></div>
              <div class="amrs-analogue">Common product analogue · Discovery / problem definition</div>
              <p class="amrs-summary-copy">Define the objective, task center, constraints, and blockers before treating the work as implementation-ready.</p>
              <span class="amrs-status">FRAMING · NO IMPLEMENTATION-READY CLAIM</span>
            </div>
            <span class="amrs-toggle" aria-hidden="true"></span>
          </summary>
          <div class="amrs-detail">
            <div class="amrs-detail-block"><h4>What exists now</h4><p>The problem is being made explicit. AIR can establish the objective, form the task center, discover constraints, and surface blockers.</p></div>
            <div class="amrs-detail-block"><h4>AIR may claim</h4><p>The problem, intended outcome, and relevant constraints are sufficiently framed to continue shaping the solution.</p></div>
            <div class="amrs-detail-block"><h4>AIR may not claim</h4><p>Production readiness, implementation readiness, or code acceptance. Those claims are explicitly blocked at AMRS-0.</p></div>
            <div class="amrs-detail-block"><h4>What moves it forward</h4><p>A coherent concept begins to emerge: architecture direction, capabilities, dependencies, and the vectors needed to solve the framed problem.</p></div>
          </div>
        </details>

        <details class="amrs-stage">
          <summary>
            <div>
              <div class="amrs-titleline"><span class="amrs-n">AMRS-1</span><span class="amrs-title">Concept shape</span></div>
              <div class="amrs-analogue">Common product analogue · Solution concept / concept definition</div>
              <p class="amrs-summary-copy">Shape the architecture, capabilities, and dependencies before calling the solution executable.</p>
              <span class="amrs-status">CONCEPT · NO DEPLOYMENT CLAIM</span>
            </div>
            <span class="amrs-toggle" aria-hidden="true"></span>
          </summary>
          <div class="amrs-detail">
            <div class="amrs-detail-block"><h4>What exists now</h4><p>AIR can develop the concept architecture, select relevant vectors, cluster capabilities, and frame dependencies.</p></div>
            <div class="amrs-detail-block"><h4>AIR may claim</h4><p>The solution concept has enough structure to evaluate its architecture and move toward executable design.</p></div>
            <div class="amrs-detail-block"><h4>AIR may not claim</h4><p>Production-grade code, deployment readiness, or acceptance of the solution without an executable design.</p></div>
            <div class="amrs-detail-block"><h4>What moves it forward</h4><p>Interfaces, architectural invariants, review and testing plans, security considerations, and the coding or implementation contract become explicit.</p></div>
          </div>
        </details>

        <details class="amrs-stage">
          <summary>
            <div>
              <div class="amrs-titleline"><span class="amrs-n">AMRS-2</span><span class="amrs-title">Executable design</span></div>
              <div class="amrs-analogue">Common product analogue · Implementation-ready design / technical specification</div>
              <p class="amrs-summary-copy">Turn the concept into a design that can actually be implemented, reviewed, and tested.</p>
              <span class="amrs-status">DESIGN · NOT IMPLEMENTATION-COMPLETE</span>
            </div>
            <span class="amrs-toggle" aria-hidden="true"></span>
          </summary>
          <div class="amrs-detail">
            <div class="amrs-detail-block"><h4>What exists now</h4><p>AIR can define executable design, interfaces, architectural invariants, review and test strategy, security planning, and the coding contract.</p></div>
            <div class="amrs-detail-block"><h4>AIR may claim</h4><p>The design is sufficiently specified for controlled implementation to begin.</p></div>
            <div class="amrs-detail-block"><h4>AIR may not claim</h4><p>Production acceptance or that implementation is complete when generated output and review evidence do not yet exist.</p></div>
            <div class="amrs-detail-block"><h4>What moves it forward</h4><p>A narrow implementation is produced and tested under explicit limits, with missing coverage, degraded behavior, and rejection conditions kept visible.</p></div>
          </div>
        </details>

        <details class="amrs-stage">
          <summary>
            <div>
              <div class="amrs-titleline"><span class="amrs-n">AMRS-3</span><span class="amrs-title">Controlled prototype</span></div>
              <div class="amrs-analogue">Common product analogue · Proof of Concept (PoC)</div>
              <p class="amrs-summary-copy">Prove that the execution path works in a controlled scope without pretending the complete system is ready.</p>
              <span class="amrs-status">PROTOTYPE · NO PRODUCTION-READY CLAIM</span>
            </div>
            <span class="amrs-toggle" aria-hidden="true"></span>
          </summary>
          <div class="amrs-detail">
            <div class="amrs-detail-block"><h4>What exists now</h4><p>AIR may perform controlled code generation, narrow-scope implementation, and controlled manual testing. Degraded mode must be explicit where applicable, missing coverage must remain visible, and rejection conditions must be stated rather than hidden.</p></div>
            <div class="amrs-detail-block"><h4>AIR may claim</h4><p>The prototype demonstrates the tested behavior within its defined scope and evidence.</p></div>
            <div class="amrs-detail-block"><h4>AIR may not claim</h4><p>That the result is production-ready unless the work is promoted through the later readiness stages.</p></div>
            <div class="amrs-detail-block"><h4>What moves it forward</h4><p>Subsystems begin operating together. Execution paths become reproducible, refactors remain contract-governed, and testing moves beyond a narrow proof into integrated-system evidence.</p></div>
          </div>
        </details>

        <details class="amrs-stage">
          <summary>
            <div>
              <div class="amrs-titleline"><span class="amrs-n">AMRS-4</span><span class="amrs-title">Integrated system</span></div>
              <div class="amrs-analogue">Common product analogue · MVP / integrated alpha</div>
              <p class="amrs-summary-copy">Connect the parts, exercise repeatable execution paths, and test the system rather than isolated pieces.</p>
              <span class="amrs-status">INTEGRATED · BLOCKERS STILL MATTER</span>
            </div>
            <span class="amrs-toggle" aria-hidden="true"></span>
          </summary>
          <div class="amrs-detail">
            <div class="amrs-detail-block"><h4>What exists now</h4><p>AIR can work across subsystem integration, reproducible execution paths, contract-governed refactors, and structured testing.</p></div>
            <div class="amrs-detail-block"><h4>AIR may claim</h4><p>The relevant parts operate together as an integrated system within the demonstrated scope.</p></div>
            <div class="amrs-detail-block"><h4>AIR must keep visible</h4><p>Unresolved blockers and integration assumptions. Integration is not permission to silently treat either as resolved.</p></div>
            <div class="amrs-detail-block"><h4>AIR may not claim</h4><p>Production approval simply because the system is integrated. That claim belongs to a later readiness state and still requires the necessary evidence and approval conditions.</p></div>
            <div class="amrs-detail-block"><h4>What moves it forward</h4><p>The integrated system is packaged and hardened as a production candidate, with deployment planning, security checks, test requirements, failure handling, rollback strategy, and explicit acceptance criteria.</p></div>
          </div>
        </details>

        <details class="amrs-stage">
          <summary>
            <div>
              <div class="amrs-titleline"><span class="amrs-n">AMRS-5</span><span class="amrs-title">Production candidate</span></div>
              <div class="amrs-analogue">Common product analogue · Beta / Release Candidate</div>
              <p class="amrs-summary-copy">Harden, package, and prepare for production — while production-critical blockers remain disqualifying.</p>
              <span class="amrs-status">CANDIDATE · PRODUCTION APPROVAL NOT YET EARNED</span>
            </div>
            <span class="amrs-toggle" aria-hidden="true"></span>
          </summary>
          <div class="amrs-detail">
            <div class="amrs-detail-block"><h4>What exists now</h4><p>AIR may perform production-candidate packaging, deployment planning, and operational hardening. This stage requires security checks, explicit test requirements, rollback and failure handling, and clear acceptance criteria.</p></div>
            <div class="amrs-detail-block"><h4>AIR may claim</h4><p>The system is a production candidate being evaluated against explicit production conditions.</p></div>
            <div class="amrs-detail-block"><h4>AIR may not claim</h4><p>Production approval while any unresolved production-critical blocker remains.</p></div>
            <div class="amrs-detail-block"><h4>What moves it forward</h4><p>All production-critical blockers are resolved, the review state is evidence-complete, the decision trace exists, and approval is explicit and visible.</p></div>
          </div>
        </details>

        <details class="amrs-stage top">
          <summary>
            <div>
              <div class="amrs-titleline"><span class="amrs-n">AMRS-6</span><span class="amrs-title">Production approved</span></div>
              <div class="amrs-analogue">Common product analogue · Production-ready / release approved</div>
              <p class="amrs-summary-copy">The production-ready claim is permitted only after the critical blockers, evidence, decision trace, and approval state are resolved.</p>
              <span class="amrs-status">PRODUCTION APPROVED</span>
            </div>
            <span class="amrs-toggle" aria-hidden="true"></span>
          </summary>
          <div class="amrs-detail">
            <div class="amrs-detail-block"><h4>What exists now</h4><p>There are no unresolved production-critical blockers. The review state is explicitly evidence-complete, the decision trace is recorded, and approval is visible.</p></div>
            <div class="amrs-detail-block"><h4>AIR may claim</h4><p>The work is <strong>production approved</strong>. This is the AMRS stage at which that claim becomes permitted.</p></div>
            <div class="amrs-detail-block"><h4>AIR may not imply</h4><p>More than the evidence establishes. AMRS-6 does not override AIR's wider evidence, assurance, or claim-boundary rules.</p></div>
            <div class="amrs-detail-block"><h4>What sustains the stage</h4><p>Production evidence and approvals must remain current. Material changes, new blockers, or invalidated evidence should trigger readiness reassessment rather than inheriting AMRS-6 automatically.</p></div>
          </div>
        </details>
      </div>

      <p class="amrs-foot">AIR fails closed if you ask for something above the current stage, and it never promotes silently. That is the mechanism behind “won't oversell a sketch” — the ruler will not let it.</p>
    </div>
  </section>'''

start_marker = '  <section class="section" id="amrs" style="padding-top:0">'
evidence_marker = '\n\n  <section class="section" style="padding-top:0">\n    <div class="container">\n      <div class="section-head">\n        <span class="eyebrow">Evidence</span>'
if text.count(start_marker) != 1:
    raise SystemExit(f'Expected exactly one AMRS section start, found {text.count(start_marker)}')
start = text.index(start_marker)
end = text.index(evidence_marker, start)
text = text[:start] + new_section + text[end:]

header_after = block(text, '<header class="site-header">', '</header>')
footer_after = block(text, '<footer class="site-footer">', '</footer>')
if header_before != header_after:
    raise SystemExit('Header changed unexpectedly')
if footer_before != footer_after:
    raise SystemExit('Footer changed unexpectedly')

checks = {
    'seven stages': text.count('<details class="amrs-stage') == 7,
    'all collapsed': '<details class="amrs-stage" open' not in text and '<details class="amrs-stage floor" open' not in text and '<details class="amrs-stage top" open' not in text,
    'old rungs removed': 'amrs-rung' not in text,
    'old TRL paragraph removed': 'NASA-style Technology Readiness Levels' not in text,
    'orientation qualifier present': 'Product analogues are orientation only' in text,
}
positions = [text.index(f'AMRS-{i}', start) for i in range(7)]
checks['stage order 0 through 6'] = positions == sorted(positions)
for label, ok in checks.items():
    if not ok:
        raise SystemExit(f'Validation failed: {label}')

if text == original:
    raise SystemExit('No changes produced')

path.write_text(text, encoding='utf-8')
print('AMRS redesign applied and validated')
for label in checks:
    print('PASS:', label)
