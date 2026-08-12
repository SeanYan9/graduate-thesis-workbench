#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render_mermaid.py — Render a .mmd file to PNG/SVG via mmdc (local) or Kroki API.

Distilled from https://github.com/Agents365-ai/mermaid-skill (MIT).
Validation-first: never export before syntax check; fall back to Kroki when
mmdc or its headless Chrome is unavailable.

Usage:
    python render_mermaid.py <input.mmd> [--out out.png] [--width 2048]
                             [--format png|svg] [--theme base]

Output: prints the exported file path.
"""
import argparse
import base64
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
import zlib
from pathlib import Path


def mmdc_cmd() -> list:
    """Windows npm global bin exposes mmdc.cmd; subprocess cannot exec a
    .cmd directly, so route through cmd /c there."""
    if os.name == "nt":
        return ["cmd", "/c", "mmdc"]
    return ["mmdc"]


def check_mmdc() -> bool:
    """mmdc must exist AND have a usable Chrome (mmdc --version passes even
    without Chrome, so probe an actual export in validate_mmdc)."""
    return shutil.which("mmdc") is not None


def validate_mmdc(mmd: Path) -> bool:
    """Try a throwaway export to prove Chrome works; ignore its output."""
    probe = Path(mmd.parent) / "_probe.png"
    try:
        r = subprocess.run(
            mmdc_cmd() + ["-i", str(mmd), "-o", str(probe), "-w", "800",
                          "--backgroundColor", "white"],
            capture_output=True, timeout=120)
        ok = r.returncode == 0 and probe.exists()
    except Exception:
        ok = False
    finally:
        if probe.exists():
            probe.unlink()
    return ok


def render_mmdc(mmd: Path, out: Path, width: int, fmt: str, theme: str) -> bool:
    cmd = mmdc_cmd() + ["-i", str(mmd), "-o", str(out), "-w", str(width),
                        "--backgroundColor", "white"]
    if theme and theme != "base":
        cmd += ["--theme", theme]
    try:
        r = subprocess.run(cmd, capture_output=True, timeout=180)
        return r.returncode == 0 and out.exists()
    except Exception:
        return False


def render_kroki(mmd: Path, out: Path, fmt: str) -> bool:
    """Kroki HTTP API: POST body to https://kroki.io/mermaid/{png|svg}.
    Zero-install fallback (only needs a network connection)."""
    url = f"https://kroki.io/mermaid/{fmt}"
    body = mmd.read_bytes()
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"Content-Type": "text/plain",
                                          "User-Agent": "thesis-workbench/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        if resp.status == 200 and data:
            out.write_bytes(data)
            return True
    except (urllib.error.URLError, urllib.error.HTTPError, OSError):
        pass
    return False


def main():
    ap = argparse.ArgumentParser(description="Render .mmd to PNG/SVG")
    ap.add_argument("input", type=Path, help="input .mmd file")
    ap.add_argument("--out", type=Path, default=None)
    ap.add_argument("--width", type=int, default=2048)
    ap.add_argument("--format", choices=["png", "svg"], default="png")
    ap.add_argument("--theme", default="base")
    args = ap.parse_args()

    mmd: Path = args.input
    if not mmd.exists():
        sys.exit(f"input not found: {mmd}")
    fmt = args.format
    out = args.out or (mmd.parent / f"{mmd.stem}.{fmt}")

    # 1) local mmdc
    if check_mmdc():
        if validate_mmdc(mmd):
            if render_mmdc(mmd, out, args.width, fmt, args.theme):
                print(f"rendered via mmdc -> {out}")
                sys.exit(0)
            sys.exit(f"mmdc export failed: {out}")
        print("mmdc found but headless Chrome missing; falling back to Kroki")
    else:
        print("mmdc not found; using Kroki API")

    # 2) Kroki API (PNG/SVG only; no PDF)
    if fmt in ("png", "svg") and render_kroki(mmd, out, fmt):
        print(f"rendered via Kroki -> {out}")
        sys.exit(0)

    sys.exit("render failed: no usable backend (mmdc+Chrome or Kroki)")


if __name__ == "__main__":
    main()
