#!/usr/bin/env python3
"""Initialize the file contract used by graduate-thesis-workbench."""

from __future__ import annotations

import argparse
from pathlib import Path


TEMPLATES = {
    "plan/project-overview.md": """# Project Overview

- Project root:
- Thesis type:
- Domain:
- Language:
- Output format:
- Formatting authority:
- Current artifact:
- Target section:
- Evidence status:
- Allowed edits:
- Open blockers:
""",
    "plan/outline.md": """# Thesis Outline

| Section | Purpose | Central claim | Inputs | Outputs | Dependencies | Status |
|---|---|---|---|---|---|---|
""",
    "plan/progress.md": """# Progress

| Item | Status | Evidence | Owner | Next action |
|---|---|---|---|---|
""",
    "plan/claim-ledger.md": """# Claim Ledger

| ID | Claim | Type | Evidence IDs | Allowed wording | Forbidden wording | Status |
|---|---|---|---|---|---|---|
""",
    "plan/evidence-map.md": """# Evidence Map

| Evidence ID | Source/data | Type | Exact finding | Claim slot | Location | Risk |
|---|---|---|---|---|---|---|
""",
    "plan/author-voice-profile.md": """# Author Voice Profile

- Author:
- Sample files:
- Sentence rhythm:
- Preferred terminology:
- Preferred transitions:
- Hedging conventions:
- Formatting conventions:
- Terms or patterns to preserve:
- Terms or patterns to avoid:
- Last reviewed:
""",
    "plan/ai-assistance-log.md": """# AI Assistance Log

| Date | Section/file | User-provided material | AI-assisted action | Author review | Evidence check | Disclosure decision |
|---|---|---|---|---|---|---|
""",
    "figures/figure-catalog.md": """# Figure Catalog

Create one brief for every figure before drawing it.

""",
    "figures/data-manifest.md": """# Data Manifest

| Figure | Data file | Real/mock | Source | Transformations | Script | Outputs |
|---|---|---|---|---|---|---|
""",
    "references/reference-ledger.csv": (
        "id,title,authors,year,venue,doi_or_url,status,verified_location,notes\n"
    ),
    "qa/audit-report.md": """# Audit Report

- Status:
- Verification command:
- Structural findings:
- Evidence findings:
- Numerical findings:
- Visual findings:
- Reference findings:
- DOCX/PDF findings:
- Remaining risk:
""",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create the graduate-thesis-workbench project contract."
    )
    parser.add_argument("project_root", help="Thesis project root")
    parser.add_argument("--title", default="", help="Working thesis title")
    parser.add_argument("--thesis-type", default="graduate thesis")
    parser.add_argument("--domain", default="")
    parser.add_argument("--language", default="Chinese")
    parser.add_argument("--output-format", default="DOCX")
    parser.add_argument("--formatting-authority", default="")
    parser.add_argument("--current-artifact", default="")
    parser.add_argument("--target-section", default="")
    parser.add_argument("--evidence-status", default="partial")
    parser.add_argument("--allowed-edits", default="")
    return parser.parse_args()


def write_if_missing(path: Path, content: str) -> str:
    if path.exists():
        return "EXISTS"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")
    return "CREATED"


def overview_text(args: argparse.Namespace) -> str:
    return f"""# Project Overview

- Project root: {Path(args.project_root).resolve()}
- Working title: {args.title}
- Thesis type: {args.thesis_type}
- Domain: {args.domain}
- Language: {args.language}
- Output format: {args.output_format}
- Formatting authority: {args.formatting_authority}
- Current artifact: {args.current_artifact}
- Target section: {args.target_section}
- Evidence status: {args.evidence_status}
- Allowed edits: {args.allowed_edits}
- Open blockers:
"""


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)

    statuses: list[str] = []
    for relative, template in TEMPLATES.items():
        if relative == "plan/project-overview.md":
            template = overview_text(args)
        status = write_if_missing(root / relative, template)
        statuses.append(status)
        print(f"[{status}] {root / relative}")

    (root / "plan/task-packets").mkdir(parents=True, exist_ok=True)
    print(f"[READY] {root / 'plan/task-packets'}")
    print(
        f"[SUMMARY] created={statuses.count('CREATED')} "
        f"existing={statuses.count('EXISTS')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
