#!/usr/bin/env python3
"""Install chant spinner verbs into Claude Code or VSCode settings."""

import argparse
import json
import os
import sys
import urllib.request
from pathlib import Path

VERBS_URL = "https://raw.githubusercontent.com/drj-chantschool/chant-spinner-verbs/master/verbs.json"


def fetch_verbs() -> list[str]:
    with urllib.request.urlopen(VERBS_URL) as r:
        return json.loads(r.read())


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
    "vscode":   vscode_path,
    "settings": lambda: claude_path(local=False),
    "local":    lambda: claude_path(local=True),
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

    verbs = fetch_verbs()
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

    data["claudeCode.spinnerVerbs"] = {"mode": args.mode, "verbs": verbs}
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Done — wrote {len(verbs)} verbs to {path}")


if __name__ == "__main__":
    main()
