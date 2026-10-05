#!/usr/bin/env python3
"""Static QA for Seminar11 Class03 Manim source."""
from __future__ import annotations
import ast
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
source = path.read_text(encoding='utf-8')
ast.parse(source)
failures=[]
warnings=[]
for pattern in [r'[A-Za-z]:[\\/]', r'/Users/', r'/home/[^/]+/']:
    if re.search(pattern, source): failures.append('absolute path detected')
if not re.search(r'class\s+Seminar11Class03ConstructorsValidState\s*\(JPClassroomScene\)', source):
    failures.append('expected scene class missing')
if not all(term in source for term in ['__init__','self.value = value','this.value = value','THREE valid objects','Measurement(12,']):
    failures.append('required curricular constructor evidence missing')
if re.search(r'\b(?:RED|BLUE|GREEN|YELLOW|PURPLE|ORANGE)\b', source):
    warnings.append('non-monochrome named color detected')
if 'config.background_color' in source:
    warnings.append('scene overrides style background; review consistency')
print(f'STYLE QA: {path}')
for m in failures: print('FAIL:', m)
for m in warnings: print('WARN:', m)
if failures:
    raise SystemExit(1)
print('PASS' if not warnings else 'PASS WITH WARNINGS')
