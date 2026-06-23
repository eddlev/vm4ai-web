<p align="center">
  <img src="https://raw.githubusercontent.com/eddlev/air-brand/main/github/readme-header.png" alt="AIR by VM4AI — Configure. Organize. Execute." width="100%">
</p>

# AIR by VM4AI — Website

[![Made with AIR](https://raw.githubusercontent.com/eddlev/air-brand/main/made-with-air/made-with-air.svg)](https://vm4ai.com)
![Static site](https://img.shields.io/badge/site-static%20%C2%B7%20no%20build-9A8F80?labelColor=1A1613)
![Deploy](https://img.shields.io/badge/deploy-Cloudflare%20Pages-FF5A1F?labelColor=1A1613)

**Configure. Organize. Execute.** — Structure for any AI work.

The source for **[vm4ai.com](https://vm4ai.com)**, the public site for **AIR**, the prompt-based framework from VM4AI. This repository is the deployable site itself — a self-contained static bundle in [`public/`](public/) with no build step and no runtime dependencies.

> AIR is an overlay for AI chatbots — ChatGPT, Claude, Gemini, Grok, Mistral, or the model you choose. It configures a session into a structured, auditable, cooperative environment. This repo is the website that explains it; the framework lives in **[vm4ai-air-kit](https://github.com/eddlev/vm4ai-air-kit)**.

---

## Structure

```
vm4ai-web/
├─ public/                 the deployable site (this is what Cloudflare Pages serves)
│  ├─ index.html           home
│  ├─ how-it-works.html · get-started.html · use-cases.html · services.html
│  ├─ about.html · blog.html
│  ├─ built-with-air.html  case study — how AIR built its own brand & site
│  ├─ made-with-air.html   showcase — projects carrying the "Made with AIR" stamp
│  ├─ privacy.html · terms.html · 404.html
│  ├─ og-image.png · favicon.* · apple-touch-icon.png · icon-192/512.png
│  ├─ air-mark.svg · site.webmanifest
│  ├─ robots.txt · sitemap.xml
│  └─ _headers            Cloudflare Pages security headers (CSP, HSTS, etc.)
├─ OFL-Space-Grotesk.txt   font license (Space Grotesk)
├─ OFL-JetBrains-Mono.txt  font license (JetBrains Mono)
└─ README.md
```

The pages are self-contained: web fonts (Space Grotesk + JetBrains Mono) are inlined as base64, so the site loads **no external CSS, JS, fonts, or images** and ships **no analytics or tracking**. That privacy posture is stated in [`privacy.html`](public/privacy.html) and enforced by the Content-Security-Policy in [`public/_headers`](public/_headers).

## Local preview

No toolchain required — serve `public/` with any static server:

```bash
cd public
python3 -m http.server 8080
# → http://localhost:8080
```

## Deploy (Cloudflare Pages)

The site deploys via Cloudflare Pages' Git integration:

| Setting | Value |
| --- | --- |
| Framework preset | None |
| Build command | *(empty)* |
| Build output directory | `public` |

`public/_headers` is applied automatically by Pages and sets the CSP, `Strict-Transport-Security`, `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, and `Permissions-Policy`. `robots.txt` and `sitemap.xml` are served from the site root.

> Note: `og:image` and `<link rel="canonical">` reference the production origin `https://vm4ai.com`, so social/share previews resolve correctly only once deployed to that domain.

## Related repositories

- **[vm4ai-air-kit](https://github.com/eddlev/vm4ai-air-kit)** — the AIR framework: runtime, control surface, profiles, and docs.
- **[air-brand](https://github.com/eddlev/air-brand)** — the AIR brand kit: logos, tokens, fonts, diagrams, and the assets this site's header and stamp link to.

## License

This site's own code and content are © Edward Levin (VM4AI) — all rights reserved. The bundled web fonts are licensed under the SIL Open Font License (see OFL-Space-Grotesk.txt and OFL-JetBrains-Mono.txt).

The AIR framework is licensed **Apache-2.0** — see [vm4ai-air-kit](https://github.com/eddlev/vm4ai-air-kit). The **AIR** and **VM4AI** names and the dot-in-frame mark are **not** granted by that license; please don't use the marks to imply endorsement or affiliation. See [air-brand/USAGE.md](https://github.com/eddlev/air-brand/blob/main/USAGE.md). The "Made with AIR" stamp is welcome on genuine AIR-built projects.

— [vm4ai.com](https://vm4ai.com)
