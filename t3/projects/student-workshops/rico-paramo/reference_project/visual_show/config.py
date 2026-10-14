from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path


@dataclass
class VisualConfig:
    width: int = 960
    height: int = 540
    fps: int = 60
    background: tuple[int, int, int] = (18, 22, 38)
    orbit_speed: float = 1.4
    orbit_radius: float = 150.0
    pulse_speed: float = 3.2
    particle_count: int = 120
    seed: int = 17


def _rgb(value, default=(18, 22, 38)):
    if not isinstance(value, list) or len(value) != 3:
        return default
    try:
        return tuple(max(0, min(255, int(x))) for x in value)
    except (TypeError, ValueError, OverflowError):
        return default


def load_config(path: Path) -> VisualConfig:
    if not path.exists():
        return VisualConfig()

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        return VisualConfig()

    if not isinstance(raw, dict):
        return VisualConfig()

    def number(key, default, minimum, maximum, integer=False):
        try:
            value = raw.get(key, default)
            if isinstance(value, bool):
                return default
            value = float(value)
            if not math.isfinite(value):
                return default
            value = max(minimum, min(maximum, value))
            return int(value) if integer else value
        except (TypeError, ValueError, OverflowError):
            return default

    return VisualConfig(
        width=number("width", 960, 320, 3840, True),
        height=number("height", 540, 180, 2160, True),
        fps=number("fps", 60, 15, 240, True),
        background=_rgb(raw.get("background")),
        orbit_speed=number("orbit_speed", 1.4, -100, 100),
        orbit_radius=number("orbit_radius", 150, 20, 2000),
        pulse_speed=number("pulse_speed", 3.2, -100, 100),
        particle_count=number("particle_count", 120, 0, 2000, True),
        seed=number("seed", 17, 0, 2147483647, True),
    )
