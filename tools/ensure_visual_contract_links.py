#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
MANIFEST = ROOT / "navigation.manifest.json"
LINK = '<link rel="stylesheet" href="air-visual-contract.css">'
CANONICAL_TAIL = LINK + "\n</head>"


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
        if count == 1 and CANONICAL_TAIL in text:
            continue

        if count == 1:
            text = text.replace(LINK, "", 1)

        text = text.replace("</head>", CANONICAL_TAIL, 1)
        file_path.write_text(text, encoding="utf-8")
        changed.append(path)

    print(f"visual contract links canonicalized: {len(changed)} page(s) changed")
    for path in changed:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
