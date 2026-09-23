#!/usr/bin/env python3
"""Static QA for Seminar 11 Class 03 · Constructors & Valid State."""
from __future__ import annotations
import ast
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
source = path.read_text(encoding="utf-8")
ast.parse(source)
failures = []
warnings = []

for pattern in [r"[A-Za-z]:[\\/]", r"/Users/", r"/home/[^/]+/"]:
    if re.search(pattern, source):
        failures.append("absolute path detected")

if not re.search(r"class\s+Seminar11Class03ConstructorsValidState\s*\(JPClassroomScene\)", source):
    failures.append("expected scene class missing")

required = [
    "__init__",
    "self.name = name",
    "self.energy = energy",
    "self.position = position",
    "self.valor = valor",
    "self.unidad = unidad",
    "factor",
    "THREE valid objects",
    'Robot("Scout", -25, 0)',
    "ENCAPSULATION & VISIBILITY",
]
for term in required:
    if term not in source:
        failures.append(f"required curricular evidence missing: {term}")

for forbidden in ["@property", "getBalance", "setBalance", "class Child(", "super().__init__"]:
    if forbidden in source:
        failures.append(f"future-session content leaked into Class 03: {forbidden}")

if re.search(r"\b(?:RED|BLUE|GREEN|YELLOW|PURPLE|ORANGE)\b", source):
    warnings.append("non-monochrome named color detected")

print(f"STYLE QA: {path}")
for message in failures:
    print("FAIL:", message)
for message in warnings:
    print("WARN:", message)
if failures:
    raise SystemExit(1)
print("PASS" if not warnings else "PASS WITH WARNINGS")
