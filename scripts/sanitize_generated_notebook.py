#!/usr/bin/env python3
"""Remove machine-local metadata from generated Jupyter notebooks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def sanitize_notebook(path: Path) -> None:
    """Remove metadata that should not be published with a generated notebook."""
    notebook = json.loads(path.read_text(encoding="utf-8"))
    if notebook.get("nbformat") != 4 or not isinstance(notebook.get("cells"), list):
        raise ValueError(f"Not a supported Jupyter notebook: {path}")

    kernelspec = notebook.get("metadata", {}).get("kernelspec", {})
    kernelspec.pop("path", None)

    serialized = json.dumps(notebook, ensure_ascii=False, indent=1)
    path.write_text(f"{serialized}\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Remove machine-local metadata from generated notebooks."
    )
    parser.add_argument("notebooks", nargs="+", type=Path)
    args = parser.parse_args()

    for notebook_path in args.notebooks:
        sanitize_notebook(notebook_path)


if __name__ == "__main__":
    main()
