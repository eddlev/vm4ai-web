#!/usr/bin/env python3
from pathlib import Path
import html
import re
import sys

ROOT = Path('.')
PUBLIC = ROOT / 'public'
TEMPLATE = PUBLIC / 'glossary.html'
DOCS = PUBLIC / 'air-docs.html'
SITEMAP = PUBLIC / 'sitemap.xml'

if not TEMPLATE.is_file():
    raise SystemExit('glossary template missing')

base = TEMPLATE.read_text(encoding='utf-8')

# Dedicated docs CSS, layered onto the existing vm4ai.com page shell.
docs_css = r'''
/* ---------- AIR documentation ---------- */
.docs-version{display:inline-flex;flex-wrap:wrap;gap:.45rem .8rem;align-items:center;margin-top:.6rem;padding:.55rem .8rem;border:1px solid var(--border-strong);border-radius:10px;background:var(--surface);font-family:var(--font-mono);font-size:.74rem;color:var(--muted)}
.docs-version strong{color:var(--brass);font-weight:500}
.docs-layout{display:grid;grid-template-columns:minmax(13rem,17rem) minmax(0,1fr);gap:clamp(2rem,5vw,4rem);align-items:start}
.docs-toc{position:sticky;top:88px;border:1px solid var(--border);border-radius:14px;background:var(--surface);padding:1rem}
.docs-toc h2{font-family:var(--font-mono);font-size:.72rem;letter-spacing:.12em;text-transform:uppercase;color:var(--brass);margin:0 0 .65rem}
.docs-toc a{display:block;color:var(--muted);text-decoration:none;font-size:.88rem;padding:.28rem .2rem}
.docs-toc a:hover{color:var(--text)}
.docs-main{min-width:0}
.docs-section{scroll-margin-top:84px;padding:0 0 3.5rem;margin:0 0 3.5rem;border-bottom:1px solid var(--border)}
.docs-section:last-child{border-bottom:0;margin-bottom:0}
.docs-section>h2{font-size:clamp(1.65rem,1.25rem+1.4vw,2.25rem);margin:0 0 .8rem}
.docs-section>p.lead{font-size:1.08rem;color:var(--muted);max-width:48rem}
.docs-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem;margin:1.3rem 0}
.docs-card{border:1px solid var(--border);border-radius:13px;background:var(--surface);padding:1.15rem 1.2rem}
.docs-card h3{font-size:1.04rem;margin:0 0 .45rem;font-weight:600}
.docs-card p{color:var(--muted);font-size:.93rem;margin:0}
.docs-card .use{display:block;margin-top:.65rem;padding-top:.65rem;border-top:1px solid var(--border);font-family:var(--font-mono);font-size:.76rem;color:var(--brass)}
.docs-table{width:100%;border-collapse:collapse;margin:1.2rem 0;font-size:.92rem}
.docs-table th,.docs-table td{text-align:left;vertical-align:top;padding:.75rem .8rem;border-bottom:1px solid var(--border)}
.docs-table th{font-family:var(--font-mono);font-size:.7rem;letter-spacing:.08em;text-transform:uppercase;color:var(--brass);font-weight:500}
.docs-table td{color:var(--muted)}
.docs-table td:first-child{color:var(--text);font-weight:500}
.docs-table code,.docs-main code{font-family:var(--font-mono);font-size:.86em;background:var(--surface-2);padding:.08rem .32rem;border-radius:5px;color:var(--text)}
.docs-list{padding-left:1.25rem;color:var(--muted)}
.docs-list li{margin:.45rem 0}
.docs-note{margin:1.2rem 0;border-left:3px solid var(--brass);background:var(--surface);padding:1rem 1.15rem;border-radius:0 11px 11px 0;color:var(--muted)}
.docs-note strong{color:var(--text)}
.docs-steps{counter-reset:docsstep;display:grid;gap:.8rem;margin:1.2rem 0}
.docs-step{counter-increment:docsstep;display:grid;grid-template-columns:2rem 1fr;gap:.75rem;border:1px solid var(--border);border-radius:12px;padding:1rem;background:var(--surface)}
.docs-step:before{content:counter(docsstep,decimal-leading-zero);font-family:var(--font-mono);color:var(--brass);font-size:.78rem;padding-top:.1rem}
.docs-step h3{font-size:1rem;margin:0 0 .3rem}.docs-step p{margin:0;color:var(--muted);font-size:.92rem}
.docs-object{display:grid;grid-template-columns:minmax(12rem,17rem) 1fr;gap:.5rem 1rem;padding:.75rem 0;border-bottom:1px solid var(--border)}
.docs-object:last-child{border-bottom:0}.docs-object dt{font-family:var(--font-mono);font-size:.82rem;color:var(--brass)}.docs-object dd{margin:0;color:var(--muted);font-size:.92rem}
@media(max-width:860px){.docs-layout{grid-template-columns:1fr}.docs-toc{position:static;columns:2}.docs-grid{grid-template-columns:1fr}}
@media(max-width:560px){.docs-toc{columns:1}.docs-object{grid-template-columns:1fr}.docs-table{display:block;overflow-x:auto;white-space:normal}}
'''

if '/* ---------- AIR documentation ---------- */' not in base:
    base = base.replace('</style>', docs_css + '\n</style>', 1)

# Head metadata.
replacements = {
    '<title>AIR glossary &amp; modifiers — AIR by VM4AI</title>': '<title>AIR documentation — AIR by VM4AI</title>',
    '<meta name="description" content="Plain-language definitions for AIR vocabulary, governance records, continuity, capability layers, and the four supported system modifiers.">': '<meta name="description" content="Canonical AIR technical documentation for the v0.4 release line: setup, runtime, objects, modifiers, evidence, handoff, packages, anti-drift checks, best practices, and future adapters.">',
    '<link rel="canonical" href="https://vm4ai.com/glossary.html">': '<link rel="canonical" href="https://vm4ai.com/air-docs.html">',
    '<meta property="og:title" content="AIR glossary &amp; modifiers — AIR by VM4AI">': '<meta property="og:title" content="AIR documentation — AIR by VM4AI">',
    '<meta property="og:description" content="Plain-language definitions for AIR vocabulary and the four supported system modifiers.">': '<meta property="og:description" content="Canonical technical documentation for AIR v0.4 and Core Runtime 2.4.2.">',
    '<meta property="og:url" content="https://vm4ai.com/glossary.html">': '<meta property="og:url" content="https://vm4ai.com/air-docs.html">',
    '<meta name="twitter:title" content="AIR glossary &amp; modifiers — AIR by VM4AI">': '<meta name="twitter:title" content="AIR documentation — AIR by VM4AI">',
    '<meta name="twitter:description" content="Plain-language definitions for AIR vocabulary and the four supported system modifiers.">': '<meta name="twitter:description" content="Canonical technical documentation for AIR v0.4 and Core Runtime 2.4.2.">',
}
for old, new in replacements.items():
    if old not in base:
        raise SystemExit(f'docs template metadata marker missing: {old[:60]}')
    base = base.replace(old, new, 1)

main = r'''
<main>
  <section class="hero" style="padding-bottom:1.5rem">
    <div class="container">
      <span class="eyebrow">AIR documentation</span>
      <h1 style="font-size:clamp(2.2rem,1.6rem+2.4vw,3.4rem);margin:1rem 0 1.1rem">The AIR technical reference.</h1>
      <p class="sub" style="max-width:48rem">Setup, runtime behavior, formal objects, modifiers, evidence, handoff, specialist packages, anti-drift checks, and implementation best practices. This is the canonical human-readable reference for the current AIR v0.4 release line.</p>
      <div class="docs-version"><strong>Release line</strong> AIR Kit v0.4.0 candidate <span>·</span> Core 2.4.2 <span>·</span> Control 2.4.2 <span>·</span> Handoff schema 2.2.0</div>
    </div>
  </section>

  <section class="section" style="padding-top:1.5rem">
    <div class="container docs-layout">
      <aside class="docs-toc" aria-label="AIR documentation sections">
        <h2>On this page</h2>
        <a href="#purpose">Purpose &amp; architecture</a>
        <a href="#prompt-based">Why prompt-based</a>
        <a href="#quick-start">Quick start</a>
        <a href="#onboarding">Onboarding</a>
        <a href="#runtime">Runtime model</a>
        <a href="#modifiers">System modifiers</a>
        <a href="#objects">Formal objects</a>
        <a href="#alignment">Alignment watchdog</a>
        <a href="#evidence">Evidence &amp; testing</a>
        <a href="#handoff">Handoff continuity</a>
        <a href="#packages">Profiles &amp; packages</a>
        <a href="#best-practices">Best practices</a>
        <a href="#troubleshooting">Troubleshooting</a>
        <a href="#adapters">Hooks &amp; adapters</a>
        <a href="#compatibility">Compatibility boundary</a>
      </aside>

      <div class="docs-main">
        <section class="docs-section" id="purpose">
          <h2>Purpose &amp; architecture</h2>
          <p class="lead">AIR (AI Resource) is a portable prompt-runtime framework for cooperative project work. It gives the host model an explicit working contract before generation: scope, active task, allowed and forbidden actions, evidence requirements, approval gates, review state, and handoff continuity.</p>
          <div class="docs-grid">
            <div class="docs-card"><h3>Prompt-runtime control</h3><p>AIR is loaded into the model context and shapes the response from the start. It is not a post-processing layer that rewrites an already-generated answer.</p></div>
            <div class="docs-card"><h3>Human authority</h3><p>The user provides direction, source truth, corrections, approvals, and irreversible decisions. AIR protects structure, evidence boundaries, blockers, continuity, and next actions.</p></div>
            <div class="docs-card"><h3>One active execution record</h3><p>Material execution is bound to exactly one current Orbit 0 <code>AIR_ARTIFACT</code>. Other records affect execution only when compiled into or explicitly referenced by it.</p></div>
            <div class="docs-card"><h3>Assurance boundary</h3><p>Prompt AIR can materially shape behavior, but it does not claim hidden reasoning access or deterministic backend enforcement without external evidence.</p></div>
          </div>
        </section>

        <section class="docs-section" id="prompt-based">
          <h2>Why AIR is prompt-based</h2>
          <p class="lead">Prompt-based is an intentional portability choice, not an attempt to disguise deterministic infrastructure as a prompt. AIR keeps the core project contract outside any single vendor's private runtime so the project can move with the user.</p>
          <div class="docs-grid">
            <div class="docs-card"><h3>Vendor independence</h3><p>AIR does not require one provider's private project state, permission model, memory system, or agent lifecycle to define the working contract.</p><span class="use">Use case · change providers without redesigning project governance</span></div>
            <div class="docs-card"><h3>Platform-agnostic core</h3><p>Orbit, artifacts, gates, evidence boundaries, approvals, and Handoff remain the same AIR concepts across compatible model interfaces even when host features differ.</p><span class="use">Use case · use the same AIR working model in chat, coding, and workflow interfaces</span></div>
            <div class="docs-card"><h3>Cross-platform portability</h3><p>Model and platform choices change. AIR keeps explicit project state in portable files and records instead of making the project dependent on a single host's private session state.</p><span class="use">Use case · move active work when a new model or platform becomes preferable</span></div>
            <div class="docs-card"><h3>Multi-session continuity</h3><p>The Handoff Card serializes explicit continuation state so a receiving compatible session can validate, rebind, and continue the project.</p><span class="use">Use case · continue a long project across sessions or compatible platforms</span></div>
            <div class="docs-card"><h3>Progressive enforcement</h3><p>The prompt layer works without dedicated infrastructure. Host-specific hooks, gateways, and adapters can later add mechanical permissions, receipts, independent tests, or action blocking.</p><span class="use">Use case · start portable, then add stronger enforcement where the host supports it</span></div>
          </div>
          <div class="docs-note"><strong>Important:</strong> platform-agnostic does not mean every host behaves identically. AIR separates the portable contract from host-specific capabilities and treats compatibility as something to verify, not assume permanently.</div>
        </section>

        <section class="docs-section" id="quick-start">
          <h2>Quick start</h2>
          <p class="lead">A fresh AIR v2 project uses the current five-file foundation. All required files must be completely available to the host; a truncated or partial load is not a valid AIR boot.</p>
          <div class="docs-steps">
            <div class="docs-step"><div><h3>Load the five foundation files</h3><p><code>AIR_CORE_RUNTIME.md</code>, <code>AIR_CONTROL_SURFACE.md</code>, <code>AIR_GOV.md</code>, <code>AIR_DEFAULT_STARTER_PROFILE.json</code>, and <code>AIR_HANDOFF_CARD_TEMPLATE.json</code>.</p></div></div>
            <div class="docs-step"><div><h3>Start AIR</h3><p>Type <code>Start a new AIR project.</code> The activation phrase starts validation and onboarding; it does not silently answer Q1.</p></div></div>
            <div class="docs-step"><div><h3>Complete Q1–Q6</h3><p>AIR asks the deterministic onboarding questions in order and compiles the working agreement from your answers and supplied sources.</p></div></div>
            <div class="docs-step"><div><h3>Work against the bound artifact</h3><p>Once <code>ARTIFACT_BOUND_EXECUTION</code> is established, material work proceeds against exactly one current active <code>AIR_ARTIFACT</code>.</p></div></div>
          </div>
          <div class="docs-note"><strong>Context limits:</strong> tokenization, attachments, and context windows vary by provider and model. AIR does not publish one universal safe token threshold. Verify complete load on the host you actually use.</div>
        </section>

        <section class="docs-section" id="onboarding">
          <h2>Onboarding</h2>
          <p class="lead">AIR does not infer the project branch. Q1 selects the starting path, then the remaining questions establish rigor, ambiguity handling, continuity preferences, project description, and the human–AIR working agreement.</p>
          <table class="docs-table"><thead><tr><th>Question</th><th>Purpose</th><th>Best practice</th></tr></thead><tbody>
            <tr><td>Q1</td><td>Select new project, import, Handoff continuation, or explain AIR first.</td><td>Choose explicitly; never let the branch be inferred from surrounding context.</td></tr>
            <tr><td>Q2</td><td>Set review rigor.</td><td>Match scrutiny to blast radius rather than using maximum ceremony everywhere.</td></tr>
            <tr><td>Q3</td><td>Set ambiguity handling.</td><td>Resolve uncertainty early when a silent guess could materially change execution.</td></tr>
            <tr><td>Q4 / Q4D</td><td>Set continuity and, where selected, delivery calibration.</td><td>Keep the answer deterministic and preserve it through Handoff.</td></tr>
            <tr><td>Q5</td><td>Describe the project and provide sources.</td><td>State the real goal, constraints, and authoritative inputs; unknowns can become research tasks.</td></tr>
            <tr><td>Q6 / Q6D</td><td>Define how the user and AIR work together.</td><td>Make approval boundaries, challenge level, delivery form, and assumptions explicit.</td></tr>
          </tbody></table>
        </section>

        <section class="docs-section" id="runtime">
          <h2>Runtime model</h2>
          <p class="lead">AIR separates project state from active execution. The project may contain many queued or deferred tasks, but Orbit 0 is the single current material task and exactly one <code>AIR_ARTIFACT</code> binds its execution.</p>
          <ul class="docs-list">
            <li><strong>Orbit 0</strong> — the current material task and active step.</li>
            <li><strong>Orbit 1</strong> — queued work with explicit resume conditions.</li>
            <li><strong>Orbit 2</strong> — deferred work that is intentionally outside the current execution surface.</li>
            <li><strong>Binding</strong> — sources, methods, profiles, packages, approvals, and instructions influence material execution only through the sole active artifact or its explicit references.</li>
            <li><strong>Fail-closed behavior</strong> — missing material evidence, ambiguity, approval, package input, or incompatible state blocks the affected action instead of being silently guessed.</li>
          </ul>
        </section>

        <section class="docs-section" id="modifiers">
          <h2>System modifiers</h2>
          <p class="lead">AIR v2 intentionally has four canonical system modifiers. Ordinary questions about status, blockers, evidence, scope, readiness, validation, or Handoff do not require command syntax.</p>
          <table class="docs-table"><thead><tr><th>Modifier</th><th>Effect</th><th>Best practice</th></tr></thead><tbody>
            <tr><td><code>air -o on</code></td><td>Use full object visibility: every formal AIR object that is generated is printed.</td><td>AIR v2 already defaults to <code>ALL_OBJECTS</code>; use this to explicitly restore full visibility after compact mode.</td></tr>
            <tr><td><code>air -o -min</code></td><td>Explicit user-selected compact visibility mode.</td><td>Use only when you want less optional repetition. Required transitions, gates, recovery records, periodic alignment records, and Handoff records still print.</td></tr>
            <tr><td><code>air -t on</code></td><td>Requests <code>FULL_TEST_EVIDENCE</code> for subsequent test/evaluation runs when available.</td><td>Enable before a run whose review or approval requires the fuller evidence package.</td></tr>
            <tr><td><code>air -t off</code></td><td>Uses the default <code>SUMMARY_ONLY</code> test-evidence delivery mode.</td><td>Use when a summary is sufficient; it does not weaken the underlying approval threshold.</td></tr>
          </tbody></table>
          <div class="docs-note"><strong>No modifier bypasses governance.</strong> Object or evidence display preferences do not override scope, approvals, safety, evidence requirements, or required AIR records.</div>
        </section>

        <section class="docs-section" id="objects">
          <h2>Formal AIR objects</h2>
          <p class="lead">AIR objects expose AIR's declared control state. Structured JSON makes those records portable and machine-readable; it does not turn model-generated state into independent proof of external events.</p>
          <dl>
            <div class="docs-object"><dt>AIR_SESSION</dt><dd>Session-level runtime state, activation, load integrity, visibility authority, watchdog counters, and other current session controls.</dd></div>
            <div class="docs-object"><dt>AIR_PRIMED_ONBOARDING</dt><dd>Fresh-boot onboarding readiness/state when that boot-stage record is generated.</dd></div>
            <div class="docs-object"><dt>AIR_PROJECT_INITIALIZATION_BRIEF</dt><dd>The compiled project framing created from onboarding and initial sources.</dd></div>
            <div class="docs-object"><dt>AIR_PROJECT_EXECUTION_MAP</dt><dd>Current project task map: Orbit 0, queued work, deferred work, and resume conditions.</dd></div>
            <div class="docs-object"><dt>AIR_ARTIFACT</dt><dd>The sole active execution record for the current material task and step.</dd></div>
            <div class="docs-object"><dt>AIR_ACTIVE_CONTRACT</dt><dd>The explicit execution contract when surfaced separately: scope, allowed actions, constraints, and obligations.</dd></div>
            <div class="docs-object"><dt>AIR_GATE</dt><dd>A decision checkpoint such as ALLOW, REVIEW, or REJECT for a consequential transition or action.</dd></div>
            <div class="docs-object"><dt>AIR_VALIDATION_REPORT</dt><dd>Validation target, basis, checks, limitations, evidence references, and decision.</dd></div>
            <div class="docs-object"><dt>AIR_ALIGNMENT_CHECK</dt><dd>Minimal anti-drift watchdog record: whether drift was detected, the user-message cadence, and the linked validation report.</dd></div>
            <div class="docs-object"><dt>AIR_ERROR</dt><dd>Fail-closed error record for load, compatibility, evidence, binding, or other governed failures.</dd></div>
            <div class="docs-object"><dt>AIR_ACTION_AUTHORIZATION</dt><dd>Single-use authorization record before a material external action is attempted.</dd></div>
            <div class="docs-object"><dt>AIR_ACTION_RECEIPT</dt><dd>Observed result record after an authorized material action is attempted.</dd></div>
            <div class="docs-object"><dt>AIR_PRIOR_EFFECT_RECORD</dt><dd>Recovery record when AIR detects a material effect that occurred outside the current valid authorization path.</dd></div>
            <div class="docs-object"><dt>AIR_HANDOFF_CARD</dt><dd>Portable transfer record for explicit project/session continuation state.</dd></div>
          </dl>
        </section>

        <section class="docs-section" id="alignment">
          <h2>Alignment watchdog</h2>
          <p class="lead">AIR 2.4.2 adds a periodic anti-drift checkpoint alongside the existing event-triggered watchdog. The purpose is to make long-session drift visible even when no single material action happens to trigger a separate reconciliation.</p>
          <div class="docs-grid">
            <div class="docs-card"><h3>Cadence</h3><p>After <code>ARTIFACT_BOUND_EXECUTION</code> begins, AIR increments a dedicated counter once per substantive user message. Every fifth counted user message triggers <code>PERIODIC_ALIGNMENT_CHECK</code>.</p></div>
            <div class="docs-card"><h3>What does not count</h3><p>Assistant replies, tool calls, connector callbacks, system/host events, hidden host events, and <code>artifact_revision</code> do not advance the cadence.</p></div>
            <div class="docs-card"><h3>No drift</h3><p>AIR prints <code>AIR_ALIGNMENT_CHECK</code> followed by <code>AIR_VALIDATION_REPORT</code>, records <code>drift_detected=false</code>, and continues.</p></div>
            <div class="docs-card"><h3>Drift</h3><p>AIR prints both records, sets <code>DRIFT_DETECTED</code>, triggers <code>ALIGNMENT_RECOVERY_SURFACE</code>, and stops affected governed work until coherent state is restored.</p></div>
          </div>
          <div class="docs-note"><strong>Prompt-layer boundary:</strong> the cadence is a non-waivable AIR Core invariant, but prompt AIR cannot make it cryptographically immutable. A future host adapter can enforce the same counter/check mechanically.</div>
        </section>

        <section class="docs-section" id="evidence">
          <h2>Evidence &amp; testing</h2>
          <p class="lead">AIR separates a surfaced governance record from independent evidence that something happened outside the prompt runtime.</p>
          <h3 style="margin:1.4rem 0 .5rem">Governance record classes</h3>
          <table class="docs-table"><thead><tr><th>Class</th><th>Meaning</th></tr></thead><tbody>
            <tr><td><code>SURFACED_OUTPUT_GOVERNANCE_RECORD</code></td><td>A visible AIR declaration/state record produced in the response.</td></tr>
            <tr><td><code>SOURCE_SUPPORTED_GOVERNANCE_RECORD</code></td><td>A record whose material claims are supported by identified supplied/retrieved sources.</td></tr>
            <tr><td><code>TOOL_OBSERVED_GOVERNANCE_RECORD</code></td><td>A record grounded in an observed tool result, such as repository state or executed checks.</td></tr>
            <tr><td><code>BACKEND_ENFORCED_GOVERNANCE_RECORD</code></td><td>Reserved for a control actually enforced by evidenced backend/client infrastructure.</td></tr>
          </tbody></table>
          <h3 style="margin:1.6rem 0 .5rem">Test evidence classes</h3>
          <table class="docs-table"><thead><tr><th>Class</th><th>Use</th></tr></thead><tbody>
            <tr><td><code>REPRODUCIBLE_EXECUTABLE</code></td><td>Executable checks with recorded run identity, exact inputs/environment, repeat executions, and compared decisions.</td></tr>
            <tr><td><code>REPLAYABLE_EVALUATION</code></td><td>Evaluation/model runs that can be replayed from recorded inputs but are not claimed deterministic in the executable sense.</td></tr>
            <tr><td><code>MANUAL_REVIEW_REQUIRED</code></td><td>Qualitative or operator judgment that remains separate from automated pass counts.</td></tr>
          </tbody></table>
          <div class="docs-note"><strong>A pass count is not enough.</strong> A statement such as “150/150 passed” does not by itself establish deterministic reproducibility. A release-grade executable claim needs the external run identity, inputs, environment/network/randomness policy, independent repeated runs, and matching decision fingerprints.</div>
        </section>

        <section class="docs-section" id="handoff">
          <h2>Handoff continuity</h2>
          <p class="lead">The Handoff Card carries explicit AIR state into another compatible session. The receiving runtime validates the current foundation, validates/restores the serialized state, and rebinds the active artifact before material execution resumes.</p>
          <ul class="docs-list">
            <li>Preserve the current active artifact and its binding/revision state.</li>
            <li>Preserve Q4/Q4D, Q6/Q6D, object visibility and its authority source, periodic alignment counter/check state, current step, blockers, approval scope, governance state, and specialist binding state when material.</li>
            <li>A Handoff Card without the active artifact may support migration or review, but cannot resume material execution.</li>
            <li>Handoff is explicit state continuity; it is not hidden-state transfer and does not promise identical inference across models or platforms.</li>
            <li>Treat a populated Handoff Card as project-sensitive data because it may contain goals, blockers, source references, approvals, and working agreements.</li>
          </ul>
        </section>

        <section class="docs-section" id="packages">
          <h2>Profiles, specialists &amp; method packs</h2>
          <p class="lead">Optional capability material is available but unbound until AIR validates compatibility, selects it for the current task, obtains approval where required, and compiles or explicitly references it through the active artifact.</p>
          <div class="docs-grid">
            <div class="docs-card"><h3>Grounding Specialist</h3><p>Supports evidence discipline, cooperative challenge, domain terminology, and bounded grounding workflows. Complete method-governed operation uses its coupled package.</p></div>
            <div class="docs-card"><h3>AI Governance Specialist</h3><p>Supports AI-governance source authority, lifecycle controls, evidence planning, claim boundaries, and conditional agentic-system governance.</p></div>
            <div class="docs-card"><h3>Capability Ecology Architect</h3><p>Supports capability decomposition, human-to-machine translation, domain capability registration, and capability-ecology design.</p></div>
            <div class="docs-card"><h3>Specification-First Verification</h3><p>Currently remains a standalone experimental Method Pack under <code>profiles/specification first method pack/</code>. It is not represented as a full specialist package until additional components are justified and tested.</p></div>
          </div>
          <div class="docs-note"><strong>Attachment is not activation.</strong> Supplying a profile/package establishes availability only. It does not establish freshness, compatibility, task fit, approval, binding, execution, or evidence sufficiency.</div>
        </section>

        <section class="docs-section" id="best-practices">
          <h2>Best practices</h2>
          <ul class="docs-list">
            <li><strong>Keep the foundation canonical.</strong> Use one current authoritative file per foundation role; keep backups and superseded variants outside the active upload set.</li>
            <li><strong>Let ambiguity surface.</strong> When a material choice would otherwise be guessed, resolve it or keep the affected action blocked.</li>
            <li><strong>Use evidence before confidence.</strong> If a claim depends on a repository, source, tool, deployment, operator, or backend event, retrieve/observe the corresponding evidence.</li>
            <li><strong>Enable full test evidence before the run.</strong> <code>air -t on</code> cannot retroactively reconstruct evidence that was not captured.</li>
            <li><strong>Keep one material step active.</strong> Queue or defer adjacent work rather than silently widening Orbit 0.</li>
            <li><strong>Refresh Handoff at meaningful boundaries.</strong> Create a new card after material state changes when continuity across sessions matters.</li>
            <li><strong>Use host-specific power as an adapter.</strong> Take advantage of platform permissions, tools, hooks, or agents without making those capabilities a requirement of the portable AIR core.</li>
          </ul>
        </section>

        <section class="docs-section" id="troubleshooting">
          <h2>Troubleshooting</h2>
          <table class="docs-table"><thead><tr><th>Symptom</th><th>Likely cause</th><th>Response</th></tr></thead><tbody>
            <tr><td>AIR starts without expected boot state</td><td>Partial load, incompatible foundation, or non-AIR roleplay response.</td><td>Check all five files, designations/versions, JSON parsing, sentinels, and required boot records before proceeding.</td></tr>
            <tr><td>Objects stop appearing</td><td>Visibility drift or required transition not being surfaced.</td><td>Remember that <code>ALL_OBJECTS</code> is the default. Request current AIR state/alignment; periodic checks must still surface even in compact mode.</td></tr>
            <tr><td>Periodic alignment detects drift</td><td>Active task/artifact/scope/approval/evidence/visibility/counter state no longer reconciles.</td><td>Stay in <code>ALIGNMENT_RECOVERY_SURFACE</code> until coherent state is visibly restored.</td></tr>
            <tr><td>AIR needs a package that is not loaded</td><td>Required capability input unavailable.</td><td>Request the smallest exact canonical component/package needed, or use an explicitly degraded safe fallback when Core permits it.</td></tr>
            <tr><td>Test result says PASS but approval is blocked</td><td>Required evidence class is not satisfied.</td><td>Check whether the gate requires full executable evidence, replayable evaluation, source evidence, or manual review rather than a summary pass count.</td></tr>
            <tr><td>Handoff will not resume execution</td><td>Missing/stale active artifact, incompatible foundation, or unresolved restoration conflict.</td><td>Validate the current foundation and the affected serialized state; use the card for migration/review until valid binding can be restored.</td></tr>
          </tbody></table>
        </section>

        <section class="docs-section" id="adapters">
          <h2>Hooks &amp; adapters</h2>
          <p class="lead">AIR's portable prompt contract is deliberately separate from platform-specific enforcement. Future integrations can bind AIR concepts to host capabilities without changing the meaning of the AIR core.</p>
          <div class="docs-grid">
            <div class="docs-card"><h3>Permission interception</h3><p>A host adapter can independently reject forbidden tool/action requests or require explicit approval before execution.</p></div>
            <div class="docs-card"><h3>Independent test execution</h3><p>CI, IDE, agent, or workflow hooks can run tests outside the model and return tool-observed receipts to AIR.</p></div>
            <div class="docs-card"><h3>Action receipts</h3><p>Adapters can capture exact external-state changes, hashes, deployment IDs, or API responses and bind them to AIR action receipts.</p></div>
            <div class="docs-card"><h3>Mechanical alignment checks</h3><p>A client can enforce the five-user-message cadence or other host-observable invariants instead of relying solely on prompt compliance.</p></div>
          </div>
          <div class="docs-note"><strong>Do not collapse the layers.</strong> An adapter may strengthen AIR, but its backend/client guarantees must be attributed to that integration and evidenced. They are not properties of the prompt-only kit by default.</div>
        </section>

        <section class="docs-section" id="compatibility">
          <h2>Compatibility boundary</h2>
          <p class="lead">AIR is designed for model and platform portability, but compatibility is observed and temporary rather than a permanent guarantee.</p>
          <ul class="docs-list">
            <li>The portable contract is the AIR files, explicit records, and shared semantics—not a promise that every host exposes the same tools, context size, memory, permissions, or attachment behavior.</li>
            <li>Test the five-file load and required object behavior on each host/model combination you intend to use.</li>
            <li>When moving platforms, use Handoff for explicit state continuity and revalidate the receiving runtime before material execution.</li>
            <li>Platform-native skills, hooks, agents, memory systems, and tool APIs can be useful integrations; keep them outside the definition of the AIR core unless AIR explicitly adopts an open interoperable contract.</li>
          </ul>
          <div style="display:flex;gap:.8rem;flex-wrap:wrap;margin-top:1.4rem">
            <a class="btn btn-primary" href="get-started.html">Get started</a>
            <a class="btn btn-outline" href="how-it-works.html">Visual architecture</a>
            <a class="btn btn-outline" href="glossary.html">Glossary</a>
            <a class="btn btn-outline" href="https://github.com/eddlev/vm4ai-air-kit/discussions" target="_blank" rel="noopener">Ask in Discussions</a>
          </div>
        </section>
      </div>
    </div>
  </section>
</main>
'''

if base.count('<main>') != 1 or base.count('</main>') != 1:
    raise SystemExit('template main markers unexpected')
base = re.sub(r'<main>.*?</main>', main.strip(), base, count=1, flags=re.S)
DOCS.write_text(base, encoding='utf-8')

# Add Docs to the shared-looking nav/footer on every page that carries those markers.
nav_old = '      <a href="how-it-works.html">How it works</a>\n      <a href="get-started.html">Get started</a>'
nav_new = '      <a href="how-it-works.html">How it works</a>\n      <a href="air-docs.html">Docs</a>\n      <a href="get-started.html">Get started</a>'
footer_old = '        <a href="how-it-works.html">How it works</a>\n        <a href="get-started.html">Get started</a>'
footer_new = '        <a href="how-it-works.html">How it works</a>\n        <a href="air-docs.html">Documentation</a>\n        <a href="get-started.html">Get started</a>'
nav_touched = 0
for page in sorted(PUBLIC.glob('*.html')):
    text = page.read_text(encoding='utf-8')
    changed = False
    if nav_old in text and 'href="air-docs.html">Docs</a>' not in text:
        text = text.replace(nav_old, nav_new, 1)
        changed = True
    if footer_old in text and 'href="air-docs.html">Documentation</a>' not in text:
        text = text.replace(footer_old, footer_new, 1)
        changed = True
    if changed:
        page.write_text(text, encoding='utf-8')
        nav_touched += 1

# Correct stale glossary statements that now conflict with AIR 2.4.2.
gloss = TEMPLATE.read_text(encoding='utf-8')
gloss = gloss.replace(
    'Plain-language definitions for the words AIR uses, and the CLI-style commands you can type to steer a session. Inside a live session, <code>air help</code> is always the source of truth — this is the at-a-glance version.',
    'Plain-language definitions for the words AIR uses, plus the four canonical system modifiers. For status, blockers, scope, evidence, readiness, validation, and Handoff, you can simply ask AIR in ordinary language.'
)
gloss = gloss.replace(
    'The set of formal JSON objects AIR emits to show its state and decisions — for example <code>AIR_SESSION</code> (where things stand), <code>AIR_GATE</code> (a checkpoint), <code>AIR_ARTIFACT</code> (a unit of work), <code>AIR_PROJECT_EXECUTION_MAP</code> (the plan), and <code>AIR_HANDOFF_CARD</code> (continuation state). Visible structure, not just talk.',
    'The formal records AIR emits to show state and decisions — including <code>AIR_SESSION</code>, <code>AIR_GATE</code>, <code>AIR_ARTIFACT</code>, <code>AIR_PROJECT_EXECUTION_MAP</code>, the periodic anti-drift <code>AIR_ALIGNMENT_CHECK</code>, validation/action records, and <code>AIR_HANDOFF_CARD</code>. Visible governance state, not hidden-model telemetry.'
)
gloss = gloss.replace(
    '<div class="row"><dt><code>air -o on</code></dt><dd>Show every AIR object that is actually generated. It does not invent extra objects.</dd></div>',
    '<div class="row"><dt><code>air -o on</code></dt><dd>Use full object visibility: every AIR object that is actually generated is shown. AIR v2 already defaults to <code>ALL_OBJECTS</code>; this modifier can explicitly restore full visibility after compact mode.</dd></div>'
)
gloss = gloss.replace(
    '<div class="row"><dt><code>air -o -min</code></dt><dd>Show only objects required by Core law or a material trigger. This is the default. Required records cannot be turned off.</dd></div>',
    '<div class="row"><dt><code>air -o -min</code></dt><dd>Explicitly select compact visibility. Optional repetition may be suppressed, but required records — including periodic <code>AIR_ALIGNMENT_CHECK</code> and its <code>AIR_VALIDATION_REPORT</code> — cannot be turned off.</dd></div>'
)
if '<code>air help</code>' in gloss:
    raise SystemExit('stale air help claim remains in glossary')
if 'This is the default. Required records cannot be turned off.' in gloss:
    raise SystemExit('stale minimum-object default remains in glossary')
TEMPLATE.write_text(gloss, encoding='utf-8')

# Add the canonical documentation page to sitemap.
sitemap = SITEMAP.read_text(encoding='utf-8')
if 'https://vm4ai.com/air-docs.html' not in sitemap:
    loc = '  <url><loc>https://vm4ai.com/air-docs.html</loc></url>\n'
    if '</urlset>' not in sitemap:
        raise SystemExit('sitemap closing marker missing')
    sitemap = sitemap.replace('</urlset>', loc + '</urlset>', 1)
    SITEMAP.write_text(sitemap, encoding='utf-8')

# Validation of the new canonical reference.
doc = DOCS.read_text(encoding='utf-8')
required = [
    'Core 2.4.2', 'Control 2.4.2', 'Handoff schema 2.2.0',
    'Why AIR is prompt-based', 'Vendor independence', 'Platform-agnostic core',
    'Cross-platform portability', 'Multi-session continuity', 'Progressive enforcement',
    'AIR defaults to <code>ALL_OBJECTS</code>', 'air -o on', 'air -o -min', 'air -t on', 'air -t off',
    'AIR_ALIGNMENT_CHECK', 'every fifth counted user message', 'artifact_revision',
    'REPRODUCIBLE_EXECUTABLE', 'REPLAYABLE_EVALUATION', 'MANUAL_REVIEW_REQUIRED',
    'SURFACED_OUTPUT_GOVERNANCE_RECORD', 'SOURCE_SUPPORTED_GOVERNANCE_RECORD',
    'TOOL_OBSERVED_GOVERNANCE_RECORD', 'BACKEND_ENFORCED_GOVERNANCE_RECORD',
    'ALIGNMENT_RECOVERY_SURFACE', 'profiles/specification first method pack/'
]
for needle in required:
    if needle not in doc:
        raise SystemExit(f'documentation missing required contract text: {needle}')

for forbidden in [
    'air help',
    'air -o -min</code></dt><dd>Show only objects required by Core law or a material trigger. This is the default',
    'deterministic LLM behavior',
    'hidden chain-of-thought telemetry'
]:
    if forbidden in doc:
        raise SystemExit(f'forbidden/stale documentation text found: {forbidden}')

# New page internal/local links must resolve.
for href in re.findall(r'href="([^"]+)"', doc):
    if href.startswith(('#', 'http://', 'https://', 'mailto:', 'tel:')):
        continue
    target = href.split('#', 1)[0].split('?', 1)[0]
    if not target:
        continue
    if not (PUBLIC / target).exists():
        raise SystemExit(f'broken local link in air-docs.html: {href}')

# Every standard page with the standard nav now exposes Docs, and sitemap contains it.
standard_pages = 0
for page in sorted(PUBLIC.glob('*.html')):
    text = page.read_text(encoding='utf-8')
    if '<nav class="nav" id="nav" aria-label="Primary">' in text and 'href="how-it-works.html">How it works</a>' in text:
        standard_pages += 1
        if 'href="air-docs.html">Docs</a>' not in text:
            raise SystemExit(f'Docs nav missing from standard page: {page}')
if standard_pages < 10:
    raise SystemExit(f'unexpectedly few standard pages validated: {standard_pages}')
if 'https://vm4ai.com/air-docs.html' not in SITEMAP.read_text(encoding='utf-8'):
    raise SystemExit('air-docs missing from sitemap')

print(f'AIR documentation build validated: nav_pages={standard_pages}, nav_files_changed={nav_touched}, docs_page={DOCS}')
