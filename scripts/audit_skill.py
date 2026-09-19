#!/usr/bin/env python3
"""Deterministic inventory and comparison for Agent Skill directories."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from collections import defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path


TEXT_SUFFIXES = {".md", ".txt", ".yaml", ".yml", ".json", ".py", ".sh", ".js", ".ts"}
SKIP_DIRS = {".git", "__pycache__", "node_modules"}
ABSOLUTE_RE = re.compile(r"\b(always|never|must|required|do not|don't|shall)\b", re.I)
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
PATH_RE = re.compile(r"(?<![\w./-])((?:references|scripts|assets|agents)/[\w./-]+)")

try:
    import tiktoken  # type: ignore

    TOKEN_ENCODER = tiktoken.get_encoding("o200k_base")
    TOKEN_METHOD = "tiktoken:o200k_base"
except (ImportError, Exception):
    TOKEN_ENCODER = None
    TOKEN_METHOD = "character heuristic: 4.0 ASCII or 2.4 non-ASCII chars/token"


@dataclass
class FileMetric:
    path: str
    tier: str
    lines: int
    words: int
    chars: int
    estimated_tokens: int


def read_text(path: Path) -> str | None:
    if path.suffix.lower() not in TEXT_SUFFIXES:
        return None
    try:
        return path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def estimate_tokens(text: str) -> int:
    """Use tiktoken when available, otherwise a script-aware character heuristic."""
    if TOKEN_ENCODER is not None:
        return len(TOKEN_ENCODER.encode(text))
    non_ascii = sum(ord(char) > 127 for char in text)
    ratio = non_ascii / max(len(text), 1)
    chars_per_token = 2.4 if ratio > 0.20 else 4.0
    return math.ceil(len(text) / chars_per_token)


def split_frontmatter(text: str) -> tuple[str, str]:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.S)
    if not match:
        return "", text
    return match.group(1), text[match.end() :]


def tier_for(relative: Path) -> str:
    value = relative.as_posix()
    if value == "SKILL.md":
        return "triggered"
    if value.startswith("references/"):
        return "on_demand"
    if value.startswith("scripts/") or value.startswith("assets/"):
        return "not_normally_loaded"
    if value == "agents/openai.yaml":
        return "interface"
    return "other"


def iter_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file() or any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def normalize_block(block: str) -> str:
    return re.sub(r"\s+", " ", block.strip()).casefold()


def collect_links(root: Path, markdown: dict[str, str]) -> tuple[list[str], list[str]]:
    linked: set[str] = set()
    broken: set[str] = set()
    for rel_name, text in markdown.items():
        source = root / rel_name
        candidates = [match.group(1).split("#", 1)[0] for match in LINK_RE.finditer(text)]
        candidates.extend(match.group(1) for match in PATH_RE.finditer(text))
        for candidate in candidates:
            if not candidate or "://" in candidate or candidate.startswith("#"):
                continue
            resolved = (source.parent / candidate).resolve()
            try:
                relative = resolved.relative_to(root.resolve()).as_posix()
            except ValueError:
                continue
            linked.add(relative)
            if not resolved.exists():
                broken.add(f"{rel_name} -> {candidate}")
    return sorted(linked), sorted(broken)


def audit(root: Path) -> dict:
    if not root.is_dir():
        raise ValueError(f"Not a directory: {root}")
    skill_file = root / "SKILL.md"
    if not skill_file.exists():
        raise ValueError(f"SKILL.md not found in {root}")

    metrics: list[FileMetric] = []
    markdown: dict[str, str] = {}
    paragraph_sources: dict[str, list[str]] = defaultdict(list)
    absolute_rules: list[dict] = []
    todos: list[str] = []

    for path in iter_files(root):
        relative = path.relative_to(root)
        text = read_text(path)
        if text is None:
            continue
        rel_name = relative.as_posix()
        metrics.append(
            FileMetric(
                path=rel_name,
                tier=tier_for(relative),
                lines=len(text.splitlines()),
                words=len(re.findall(r"\b\w+\b", text, re.UNICODE)),
                chars=len(text),
                estimated_tokens=estimate_tokens(text),
            )
        )
        if path.suffix.lower() == ".md":
            markdown[rel_name] = text
            for index, paragraph in enumerate(re.split(r"\n\s*\n", text), start=1):
                normalized = normalize_block(paragraph)
                if len(normalized) >= 100 and not normalized.startswith("```"):
                    paragraph_sources[normalized].append(f"{rel_name}:block-{index}")
        for line_no, line in enumerate(text.splitlines(), start=1):
            if ABSOLUTE_RE.search(line) and len(line.strip()) >= 20:
                absolute_rules.append({"location": f"{rel_name}:{line_no}", "text": line.strip()[:240]})
            if path.suffix.lower() in {".md", ".txt", ".yaml", ".yml"} and re.search(
                r"\b(TODO|FIXME|TBD)\b|\[TODO:", line, re.I
            ):
                todos.append(f"{rel_name}:{line_no}")

    skill_text = skill_file.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(skill_text)
    description_match = re.search(r"(?m)^description:\s*(.+)$", frontmatter)
    description = description_match.group(1).strip().strip('"\'') if description_match else ""

    linked, broken = collect_links(root, markdown)
    candidate_resources = {
        metric.path
        for metric in metrics
        if metric.path.startswith(("references/", "scripts/", "assets/"))
    }
    orphans = sorted(candidate_resources - set(linked))
    duplicates = [sources for sources in paragraph_sources.values() if len(sources) > 1]

    tiers: dict[str, dict[str, int]] = defaultdict(lambda: {"files": 0, "lines": 0, "chars": 0, "estimated_tokens": 0})
    for metric in metrics:
        bucket = tiers[metric.tier]
        bucket["files"] += 1
        bucket["lines"] += metric.lines
        bucket["chars"] += metric.chars
        bucket["estimated_tokens"] += metric.estimated_tokens

    tiers["discovery"] = {
        "files": 1,
        "lines": len(frontmatter.splitlines()),
        "chars": len(frontmatter),
        "estimated_tokens": estimate_tokens(frontmatter),
    }
    tiers["triggered"] = {
        "files": 1,
        "lines": len(body.splitlines()),
        "chars": len(body),
        "estimated_tokens": estimate_tokens(body),
    }

    return {
        "root": str(root.resolve()),
        "token_method": TOKEN_METHOD,
        "description": description,
        "tiers": dict(sorted(tiers.items())),
        "files": [asdict(metric) for metric in metrics],
        "checks": {
            "linked_resources": linked,
            "broken_links": broken,
            "orphaned_resources": orphans,
            "exact_duplicate_blocks": duplicates,
            "absolute_rule_count": len(absolute_rules),
            "absolute_rules": absolute_rules,
            "unfinished_markers": todos,
        },
    }


def comparison(before: dict, after: dict) -> dict:
    tiers = sorted(set(before["tiers"]) | set(after["tiers"]))
    delta = {}
    for tier in tiers:
        old = before["tiers"].get(tier, {}).get("estimated_tokens", 0)
        new = after["tiers"].get(tier, {}).get("estimated_tokens", 0)
        delta[tier] = {
            "before": old,
            "after": new,
            "delta": new - old,
            "percent": round(((new - old) / old) * 100, 1) if old else None,
        }
    return {"before": before, "after": after, "token_delta_by_tier": delta}


def render_text(report: dict) -> str:
    if "token_delta_by_tier" in report:
        lines = ["Skill comparison", "", "Tier | Before | After | Delta | Percent", "--- | ---: | ---: | ---: | ---:"]
        for tier, values in report["token_delta_by_tier"].items():
            percent = "n/a" if values["percent"] is None else f'{values["percent"]:+.1f}%'
            lines.append(f'{tier} | {values["before"]} | {values["after"]} | {values["delta"]:+d} | {percent}')
        return "\n".join(lines)

    lines = [f'Skill audit inventory: {report["root"]}', f'Token estimate: {report["token_method"]}', "", "Loading tier | Files | Lines | Estimated tokens", "--- | ---: | ---: | ---:"]
    for tier, values in report["tiers"].items():
        lines.append(f'{tier} | {values["files"]} | {values["lines"]} | {values["estimated_tokens"]}')
    checks = report["checks"]
    lines.extend(
        [
            "",
            f'Broken links: {len(checks["broken_links"])}',
            f'Orphaned resources: {len(checks["orphaned_resources"])}',
            f'Exact duplicate blocks: {len(checks["exact_duplicate_blocks"])}',
            f'Absolute-rule candidates: {checks["absolute_rule_count"]}',
            f'Unfinished markers: {len(checks["unfinished_markers"])}',
        ]
    )
    for key in ("broken_links", "orphaned_resources", "exact_duplicate_blocks", "unfinished_markers"):
        if checks[key]:
            lines.append(f"\n{key}:")
            lines.extend(f"- {item}" for item in checks[key])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_directory", type=Path)
    parser.add_argument("--compare", type=Path, help="Candidate skill directory for before/after comparison")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    args = parser.parse_args()

    try:
        before = audit(args.skill_directory)
        report = comparison(before, audit(args.compare)) if args.compare else before
    except (OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    print(json.dumps(report, indent=2, ensure_ascii=False) if args.json else render_text(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
