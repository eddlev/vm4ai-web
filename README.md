<p align="center">
  <img src="github/readme-header.png" alt="AIR by VM4AI — Configure. Organize. Execute." width="100%">
</p>

# AIR by VM4AI — Brand Kit

![License](https://img.shields.io/badge/license-Apache--2.0-C9A227?labelColor=1A1613)
![Framework](https://img.shields.io/badge/framework-prompt--based-9A8F80?labelColor=1A1613)
![Made with AIR](https://img.shields.io/badge/made%20with-AIR-FF5A1F?labelColor=1A1613)

**Configure. Organize. Execute.** — Structure for any AI work.

The complete brand system for **AIR**, the prompt-based framework from VM4AI. Open **`brand-book.html`** for the full reference (strategy, voice, logo, color, type, the AIR model diagrams, and usage rules).

---

## Structure

```
brand/
├─ brand-book.html        the full brand book (open in a browser)
├─ brand-ai-brief.md      paste into any AI for on-brand output
├─ USAGE.md               brand mark & stamp usage terms
├─ logos/                 12 logo SVGs (primary · stacked · wordmark · mono · mark · favicon)
├─ tokens/
│  ├─ air-tokens.css      design tokens (color · type · light/dark · @font-face)
│  ├─ tokens.json         the same tokens as JSON
│  └─ fonts/              self-hosted Space Grotesk + JetBrains Mono (.woff)
├─ web/                   favicon set · site.webmanifest · og-image (1200×630)
├─ social/                X · LinkedIn · GitHub avatars, banners, post templates
├─ made-with-air/         attribution stamp — pill & seal, clean & period, SVG + PNG
├─ diagrams/              the AIR model diagrams (standalone SVG + PNG)
├─ templates/             deck (.pptx) · letterhead (.docx) · email signature · cheat-sheet (.pdf)
└─ github/                README header, divider, section header
```

## Quick start

- **Colors & type** — drop `tokens/air-tokens.css` into any page; it ships light/dark theming and `@font-face`.
- **Logos** — use `logos/air-logo-primary-dark.svg` on dark, `…-light.svg` on light; `logos/air-mark.svg` for square/avatar use.
- **Fonts** — self-host from `tokens/fonts/`, or load Space Grotesk + JetBrains Mono from Google Fonts.
- **Generating with AI** — paste `brand-ai-brief.md` into any AI tool before producing posts, docs, decks, or images.

## Made with AIR

If your project is built with AIR, add the badge:

```markdown
[![Made with AIR](made-with-air/made-with-air.svg)](https://vm4ai.com)
```

[![Made with AIR](made-with-air/made-with-air.svg)](https://vm4ai.com)

## License

The framework code is licensed under **Apache-2.0**. The brand itself — the **AIR** and **VM4AI** names and the dot-in-frame mark — is **not** granted by that license; please don't use the marks to imply endorsement or affiliation. The "Made with AIR" stamp is welcome on genuine AIR-built projects.

— vm4ai.com
