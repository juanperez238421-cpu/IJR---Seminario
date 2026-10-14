from __future__ import annotations

import sys
from pathlib import Path


def runtime_root() -> Path:
    """External config lives beside the portable executable, not its temp bundle."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parents[1]


def resource_path(relative: str) -> Path:
    return runtime_root() / relative
