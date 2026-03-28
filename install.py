#!/usr/bin/env python3
"""Install chant spinner verbs into Claude Code or VSCode settings."""

import argparse
import json
import os
import sys
from pathlib import Path

VERBS = [
    "Removing the flats from all the O Antiphons",
    "Putting flats in all the O Antiphons",
    "Reading the antiphon you were supposed to be singing",
    "Singing the diamond notes too quickly",
    "Singing the diamond notes too slowly",
    "Singing the diamond notes at the right speed",
    "Arguing with the ccwatershed guy about how to sing the diamond notes",
    "Adding inappropriate ictus marks",
    "Removing appropriate ictus marks",
    "Adding a swing rhythm to 'Qui habitat'",
    "Adding a swing rhythm to 'Requiem aeternam'",
    "Adding a hiphop beat to 'In paradisum'",
    "Replacing all the choir robes with pink",
    "Sneaking into the Vatican and changing all the choir robes to pink",
    "Sneaking into the Vatican and changing all the choir robes to pink while singing 'In paradisum'",
    "Sneaking 'Canada' into the O Antiphon sequence",
    "Replacing all the choir robes with pantsuits",
    "Sneaking pollen into the incense",
    "Blocking both ends of the otherwise empty pew",
    "Adding bunny ears to the artwork on the hymnals",
    "Intoning a random Mass part you hadn't prepared",
]


def vscode_path() -> Path:
    if sys.platform == "win32":
        return Path(os.environ["APPDATA"]) / "Code/User/settings.json"
    if sys.platform == "darwin":
        return Path.home() / "Library/Application Support/Code/User/settings.json"
    return Path.home() / ".config/Code/User/settings.json"


def claude_path(local: bool = False) -> Path:
    name = "settings.local.json" if local else "settings.json"
    return Path.home() / ".claude" / name


TARGETS = {
    "vscode":    vscode_path,
    "settings":  lambda: claude_path(local=False),
    "local":     lambda: claude_path(local=True),
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Install chant spinner verbs for Claude Code.")
    parser.add_argument(
        "--target", choices=list(TARGETS), default="vscode",
        help="Which settings file to update (default: vscode)",
    )
    parser.add_argument(
        "--mode", choices=["replace", "append"], default="replace",
        help="replace = only these verbs; append = add to Claude defaults (default: replace)",
    )
    args = parser.parse_args()

    path = TARGETS[args.target]()

    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print(f"Error: {path} is not valid JSON. Please fix it first.", file=sys.stderr)
            sys.exit(1)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        data = {}

    data["claudeCode.spinnerVerbs"] = {"mode": args.mode, "verbs": VERBS}
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Done — wrote {len(VERBS)} verbs to {path}")


if __name__ == "__main__":
    main()
