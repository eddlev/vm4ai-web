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

The deployable site lives in [`public/`](public/) and has no build step. The homepage is the Brand v2 implementation: outcome-first positioning, the Focused / Fluid / AIR visual grammar, light/dark parity, structured continuity messaging, and explicit prompt-layer trust boundaries.

---

## Brand center

- **Promise:** AI work, carried forward.
- **Signature:** Focused. Fluid. AIR.
- **Focused:** one active task at a time.
- **Fluid:** continue without reconstructing the project.
- **AIR:** the project persists across sessions and compatible platforms.

The canonical brand rules and authored diagrams live in **[eddlev/air-brand](https://github.com/eddlev/air-brand)**.

## Structure

```text
vm4ai-web/
├─ navigation.manifest.json    canonical page, journey and target-navigation contract
├─ tools/
│  └─ validate_navigation.py   deterministic site/link/navigation validator
├─ public/
│  ├─ index.html               Brand v2 homepage
│  ├─ explore-air.html         human-facing site map
│  ├─ where-air-fits.html      category / architecture map
│  ├─ air-for-development.html · spec-driven-development.html
│  ├─ specification-first-verification.html · testing-and-evidence.html
│  ├─ air-v2.css               homepage visual system + responsive/light-dark rules
│  ├─ air-v2.js                theme persistence + mobile navigation
│  ├─ how-it-works.html · get-started.html · use-cases.html · services.html
│  ├─ about.html · blog.html · air-docs.html · glossary.html
│  ├─ built-with-air.html · recovered-with-air.html · real-boot-vs-roleplay.html
│  ├─ from-morphic-to-air.html · showcase.html · made-with-air.html
│  ├─ privacy.html · terms.html · 404.html
│  ├─ og-image.png · favicon.* · apple-touch-icon.png · icon-192/512.png
│  ├─ site.webmanifest · robots.txt · sitemap.xml
│  └─ _headers                 Cloudflare Pages security headers / CSP
├─ OFL-Space-Grotesk.txt
├─ OFL-JetBrains-Mono.txt
└─ README.md
```

## Navigation contract

[`navigation.manifest.json`](navigation.manifest.json) is the canonical inventory for the site's public HTML pages and intended navigation model. It records:

- every top-level public HTML page, including whether it belongs in `sitemap.xml`;
- minimum inbound-link requirements for important discovery surfaces;
- the primary-navigation and footer labels targeted by the future shared-chrome refactor;
- the visitor journeys used by **Explore AIR**: Start, Understand, Use, Trust & Evidence, and VM4AI.

Run the deterministic standard-library validator from the repository root:

```bash
python3 tools/validate_navigation.py
```

The normal check fails on structural defects that should not ship:

- a top-level HTML page is missing from the manifest, or a manifest page is missing from `public/`;
- `sitemap.xml` disagrees with the manifest's explicit sitemap policy;
- an internal `href` points to a missing local target;
- an important page falls below its configured minimum number of unique inbound source pages;
- the manifest's own navigation or journey references point to unregistered pages.

Shared header/footer markup is still duplicated across the legacy HTML pages. Until that refactor is complete, differences between current page chrome and the manifest's target chrome are reported as warnings rather than hard failures.

For the shared-chrome refactor and its final verification, use:

```bash
python3 tools/validate_navigation.py --strict-chrome
```

`--strict-chrome` turns primary-navigation/footer drift into an error gate. This lets the manifest become the contract for generated shared chrome without making the current legacy duplication block unrelated content work in the meantime.

The validator is a development/release check only. It does **not** add a build step or runtime dependency to the deployed site.

## Runtime/privacy posture

The site is static and ships no analytics or tracking. `public/_headers` keeps the runtime locked to the site origin (`default-src 'self'`) with no third-party script, connection, or font origin enabled.

The Brand v2 homepage currently uses the local/system font fallback stack under that CSP. The remaining legacy pages retain their existing embedded font treatment. Moving the canonical WOFF files into the site bundle is a separate asset migration; it should not be solved by loosening the CSP to a third-party font origin.

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

- **[vm4ai-air-kit](https://github.com/eddlev/vm4ai-air-kit)** — AIR framework/runtime package.
- **[air-brand](https://github.com/eddlev/air-brand)** — canonical AIR brand system, tokens, logos, fonts, and diagrams.

## License

This site's own code and content are © Edward Levin (VM4AI) — all rights reserved. The included font licenses are SIL Open Font License 1.1.

The AIR framework is licensed **Apache-2.0**. The **AIR** and **VM4AI** names and the dot-in-frame mark are reserved; see the brand usage terms in `air-brand`.

— [vm4ai.com](https://vm4ai.com)
