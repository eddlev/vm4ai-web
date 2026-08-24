from pathlib import Path
import re
import subprocess
import sys

BASE = "fca17ec14559f47138ab564b410b2b58a55fe420"
P = Path("public")
changed = set()


def fail(message):
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def text(name):
    return (P / name).read_text(encoding="utf-8")


def save(name, value):
    path = P / name
    path.write_text(value, encoding="utf-8")
    changed.add(str(path))


def replace_required(name, old, new, expected=1):
    value = text(name)
    count = value.count(old)
    if count != expected:
        fail(f"{name}: expected {expected} occurrence(s), found {count}: {old[:120]!r}")
    save(name, value.replace(old, new, expected))


def regex_required(name, pattern, replacement, expected=1):
    value = text(name)
    new_value, count = re.subn(pattern, replacement, value, count=expected, flags=re.S)
    if count != expected:
        fail(f"{name}: expected {expected} regex match(es), found {count}: {pattern[:120]!r}")
    save(name, new_value)


# Shared secondary-page positioning. Landing page is explicitly excluded.
footer_old = "An overlay for AI chatbots that turns your session into a structured, auditable environment. VM4AI is the concept; AIR is the framework built on it."
footer_new = "AI work, carried forward. A prompt-based framework for focused work, structured continuity and compatible-platform handoff."
for path in sorted(P.glob("*.html")):
    if path.name == "index.html":
        continue
    value = path.read_text(encoding="utf-8")
    if footer_old in value:
        path.write_text(value.replace(footer_old, footer_new), encoding="utf-8")
        changed.add(str(path))


# ABOUT — preserve the creator story, portrait, layout, and page purpose.
replace_required(
    "about.html",
    "AIR — under a different name at the time — was the answer: while you are still searching for the right hire or raising the funds to bring a specialist on, AIR can stand in for those roles as a cooperative AI teammate.",
    "AIR — under a different name at the time — was the answer: while you are still searching for the right hire or raising the funds to bring a specialist on, AIR can bring structured specialist capability into the work while keeping the human role, judgment, and authority distinct."
)
replace_required(
    "about.html",
    "I approached trust through transparency. The AIR objects that print into the chat — structured JSON blocks — show exactly how AIR is executing every task, out in the open, so none of its reasoning stays hidden.",
    "I approached trust through visibility. AIR surfaces structured governance records for state, scope, assumptions, blockers, approvals, and decisions. They make the working contract inspectable; they do not expose hidden chain-of-thought or prove external actions without the evidence for those actions."
)
replace_required(
    "about.html",
    "Continuity comes from the handoff card: a JSON block that captures where the project stands and what the next step should be. Because JSON travels everywhere, that card carries a project not just into a new session but onto an entirely different platform, so the work continues seamlessly even as the AI landscape keeps shifting.",
    "Continuity comes from the Handoff Card: structured JSON that captures explicit project state, including where the work stands and what should happen next. A receiving AIR session validates and rebinds that state, so the project can continue without reconstructing the work from the whole transcript."
)
replace_required(
    "about.html",
    "That same portability frees AIR from any single model or platform. You boot a new session wherever you like and carry on from the card. The one honest caveat is that the output is always shaped by whichever model happens to be hosting it.",
    "That portability keeps the project from depending on one model or platform's private session state. You can carry the Handoff Card into another compatible AIR host and continue from the recorded state. The host model still shapes the output, and compatibility is something to verify rather than assume."
)
replace_required(
    "about.html",
    '<div class="principle"><div class="pk">Transparency</div><h4>Show the work</h4><p>Every task is shown in the open as AIR objects — structured JSON you can inspect.</p></div>',
    '<div class="principle"><div class="pk">Transparency</div><h4>Show the state</h4><p>AIR surfaces required governance records when they matter — structured JSON for the state, boundaries, gates, assumptions, and decisions you can inspect.</p></div>'
)
replace_required(
    "about.html",
    '<div class="principle"><div class="pk">Restraint</div><h4>Won\'t guess</h4><p>When AIR is unsure, it won\'t invent an answer. It stops, flags the gap, and follows its protocol instead of guessing.</p></div>',
    '<div class="principle"><div class="pk">Restraint</div><h4>Won\'t turn uncertainty into fact</h4><p>When a material uncertainty would change the work, AIR keeps it unresolved, asks for the missing input or evidence, and blocks only the affected action until it is safe to continue.</p></div>'
)


# HOW IT WORKS — retain architecture, diagrams, AMRS, and page sequence.
replace_required(
    "how-it-works.html",
    "AIR — short for AI Resource — turns a chatbot session into a structured, auditable environment, with a teammate's discipline rather than an agent's autonomy. Here is the machinery, from the first question to the final handoff.",
    "AIR — short for AI Resource — turns a compatible AI session into a structured, reviewable working environment, with a teammate's discipline rather than an agent's autonomy. Here is the machinery, from the first question to the final handoff."
)
replace_required(
    "how-it-works.html",
    "A default profile governs by default. On top of it AIR binds reusable capability — a <strong>Specialist</strong> (a capability profile), a <strong>Domain pack</strong> (a standards overlay), a <strong>Method pack</strong> (a procedure with its own gates), and <strong>Executors</strong> (bounded, callable operations, not agents). Each stays subordinate to the contract and the gates, and nothing binds until it clears the capability gate. <a href=\"https://github.com/eddlev/vm4ai-air-kit\" target=\"_blank\" rel=\"noopener\">Full specs in the repo →</a>",
    "The Default Starter helps compile the first task artifact and supplies a conservative fallback capability posture; it is an input, not execution authority. AIR can then add reusable capability — a <strong>Specialist</strong> (bounded capability profile), a <strong>Domain package</strong> (domain constraints and evidence expectations), a <strong>Method pack</strong> (a procedure with its own state), and <strong>Executors</strong> (bounded operations, not agents). A layer becomes operative only after task-fit selection, validation, required approval, and compilation into or explicit reference by the sole bound Orbit 0 artifact. <a href=\"https://github.com/eddlev/vm4ai-air-kit\" target=\"_blank\" rel=\"noopener\">Full specs in the repo →</a>"
)
replace_required("how-it-works.html", "normal starting point · governs by default", "bootstrap input · no execution authority")
replace_required("how-it-works.html", "<h3>Keep context in orbit</h3>", "<h3>Keep work in orbit</h3>")
replace_required(
    "how-it-works.html",
    "The active task sits at Orbit 0. Supporting and background context orbit around it and inform inward, so focus stays on what is live without losing the surroundings.",
    "The current executing task sits at Orbit 0. Other tasks can wait in Orbit 1 or be deliberately deferred to Orbit 2. They stay non-executing until promoted, so adjacent work remains visible without competing with the live step."
)
replace_required("how-it-works.html", "Orbit 2 · background context", "Orbit 2 · deferred work")
replace_required("how-it-works.html", "Orbit 1 · supporting context", "Orbit 1 · queued work")
replace_required("how-it-works.html", "informs inward", "promote when ready")
replace_required(
    "how-it-works.html",
    "Procedures track their own live state, and gates decide when work advances. When two gates disagree, the stricter one governs.",
    "Procedures track their own live state, and gates decide when work advances. When two gates disagree, the stricter practical consequence governs. AIR also reconciles active state periodically and at material boundaries; detected runtime drift routes to alignment recovery rather than silently continuing as ordinary chat."
)
replace_required(
    "how-it-works.html",
    "The first thing a real session prints:",
    "At a fresh boot, AIR must surface the required session record. This simplified excerpt shows a few identifying fields; the complete canonical object contains additional required state:"
)
regex_required(
    "how-it-works.html",
    r'(<div class="cb-label">Required boot record example</div>\s*<pre>).*?(</pre>)',
    r'''\1{
  "AIR_SESSION": {
    "object_version": "2.0.0",
    "record_class": "SESSION_STATE_RECORD",
    "runtime_origin": "PROMPT_COMPILED",
    "artifact_presence": "NO_ARTIFACT_PRESENT",
    "object_visibility_mode": "ALL_OBJECTS",
    "backend_validation_claimed": false,
    "hidden_reasoning_claimed": false
  }
}\2'''
)


# AIR DOCS — retain the technical reference; update release, authority, AMRS and SFV state.
replace_required(
    "air-docs.html",
    "Setup, runtime behavior, formal objects, modifiers, evidence, handoff, specialist packages, anti-drift checks, and implementation best practices. This is the canonical human-readable reference for the current AIR v0.4 release line.",
    "Setup, runtime behavior, formal objects, modifiers, evidence, handoff, specialist packages, anti-drift checks, and implementation best practices. This page is a human-readable guide to the current prompt set; the repository remains the operative source of truth."
)
replace_required(
    "air-docs.html",
    '<div class="docs-version"><strong>Release line</strong> AIR Kit v0.4.0 candidate <span>·</span> Core 2.4.2 <span>·</span> Control 2.4.2 <span>·</span> Handoff schema 2.2.0</div>',
    '<div class="docs-version"><strong>Current prompts</strong> Core 2.4.3 <span>·</span> Control 2.4.3 <span>·</span> Governance 2.2.0 <span>·</span> Starter 2.4.3 <span>·</span> Handoff schema 2.2.0</div>'
)
replace_required(
    "air-docs.html",
    '<li><strong>Fail-closed behavior</strong> — missing material evidence, ambiguity, approval, package input, or incompatible state blocks the affected action instead of being silently guessed.</li>',
    '<li><strong>Fail-closed behavior</strong> — missing material evidence, ambiguity, approval, package input, or incompatible state blocks the affected action instead of being silently guessed.</li>\n            <li><strong>Readiness (AMRS)</strong> — maturity-bearing work uses the AIR Maturity Readiness Scale from AMRS-0 problem framing through AMRS-6 production approved; promotion is explicit and higher-stage claims stay blocked until earned.</li>'
)
replace_required(
    "air-docs.html",
    '<div class="docs-object"><dt>AIR_SESSION</dt><dd>Session-level runtime state, activation, load integrity, visibility authority, watchdog counters, and other current session controls.</dd></div>',
    '<div class="docs-object"><dt>AIR_RUNTIME_BRIDGE</dt><dd>State-transition record that compiles approved onboarding answers into the initial AIR v2 runtime state for new/import activation.</dd></div>\n            <div class="docs-object"><dt>AIR_SESSION</dt><dd>Session-level runtime state, activation, load integrity, visibility authority, watchdog counters, and other current session controls.</dd></div>'
)
replace_required(
    "air-docs.html",
    '<div class="docs-object"><dt>AIR_PRIMED_ONBOARDING</dt><dd>Fresh-boot onboarding readiness/state when that boot-stage record is generated.</dd></div>',
    '<div class="docs-object"><dt>AIR_PRIMED_ONBOARDING</dt><dd>Reserved compatibility label in the current prompt set; it is not part of the routine current boot sequence described above.</dd></div>'
)
replace_required(
    "air-docs.html",
    '<div class="docs-object"><dt>AIR_ACTIVE_CONTRACT</dt><dd>The explicit execution contract when surfaced separately: scope, allowed actions, constraints, and obligations.</dd></div>',
    '<div class="docs-object"><dt>AIR_ACTIVE_CONTRACT</dt><dd>An artifact-input contract for candidate scope, allowed actions, constraints, evidence requirements, and rescope rules. Positive execution authority still belongs only to the bound Orbit 0 AIR_ARTIFACT.</dd></div>'
)
replace_required("air-docs.html", "AIR 2.4.2 adds a periodic anti-drift checkpoint alongside the existing event-triggered watchdog.", "AIR 2.4.3 includes a periodic anti-drift checkpoint alongside event-triggered runtime reconciliation.")
replace_required("air-docs.html", '<h3 style="margin:1.4rem 0 .5rem">Governance record classes</h3>', '<h3 style="margin:1.4rem 0 .5rem">Governance evidence classes</h3>')
replace_required(
    "air-docs.html",
    '<div class="docs-card"><h3>Specification-First Verification</h3><p>Currently remains a standalone experimental Method Pack under <code>profiles/specification first method pack/</code>. It is not represented as a full specialist package until additional components are justified and tested.</p></div>',
    '<div class="docs-card"><h3>Specification-First Verification</h3><p>Current SFV is a complete non-agent specialist package at version 2.3.6: Domain Package, Method Pack, Specialist, Executor, and package manifest. It adds intent-to-specification traceability, specification adequacy, evidence classification, failure localization, and final intent reconciliation.</p></div>'
)


# GET STARTED — keep the low-friction conversion path; qualify host compatibility.
replace_required(
    "get-started.html",
    "There is nothing to install and no account to create. You bring a chatbot and a project; AIR — short for AI Resource — brings the structure: a teammate that works the project with you, not an autopilot you hand it to.",
    "There is nothing to install and no AIR account to create. You bring a compatible AI host and a project; AIR — short for AI Resource — brings the structure: a teammate-style working frame that keeps the project focused, reviewable, and portable."
)
replace_required("get-started.html", "<span>Any AI chatbot</span><span>The boot bundle</span><span>A project in mind</span>", "<span>A compatible AI host</span><span>The AIR foundation</span><span>A project in mind</span>")
replace_required(
    "get-started.html",
    "Start a fresh session in whatever you already use — ChatGPT, Claude, Gemini, Grok, Mistral, or your own model. AIR depends on none of them in particular.",
    "Start a fresh session on a host that can accept the complete current foundation. AIR is provider-independent at the framework level, but host behavior, attachment handling, context limits, and compatibility vary by interface and model."
)
replace_required(
    "get-started.html",
    "Behavior varies by model — some boot cleanly, some role-play, some refuse the files — so if yours refuses or role-plays, <a href=\"https://github.com/eddlev/vm4ai-air-kit/discussions\" target=\"_blank\" rel=\"noopener\">tell us in Discussions</a>.",
    "Behavior varies by host — some boot cleanly, some refuse the files, and some fail required AIR surface obligations — so if yours refuses or does not satisfy the boot checks, <a href=\"https://github.com/eddlev/vm4ai-air-kit/discussions\" target=\"_blank\" rel=\"noopener\">tell us in Discussions</a>."
)
replace_required("get-started.html", "Get the boot bundle", "Get the AIR foundation")
replace_required("get-started.html", "Grab the boot bundle and start your first session, or read the model behind it first.", "Grab the current AIR foundation and start your first session, or read the model behind it first.")


# GLOSSARY — current onboarding, Orbit, capability, Handoff and AMRS semantics.
replace_required(
    "glossary.html",
    "A prompt-based framework that governs how an AI chatbot works, by direct analogy to HR. It gives a capable model a set of working rules — how to scope, check, and deliver — so it behaves like an accountable teammate rather than a free-form assistant.",
    "A portable prompt-runtime framework, named by direct analogy to HR. It gives a compatible host model an explicit working contract for scope, active task, evidence, approvals, review, and continuity — a structured teammate-style frame rather than free-form chat."
)
replace_required(
    "glossary.html",
    '<div class="row"><dt>Q4 — What should AIR keep consistent?</dt><dd>What to hold steady as you work — structure and logic, structure and tone, and so on.</dd></div>',
    '<div class="row"><dt>Q4 — What should AIR keep consistent?</dt><dd>Selects the continuity/delivery posture: <strong>A</strong> structure and logic, <strong>B</strong> structure and tone, <strong>C</strong> creative narrative continuity, or <strong>D</strong> the neurodivergent delivery modifier.</dd></div>\n          <div class="row"><dt>Q4D — base continuity mode</dt><dd>When Q4=D, Q4D selects the underlying A, B, or C continuity mode. Q4=D is incomplete until Q4D is resolved.</dd></div>'
)
replace_required(
    "glossary.html",
    '<div class="row"><dt>Q6 — AIR &amp; user alignment</dt><dd>The working agreement: who leads, how AIR reviews, how it delivers. Project-scoped by default.</dd></div>',
    '<div class="row"><dt>Q6 — AIR &amp; user alignment</dt><dd>The working agreement: responsibility split, delivery form, explanation depth, challenge posture, approval boundaries, and assumptions to avoid. Project-scoped by default.</dd></div>\n          <div class="row"><dt>Q6D — delivery calibration</dt><dd>When Q4=D, Q6D keeps the ordinary Q6 agreement and adds functional presentation, side-track, focus, momentum, communication, and optional break-support preferences.</dd></div>'
)
replace_required(
    "glossary.html",
    '<div class="row"><dt>Orbit 0 contract</dt><dd>The active working agreement for the task at hand — what AIR is doing right now, and on what terms. AIR keeps it in view so the session doesn\'t drift.</dd></div>',
    '<div class="row"><dt>Orbit 0</dt><dd>The sole current executing task/artifact. Orbit 1 holds queued work with resume conditions; Orbit 2 holds deliberately deferred work. Only the bound Orbit 0 AIR_ARTIFACT supplies positive material execution authority.</dd></div>'
)
replace_required(
    "glossary.html",
    '<div class="row"><dt>Specialist</dt><dd>A grounding profile that gives the session focused expertise for a particular kind of work, when the project needs more than the general runtime.</dd></div>',
    '<div class="row"><dt>Specialist</dt><dd>A bounded non-agent capability profile for a particular kind of work. It can shape the active task only after validation, task-fit selection, required approval, and binding through the current Orbit 0 artifact.</dd></div>'
)
replace_required(
    "glossary.html",
    '<div class="row"><dt>Domain Package</dt><dd>Grounding for a specific subject area — the facts, constraints, and vocabulary of a domain — layered on when the work depends on them.</dd></div>',
    '<div class="row"><dt>Domain Package</dt><dd>A bounded domain overlay/source package for task-relevant terminology, constraints, evidence classes, and domain expectations. Availability alone does not bind it.</dd></div>'
)
replace_required(
    "glossary.html",
    '<div class="row"><dt>Method Pack</dt><dd>Grounding for a specific way of working — a procedure AIR should follow — added when the task calls for it.</dd></div>',
    '<div class="row"><dt>Method Pack</dt><dd>A reusable procedure with explicit execution state, gates, evidence expectations, and handoff state. It does not execute or govern independently of the bound artifact.</dd></div>'
)
replace_required(
    "glossary.html",
    '<div class="row"><dt>Handoff card</dt><dd>A structured snapshot of the session\'s state that lets you resume the work later — in the same model or a different one — from where you left off. Created when you ask AIR to make a handoff and the required handoff inputs are available. Treat it as sensitive: it can carry project detail.</dd></div>',
    '<div class="row"><dt>Handoff Card</dt><dd>A structured transfer record for explicit project state. A receiving compatible AIR session validates the card and rebinds the nominated active artifact before material work continues. It carries recorded state, not hidden model state or guaranteed identical inference. Treat it as sensitive: it can carry project detail.</dd></div>'
)


# USE CASES — capability can move toward a gap; authority does not move with it.
replace_required("use-cases.html", "<h2>On the hard parts, hand over the lead.</h2>", "<h2>On the hard parts, bring in the missing capability.</h2>")
replace_required(
    "use-cases.html",
    "You reach for AIR because something is missing — a skill, a perspective, the time to learn it. That same gap is why leading the work yourself is harder: you can't account for what you don't know.",
    "You reach for AIR because something is missing — a skill, a perspective, or the time to learn it. AIR can bring bounded specialist capability into the active task while keeping scope, evidence, and approvals visible."
)
replace_required(
    "use-cases.html",
    "With the lead, AIR brings the capability you're missing, and weighs each task for its blast radius — the adjacent risks, dependencies, and blind spots the work touches but you might not see. For example: ask it to add a feature, and it flags the security and legal exposure before you hit it.",
    "AIR can weigh each task for its blast radius — the adjacent risks, dependencies, and blind spots the work touches but you might not see. Ask it to add a feature, for example, and the working frame can surface security, legal, evidence, or integration pressure before the change is treated as ready."
)
replace_required(
    "use-cases.html",
    "This is not surrender. AIR recommends and outlines; you support, steer, and overwrite; and it pushes back when a call is off. The lead is AIR's — the project stays yours.",
    "This is still cooperative work. AIR can recommend, challenge, generate, and execute within the current bound task and approvals; you steer, approve, correct, and make the decisions that remain yours. The capability can move closer to the gap without the authority moving with it."
)


# SERVICES — preserve offer structure; remove role-replacement implication.
replace_required(
    "services.html",
    "Beyond the open framework — hands-on help to put AIR (short for AI Resource) to work as a cooperative teammate for the roles you can't yet fill, and support for the teams that depend on it.",
    "Beyond the open framework — hands-on help to put AIR (short for AI Resource) to work where your team has a capability gap, plus support for teams that depend on the framework."
)


# LOAD INTEGRITY — observable conformance, not hidden-state diagnosis.
replace_required(
    "real-boot-vs-roleplay.html",
    "AIR is prompt-based. You hand a model a small set of files and ask it to boot a project. Most of the time it does. But there is a failure mode that is easy to miss, and worth naming plainly: a capable model can read the AIR files, recognize what AIR is, and <em>perform</em> it — reproducing the vocabulary, the tone, even the onboarding flow — without ever actually running it. It looks like AIR. It talks like AIR. It just isn't AIR.",
    "AIR is prompt-based. You hand a compatible host the current foundation and ask it to boot a project. A capable model can read those files, reproduce AIR vocabulary, and even mimic the onboarding flow while still missing required AIR obligations. The useful distinction is observable conformance: did the foundation validate, did required formal records appear at their trigger points, and did later work remain bound to the active AIR artifact? If not, the run is non-conformant and must be recovered rather than trusted because it sounds right."
)
replace_required(
    "real-boot-vs-roleplay.html",
    "This is not hypothetical. A frontier model was handed the AIR boot files and asked to start a project. It reproduced the onboarding questions, answered them, and announced the project was active. It used the right words — active step, gate, benchmark, review — and the work it produced was, on the surface, decent. Yet across thousands of lines, it never once emitted a single AIR object: no <code>AIR_SESSION</code>, no execution map, no artifact — only prose that <em>named</em> those things. At one point it pressed past the gates entirely and treated a change to a live page as already done, with no approval and no record. It was not so much lying as improvising a role. The structure was theater.",
    "This is not hypothetical. A frontier model was handed the AIR files and asked to start a project. It reproduced the onboarding questions, answered them, and announced the project was active. It used the right words — active step, gate, benchmark, review — and the work it produced was, on the surface, decent. Yet across thousands of lines it never emitted the required AIR records: no <code>AIR_SESSION</code>, no execution map, no artifact — only prose that named those things. At one point it also pressed past the gates and treated a live-page change as already done, with no approval record. Under current AIR rules those are concrete conformance failures. We do not need to infer a hidden internal state to say that; the required surfaced obligations themselves failed."
)
replace_required(
    "real-boot-vs-roleplay.html",
    "A fresh AIR boot has required visible conditions: the foundation files must pass the runtime's load checks, and the formal governance records required at each trigger point must actually be surfaced. Their presence shows the response is following AIR's required prompt-layer surface at that point. They do <strong>not</strong> independently prove that every prompt law was followed, reveal hidden reasoning, or prove an external action occurred. The first required boot record looks like this:",
    "A fresh AIR boot has required visible conditions: the foundation files must pass the runtime's load checks, and the formal governance records required at each trigger point must actually be surfaced. Their presence is necessary visible evidence of AIR conformance at that point. They do <strong>not</strong> independently prove that every prompt law was followed, reveal hidden reasoning, or prove an external action occurred. The complete current <code>AIR_SESSION</code> carries more state than the simplified excerpt below:"
)
regex_required(
    "real-boot-vs-roleplay.html",
    r'(<div class="cb-label">Required boot record example</div>\s*<pre>).*?(</pre>)',
    r'''\1{
  "AIR_SESSION": {
    "object_version": "2.0.0",
    "record_class": "SESSION_STATE_RECORD",
    "runtime_origin": "PROMPT_COMPILED",
    "artifact_presence": "NO_ARTIFACT_PRESENT",
    "object_visibility_mode": "ALL_OBJECTS",
    "backend_validation_claimed": false,
    "hidden_reasoning_claimed": false
  }
}\2'''
)
replace_required(
    "real-boot-vs-roleplay.html",
    "Role-play cannot conjure that convincingly, because the objects are not decoration — they are the runtime's own evidence, with a fixed shape and required fields. A model that is <em>performing</em> AIR writes about <code>AIR_SESSION</code>. A model that is <em>running</em> AIR emits it.",
    "The important point is not that a model is incapable of imitating JSON. It can. AIR defines required records, schemas, transitions, gates, and recovery behavior that can be checked against the current prompt contract. A missing required record is an observable process defect; a present record is a governance record whose claims remain bounded by its evidence."
)
replace_required(
    "real-boot-vs-roleplay.html",
    "Put them side by side and the gap is plain. Default output is a confident paragraph that says \"AIR project activated\" and describes what it is doing. AIR output is an object that states its runtime origin, whether it is backend-validated, which onboarding question it is on, and what it is blocked on — and only then, the work. One <em>asserts</em> structure. The other <em>is</em> structured.",
    "Put them side by side and the practical gap is plain. Default-style output may simply announce that a project is active. A conformant AIR run must surface the formal records required by the current runtime when their triggers occur, then keep later work reconciled to the bound artifact. The distinction is contractual and observable, not a claim that we can inspect the model's hidden internal state."
)
replace_required(
    "real-boot-vs-roleplay.html",
    "When you boot AIR, look for the object. If a model replies with prose about AIR but no <code>AIR_SESSION</code> appears, it has not booted — it is role-playing, and the fix is to re-boot or try a different model. AIR runs on whatever chatbot you bring, so behavior varies: some models refuse the files, some boot cleanly, and some perform without running. If a model refuses or role-plays AIR, <a href=\"https://github.com/eddlev/vm4ai-air-kit/discussions\" target=\"_blank\" rel=\"noopener\">tell us in Discussions</a> — those reports are how the compatibility picture stays honest.",
    "When you boot AIR, check the required record and the load-integrity result. If required boot state is missing, treat the boot as invalid or non-conformant and recover or retry; do not infer a hidden explanation for why it failed. Host behavior varies: some models refuse the files, some boot cleanly, and some miss required AIR obligations. If a host refuses AIR or repeatedly fails the checks, <a href=\"https://github.com/eddlev/vm4ai-air-kit/discussions\" target=\"_blank\" rel=\"noopener\">tell us in Discussions</a> — those reports help keep the compatibility picture honest."
)
replace_required(
    "real-boot-vs-roleplay.html",
    "A product about honesty has to be checkable, or it is just another claim. The formal objects are what turn \"is it actually doing what it says?\" into a question you can answer for yourself, in seconds, without taking anyone's word for it. That is the whole idea — and it is the one thing role-play cannot copy. You can tell when it is real.",
    "A product about honesty has to be checkable, or it is just another claim. AIR's formal records give you an inspectable contract surface: what state was declared, what was blocked, what was approved, and what evidence was cited. That does not prove hidden execution or correctness by itself. It does make failures such as missing records, broken binding, skipped approvals, and unsupported external-action claims visible enough to challenge and recover."
)


# CASE STUDIES — preserve observed history; tighten universal/general claims.
replace_required("built-with-air.html", "it runs on whichever chatbot you bring", "it runs in compatible host-model interfaces")
replace_required("built-with-air.html", "printed its reasoning as AIR objects", "surfaced its working state as AIR objects")
replace_required("built-with-air.html", "the work resumed exactly where it left off", "the recorded project state was restored and the work continued from there")
replace_required("built-with-air.html", "stayed coherent, auditable, and resumable", "stayed coherent, reviewable, and resumable")

replace_required(
    "recovered-with-air.html",
    "That symptom — start, then nothing — is what a context window looks like when it is too full to generate a reply. It reads like a crash; it is really exhaustion.",
    "In that observed run, the behavior was consistent with an exhausted context window: the session could no longer produce a usable reply."
)
replace_required(
    "recovered-with-air.html",
    "Both recoveries happened to use the model's ability to search past sessions, which made them smooth. But that feature is not the mechanism. The same recovery works without it: paste the dead session's transcript into a file and run the handoff flow against it. The card, the template, and the runtime are plain prompt files — the method travels to any model that can read them.",
    "Both recoveries happened to use the model's ability to search past sessions, which made them smooth. But past-session search is not the Handoff mechanism. Where a compatible host can ingest the AIR foundation plus an authoritative transcript or saved project evidence, that material can be used to reconstruct a Handoff candidate for validation and rebinding. The portability comes from the explicit transfer record, not from one vendor's history feature."
)
replace_required("recovered-with-air.html", "finished anyway — coherent, auditable, and resumable each time", "finished anyway — coherent, reviewable, and resumable each time")


# MADE WITH AIR — provenance/process mark, not certification.
replace_required(
    "made-with-air.html",
    "Projects built on the AIR framework (short for AI Resource). Each one carries the Made with AIR stamp — a small mark that says the work was done in a structured, honest environment.",
    "Projects built with the AIR framework (short for AI Resource). The Made with AIR stamp marks genuine use of AIR in the working process; it is a provenance mark, not a quality or compliance badge."
)
replace_required(
    "made-with-air.html",
    "The stamp marks work produced in an AIR session — structured, gated, and auditable. It is a statement of process, not a guarantee of quality. The usage terms live in the <a href=\"https://github.com/eddlev/air-brand/blob/main/USAGE.md\" target=\"_blank\" rel=\"noopener\" style=\"color:var(--brass)\">brand kit</a>.",
    "The stamp means AIR was genuinely used in the project's workflow. It does not certify correctness, quality, safety, compliance, or backend enforcement. The usage terms live in the <a href=\"https://github.com/eddlev/air-brand/blob/main/USAGE.md\" target=\"_blank\" rel=\"noopener\" style=\"color:var(--brass)\">brand kit</a>."
)


# ORIGIN — preserve history; avoid unsupported hidden-internal mechanism wording.
replace_required(
    "from-morphic-to-air.html",
    "It should be machine-native and vector-first — carry only what the task actually requires, in the form the model actually reasons in.",
    "It should be machine-oriented and vector-first — carry only what the task actually requires, expressed as AIR task and capability vectors instead of a borrowed human job description."
)


# SHOWCASE — preserve screenshots/raw evidence and AMRS; mark versioned object shapes honestly.
replace_required(
    "showcase.html",
    "Everywhere else, this site <em>tells</em> you AIR is verifiable, structured, and resumable. This page shows it. Below is a real AIR session — booted on Claude Opus 4.8, captured object for object, nothing tidied. AIR frames a risky project, refuses to guess at the part that matters most, stages how mature the work actually is, and stops at a clean save point. Then the same project travels to a different model and picks up exactly where it left off.",
    "Everywhere else, this site tells you AIR is structured, inspectable, and resumable. This page shows an earlier captured AIR session — booted on Claude Opus 4.8, preserved object for object, nothing tidied. AIR frames a risky project, refuses to guess at the part that matters most, uses AMRS to stage how mature the work actually is, and stops at a clean save point. The project then moves to a different model and continues from recorded Handoff state. The object shapes shown here belong to the AIR version captured at the time; the current repository defines today's canonical schemas."
)
replace_required(
    "showcase.html",
    "Everything AIR does next is shaped by a non-technical person asking it to lead on something genuinely risky.",
    "Everything AIR does next is shaped by a non-technical person asking it to guide the work and fill capability gaps on something genuinely risky."
)


# Deterministic SFV-style assertions.
index_now = (P / "index.html").read_bytes()
index_base = subprocess.check_output(["git", "show", f"{BASE}:public/index.html"])
if index_now != index_base:
    fail("public/index.html changed; landing page is locked")

how = text("how-it-works.html")
gloss = text("glossary.html")
if 'id="amrs"' not in how or "AMRS-6" not in how or "AMRS — AIR Maturity Readiness Scale" not in gloss:
    fail("AMRS preservation check failed")

docs = text("air-docs.html")
for marker in ["Core 2.4.3", "Control 2.4.3", "Starter 2.4.3", "Handoff schema 2.2.0", "version 2.3.6"]:
    if marker not in docs:
        fail(f"air-docs missing current marker: {marker}")

about = text("about.html")
for marker in ["Creator of VM4AI AIR", "AIR is short for AI Resource", "Based in Denmark", "Principles"]:
    if marker not in about:
        fail(f"about page identity marker missing: {marker}")

residues = {
    "Core 2.4.2": "stale Core version",
    "Control 2.4.2": "stale Control version",
    "v0.4.0 candidate": "stale release candidate label",
    "governs by default": "Default Starter authority overclaim",
    "none of its reasoning stays hidden": "hidden-reasoning overclaim",
    "printed its reasoning as AIR objects": "hidden-reasoning overclaim",
    "The lead is AIR's": "authority-transfer language",
    "Role-play cannot conjure": "hidden-state diagnosis",
    "it has not booted — it is role-playing": "hidden-state diagnosis",
    "Orbit 1 · supporting context": "stale Orbit model",
    "Orbit 2 · background context": "stale Orbit model",
    "Any AI chatbot": "universal compatibility claim",
    "picks up exactly where it left off": "Handoff identity overclaim",
    "resumed exactly where it left off": "Handoff identity overclaim"
}
corpus = "\n".join(path.read_text(encoding="utf-8") for path in P.glob("*.html"))
for needle, reason in residues.items():
    if needle in corpus:
        fail(f"residue remains ({reason}): {needle}")

for path_string in sorted(changed):
    path = Path(path_string)
    if path.suffix == ".html":
        value = path.read_text(encoding="utf-8")
        if "</html>" not in value or "</body>" not in value:
            fail(f"{path_string}: incomplete HTML")

allowed = {
    "public/404.html", "public/about.html", "public/air-docs.html", "public/blog.html",
    "public/built-with-air.html", "public/from-morphic-to-air.html", "public/get-started.html",
    "public/glossary.html", "public/how-it-works.html", "public/made-with-air.html",
    "public/privacy.html", "public/real-boot-vs-roleplay.html", "public/recovered-with-air.html",
    "public/services.html", "public/showcase.html", "public/terms.html", "public/use-cases.html"
}
unexpected = changed - allowed
if unexpected:
    fail(f"unexpected patched files: {sorted(unexpected)}")

print("Patched files:")
for path in sorted(changed):
    print(" -", path)
print("All targeted AIR/Product Marketing/SFV assertions passed.")
