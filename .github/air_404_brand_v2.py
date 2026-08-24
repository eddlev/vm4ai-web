from pathlib import Path
import re

PAGE = Path('public/404.html')
ABOUT = Path('public/about.html')

FOOTER_RE = re.compile(r'<footer class="site-footer">.*?</footer>', re.S)
HEADER_RE = re.compile(r'<header class="site-header">.*?</header>', re.S)
STYLE_RE = re.compile(r'/\* ---------- 404 ---------- \*/.*?/\* ---------- attentive header eye ---------- \*/', re.S)
MAIN_RE = re.compile(r'<main>.*?</main>', re.S)

text = PAGE.read_text(encoding='utf-8')
about = ABOUT.read_text(encoding='utf-8')

old_header = HEADER_RE.search(text)
old_footer = FOOTER_RE.search(text)
about_footer = FOOTER_RE.search(about)
if not old_header or not old_footer or not about_footer:
    raise SystemExit('Required header/footer block missing')
if old_footer.group(0) != about_footer.group(0):
    raise SystemExit('404 footer is not canonical before redesign')
if len(STYLE_RE.findall(text)) != 1:
    raise SystemExit('Expected exactly one 404 style block')
if len(MAIN_RE.findall(text)) != 1:
    raise SystemExit('Expected exactly one main block')

new_styles = r'''/* ---------- 404 ---------- */
.nf-main{overflow:hidden}
.nf-section{padding:clamp(3.2rem,7vw,6.2rem) 0}
.nf-wrap{position:relative;max-width:58rem;margin:0 auto;text-align:center;border:1px solid var(--border-strong);border-radius:28px;padding:clamp(2rem,5vw,4.25rem);background-color:var(--surface);background-image:linear-gradient(rgba(201,162,39,.055) 1px,transparent 1px),linear-gradient(90deg,rgba(201,162,39,.055) 1px,transparent 1px);background-size:28px 28px;box-shadow:var(--card-shadow);overflow:hidden}
.nf-wrap::after{content:"";position:absolute;inset:auto -12% -45% -12%;height:58%;background:radial-gradient(circle at center,color-mix(in srgb,var(--brass) 10%,transparent),transparent 68%);pointer-events:none}
.nf-stage{position:relative;width:min(280px,66vw);aspect-ratio:1;margin:0 auto .65rem;display:grid;place-items:center}
.nf-orbit{position:absolute;inset:7%;border:1px dashed color-mix(in srgb,var(--brass) 58%,transparent);border-radius:50%;animation:nf-orbit-spin 18s linear infinite}
.nf-orbit::before,.nf-orbit::after{content:"";position:absolute;width:8px;height:8px;border-radius:50%;background:var(--brass);box-shadow:0 0 0 5px color-mix(in srgb,var(--brass) 10%,transparent)}
.nf-orbit::before{left:8%;top:20%}.nf-orbit::after{right:4%;bottom:25%;opacity:.45}
.eye{width:clamp(112px,20vw,148px);height:auto;display:block;filter:drop-shadow(0 18px 32px rgba(0,0,0,.12))}
.eye .frame{fill:var(--surface-2);stroke:var(--brass)}
.eye .pupil{fill:var(--ember)}
.eye-pupil{transform-box:fill-box;transform-origin:center;animation:eye-search 5.2s ease-in-out infinite}
@keyframes eye-search{0%,10%{transform:translate(0,0) scaleY(1)}20%,28%{transform:translate(-7px,1px) scaleY(1)}38%,46%{transform:translate(7px,1px) scaleY(1)}56%,64%{transform:translate(0,-6px) scaleY(1)}72%,84%{transform:translate(0,0) scaleY(1)}92%,100%{transform:translate(0,0) scaleY(.16)}}
@keyframes nf-orbit-spin{to{transform:rotate(360deg)}}
.nf-kicker{font-family:var(--font-mono);font-size:.78rem;letter-spacing:.16em;text-transform:uppercase;color:var(--brass)}
.nf-wrap h1{font-size:clamp(2.25rem,1.45rem+3vw,4.15rem);margin:.72rem auto 1rem;max-width:15ch;line-height:1.02;letter-spacing:-.045em}
.nf-lead{color:var(--muted);max-width:38rem;margin:0 auto 1.8rem;font-size:clamp(1rem,.94rem+.3vw,1.12rem)}
.nf-diagnostic{position:relative;z-index:1;max-width:38rem;margin:0 auto 1.8rem;text-align:left;background:color-mix(in srgb,var(--surface-2) 94%,transparent);border:1px solid var(--border);border-radius:15px;overflow:hidden;box-shadow:0 14px 38px rgba(0,0,0,.08)}
.nf-diagnostic-head{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:.8rem 1rem;border-bottom:1px solid var(--border);font-family:var(--font-mono);font-size:.7rem;text-transform:uppercase;letter-spacing:.1em;color:var(--subtle)}
.nf-signal{display:inline-flex;align-items:center;gap:.45rem;color:var(--brass)}
.nf-signal::before{content:"";width:7px;height:7px;border-radius:50%;background:var(--ember)}
.nf-diagnostic dl{display:grid;grid-template-columns:minmax(112px,.7fr) 1.3fr;margin:0;padding:.9rem 1rem 1rem;font-family:var(--font-mono);font-size:.8rem;line-height:1.55}
.nf-diagnostic dt,.nf-diagnostic dd{margin:0;padding:.38rem 0;border-bottom:1px solid color-mix(in srgb,var(--border) 70%,transparent)}
.nf-diagnostic dt{color:var(--subtle)}.nf-diagnostic dd{color:var(--text);overflow-wrap:anywhere}
.nf-diagnostic dt:nth-last-of-type(1),.nf-diagnostic dd:nth-last-of-type(1){border-bottom:0}
.nf-state-warn{color:var(--ember-ink)!important}.nf-state-ok{color:var(--brass)!important}
.nf-actions{position:relative;z-index:1;display:flex;gap:.75rem;justify-content:center;flex-wrap:wrap}
.nf-footnote{position:relative;z-index:1;margin:1.15rem 0 0!important;font-family:var(--font-mono);font-size:.72rem;color:var(--subtle)!important}
@media(max-width:560px){.nf-wrap{border-radius:20px;padding:1.6rem 1rem 2rem}.nf-stage{width:min(220px,62vw)}.nf-diagnostic dl{grid-template-columns:1fr}.nf-diagnostic dt{padding-bottom:0;border-bottom:0}.nf-diagnostic dd{padding-top:.1rem}.nf-actions{flex-direction:column}.nf-actions .btn{width:100%}}
@media(prefers-reduced-motion:reduce){.nf-orbit,.eye-pupil{animation:none!important}}

/* ---------- attentive header eye ---------- */'''

new_main = r'''<main class="nf-main">
  <section class="section nf-section">
    <div class="container">
      <div class="nf-wrap">
        <div class="nf-stage" aria-hidden="true">
          <div class="nf-orbit"></div>
          <svg class="eye" viewBox="0 0 64 64">
            <rect class="frame" x="9.5" y="9.5" width="45" height="45" rx="13" stroke-width="5"/>
            <g class="eye-pupil"><circle class="pupil" cx="32" cy="32" r="8.5"/></g>
          </svg>
        </div>
        <div class="nf-kicker">404 · route not found</div>
        <h1>This page didn't make the handoff.</h1>
        <p class="nf-lead">We checked the current state, the queue, and under the sofa. Nothing. AIR could make a page up, but that would rather defeat the point.</p>

        <div class="nf-diagnostic" aria-label="Route diagnostic">
          <div class="nf-diagnostic-head"><span>route diagnostic</span><span class="nf-signal">recovery available</span></div>
          <dl>
            <dt>requested_route</dt><dd id="nf-route">unknown</dd>
            <dt>route_state</dt><dd class="nf-state-warn">NOT_FOUND</dd>
            <dt>fabrication</dt><dd>REJECTED</dd>
            <dt>next_step</dt><dd class="nf-state-ok">CHOOSE_A_REAL_ROUTE</dd>
          </dl>
        </div>

        <div class="nf-actions">
          <a class="btn btn-primary" href="index.html">Return home</a>
          <a class="btn btn-outline" href="how-it-works.html">How AIR works</a>
          <a class="btn btn-outline" href="https://github.com/eddlev/vm4ai-air-kit" target="_blank" rel="noopener">Open GitHub</a>
        </div>
        <p class="nf-footnote">No pages were hallucinated in the making of this 404.</p>
      </div>
    </div>
  </section>
  <script>
  (function(){
    var route=document.getElementById('nf-route');
    if(route)route.textContent=location.pathname+location.search;
  })();
  </script>
</main>'''

updated = text
updated = updated.replace('<meta name="description" content="Page not found. AIR fails closed rather than invent one.">', '<meta name="description" content="This page did not make the handoff. An AIR-branded 404 with a safe route back to the project.">\n<meta name="robots" content="noindex,follow">')
updated = updated.replace('<meta property="og:description" content="Page not found. AIR fails closed rather than invent one.">', '<meta property="og:description" content="This page did not make the handoff. Pick a route that exists and carry on.">')
updated = updated.replace('<meta name="twitter:description" content="Page not found. AIR fails closed rather than invent one.">', '<meta name="twitter:description" content="This page did not make the handoff. Pick a route that exists and carry on.">')
updated, n_style = STYLE_RE.subn(new_styles, updated)
updated, n_main = MAIN_RE.subn(new_main, updated)
if n_style != 1 or n_main != 1:
    raise SystemExit(f'Replacement count mismatch: style={n_style} main={n_main}')

new_header = HEADER_RE.search(updated)
new_footer = FOOTER_RE.search(updated)
if not new_header or new_header.group(0) != old_header.group(0):
    raise SystemExit('Header changed unexpectedly')
if not new_footer or new_footer.group(0) != about_footer.group(0):
    raise SystemExit('Canonical footer changed unexpectedly')
if '"air_object"' in updated or 'AIR_OBJECT' in updated:
    raise SystemExit('Fake formal AIR object residue remains')
if "route.textContent=location.pathname+location.search" not in updated:
    raise SystemExit('Safe missing-route rendering is absent')
if 'prefers-reduced-motion:reduce' not in updated:
    raise SystemExit('Reduced-motion handling is absent')

PAGE.write_text(updated, encoding='utf-8')
print('404 redesign applied and verified.')
print('Header preserved: PASS')
print('Canonical About footer preserved: PASS')
print('Formal-object boundary: PASS')
print('Safe route rendering: PASS')
print('Reduced-motion handling: PASS')
