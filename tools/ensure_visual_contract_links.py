#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
MANIFEST = ROOT / "navigation.manifest.json"
LINK = '<link rel="stylesheet" href="air-visual-contract.css">'


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    changed: list[str] = []
    for entry in manifest["pages"]:
        path = str(entry["path"])
        file_path = PUBLIC / path
        text = file_path.read_text(encoding="utf-8")

        if text.count("</head>") != 1:
            raise SystemExit(f"{path}: expected exactly one </head> marker")

        count = text.count(LINK)
        if count > 1:
            raise SystemExit(f"{path}: expected at most one shared visual contract link, found {count}")

        head_close = text.index("</head>")
        if count == 1:
            link_pos = text.index(LINK)
            between = text[link_pos + len(LINK) : head_close]
            if not between.strip():
                continue
            text = text[:link_pos] + text[link_pos + len(LINK) :]
            head_close = text.index("</head>")

        text = text[:head_close] + LINK + "\n" + text[head_close:]
        file_path.write_text(text, encoding="utf-8")
        changed.append(path)

    print(f"visual contract links canonicalized: {len(changed)} page(s) changed")
    for path in changed:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
