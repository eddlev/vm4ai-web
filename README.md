<p align="center">
  <picture>
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/eddlev/air-brand/main/github/readme-header-v2-light.svg?v=7">
    <img src="https://raw.githubusercontent.com/eddlev/air-brand/main/github/readme-header-v2-dark.svg?v=7" alt="AIR by VM4AI — Focused. Fluid. AIR." width="100%">
  </picture>
</p>

# AIR by VM4AI — Website

[![Made with AIR](https://raw.githubusercontent.com/eddlev/air-brand/main/made-with-air/made-with-air.svg)](https://vm4ai.com)
![Static site](https://img.shields.io/badge/site-static%20%C2%B7%20no%20build-9A8F80?labelColor=1A1613)
![Deploy](https://img.shields.io/badge/deploy-Cloudflare%20Pages-FF5A1F?labelColor=1A1613)

**Focused. Fluid. AIR.** — AI work, carried forward.

The source for **[vm4ai.com](https://vm4ai.com)**, the public site for **AIR**, the prompt-based framework from VM4AI.

The deployable site lives in [`public/`](public/) and has no build step. The landing page carries the Brand v2 positioning and visual system. The secondary pages are aligned to the current AIR **2.4.3** runtime semantics, including current onboarding, sole Orbit 0 artifact authority, capability packages, evidence/action boundaries, active-state reconciliation, alignment checks, and Handoff schema 2.2.0.

---

## Brand center

- **Promise:** AI work, carried forward.
- **Signature:** Focused. Fluid. AIR.
- **Focused:** one active task at a time.
- **Fluid:** continue without reconstructing the project.
- **AIR:** the project persists across sessions and platforms, subject to host compatibility.

The canonical brand rules and authored diagrams live in **[eddlev/air-brand](https://github.com/eddlev/air-brand)**.

## Runtime source of truth

Website explanations are derived from **[eddlev/vm4ai-air-kit](https://github.com/eddlev/vm4ai-air-kit)**. The repository runtime/contracts remain authoritative if website copy ever drifts.

Current public reference line:

- Core Runtime `2.4.3`
- Control Surface `2.4.3`
- Default Starter `2.4.3`
- Governance Supplement `2.2.0`
- Handoff schema `2.2.0`
- Floor registry `2.1.0`

## Structure

```text
vm4ai-web/
├─ public/
│  ├─ index.html           Brand v2 landing page
│  ├─ air-v2.css           shared Brand v2 base visual system
│  ├─ air-v2.js            landing-page behavior
│  ├─ air-pages.css        shared secondary-page layout/reference styles
│  ├─ air-site.js          shared secondary-page theme/nav/attentive-mark behavior
│  ├─ how-it-works.html    current conceptual runtime model
│  ├─ air-docs.html        AIR 2.4.3 human-readable technical reference
│  ├─ get-started.html     current boot → bind → work → Handoff path
│  ├─ glossary.html        current terminology and canonical modifiers
│  ├─ use-cases.html · about.html · services.html · blog.html
│  ├─ built-with-air.html · recovered-with-air.html · real-boot-vs-roleplay.html
│  ├─ from-morphic-to-air.html · showcase.html · made-with-air.html
│  ├─ showcase-session.md · showcase-handoff-card.json   historical evidence artifacts
│  ├─ privacy.html · terms.html · 404.html
│  ├─ og-image.png · favicon.* · apple-touch-icon.png · icon-192/512.png
│  ├─ site.webmanifest · robots.txt · sitemap.xml
│  └─ _headers             Cloudflare Pages security headers / CSP
├─ OFL-Space-Grotesk.txt
├─ OFL-JetBrains-Mono.txt
└─ README.md
```

## Site behavior

The small AIR mark in the navigation is the interactive/attentive website expression: the ember tracks the pointer and uses the restrained AIR blink. Secondary pages share that implementation through `air-site.js`; the large canonical/hero marks stay static.

The site is static and ships no analytics or tracking. `public/_headers` keeps the runtime locked to the site origin (`default-src 'self'`) with no third-party script, connection, or font origin enabled.

## Historical material

Some case-study evidence was captured on earlier AIR builds. Historical pages are labeled as such rather than silently rewritten to look like AIR 2.4.3. Retired concepts such as AMRS may still appear inside the preserved historical source artifacts, but they are not presented as current runtime semantics.

## Local preview

No toolchain required:

```bash
cd public
python3 -m http.server 8080
# http://localhost:8080
```

## Deploy — Cloudflare Pages

The site deploys via Cloudflare Pages Git integration:

| Setting | Value |
| --- | --- |
| Framework preset | None |
| Build command | *(empty)* |
| Build output directory | `public` |

`public/_headers` is applied automatically by Pages and sets CSP, HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy, and Permissions-Policy.

## Related repositories

- **[vm4ai-air-kit](https://github.com/eddlev/vm4ai-air-kit)** — operative AIR framework/runtime package.
- **[air-brand](https://github.com/eddlev/air-brand)** — canonical AIR brand system, tokens, logos, and authored diagrams.

## License

This site's own code and content are © Edward Levin (VM4AI) — all rights reserved. The included font licenses are SIL Open Font License 1.1.

The AIR framework code is licensed **Apache-2.0**. The **AIR** and **VM4AI** names and the dot-in-frame mark are reserved; see the brand usage terms in `air-brand`.

— [vm4ai.com](https://vm4ai.com)
