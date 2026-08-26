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
        if LINK in text:
            continue
        if text.count("</head>") != 1:
            raise SystemExit(f"{path}: expected exactly one </head> marker")
        text = text.replace("</head>", LINK + "\n</head>", 1)
        file_path.write_text(text, encoding="utf-8")
        changed.append(path)

    print(f"visual contract links ensured: {len(changed)} page(s) changed")
    for path in changed:
        print(f"- {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
