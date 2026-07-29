#!/usr/bin/env python3
"""Replace double-brace placeholder values in a training repository.

The values file can be JSON or a small YAML subset using one `key: value` pair
per line. This script intentionally avoids third-party dependencies so it can
run before a training environment has been created.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


PLACEHOLDER_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")
SKIP_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "__pycache__",
    ".ipynb_checkpoints",
    ".quarto",
    "build",
    "dist",
}
TEXT_SUFFIXES = {
    ".bash",
    ".cfg",
    ".css",
    ".html",
    ".jl",
    ".js",
    ".json",
    ".md",
    ".py",
    ".qmd",
    ".sh",
    ".toml",
    ".txt",
    ".yml",
    ".yaml",
}
TEXT_NAMES = {
    ".gitignore",
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE",
    "README.md",
    "SETUP.md",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Replace double-brace placeholder values in text files."
    )
    parser.add_argument(
        "values_file",
        type=Path,
        help="JSON or simple YAML file containing placeholder values.",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path.cwd(),
        help="Repository root to update. Defaults to the current directory.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show files that would change, but do not write them.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Fail if placeholders remain after replacement.",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List placeholders currently present under --root and exit.",
    )
    return parser.parse_args()


def load_values(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() == ".json":
        raw_values = json.loads(text)
    else:
        raw_values = parse_simple_yaml(text)
    values: dict[str, str] = {}
    for key, value in raw_values.items():
        placeholder = key.strip()
        if placeholder.startswith("{{") and placeholder.endswith("}}"):
            placeholder = placeholder[2:-2].strip()
        if not PLACEHOLDER_RE.fullmatch("{{" + placeholder + "}}"):
            raise ValueError(f"invalid placeholder name: {key!r}")
        values[placeholder] = str(value)
    return values


def parse_simple_yaml(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"line {line_number}: expected 'KEY: value'")
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if (
            len(value) >= 2
            and value[0] == value[-1]
            and value[0] in {"'", '"'}
        ):
            value = value[1:-1]
        values[key] = value
    return values


def iter_text_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in path.relative_to(root).parts):
            continue
        if not path.is_file():
            continue
        if path.suffix in TEXT_SUFFIXES or path.name in TEXT_NAMES:
            files.append(path)
    return files


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def placeholders_in(root: Path) -> set[str]:
    placeholders: set[str] = set()
    for path in iter_text_files(root):
        text = read_text(path)
        if text is None:
            continue
        placeholders.update(PLACEHOLDER_RE.findall(text))
    return placeholders


def replace_placeholders(text: str, values: dict[str, str]) -> str:
    def replacement(match: re.Match[str]) -> str:
        name = match.group(1)
        return values.get(name, match.group(0))

    return PLACEHOLDER_RE.sub(replacement, text)


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    if args.list:
        for name in sorted(placeholders_in(root)):
            print(name)
        return 0

    values_file = args.values_file.resolve()
    values = load_values(values_file)
    changed: list[Path] = []
    remaining: set[str] = set()
    for path in iter_text_files(root):
        if path.resolve() == values_file:
            continue
        text = read_text(path)
        if text is None:
            continue
        updated = replace_placeholders(text, values)
        remaining.update(PLACEHOLDER_RE.findall(updated))
        if updated != text:
            changed.append(path)
            if not args.dry_run:
                path.write_text(updated, encoding="utf-8")

    for path in changed:
        print(path.relative_to(root))

    if args.strict and remaining:
        print(
            "unresolved placeholders: " + ", ".join(sorted(remaining)),
            file=sys.stderr,
        )
        return 1

    if args.dry_run:
        print(f"{len(changed)} file(s) would change")
    else:
        print(f"{len(changed)} file(s) changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
