#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Layout-safe render entry point for the real Seminar 11 Class 04.

The complete lesson remains defined in Seminar11_Class04_Encapsulation_Visibility.py.
This V2 subclass corrects the project-transfer grid discovered by literal full-scene
PQL QA: the original ragged 3x2 grid was shifted right and exceeded the 16:9 safe
frame. The corrected scene is centered and capped at 12.40 Manim units wide.
"""
from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from Seminar11_Class04_Encapsulation_Visibility import *  # noqa: F401,F403,E402


class Seminar11Class04EncapsulationVisibilityV2(Seminar11Class04EncapsulationVisibility):
    """Final Class 04 scene with senior safe-frame correction."""

    def scene_10_project_transfer(self):
        self.set_header(
            10,
            "TRANSFER ENCAPSULATION TO YOUR PROJECT DOMAIN",
            "Find one piece of state that should not be freely overwritten, then define the public operation that changes it safely."
        )
        flow = self.flow_strip("MODIFY")

        cards = VGroup(
            self.domain_card("WEB", "Product", "- price", "+ changePrice(value)"),
            self.domain_card("DATA SCIENCE", "Dataset", "- rows", "+ load(path)"),
            self.domain_card("DEFENSIVE CYBERSECURITY", "LogEvent", "- severity", "+ classify(level)"),
            self.domain_card("3D PROGRAMMING", "Mesh", "- scale", "+ resize(value)"),
            self.domain_card("ROBOTICS", "Robot", "- battery", "+ consume(amount)"),
        ).arrange_in_grid(rows=3, cols=2, buff=(0.34, 0.26))

        # A 5-card 3x2 grid is ragged. Explicitly re-center the complete group and
        # scale only when required so no blank-cell bias can move cards off-screen.
        if cards.width > 12.40:
            cards.scale_to_fit_width(12.40)
        if cards.height > 4.45:
            cards.scale_to_fit_height(4.45)
        cards.move_to(UP * 0.22)

        question = self.txt(
            "What rule must stay true after every public change?", 30, BOLD
        ).move_to(DOWN * 2.55)

        self.assert_content(VGroup(cards, question), "scene10-v2")
        self.play(FadeIn(flow), run_time=RUN_QUICK)
        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.08) for c in cards], lag_ratio=0.12),
            run_time=RUN_SLOW * 1.5,
        )
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(question), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()
