#!/usr/bin/env python3
"""Validate a graduate thesis workspace against the skill's hard gates."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


REQUIRED_FILES = (
    "plan/project-overview.md",
    "plan/outline.md",
    "plan/progress.md",
    "plan/claim-ledger.md",
    "plan/evidence-map.md",
    "figures/figure-catalog.md",
    "figures/data-manifest.md",
    "references/reference-ledger.csv",
    "qa/audit-report.md",
)

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "__pycache__",
    "agents",
    "figures",
    "plan",
    "qa",
    "references",
    "scripts",
    "tests",
    "_thesis_build",
}

MANUSCRIPT_SUFFIXES = {".md", ".tex", ".txt", ".rst"}
BLOCKING_CLAIM_STATUSES = {
    "needs-evidence",
    "needs_data",
    "needs-data",
    "placeholder",
    "blocked",
    "unverified",
    "unverifiable",
}
VALID_CLAIM_STATUSES = {
    "verified",
    "supported",
    "observed",
    "inferred",
    *BLOCKING_CLAIM_STATUSES,
}


@dataclass
class Finding:
    severity: str
    code: str
    message: str
    path: str = ""


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower())


def split_md_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def is_separator(line: str) -> bool:
    cells = split_md_row(line)
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def read_markdown_table(path: Path) -> list[dict[str, str]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    for index in range(len(lines) - 1):
        if "|" not in lines[index] or not is_separator(lines[index + 1]):
            continue
        headers = split_md_row(lines[index])
        rows: list[dict[str, str]] = []
        for row_line in lines[index + 2 :]:
            if "|" not in row_line or not row_line.strip():
                if rows:
                    break
                continue
            if is_separator(row_line):
                continue
            values = split_md_row(row_line)
            if len(values) != len(headers):
                continue
            rows.append({norm(key): value.strip() for key, value in zip(headers, values)})
        return rows
    return []


def get_field(row: dict[str, str], *aliases: str) -> str:
    for alias in aliases:
        value = row.get(norm(alias))
        if value is not None:
            return value.strip()
    return ""


def add(
    findings: list[Finding],
    severity: str,
    code: str,
    message: str,
    path: Path | None = None,
) -> None:
    findings.append(
        Finding(
            severity=severity,
            code=code,
            message=message,
            path=str(path) if path else "",
        )
    )


def parse_ids(value: str, prefix: str) -> set[str]:
    return set(re.findall(rf"\b{re.escape(prefix)}-\d+\b", value, flags=re.I))


def expand_citation_token(token: str) -> set[int]:
    token = token.replace("，", ",").replace("–", "-").replace("—", "-")
    result: set[int] = set()
    for part in token.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = (piece.strip() for piece in part.split("-", 1))
            if start.isdigit() and end.isdigit() and int(start) <= int(end):
                result.update(range(int(start), int(end) + 1))
        elif part.isdigit():
            result.add(int(part))
    return result


def manuscript_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in MANUSCRIPT_SUFFIXES:
            continue
        relative_parts = set(path.relative_to(root).parts)
        if relative_parts & EXCLUDED_DIRS:
            continue
        files.append(path)
    return sorted(files)


def validate_contract(root: Path, findings: list[Finding]) -> None:
    for relative in REQUIRED_FILES:
        path = root / relative
        if not path.exists():
            add(findings, "error", "MISSING_CONTRACT", "Required project file is missing.", path)


def validate_claims_and_evidence(root: Path, findings: list[Finding]) -> None:
    claim_path = root / "plan/claim-ledger.md"
    evidence_path = root / "plan/evidence-map.md"
    if not claim_path.exists() or not evidence_path.exists():
        return

    claims = read_markdown_table(claim_path)
    evidence_rows = read_markdown_table(evidence_path)
    evidence_ids = {
        get_field(row, "Evidence ID", "Evidence")
        for row in evidence_rows
        if get_field(row, "Evidence ID", "Evidence")
    }
    if not claims:
        add(findings, "error", "EMPTY_CLAIM_LEDGER", "Claim ledger has no substantive rows.", claim_path)
    if not evidence_rows:
        add(findings, "error", "EMPTY_EVIDENCE_MAP", "Evidence map has no substantive rows.", evidence_path)

    for row in claims:
        claim_id = get_field(row, "ID", "Claim ID") or "<unknown claim>"
        status = norm(get_field(row, "Status"))
        if status not in VALID_CLAIM_STATUSES:
            add(
                findings,
                "error",
                "INVALID_CLAIM_STATUS",
                f"{claim_id} has unsupported status {status!r}.",
                claim_path,
            )
        if status in BLOCKING_CLAIM_STATUSES:
            add(
                findings,
                "error",
                "BLOCKED_CLAIM",
                f"{claim_id} is marked {status}; it cannot enter final manuscript prose.",
                claim_path,
            )
        evidence_value = get_field(row, "Evidence IDs", "Evidence ID", "Evidence")
        referenced = parse_ids(evidence_value, "E")
        missing = sorted(referenced - evidence_ids)
        if missing:
            add(
                findings,
                "error",
                "MISSING_EVIDENCE_LINK",
                f"{claim_id} refers to missing evidence IDs: {', '.join(missing)}.",
                claim_path,
            )
        if status in {"verified", "supported", "observed", "inferred"} and not referenced:
            add(
                findings,
                "error",
                "CLAIM_WITHOUT_EVIDENCE",
                f"{claim_id} has status {status} but no evidence ID.",
                claim_path,
            )

    for row in evidence_rows:
        evidence_id = get_field(row, "Evidence ID", "Evidence") or "<unknown evidence>"
        location = get_field(row, "Location")
        exact_finding = get_field(row, "Exact finding", "Finding")
        if not location or not exact_finding:
            add(
                findings,
                "error",
                "INCOMPLETE_EVIDENCE",
                f"{evidence_id} must include an exact finding and a source/data location.",
                evidence_path,
            )


def validate_references(root: Path, findings: list[Finding]) -> set[int]:
    reference_path = root / "references/reference-ledger.csv"
    if not reference_path.exists():
        return set()

    with reference_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        add(findings, "error", "EMPTY_REFERENCE_LEDGER", "Reference ledger has no entries.", reference_path)
        return set()

    identifiers: set[int] = set()
    for row_number, row in enumerate(rows, start=2):
        normalized = {norm(key): (value or "").strip() for key, value in row.items()}
        raw_id = (
            normalized.get("id")
            or normalized.get("number")
            or normalized.get("ref_id")
            or normalized.get("citation")
        )
        status = norm(normalized.get("status", ""))
        title = normalized.get("title", "")
        location = normalized.get("verified_location", "") or normalized.get("doi_or_url", "")
        if raw_id and raw_id.strip("[]").isdigit():
            identifiers.add(int(raw_id.strip("[]")))
        else:
            add(
                findings,
                "error",
                "INVALID_REFERENCE_ID",
                f"Reference row {row_number} has a non-numeric citation ID.",
                reference_path,
            )
        if not title:
            add(findings, "error", "MISSING_REFERENCE_TITLE", f"Reference row {row_number} has no title.", reference_path)
        if status != "verified":
            add(
                findings,
                "error",
                "UNVERIFIED_REFERENCE",
                f"Reference row {row_number} is not verified: {status or '<blank>'}.",
                reference_path,
            )
        if not location:
            add(
                findings,
                "error",
                "REFERENCE_WITHOUT_LOCATION",
                f"Reference row {row_number} has no DOI, URL, or verified location.",
                reference_path,
            )
    return identifiers


def validate_manuscript(
    root: Path,
    findings: list[Finding],
    reference_ids: set[int],
) -> set[int]:
    cited: set[int] = set()
    files = manuscript_files(root)
    if not files:
        add(findings, "warning", "NO_MANUSCRIPT_TEXT", "No Markdown, LaTeX, text, or reStructuredText manuscript file was found.")
        return cited

    citation_pattern = re.compile(r"\[((?:\d+\s*(?:[,，]\s*\d+|\s*[-–—]\s*\d+)*))\]")
    forbidden = re.compile(
        r"(?:TODO|TBD|待核验|待补充|待完善|NEEDS_EVIDENCE|NEEDS_DATA|"
        r"\bmock[_-]|\bsynthetic[_-])",
        flags=re.I,
    )
    for path in files:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        for line_number, line in enumerate(lines, start=1):
            for match in citation_pattern.finditer(line):
                cited.update(expand_citation_token(match.group(1)))
            if forbidden.search(line):
                add(
                    findings,
                    "error",
                    "MANUSCRIPT_PLACEHOLDER",
                    "Manuscript contains a planning placeholder, unresolved evidence marker, or mock/synthetic data token.",
                    path,
                )
            if "注:" in line or "注：" in line:
                following = next((item.strip() for item in lines[line_number:] if item.strip()), "")
                if not following.startswith("数据来源:") and not following.startswith("数据来源："):
                    add(
                        findings,
                        "error",
                        "TABLE_SOURCE_LINE_MISSING",
                        "A table note must be followed by a separate data-source line.",
                        path,
                    )

    missing = sorted(cited - reference_ids)
    if missing:
        add(
            findings,
            "error",
            "CITATION_NOT_IN_LEDGER",
            f"In-text citations are absent from the reference ledger: {', '.join(map(str, missing))}.",
        )
    return cited


def parse_figure_briefs(path: Path) -> dict[str, dict[str, str]]:
    briefs: dict[str, dict[str, str]] = {}
    current_id = ""
    current: dict[str, str] = {}
    field_pattern = re.compile(r"^\s*-\s*([A-Za-z][A-Za-z _/-]*):\s*(.*?)\s*$")
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        heading = re.match(r"^\s*#{1,3}\s+Figure\s+(F-\d+)\b", line, flags=re.I)
        if heading:
            if current_id:
                briefs[current_id] = current
            current_id = heading.group(1).upper()
            current = {}
            continue
        match = field_pattern.match(line)
        if match and current_id:
            current[norm(match.group(1))] = match.group(2).strip()
    if current_id:
        briefs[current_id] = current
    return briefs


def validate_figures(root: Path, findings: list[Finding]) -> None:
    catalog_path = root / "figures/figure-catalog.md"
    manifest_path = root / "figures/data-manifest.md"
    if not catalog_path.exists() or not manifest_path.exists():
        return

    briefs = parse_figure_briefs(catalog_path)
    manifest_rows = read_markdown_table(manifest_path)
    if not briefs and manifest_rows:
        add(findings, "error", "FIGURE_BRIEF_MISSING", "Data manifest has figures but figure catalog has no figure briefs.", catalog_path)
    if not manifest_rows and briefs:
        add(findings, "error", "FIGURE_MANIFEST_MISSING", "Figure catalog has briefs but data manifest has no rows.", manifest_path)

    required_brief_fields = {
        "claim supported",
        "artifact type",
        "provenance",
        "caption takeaway",
    }
    for figure_id, fields in briefs.items():
        missing = sorted(field for field in required_brief_fields if not fields.get(field))
        if missing:
            add(
                findings,
                "error",
                "INCOMPLETE_FIGURE_BRIEF",
                f"{figure_id} is missing: {', '.join(missing)}.",
                catalog_path,
            )
        artifact_type = norm(fields.get("artifact type", ""))
        if artifact_type == "exact-data" and not fields.get("data source"):
            add(findings, "error", "EXACT_FIGURE_WITHOUT_DATA", f"{figure_id} is exact-data but has no data source.", catalog_path)

    for row in manifest_rows:
        figure_id = get_field(row, "Figure")
        data_file = get_field(row, "Data file")
        real_mock = norm(get_field(row, "Real/mock", "Real / mock"))
        source = get_field(row, "Source")
        script = get_field(row, "Script")
        outputs = get_field(row, "Outputs")
        if not figure_id:
            add(findings, "error", "FIGURE_ID_MISSING", "A data-manifest row has no figure ID.", manifest_path)
            continue
        figure_id = figure_id.upper()
        if figure_id not in briefs:
            add(findings, "error", "FIGURE_WITHOUT_BRIEF", f"{figure_id} is in the data manifest but not the figure catalog.", manifest_path)
        if "mock" in real_mock or "synthetic" in real_mock or re.search(r"\b(?:mock|synthetic)[_-]", data_file, flags=re.I):
            add(
                findings,
                "error",
                "MOCK_DATA_BLOCKED",
                f"{figure_id} uses mock or synthetic data; exact results figures require real traceable data.",
                manifest_path,
            )
        if not data_file or not source or not script or not outputs:
            add(
                findings,
                "error",
                "INCOMPLETE_DATA_MANIFEST",
                f"{figure_id} must include data file, source, script, and outputs.",
                manifest_path,
            )
            continue
        for label, raw_paths in (
            ("data file", data_file),
            ("script", script),
            ("output", outputs),
        ):
            for raw_path in re.split(r"[,;]", raw_paths):
                candidate = raw_path.strip().strip("`")
                if not candidate or candidate.lower() in {"n/a", "na", "none"}:
                    continue
                candidate_path = root / candidate
                if not candidate_path.exists():
                    add(
                        findings,
                        "error",
                        "FIGURE_ARTIFACT_MISSING",
                        f"{figure_id} {label} does not exist: {candidate}.",
                        manifest_path,
                    )


def determine_status(findings: Iterable[Finding]) -> str:
    findings = list(findings)
    errors = [item for item in findings if item.severity == "error"]
    if not errors:
        return "DONE_WITH_CONCERNS" if findings else "DONE"
    codes = {item.code for item in errors}
    if codes & {"MOCK_DATA_BLOCKED", "INCOMPLETE_DATA_MANIFEST", "FIGURE_ARTIFACT_MISSING", "EXACT_FIGURE_WITHOUT_DATA"}:
        return "NEEDS_DATA"
    if codes & {
        "BLOCKED_CLAIM",
        "MISSING_EVIDENCE_LINK",
        "CLAIM_WITHOUT_EVIDENCE",
        "INCOMPLETE_EVIDENCE",
        "UNVERIFIED_REFERENCE",
        "REFERENCE_WITHOUT_LOCATION",
        "CITATION_NOT_IN_LEDGER",
        "MANUSCRIPT_PLACEHOLDER",
    }:
        return "NEEDS_EVIDENCE"
    if codes & {"TABLE_SOURCE_LINE_MISSING", "INCOMPLETE_FIGURE_BRIEF", "FIGURE_BRIEF_MISSING", "FIGURE_MANIFEST_MISSING"}:
        return "NEEDS_FORMAT_CHECK"
    return "BLOCKED"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fail-closed validation for a graduate thesis workspace."
    )
    parser.add_argument("project_root", help="Thesis project root")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.project_root).expanduser().resolve()
    findings: list[Finding] = []
    if not root.exists() or not root.is_dir():
        add(findings, "error", "INVALID_ROOT", "Project root does not exist or is not a directory.", root)
    else:
        validate_contract(root, findings)
        validate_claims_and_evidence(root, findings)
        reference_ids = validate_references(root, findings)
        cited = validate_manuscript(root, findings, reference_ids)
        validate_figures(root, findings)

    status = determine_status(findings)
    report = {
        "status": status,
        "project_root": str(root),
        "cited_reference_ids": sorted(cited) if "cited" in locals() else [],
        "findings": [asdict(item) for item in findings],
    }
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(f"STATUS: {status}")
        print(f"PROJECT: {root}")
        if not findings:
            print("PASS: no blocking findings")
        for item in findings:
            location = f" [{item.path}]" if item.path else ""
            print(f"{item.severity.upper()} {item.code}: {item.message}{location}")
        print(f"FINDINGS: {len(findings)}")
    return 0 if status in {"DONE", "DONE_WITH_CONCERNS"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
