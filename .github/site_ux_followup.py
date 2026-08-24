from pathlib import Path
import sys

P = Path('public')
CHANGED = []


def fail(msg):
    print('ERROR:', msg, file=sys.stderr)
    raise SystemExit(1)


def read(name):
    return (P / name).read_text(encoding='utf-8')


def write(name, text):
    (P / name).write_text(text, encoding='utf-8')
    CHANGED.append(name)


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        fail(f'{label}: expected exactly 1 occurrence, found {count}')
    return text.replace(old, new, 1)


# ------------------------------------------------------------
# HOW IT WORKS
# Preserve all existing diagrams; add a render guard and a
# dedicated neurodivergent-delivery explanation.
# ------------------------------------------------------------
name = 'how-it-works.html'
s = read(name)
if s.count('class="diagram"') < 7:
    fail('how-it-works: expected at least seven existing diagrams before patch')

s = replace_once(
    s,
    '<p style="font-family:var(--font-mono);font-size:.84rem;margin:.5rem 0 0"><a href="glossary.html">New to the vocabulary? See the glossary →</a></p>',
    '<p style="font-family:var(--font-mono);font-size:.84rem;margin:.5rem 0 0"><a href="glossary.html">New to the vocabulary? See the glossary →</a> <span aria-hidden="true">·</span> <a href="#neurodivergent-delivery">Neurodivergent delivery →</a></p>',
    'how-it-works hero links'
)

s = replace_once(
    s,
    '.diagram svg{width:100%;height:auto;display:block}',
    '.diagram svg{width:100%;height:auto;display:block;visibility:visible;opacity:1;overflow:visible}',
    'how-it-works diagram css'
)

nd_section = '''  <section class="section" id="neurodivergent-delivery" style="padding-top:0">
    <div class="container">
      <div class="section-head">
        <span class="eyebrow">Delivery modifier</span>
        <h2>Neurodivergent delivery changes the interaction, not the standard.</h2>
        <p class="sub" style="max-width:48rem">Q4=D does not diagnose or classify the user. It opens an explicit delivery modifier, then Q4D preserves the underlying continuity style and Q6D calibrates how AIR presents and manages the work.</p>
      </div>
      <div class="cards">
        <div class="card">
          <div class="k">Q4D · continuity</div>
          <h3>Keep the base working style</h3>
          <p>Choose structure + logic, structure + tone, or creative narrative continuity. The neurodivergent modifier sits on top of that choice rather than replacing it.</p>
        </div>
        <div class="card">
          <div class="k">Q6D · interaction</div>
          <h3>Calibrate how work reaches you</h3>
          <p>AIR asks how important information should be presented, how side tracks should be handled, what helps when focus drops, how momentum should be managed, and which communication needs it should follow.</p>
        </div>
        <div class="card">
          <div class="k">What may change</div>
          <h3>Pacing, chunking and redirection</h3>
          <p>The modifier can change chunk size, transitions, presentation order, explanation depth, side-track handling, momentum support and managed breaks. It can also accommodate functional needs such as voice-to-text or memory support.</p>
        </div>
        <div class="card">
          <div class="k">What does not change</div>
          <h3>Evidence and governance stay intact</h3>
          <p>Truth, evidence, scope, AIR_GATE, safety, approvals, artifact visibility and backend boundaries do not get weaker. AIR does not require a diagnosis, and project-scoped interaction preferences remain visible and correctable.</p>
        </div>
      </div>
    </div>
  </section>

'''
marker = '  <section class="section" id="amrs" style="padding-top:0">'
if marker not in s:
    fail('how-it-works: AMRS section marker missing')
s = s.replace(marker, nd_section + marker, 1)

render_guard = '''
<script>
/* Diagram render guard: preserve intrinsic SVG ratio if a browser reports a collapsed box. */
(function(){
  function repair(){
    document.querySelectorAll('.diagram svg[viewBox]').forEach(function(svg){
      var box=svg.getBoundingClientRect();
      var vb=svg.viewBox && svg.viewBox.baseVal;
      if(box.width>0 && box.height<24 && vb && vb.width>0 && vb.height>0){
        svg.style.height=Math.round(box.width*(vb.height/vb.width))+'px';
      }
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',repair);
  else repair();
  window.addEventListener('resize',repair,{passive:true});
})();
</script>
'''
s = replace_once(s, '</body>', render_guard + '</body>', 'how-it-works body close')

if s.count('class="diagram"') < 7:
    fail('how-it-works: diagrams disappeared during patch')
for required in ['id="neurodivergent-delivery"', 'Q4D · continuity', 'Q6D · interaction', 'Diagram render guard']:
    if required not in s:
        fail('how-it-works missing required follow-up content: ' + required)
write(name, s)


# ------------------------------------------------------------
# AIR DOCS
# Add formal neurodivergent modifier documentation and repair
# stale metadata that still named the older release line.
# ------------------------------------------------------------
name = 'air-docs.html'
s = read(name)
s = replace_once(
    s,
    'Canonical AIR technical documentation for the v0.4 release line: setup, runtime, objects, modifiers, evidence, handoff, packages, anti-drift checks, best practices, and future adapters.',
    'Human-readable AIR 2.4.3 technical reference: setup, onboarding, runtime, objects, neurodivergent delivery, evidence, handoff, packages, anti-drift checks, and implementation guidance.',
    'air-docs meta description'
)
s = replace_once(
    s,
    'Canonical technical documentation for AIR v0.4 and Core Runtime 2.4.2.',
    'Human-readable technical reference for AIR Core and Control 2.4.3, including onboarding, governance, continuity and delivery modifiers.',
    'air-docs social description',
) if False else s
# The old social description appears twice; replace both intentionally.
old_social = 'Canonical technical documentation for AIR v0.4 and Core Runtime 2.4.2.'
if s.count(old_social) != 2:
    fail(f'air-docs social description: expected 2 occurrences, found {s.count(old_social)}')
s = s.replace(old_social, 'Human-readable technical reference for AIR Core and Control 2.4.3, including onboarding, governance, continuity and delivery modifiers.')

s = replace_once(
    s,
    '        <a href="#onboarding">Onboarding</a>\n        <a href="#runtime">Runtime model</a>',
    '        <a href="#onboarding">Onboarding</a>\n        <a href="#neurodivergent">Neurodivergent delivery</a>\n        <a href="#runtime">Runtime model</a>',
    'air-docs toc neurodivergent link'
)

docs_nd = '''        <section class="docs-section" id="neurodivergent">
          <h2>Neurodivergent delivery modifier</h2>
          <p class="lead">Q4=D is an explicit delivery and interaction modifier. It is not a diagnosis, identity classification, or lower-rigor mode. AIR does not infer a condition and the user does not need to disclose one to request functional support.</p>
          <div class="docs-grid">
            <div class="docs-card"><h3>Q4D keeps continuity explicit</h3><p>After Q4=D, Q4D chooses the underlying continuity preference: structure + logic, structure + tone, or creative narrative continuity — each with neurodivergent delivery layered on top.</p></div>
            <div class="docs-card"><h3>Q6D calibrates interaction</h3><p>Q6D retains the normal working-agreement responsibilities and adds functional calibration: important-information presentation, side-track handling, focus-drop support, momentum management, and communication needs.</p></div>
            <div class="docs-card"><h3>Delivery can adapt</h3><p>AIR may change pacing, chunk size, transition style, redirection, explanation depth, break support and presentation order. Functional needs can include voice-to-text handling, memory support and managed breaks.</p></div>
            <div class="docs-card"><h3>Governance cannot</h3><p>The modifier must not weaken truth, evidence, scope, AIR_GATE, safety, approvals, artifact visibility or backend boundaries. Project-scoped preferences remain visible, correctable and revisable.</p></div>
          </div>
          <div class="docs-note"><strong>Practical effect:</strong> AIR can change <em>how</em> the work is delivered without changing what counts as adequate evidence, what requires approval, or what the active contract allows.</div>
        </section>

'''
runtime_marker = '        <section class="docs-section" id="runtime">'
if runtime_marker not in s:
    fail('air-docs runtime section marker missing')
s = s.replace(runtime_marker, docs_nd + runtime_marker, 1)
for required in ['id="neurodivergent"', 'Q6D calibrates interaction', 'Core 2.4.3']:
    if required not in s:
        fail('air-docs missing required content: ' + required)
write(name, s)


# ------------------------------------------------------------
# USE CASES
# Add best-practice onboarding starting points plus concrete Q5
# and Q6 examples. Recommendations are labelled as starting
# points and never presented as automatic AIR selections.
# ------------------------------------------------------------
name = 'use-cases.html'
s = read(name)
css_old = '.uc-more{font-family:var(--font-mono);font-size:.85rem;color:var(--muted);margin-top:1.4rem}\n.casestudy{'
css_new = '''.uc-more{font-family:var(--font-mono);font-size:.85rem;color:var(--muted);margin-top:1.4rem}
.onboard-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:1rem;margin-top:1.4rem}
@media(max-width:840px){.onboard-grid{grid-template-columns:1fr}}
.onboard-card{border:1px solid var(--border);border-radius:16px;background:var(--surface);padding:1.4rem;box-shadow:var(--card-shadow)}
.onboard-card .k{font-family:var(--font-mono);font-size:.72rem;letter-spacing:.1em;text-transform:uppercase;color:var(--brass)}
.onboard-card h3{font-size:1.2rem;margin:.45rem 0 .55rem;font-weight:500}
.onboard-card .qline{font-family:var(--font-mono);font-size:.78rem;color:var(--text);border:1px solid var(--border-strong);border-radius:9px;padding:.55rem .7rem;margin:.7rem 0 1rem}
.onboard-card details{border-top:1px solid var(--border);padding:.75rem 0 0;margin-top:.75rem}
.onboard-card summary{cursor:pointer;font-family:var(--font-mono);font-size:.78rem;color:var(--brass)}
.onboard-card details p{color:var(--muted);font-size:.9rem;line-height:1.55;margin:.65rem 0 0}
.casestudy{'''
s = replace_once(s, css_old, css_new, 'use-cases onboarding css')

onboarding_section = '''  <section class="section" id="onboarding-patterns" style="padding-top:0">
    <div class="container">
      <div class="section-head">
        <span class="eyebrow">Onboarding patterns</span>
        <h2>Good starting choices for different kinds of work.</h2>
        <p>These are best-practice starting points, not automatic AIR selections. Q1 is about project state, not domain: use A for a new project, B to import existing non-AIR work, C for a Handoff continuation, or D for orientation. The cards below assume a new project.</p>
      </div>
      <div class="callout"><div class="label">Reading the choices</div><p>Q2 sets checking rigor. Q3 sets ambiguity handling. Q4 sets continuity. If you want neurodivergent delivery, choose Q4=D and use Q4D to preserve the matching base continuity style. AIR still asks the questions; these recommendations do not bypass onboarding.</p></div>
      <div class="onboard-grid">
        <div class="onboard-card"><div class="k">Code</div><h3>Development</h3><div class="qline">Q1 A* · Q2 C · Q3 A · Q4 A</div><p>Strict checks, early ambiguity resolution, structure + logic.</p><details><summary>Q5 example</summary><p>Refactor authentication to add passkeys while preserving the password flow. Node/TypeScript; no API break; tests and security review required. Sources: repository, current auth contract and WebAuthn specification.</p></details><details><summary>Q6 working-contract example</summary><p>AIR may inspect and propose edits. Deliver unified diffs first; do not mutate main without my approval. I run tests locally and return the logs. Stop on security, type or test failures. Ask before dependency or schema changes, challenge architecture assumptions, and explain non-obvious decisions.</p></details></div>
        <div class="onboard-card"><div class="k">Research</div><h3>Evidence-heavy research</h3><div class="qline">Q1 A* · Q2 C · Q3 A · Q4 A</div><p>Strict evidence handling, resolve material ambiguity early, preserve structure + logic.</p><details><summary>Q5 example</summary><p>Compare EU AI Act Article 50 obligations relevant to deployers of generative AI. Use EU primary sources first; distinguish law, guidance and interpretation. Deliver a cited memo with unresolved questions.</p></details><details><summary>Q6 working-contract example</summary><p>AIR finds, organizes and synthesizes sources. Cite every material claim and label source-supported fact, inference and unknowns separately. I approve changes to scope or thesis. Do not fill source gaps with plausible prose; surface them.</p></details></div>
        <div class="onboard-card"><div class="k">Writing</div><h3>Writing &amp; content</h3><div class="qline">Q1 A* · Q2 B · Q3 B · Q4 B</div><p>Balanced review, keep non-blocking ambiguity open, preserve structure + tone.</p><details><summary>Q5 example</summary><p>Draft a 1,500-word technical article for senior engineers explaining AIR Handoff. Clear, dry voice; no hype. Preserve verified claims and include one concrete continuation example.</p></details><details><summary>Q6 working-contract example</summary><p>AIR drafts section by section. I approve the outline and any major voice change. Preserve supplied facts, flag unverifiable claims, and deliver complete revised sections rather than tiny fragments. Challenge weak structure without flattening the voice.</p></details></div>
        <div class="onboard-card"><div class="k">Creative</div><h3>Creative development</h3><div class="qline">Q1 A* · Q2 B · Q3 C · Q4 C</div><p>Balanced quality control, deliberate ambiguity can stay open, preserve narrative continuity.</p><details><summary>Q5 example</summary><p>Develop a five-song concept arc about migration without literal exposition. Dark electronic/pop; preserve recurring signal/noise imagery. Deliver concepts and lyric skeletons, not final audio.</p></details><details><summary>Q6 working-contract example</summary><p>AIR generates options, not final canon. Keep creative ambiguity unless it breaks continuity. I choose the canon. Preserve motifs and voice; do not rationalize away deliberate contradictions. Ask before changing the core premise.</p></details></div>
        <div class="onboard-card"><div class="k">Brand</div><h3>Brand &amp; marketing</h3><div class="qline">Q1 A* · Q2 B · Q3 A · Q4 B</div><p>Balanced review, resolve positioning ambiguity early, preserve structure + tone.</p><details><summary>Q5 example</summary><p>Define the launch campaign for AIR 2.4.3. Preserve Brand v2 promise, signature, mark and palette. Audience: AI power users and small teams. Deliver messaging hierarchy, campaign concepts and an asset brief.</p></details><details><summary>Q6 working-contract example</summary><p>AIR may propose positioning, copy and assets, but public promise changes require my approval. The brand book is source truth. Deliver options with rationale and claim-risk notes. Do not change the mark, palette or core signature without approval.</p></details></div>
        <div class="onboard-card"><div class="k">Strategy</div><h3>Strategy &amp; decisions</h3><div class="qline">Q1 A* · Q2 C · Q3 A · Q4 A</div><p>Strict decision support, resolve material uncertainty early, preserve structure + logic.</p><details><summary>Q5 example</summary><p>Choose an EU-first go-to-market path for AIR. Compare open-source adoption, services revenue and enterprise licensing under a 12-month runway. Deliver a decision memo with assumptions, risks and next experiments.</p></details><details><summary>Q6 working-contract example</summary><p>AIR builds models and tests assumptions; distinguish fact, estimate and judgment. I make irreversible business decisions. Stop when missing evidence could change the recommendation. Present the recommendation, the strongest counter-case and the triggers that should make us revise it.</p></details></div>
      </div>
      <p class="uc-more">* Q1=A assumes a fresh project. Use Q1=B for an existing non-AIR project and Q1=C when continuing from a Handoff Card.</p>
    </div>
  </section>

'''
insert_marker = '''  <section class="section" style="padding-top:0">
    <div class="container">
      <div class="section-head">
        <span class="eyebrow">Case studies</span>'''
if insert_marker not in s:
    fail('use-cases case-study section marker missing')
s = s.replace(insert_marker, onboarding_section + insert_marker, 1)
for required in ['id="onboarding-patterns"', 'Q1 A* · Q2 C · Q3 A · Q4 A', 'Q6 working-contract example', 'Creative development', 'Strategy &amp; decisions']:
    if required not in s:
        fail('use-cases missing required content: ' + required)
write(name, s)


# ------------------------------------------------------------
# ABOUT
# Keep portrait/origin story intact, but make current AIR visibly
# present rather than relying on subtle sentence edits.
# ------------------------------------------------------------
name = 'about.html'
s = read(name)
about_today = '''  <section class="section" id="air-today" style="padding-top:0">
    <div class="container">
      <div class="section-head">
        <span class="eyebrow">AIR today · 2.4.3</span>
        <h2>AI work, carried forward.</h2>
        <p>The original idea was a structured AI teammate. Current AIR is more explicit: a prompt-based framework that binds one material task at a time, keeps the working contract inspectable, carries recorded project state through Handoff, and layers specialist capability without giving those layers independent authority.</p>
      </div>
      <div class="principles">
        <div class="principle"><div class="pk">Focused</div><h4>One material task at a time</h4><p>Orbit 0 holds the current executing task and its bound AIR_ARTIFACT. Queued and deferred work stay visible without competing for execution.</p></div>
        <div class="principle"><div class="pk">Fluid</div><h4>Continue from explicit state</h4><p>The Handoff Card carries the recorded working state into another compatible AIR session, where it is validated and rebound instead of rebuilding the project from the whole transcript.</p></div>
        <div class="principle"><div class="pk">AIR</div><h4>The project is not one session</h4><p>The framework keeps project state outside a single provider's private session state, so compatible hosts can continue the same working record while the host model still shapes the output.</p></div>
        <div class="principle"><div class="pk">Boundary</div><h4>Visible state, not hidden reasoning</h4><p>AIR surfaces its declared state, gates, assumptions and evidence posture. It does not claim access to hidden chain-of-thought or deterministic backend enforcement without external evidence.</p></div>
      </div>
    </div>
  </section>

'''
principles_marker = '''  <section class="section" style="padding-top:0">
    <div class="container">
      <div class="section-head">
        <span class="eyebrow" id="principles">Principles</span>'''
if principles_marker not in s:
    fail('about principles marker missing')
s = s.replace(principles_marker, about_today + principles_marker, 1)
for required in ['id="air-today"', 'AIR today · 2.4.3', 'One material task at a time', 'Visible state, not hidden reasoning']:
    if required not in s:
        fail('about missing required current-state content: ' + required)
write(name, s)


# Global invariants for this patch.
if set(CHANGED) != {'how-it-works.html', 'air-docs.html', 'use-cases.html', 'about.html'}:
    fail('unexpected changed-file bookkeeping: ' + repr(CHANGED))
if read('index.html') != Path('/tmp/index-baseline').read_text(encoding='utf-8') if Path('/tmp/index-baseline').exists() else False:
    fail('index.html changed unexpectedly')

print('PATCH_OK')
for item in CHANGED:
    print(item)
