# AIR v2.4 current session walkthrough

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
