#!/usr/bin/env python3
"""Audit recurring source terms and their established Chinese translations.

This tool is read-only. It searches English source/Chinese target pairs across the
repository so repeated character addresses, catchphrases, and proper names can be
reviewed across files before a translation is finalized.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
from pathlib import Path
import re
import subprocess
import sys
from typing import Iterable

TOOLS_DIR = Path(__file__).resolve().parent
ROOT = TOOLS_DIR.parent
sys.path.insert(0, str(TOOLS_DIR))

from validate_translations import decode, iter_pairs  # noqa: E402

DEFAULT_REGISTRY = ROOT / "translation_context" / "recurring_terms.json"


@dataclass(frozen=True)
class Hit:
    path: Path
    source_line: int
    target_line: int
    source: str
    target: str
    valid: bool | None


def git_changed_rpy(ref: str) -> set[Path]:
    proc = subprocess.run(
        ["git", "diff", "--name-only", ref, "--", "*.rpy"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        stdout=subprocess.PIPE,
        check=True,
    )
    return {(ROOT / line.strip()).resolve() for line in proc.stdout.splitlines() if line.strip()}


def iter_rpy_files(search_root: Path, changed: set[Path] | None) -> Iterable[Path]:
    for path in sorted(search_root.rglob("*.rpy")):
        if changed is None or path.resolve() in changed:
            yield path


def load_registry(path: Path) -> list[dict[str, object]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    terms = data.get("terms")
    if not isinstance(terms, list):
        raise ValueError(f"{path}: expected a top-level 'terms' list")
    return terms


def scan(pattern: re.Pattern[str], target_patterns: list[re.Pattern[str]] | None,
         files: Iterable[Path],
         source_exceptions: list[re.Pattern[str]] | None = None) -> list[Hit]:
    hits: list[Hit] = []
    for path in files:
        text, _ = decode(path.read_bytes(), path)
        for pair in iter_pairs(text.splitlines()):
            if not pattern.search(pair.source):
                continue
            if source_exceptions and any(exc.search(pair.source)
                                         for exc in source_exceptions):
                continue
            valid = None if target_patterns is None else any(
                expected.search(pair.target) for expected in target_patterns
            )
            hits.append(Hit(path, pair.source_line, pair.target_line,
                            pair.source, pair.target, valid))
    return hits


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def print_hits(label: str, hits: list[Hit], show_all: bool) -> int:
    files = {hit.path for hit in hits}
    mismatches = [hit for hit in hits if hit.valid is False]
    print(f"{label}: {len(hits)} occurrence(s) in {len(files)} file(s); "
          f"{len(mismatches)} mismatch(es)")
    shown = hits if show_all else mismatches
    for hit in shown:
        state = "OK" if hit.valid is True else "MISMATCH" if hit.valid is False else "HIT"
        print(f"  [{state}] {display_path(hit.path)}:{hit.source_line}->{hit.target_line}")
        print(f"    EN: {hit.source}")
        print(f"    ZH: {hit.target}")
    return len(mismatches)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--path", type=Path, default=ROOT / "tl" / "zh_hans")
    parser.add_argument("--term", action="append", dest="term_ids",
                        help="Only audit this registry id; may be repeated.")
    parser.add_argument("--query", action="append", default=[],
                        help="Ad-hoc literal source phrase search; may be repeated.")
    parser.add_argument("--changed", action="store_true",
                        help="Only scan tracked .rpy files changed from --ref.")
    parser.add_argument("--ref", default="HEAD")
    parser.add_argument("--show-all", action="store_true",
                        help="Show every hit, not only translation mismatches.")
    parser.add_argument("--fail-on-mismatch", action="store_true",
                        help="Exit non-zero when an established term is inconsistent.")
    args = parser.parse_args()

    search_root = args.path if args.path.is_absolute() else ROOT / args.path
    changed = git_changed_rpy(args.ref) if args.changed else None
    files = list(iter_rpy_files(search_root, changed))
    terms = load_registry(args.registry)
    selected = set(args.term_ids or [])
    known_ids = {str(term.get("id")) for term in terms}
    unknown = selected - known_ids
    if unknown:
        parser.error(f"unknown term id(s): {', '.join(sorted(unknown))}")

    mismatch_count = 0
    for term in terms:
        term_id = str(term["id"])
        if selected and term_id not in selected:
            continue
        source_pattern = re.compile(str(term["source_regex"]), re.IGNORECASE)
        raw_targets = term.get("target_regexes", [])
        target_patterns = [re.compile(str(value)) for value in raw_targets]
        raw_exceptions = term.get("source_exceptions", [])
        source_exceptions = [re.compile(str(value), re.IGNORECASE)
                             for value in raw_exceptions]
        hits = scan(source_pattern, target_patterns, files, source_exceptions)
        mismatch_count += print_hits(term_id, hits, args.show_all)

    for query in args.query:
        hits = scan(re.compile(re.escape(query), re.IGNORECASE), None, files)
        print_hits(f"query:{query}", hits, True)

    if args.fail_on_mismatch and mismatch_count:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
