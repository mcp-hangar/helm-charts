#!/usr/bin/env python3
"""Vendor the operator's generated CRDs into the operator chart's templates.

The chart ships the CRDs as templates rather than in `crds/`, so `crds.install`
and `crds.keep` can govern them and they carry the chart's labels. That means a
copy is not enough: four edits turn a generated CRD into the chart's template,
and doing them by hand is how the vendored copies fell two releases behind the
API they describe (#168).

Usage:
    python scripts/vendor-operator-crds.py --operator /path/to/mcp-hangar-operator
    python scripts/vendor-operator-crds.py --operator ... --check

`--check` rewrites nothing and exits 1 if any vendored file is out of date, for
asking "are we behind" in CI without writing.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

CHART = "mcp-hangar-operator"
#: generated basename -> vendored template basename
CRDS = {
    "mcp-hangar.io_mcpservers.yaml": "mcpserver.yaml",
    "mcp-hangar.io_mcpdiscoverysources.yaml": "mcpdiscoverysource.yaml",
    "mcp-hangar.io_mcpegresspolicies.yaml": "mcpegresspolicy.yaml",
    "mcp-hangar.io_mcpservergroups.yaml": "mcpservergroup.yaml",
}

KEEP_BLOCK = [
    "    {{- if .Values.crds.keep }}",
    "    helm.sh/resource-policy: keep",
    "    {{- end }}",
]
LABELS_BLOCK = [
    "  labels:",
    '    {{- include "mcp-hangar-operator.labels" . | nindent 4 }}',
]


def to_template(generated: str) -> str:
    """Apply the chart's four edits to a generated CRD.

    Anchored on the lines controller-gen always emits, and each anchor is
    asserted: a silent no-op here would vendor a CRD the chart cannot govern.
    """
    lines = generated.splitlines()

    try:
        ann = next(i for i, l in enumerate(lines) if l == "  annotations:")
        name = next(i for i, l in enumerate(lines) if l.startswith("  name: "))
    except StopIteration:  # pragma: no cover -- guarded, not expected
        raise SystemExit("generated CRD has no metadata.annotations / metadata.name")
    if not name > ann:
        raise SystemExit("unexpected CRD layout: name does not follow annotations")

    # Insert from the bottom up so the earlier index stays valid.
    lines[name + 1 : name + 1] = LABELS_BLOCK
    lines[ann + 2 : ann + 2] = KEEP_BLOCK  # after the controller-gen annotation

    return "\n".join(["{{- if .Values.crds.install }}", *lines, "{{- end }}"]) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--operator", required=True, help="Path to the mcp-hangar-operator checkout.")
    ap.add_argument("--charts", default=".", help="Path to the helm-charts repo root.")
    ap.add_argument("--check", action="store_true", help="Report drift, write nothing, exit 1 if behind.")
    args = ap.parse_args()

    bases = Path(args.operator).expanduser().resolve() / "config" / "crd" / "bases"
    dest = Path(args.charts).expanduser().resolve() / CHART / "templates" / "crds"
    if not bases.is_dir():
        raise SystemExit(f"no generated CRDs at {bases}")

    stale = []
    for src_name, out_name in CRDS.items():
        src, out = bases / src_name, dest / out_name
        if not src.is_file():
            raise SystemExit(f"missing generated CRD: {src}")
        want = to_template(src.read_text(encoding="utf-8"))
        have = out.read_text(encoding="utf-8") if out.is_file() else ""
        if want == have:
            print(f"up to date: {out_name}")
            continue
        stale.append(out_name)
        if args.check:
            print(f"STALE: {out_name} ({len(have)} -> {len(want)} bytes)")
        else:
            out.write_text(want, encoding="utf-8")
            print(f"vendored: {out_name} ({len(have)} -> {len(want)} bytes)")

    if args.check and stale:
        print(f"\nFAIL: {len(stale)} vendored CRD(s) behind the operator. Run without --check.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
