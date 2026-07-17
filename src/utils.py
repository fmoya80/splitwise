"""File-system helpers for raw Splitwise API responses."""

import json
from pathlib import Path
from typing import Any


RAW_DATA_DIRECTORY = Path("data/raw")


def ensure_directories() -> None:
    """Create the directory used to store raw API responses."""
    RAW_DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)


def save_json(data: Any, path: str | Path) -> None:
    """Save JSON-compatible *data* using UTF-8 and readable indentation."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)
        file.write("\n")
