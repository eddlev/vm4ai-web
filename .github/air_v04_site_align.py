from pathlib import Path
import json
import re
import urllib.request

P = Path('public')

def text(name):
    return (P / name).read_text(encoding='utf-8')

def save(name, value):
    (P / name).write_text(value, encoding='utf-8')

def replace_required(value, old, new, name):
    if old not in value:
        raise RuntimeError(f'missing expected text in {name}: {old[:120]}')
    return value.replace(old, new)

# Get Started.
name = 'get-started.html'
s = text(name)
s = s.replace('Boot AIR in minutes: grab the boot bundle, open any AI chatbot, activate AIR, answer the onboarding, and work with structure. Nothing to install.', 'Boot AIR in minutes: attach the current AIR foundation files, open a capable AI interface, activate AIR, answer onboarding, and work with an explicit project contract. Nothing to install.')
s = replace_required(s, '<p>One requirement does apply: the boot bundle is ~130k tokens, so use a model tier with a 200k-token context window or larger. On smaller windows the files load only partially &mdash; and a partially loaded AIR role-plays instead of running (see: <a href="real-boot-vs-roleplay.html">real boot vs roleplay</a>).</p>', '<p>One requirement does apply: the complete current foundation set must fit in the host interface without truncation. Tokenization, attachment handling, and context limits vary by provider and model, so AIR does not claim one universal token threshold. If a required file is partial or missing, treat the boot as invalid rather than guessing around the missing rules. See <a href="real-boot-vs-roleplay.html">AIR load integrity</a>.</p>', name)
s = replace_required(s, '<div class="gstep"><div class="gn">1</div><div><h3>Get the boot bundle</h3><p>Open the <a href="https://github.com/eddlev/vm4ai-air-kit" target="_blank" rel="noopener">AIR repository</a> and grab the boot files. Nothing to install, no account to create — AIR is a prompt-based framework.</p></div></div>', '<div class="gstep"><div class="gn">1</div><div><h3>Get the current foundation</h3><p>Open the <a href="https://github.com/eddlev/vm4ai-air-kit/tree/main/prompts" target="_blank" rel="noopener">AIR prompts directory</a> and attach the current five foundation files: Core Runtime, Control Surface, Governance supplement, Default Starter Profile, and Handoff Card Template. Nothing to install — AIR is a prompt-runtime framework.</p></div></div>', name)
s = replace_required(s, '<div class="gstep"><div class="gn">3</div><div><h3>Activate AIR</h3><p>Paste the boot bundle into the session. AIR loads, configures the environment, and takes over the structure of the work.</p></div></div>', '<div class="gstep"><div class="gn">3</div><div><h3>Activate AIR</h3><p>Attach the foundation files and type <code>Start a new AIR project.</code> AIR verifies the required load state before onboarding; the activation phrase does not silently choose Q1 for you.</p></div></div>', name)
s = replace_required(s, '<div class="gstep"><div class="gn">5</div><div><h3>Work, with structure</h3><p>From here AIR runs the work: roadmap first, one active step at a time, with the AIR objects printing into the chat so you can see exactly what it is doing.</p></div></div>', '<div class="gstep"><div class="gn">5</div><div><h3>Work, with structure</h3><p>From here AIR keeps one material step active at a time and surfaces required governance records when state changes. Those records show AIR\'s declared prompt-layer state, assumptions, gates, and evidence posture — not hidden chain-of-thought or independent proof of external actions.</p></div></div>', name)
s = replace_required(s, '<div class="gstep"><div class="gn">6</div><div><h3>Continue anywhere</h3><p>When you stop, AIR emits a <strong>handoff card</strong> — a JSON block capturing the project and the next step. Paste it into a new session, on the same model or a different platform, to pick up exactly where you left off.</p></div></div>', '<div class="gstep"><div class="gn">6</div><div><h3>Continue across compatible sessions</h3><p>A populated <strong>Handoff Card</strong> carries recorded project state into another compatible AIR session. The receiving runtime validates and rebinds that state. It preserves the working record — not hidden model state or byte-for-byte identical inference.</p></div></div>', name)
s = s.replace('A real boot prints a formal <code>AIR_SESSION</code> object into the chat — structured JSON, not prose. If your model only <em>describes</em> AIR without emitting the object, it is role-playing, not running; re-boot or try another model.', 'A valid fresh AIR boot must surface the required <code>AIR_SESSION</code> governance record. If a required boot record is missing, or required files fail load-integrity checks, do not treat the boot as valid. The record exposes declared AIR state; by itself it does not prove hidden execution or external actions.')
s = s.replace('More on the tell: <a href="real-boot-vs-roleplay.html">real boot vs roleplay</a>', 'More on the check: <a href="real-boot-vs-roleplay.html">AIR load integrity</a>')
save(name, s)

# Glossary: current metadata and four modifiers only.
name = 'glossary.html'
s = text(name)
s = s.replace('<title>Glossary &amp; commands — AIR by VM4AI</title>', '<title>AIR glossary &amp; modifiers — AIR by VM4AI</title>')
s = s.replace("Plain-language definitions for AIR's vocabulary — Q-codes, blast radius, AMRS, gates, grounding layers — and the full set of CLI-style air commands you can type to steer a session.", 'Plain-language definitions for AIR vocabulary, governance records, continuity, capability layers, and the four supported system modifiers.')
s = s.replace('<meta property="og:title" content="Get started — AIR by VM4AI">', '<meta property="og:title" content="AIR glossary &amp; modifiers — AIR by VM4AI">')
s = s.replace('<meta property="og:description" content="Boot AIR in minutes: grab the boot bundle, open any AI chatbot, activate AIR, answer the onboarding, and work with structure. Nothing to install.">', '<meta property="og:description" content="Plain-language definitions for AIR vocabulary and the four supported system modifiers.">')
s = s.replace('<meta property="og:url" content="https://vm4ai.com/get-started.html">', '<meta property="og:url" content="https://vm4ai.com/glossary.html">')
s = s.replace('<meta name="twitter:title" content="Get started — AIR by VM4AI">', '<meta name="twitter:title" content="AIR glossary &amp; modifiers — AIR by VM4AI">')
s = s.replace('<meta name="twitter:description" content="Boot AIR in minutes: grab the boot bundle, open any AI chatbot, activate AIR, answer the onboarding, and work with structure. Nothing to install.">', '<meta name="twitter:description" content="Plain-language definitions for AIR vocabulary and the four supported system modifiers.">')
s = s.replace('<div class="row"><dt>Real boot vs roleplay</dt><dd>A real boot emits formal AIR objects — structured JSON — into the chat. A model that only <em>describes</em> AIR in prose is role-playing, not running it. The objects are the tell. <a href="real-boot-vs-roleplay.html">How to tell →</a></dd></div>', '<div class="row"><dt>AIR load integrity</dt><dd>A fresh boot is valid only when the required foundation files pass load checks and required surfaced records appear at their trigger points. Those records expose declared AIR state; they are not hidden-model telemetry or independent proof of external execution. <a href="real-boot-vs-roleplay.html">How to check →</a></dd></div>')
s = s.replace('Created with <code>air handoff</code>. Treat it as sensitive: it can carry project detail.', 'Created when you ask AIR to make a handoff and the required handoff inputs are available. Treat it as sensitive: it can carry project detail.')
start = s.index('<section class="section" style="padding-top:0">', s.index('<h2 class="grp-head">CLI-style commands</h2>') - 300)
end = s.index('</section>', start) + len('</section>')
modifier_section = '''<section class="section" style="padding-top:0">
    <div class="container narrow">
      <h2 class="grp-head">System modifiers</h2>
      <p class="grp-intro">AIR v2 keeps the CLI-like surface intentionally small. There are four canonical modifiers. Everything else — status, blockers, scope, benchmark, evidence, risks, sources, readiness, approval, patching, validation, task switching, queue review, and handoff — can be requested in ordinary language.</p>
      <div class="defgroup"><h3>Object visibility</h3><dl class="deflist cmds">
        <div class="row"><dt><code>air -o on</code></dt><dd>Show every AIR object that is actually generated. It does not invent extra objects.</dd></div>
        <div class="row"><dt><code>air -o -min</code></dt><dd>Show only objects required by Core law or a material trigger. This is the default. Required records cannot be turned off.</dd></div>
      </dl></div>
      <div class="defgroup"><h3>Test-evidence delivery</h3><dl class="deflist cmds">
        <div class="row"><dt><code>air -t on</code></dt><dd>For subsequent test/evaluation runs, request the fuller reviewable evidence package when available.</dd></div>
        <div class="row"><dt><code>air -t off</code></dt><dd>Use summary-only test reporting. This is the default and does not reduce the underlying test rigor or approval threshold.</dd></div>
      </dl></div>
      <div class="callout"><div class="label">Ask normally for everything else</div><p>Examples: “What are we doing now?”, “What is blocking this?”, “Show the evidence.”, “Is this ready?”, or “Make a handoff.” System modifiers never bypass AIR gates, evidence requirements, active scope, approvals, safety, or required object emission.</p></div>
    </div>
  </section>'''
s = s[:start] + modifier_section + s[end:]
save(name, s)

# How it works: preserve architecture, update stale labels.
name = 'how-it-works.html'
s = text(name).replace('boot bundle · 3 files', 'foundation · 5 files').replace('card + core runtime', 'validated card + runtime')
s = s.replace('<h2>What a real boot emits</h2>', '<h2>What a valid AIR boot surfaces</h2>').replace('<div class="cb-label">A real boot emits this</div>', '<div class="cb-label">Required boot record example</div>')
s = s.replace('how to tell a real boot from a roleplay', 'how AIR load integrity is checked')
save(name, s)

# Landing/blog/use-cases evidence wording.
name = 'index.html'; s = text(name)
s = s.replace('<!-- SELF-APPLIED PROOF -->', '<!-- SELF-APPLIED EVIDENCE -->').replace('id="proof"', 'id="evidence"').replace('Self-applied proof', 'Self-applied evidence').replace('The proof is the work itself.', 'The evidence is in the work.').replace('Read the proof path', 'Read the evidence path').replace('<div class="k">Case study</div><h3>Real boot vs roleplay</h3>', '<div class="k">Integrity guide</div><h3>AIR load integrity</h3>').replace('A model can accept the files and perform AIR without running it. Here&rsquo;s how to tell a real boot from the performance.', 'Required files and surfaced records make prompt-layer state inspectable, but they are not independent proof. Here is how to validate the load and keep the assurance boundary clear.')
save(name, s)
name = 'blog.html'; s = text(name).replace('<h2>Real boot vs roleplay</h2>', '<h2>AIR load integrity</h2>').replace('A capable model can accept the AIR files and talk like AIR without ever booting it. A real boot emits formal objects into the chat; role-play only names them in prose — an honest look at the difference, and how to tell which one you’re getting.', 'A practical guide to checking required file load and surfaced AIR state without mistaking model-generated records for backend proof, hidden reasoning, or external execution evidence.')
save(name, s)
name = 'use-cases.html'; s = text(name)
s = s.replace('Proof, not promises.', 'Evidence, not promises.').replace('Featured · proof of use', 'Featured · observed use').replace("Both times AIR's handoff cards reconstructed the project from history and resumed it with nothing lost. Proof the continuity mechanism holds when a session doesn't.", "In those incidents AIR's recorded state and available history were sufficient to reconstruct the project and continue without an observed loss that blocked the work. That is an observed case outcome, not a guarantee of exact state or identical inference.").replace('Method · proof', 'Method · integrity check').replace('Telling a real boot from a roleplay', 'Checking AIR load integrity').replace('Hand the AIR files to a model and it can do one of two things: actually boot the framework, or just describe it convincingly. The difference is visible — a real boot prints structured AIR objects; a roleplay only talks about them. How to spot the tell, and why it is the point.', 'A valid fresh boot requires the complete foundation load and the records required by the current runtime. The records make declared prompt-layer state inspectable; they do not independently prove hidden execution. Here is how to check the boundary.')
save(name, s)

# Historical recovery case.
name = 'recovered-with-air.html'; s = text(name)
s = replace_required(s, 'A framework that promises continuity should be able to prove it the day a session dies without warning — not in theory, but on a real project, reported honestly. This site, its brand, and the kit behind it were built across several sessions. Twice, a working session stopped before it could hand off. Both times the project resumed in a new session with nothing lost. This is an account of how that worked — and where it would not have.', 'A framework built for continuity should be stress-tested when a session dies without warning — not only in theory, but on real project work reported honestly. This site, its brand, and the kit behind it were built across several sessions. Twice, a working session stopped before it could hand off. In those two incidents, the available AIR state and conversation history were sufficient to reconstruct the project and continue without an observed loss that blocked the work. This is an account of those outcomes — not a guarantee of exact state transfer or identical inference.', name)
save(name, s)

# Keep legacy URL, rewrite the assurance claim.
name = 'real-boot-vs-roleplay.html'; s = text(name)
s = s.replace('Real boot vs roleplay — AIR by VM4AI', 'AIR load integrity — AIR by VM4AI').replace('An honest case study: a capable model can accept the AIR files and role-play AIR without running it. A real boot emits formal objects — here is how to tell the difference.', 'A practical integrity guide: validate the required AIR file load and surfaced governance records without treating model-generated records as backend proof.').replace('<h1>Real boot vs roleplay</h1>', '<h1>AIR load integrity</h1>').replace('<h2>The tell</h2>', '<h2>What the visible records tell you</h2>').replace('<div class="cb-label">A real boot emits this</div>', '<div class="cb-label">Required boot record example</div>')
s = replace_required(s, 'Here is the difference, and it stops being subtle once you know where to look. A genuine AIR boot emits <strong>formal objects</strong> — machine-readable JSON that the runtime requires as evidence that it is actually running. The first thing a real session produces looks like this:', "A fresh AIR boot has required visible conditions: the foundation files must pass the runtime's load checks, and the formal governance records required at each trigger point must actually be surfaced. Their presence shows the response is following AIR's required prompt-layer surface at that point. They do <strong>not</strong> independently prove that every prompt law was followed, reveal hidden reasoning, or prove an external action occurred. The first required boot record looks like this:", name)
save(name, s)

# Historical showcase with current replacement downloads.
name = 'showcase.html'; s = text(name)
s = s.replace('<meta property="og:title" content="Real boot vs roleplay — AIR by VM4AI">', '<meta property="og:title" content="See a full AIR session — AIR by VM4AI">').replace('<meta property="og:description" content="An honest case study: a capable model can accept the AIR files and role-play AIR without running it. A real boot emits formal objects — here is how to tell the difference.">', '<meta property="og:description" content="A historical AIR session showing project framing, active-step execution, readiness review, handoff, and cross-model continuation — with current assurance notes.">').replace('<meta property="og:url" content="https://vm4ai.com/real-boot-vs-roleplay.html">', '<meta property="og:url" content="https://vm4ai.com/showcase.html">').replace('<meta name="twitter:title" content="Real boot vs roleplay — AIR by VM4AI">', '<meta name="twitter:title" content="See a full AIR session — AIR by VM4AI">').replace('<meta name="twitter:description" content="An honest case study: a capable model can accept the AIR files and role-play AIR without running it. A real boot emits formal objects — here is how to tell the difference.">', '<meta name="twitter:description" content="A historical AIR session with current notes on prompt-runtime assurance and continuity.">')
s = s.replace('<dt>Orbit 0</dt><dd>The contract currently governing the session — the task AIR is bound to right now.</dd>', '<dt>Orbit 0</dt><dd>The active task currently bound under the working contract.</dd>').replace("A real boot's first act is to emit a formal object — not prose claiming it started, an actual record that states what it is and, just as importantly, what it is <em>not</em>.", "This historical capture begins with the formal boot record required by the AIR version used at the time. Current AIR still requires surfaced governance records at defined trigger points, but those records describe declared prompt-layer state; they are not hidden-model telemetry or independent proof of external execution.").replace('The first object a real boot emits — abridged', 'Historical boot record — abridged').replace('At AMRS-0 it <em>blocks itself</em> from saying anything is implementation-ready, production-ready, or accepted. It cannot overclaim, because the ruler will not let it.', 'At AMRS-0 the prompt contract binds a claim ceiling: AIR is instructed not to describe the work as implementation-ready, production-ready, or accepted without the required evidence. That is a prompt-layer control, not deterministic backend enforcement.').replace('The proof: the project traveled to another model', 'The continuity test: the project traveled to another model')
s = replace_required(s, 'Everything here is downloadable. Grab the boot files from the kit, grab the card, start AIR, choose <strong>Q1 = C (Continue from handoff card)</strong>, and attach the card — you will land on the same access-tier decision this session stopped at. If you would rather read the whole thing first, the full unedited transcript is here too.', 'The original historical download artifacts linked from this page were never committed to the site repository. Rather than inventing those originals after the fact, the links below now provide <strong>current AIR v2.4 examples</strong>, clearly separate from the historical capture above. Use the current Handoff template as a schema/reference file, and the walkthrough to reproduce a fresh current-format session.', name)
s = s.replace('↓ Handoff card (.json)', '↓ Current Handoff template (.json)').replace('↓ Full transcript (.md)', '↓ Current session walkthrough (.md)').replace('If your model role-plays instead of booting, the resume will not produce these objects — and now you know <a href="real-boot-vs-roleplay.html">how to tell</a>.', 'If a required file or surfaced record is missing, treat the boot or continuation as invalid and use the <a href="real-boot-vs-roleplay.html">load-integrity guide</a> rather than inferring hidden state from style alone.')
save(name, s)

# Current handoff template at the existing broken URL.
url = 'https://raw.githubusercontent.com/eddlev/vm4ai-air-kit/agent/air-v0.4-alignment/prompts/AIR_HANDOFF_CARD_TEMPLATE.json'
with urllib.request.urlopen(url, timeout=30) as r:
    handoff = r.read().decode('utf-8')
(P / 'showcase-handoff-card.json').write_text(handoff, encoding='utf-8')

walkthrough = '''# AIR v2.4 current session walkthrough

> Current-format walkthrough, August 2026. This is **not** the historical showcase transcript. The original historical download file was never committed, so this file is provided as a truthful current replacement rather than a reconstructed original.

## Start a fresh project

Attach the current five foundation files from `vm4ai-air-kit/prompts/`: Core Runtime, Control Surface, Governance supplement, Default Starter Profile, and Handoff Card Template. The complete files must fit without truncation. Then type `Start a new AIR project.`

A valid fresh boot performs its required load checks, surfaces the required `AIR_SESSION` governance record, and asks Q1. The activation phrase does not answer Q1 for you.

## Complete onboarding

AIR asks Q1-Q6 in order. Current Q4 choices are Structure and logic, Structure and tone, Creative narrative continuity, and Neurodivergent delivery modifier.

After onboarding, AIR compiles the project map and binds exactly one Orbit 0 artifact for material execution.

## Read the records correctly

AIR governance records expose declared prompt-layer state: active task, scope, assumptions, blockers, gates, evidence posture, and delivery state. They do not reveal hidden chain-of-thought and are not independent proof that an external action occurred.

## Optional system modifiers

- `air -o on` — show every AIR object actually generated
- `air -o -min` — minimum required objects (default)
- `air -t on` — fuller reviewable test-evidence packaging for subsequent runs
- `air -t off` — summary-only test reporting (default)

Everything else can be requested in ordinary language.

## Continue with a Handoff Card

Ask AIR to create a populated Handoff Card. In a new compatible session, load the current foundation required by the runtime plus that populated card and choose Q1 = C. The receiving runtime validates and rebinds the recorded state.

Handoff preserves recorded project state and the working contract; it does not transfer hidden model state or guarantee identical inference across providers/models.

The companion `showcase-handoff-card.json` download is the **current template/schema reference**, not the historical project card and not a populated continuation card.
'''
(P / 'showcase-session.md').write_text(walkthrough, encoding='utf-8')

# Validate.
d = json.loads((P / 'showcase-handoff-card.json').read_text(encoding='utf-8'))['AIR_HANDOFF_CARD']
assert d['SCHEMA_VERSION'] == d['schema_version'] == '2.2.0'
assert d['governance_state']['governance_supplement_version'] == '2.2.0'
assert d['governance_state']['governance_floor_version'] == '2.1.0'
assert d['governance_state']['floor_invariant_reference']['registry_version'] == '2.1.0'
checks = {
    'get-started.html': ['~130k', '200k-token', 'see exactly what it is doing', 'pick up exactly where you left off'],
    'glossary.html': ['<code>air status</code>', '<code>air immersive</code>', '<code>air lanes</code>', '<code>air handoff</code>', 'inspect how AIR is thinking'],
    'how-it-works.html': ['boot bundle · 3 files'],
    'use-cases.html': ['resumed it with nothing lost'],
}
for filename, bad in checks.items():
    value = text(filename)
    for phrase in bad:
        assert phrase not in value, (filename, phrase)
for filename in ['get-started.html','glossary.html','how-it-works.html','index.html','blog.html','use-cases.html','recovered-with-air.html','real-boot-vs-roleplay.html','showcase.html']:
    value = text(filename)
    assert '<main>' in value and '</html>' in value, filename
assert (P / 'showcase-session.md').stat().st_size > 1000
print('AIR v0.4 website alignment validation: PASS')
