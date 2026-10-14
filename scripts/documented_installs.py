#!/usr/bin/env python3
"""List the install commands the READMEs document, ready to run on kind (#317).

Three documented `helm install` commands set neither `auth` nor
`config.unsafeNoAuth`. Core 2.26.0 refuses to serve HTTP on a non-loopback
address without authentication, so a reader who pasted any of them got a pod
that never became Ready, and `NOTES.txt` said so. Nothing in CI ran what the
READMEs tell a reader to run: the install smoke runs its own flags.

A fenced block with `<!-- ci:documented-install -->` on the line above it is a
promise that every `helm install` in it reaches Ready. This prints those
commands, one block at a time, for `ci-charts` to run:

    ### README.md:80
    helm install mcp-hangar ./mcp-hangar --set ...

Two things are rewritten, and nothing else:

- `oci://ghcr.io/mcp-hangar/charts/<chart>` becomes `./<chart>`, because the
  command in the README installs the *published* chart and the job must test the
  one in the tree.
- a command is joined across its `\\` continuations onto one line.

`--list` prints only `file:line` and the command count, for a quick look.

Usage: scripts/documented_installs.py [--list]
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
READMES = ("README.md", "mcp-hangar/README.md", "mcp-hangar-operator/README.md")
MARKER = "<!-- ci:documented-install -->"
OCI = re.compile(r"oci://ghcr\.io/mcp-hangar/charts/([A-Za-z0-9._-]+)")


def blocks(path: Path) -> list[tuple[int, list[str]]]:
    """Each marked fence of *path*: the line of the fence and its `helm install` commands."""
    lines = path.read_text(encoding="utf-8").splitlines()
    found: list[tuple[int, list[str]]] = []
    for index, line in enumerate(lines):
        if line.strip() != MARKER:
            continue
        fence = index + 1
        if fence >= len(lines) or not lines[fence].startswith("```"):
            raise SystemExit(f"{path}:{index + 1}: the marker is not directly above a fenced block")
        body: list[str] = []
        cursor = fence + 1
        while cursor < len(lines) and not lines[cursor].startswith("```"):
            body.append(lines[cursor])
            cursor += 1
        found.append((fence + 1, commands(body)))
    return found


def commands(body: list[str]) -> list[str]:
    """The `helm install` commands of a block, continuations joined and charts made local."""
    joined: list[str] = []
    pending = ""
    for raw in body:
        text = raw.strip()
        if not pending and (not text or text.startswith("#")):
            continue
        if text.endswith("\\"):
            pending += text[:-1].strip() + " "
            continue
        joined.append((pending + text).strip())
        pending = ""
    return [OCI.sub(r"./\1", command) for command in joined if command.startswith("helm install ")]


def main(argv: list[str]) -> int:
    total = 0
    for name in READMES:
        path = ROOT / name
        if not path.exists():
            continue
        for line, found in blocks(path):
            if not found:
                raise SystemExit(f"{name}:{line}: marked block has no `helm install` command")
            total += len(found)
            print(f"### {name}:{line}")
            if "--list" not in argv:
                print("\n".join(found))
    if total == 0:
        raise SystemExit("no documented install command is marked; the check would pass on nothing")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
