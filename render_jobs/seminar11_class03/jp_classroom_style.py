#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Minimal JP classroom style helper for Seminar 11 Class 03.

This is intentionally scoped to the layout primitives required by the lesson while
preserving the established ManimCE classroom contract: 1920x1080, 30 fps, white
background, monochrome hierarchy, persistent numbered headers, safe margins and
LESSON_TIME_SCALE for fast QA previews.
"""
from __future__ import annotations

import os
from manim import *

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

BLACK_TEXT = BLACK
BLACK_LINE = BLACK
DARK_GRAY = "#303030"
MID_GRAY = "#787878"
LIGHT_GRAY = "#D7D7D7"
VERY_LIGHT_GRAY = "#F0F0F0"
PAPER_GRAY = "#F8F8F8"

FRAME_WIDTH = 16.0
FRAME_HEIGHT = 9.0
SAFE_WIDTH = 14.75
SAFE_HEIGHT = 7.65
CONTENT_TOP_Y = 2.42
CONTENT_BOTTOM_Y = -4.05

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

RUN_QUICK = 0.70
RUN_NORMAL = 1.00
RUN_SLOW = 1.35
RUN_CAMERA = 1.25

PAUSE_SHORT = 0.85
PAUSE_READ = 1.80
PAUSE_EXPLAIN = 2.80
PAUSE_WORK = 3.80
PAUSE_SUMMARY = 4.60
PAUSE_FINAL = 5.20


class JPClassroomScene(Scene):
    """Small reusable base with the exact visual safeguards needed here.

    A plain ``Scene`` is intentional. Class 03 does not use camera zooming, and
    avoiding a moving-camera dependency keeps the helper fully compatible with
    the ManimCE 0.20.1 renderer used by the repository workflow.
    """

    def setup(self) -> None:
        super().setup()
        self.validate_lesson_data()
        self.camera.background_color = WHITE
        self.header_group: VGroup | None = None
        self.subtitle_group: Mobject | None = None

    def validate_lesson_data(self) -> None:
        pass

    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration: float = DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    def text(self, content: str, size: int = 30, weight=NORMAL, **kwargs) -> Text:
        return Text(
            content,
            font_size=size,
            color=BLACK_TEXT,
            weight=weight,
            line_spacing=0.92,
            **kwargs,
        )

    def fit(self, mob: Mobject, max_width: float = SAFE_WIDTH, max_height: float = SAFE_HEIGHT) -> Mobject:
        if mob.width > max_width:
            mob.scale_to_fit_width(max_width)
        if mob.height > max_height:
            mob.scale_to_fit_height(max_height)
        return mob

    def set_header(self, number: int, title: str, subtitle: str) -> None:
        number_box = RoundedRectangle(
            width=0.78,
            height=0.58,
            corner_radius=0.10,
            stroke_color=BLACK_LINE,
            stroke_width=2.0,
            fill_color=WHITE,
            fill_opacity=1.0,
        )
        number_text = self.text(f"{number:02d}", 25, BOLD).move_to(number_box)
        title_text = self.text(title, 38, BOLD)
        self.fit(title_text, SAFE_WIDTH - number_box.width - 0.40, 0.64)
        title_row = VGroup(VGroup(number_box, number_text), title_text).arrange(RIGHT, buff=0.25)
        title_row.to_edge(UP, buff=0.13).to_edge(LEFT, buff=0.48)

        rule = Line(LEFT * 7.48, RIGHT * 7.48, color=LIGHT_GRAY, stroke_width=2)
        rule.next_to(title_row, DOWN, buff=0.07)

        words = subtitle.split()
        if len(subtitle) > 96:
            midpoint = len(words) // 2
            best = midpoint
            best_gap = 10**9
            for index in range(max(1, midpoint - 5), min(len(words), midpoint + 6)):
                gap = abs(len(" ".join(words[:index])) - len(" ".join(words[index:])))
                if gap < best_gap:
                    best = index
                    best_gap = gap
            subtitle_text = VGroup(
                self.text(" ".join(words[:best]), 22),
                self.text(" ".join(words[best:]), 22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.04)
        else:
            subtitle_text = self.text(subtitle, 23)
        self.fit(subtitle_text, 14.25, 0.78)
        subtitle_text.next_to(rule, DOWN, buff=0.07).align_to(title_row, LEFT)

        new_header = VGroup(title_row, rule)
        # V2.1: remove the previous header completely before drawing the next one.
        # This avoids glyph-to-glyph ReplacementTransform collisions during chapter changes.
        if self.header_group is not None or self.subtitle_group is not None:
            old_items = [m for m in (self.header_group, self.subtitle_group) if m is not None]
            if old_items:
                self.play(*[FadeOut(m) for m in old_items], run_time=0.38)

        self.header_group = new_header
        self.subtitle_group = subtitle_text
        self.play(FadeIn(new_header), FadeIn(subtitle_text), run_time=0.46)

    def clear_stage(self, keep_header: bool = True) -> None:
        keep_family_ids: set[int] = set()
        if keep_header:
            for persistent in (self.header_group, self.subtitle_group):
                if persistent is not None:
                    keep_family_ids.update(id(member) for member in persistent.get_family())
        removable = [mob for mob in self.mobjects if id(mob) not in keep_family_ids]
        if removable:
            self.play(*[FadeOut(mob) for mob in removable], run_time=RUN_NORMAL)

    def assert_within_frame(self, mob: Mobject, label: str, margin: float = 0.03) -> None:
        left, right = mob.get_left()[0], mob.get_right()[0]
        bottom, top = mob.get_bottom()[1], mob.get_top()[1]
        if left < -FRAME_WIDTH / 2 + margin or right > FRAME_WIDTH / 2 - margin:
            raise ValueError(f"{label} exceeds horizontal frame bounds: left={left:.3f}, right={right:.3f}")
        if bottom < -FRAME_HEIGHT / 2 + margin or top > FRAME_HEIGHT / 2 - margin:
            raise ValueError(f"{label} exceeds vertical frame bounds: bottom={bottom:.3f}, top={top:.3f}")

    def assert_content_safe(self, mob: Mobject, label: str) -> None:
        self.assert_within_frame(mob, label, margin=0.15)
        if mob.get_top()[1] > CONTENT_TOP_Y:
            raise ValueError(f"{label} overlaps the persistent header zone")
        if mob.get_bottom()[1] < CONTENT_BOTTOM_Y:
            raise ValueError(f"{label} exceeds the safe lower content zone")