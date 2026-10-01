#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Seminar 11 · Class 04
Encapsulation & Visibility

Curriculum lock:
- t3/common/index.html -> Week 4: Encapsulation / Visibility + / - / # / m10 / Protected state
- t3/oop-uml/course-data.js -> Encapsulation & Visibility
- t3/data/modules/m10.json -> Python _attribute + @property + setter validation;
  Java private/public/protected; getters/setters only when they protect a rule.

Render target: ManimCE 0.20.1 · 1920x1080 · 30 fps · white background.
"""
from __future__ import annotations

import os
from manim import *

# ---------------------------------------------------------------------
# RENDER CONTRACT
# ---------------------------------------------------------------------
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

BLACK_TEXT = BLACK
BLACK_LINE = BLACK
DARK_GRAY = "#303030"
MID_GRAY = "#777777"
LIGHT_GRAY = "#D8D8D8"
VERY_LIGHT_GRAY = "#F1F1F1"
PAPER_GRAY = "#FAFAFA"

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

RUN_QUICK = 0.65
RUN_NORMAL = 0.95
RUN_SLOW = 1.35

PAUSE_SHORT = 0.90
PAUSE_READ = 1.85
PAUSE_EXPLAIN = 2.80
PAUSE_WORK = 3.80
PAUSE_FINAL = 5.00

FRAME_W = 16.0
FRAME_H = 9.0
CONTENT_TOP = 2.55
CONTENT_BOTTOM = -4.05


class Seminar11Class04EncapsulationVisibility(Scene):
    """Full Class 04 lesson: encapsulation, visibility and protected state."""

    def setup(self):
        super().setup()
        self.camera.background_color = WHITE
        self.header_group = None
        self.subtitle_group = None

    # ------------------------------ timing ------------------------------
    def play(self, *animations, **kwargs):
        if kwargs.get("run_time") is not None:
            kwargs["run_time"] *= TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=DEFAULT_WAIT_TIME, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    # ------------------------------ primitives ------------------------------
    def txt(self, s, size=28, weight=NORMAL, **kwargs):
        return Text(
            s,
            font_size=size,
            color=BLACK_TEXT,
            weight=weight,
            font="DejaVu Sans",
            line_spacing=0.92,
            **kwargs,
        )

    def mono(self, s, size=24, **kwargs):
        return Text(
            s,
            font_size=size,
            color=BLACK_TEXT,
            font="DejaVu Sans Mono",
            **kwargs,
        )

    def fit(self, mob, max_w=14.8, max_h=7.6):
        if mob.width > max_w:
            mob.scale_to_fit_width(max_w)
        if mob.height > max_h:
            mob.scale_to_fit_height(max_h)
        return mob

    def assert_frame(self, mob, label, margin=0.10):
        l, r = mob.get_left()[0], mob.get_right()[0]
        b, t = mob.get_bottom()[1], mob.get_top()[1]
        if l < -FRAME_W/2 + margin or r > FRAME_W/2 - margin:
            raise ValueError(f"{label}: horizontal overflow {l:.3f}, {r:.3f}")
        if b < -FRAME_H/2 + margin or t > FRAME_H/2 - margin:
            raise ValueError(f"{label}: vertical overflow {b:.3f}, {t:.3f}")

    def assert_content(self, mob, label):
        self.assert_frame(mob, label, 0.15)
        if mob.get_top()[1] > CONTENT_TOP:
            raise ValueError(f"{label}: overlaps header")
        if mob.get_bottom()[1] < CONTENT_BOTTOM:
            raise ValueError(f"{label}: below safe area")

    def set_header(self, number, title, subtitle):
        num_box = RoundedRectangle(
            width=0.72, height=0.52, corner_radius=0.10,
            stroke_color=BLACK_LINE, stroke_width=2,
            fill_color=WHITE, fill_opacity=1,
        )
        num = self.txt(f"{number:02d}", 23, BOLD).move_to(num_box)
        title_m = self.txt(title, 34, BOLD)
        self.fit(title_m, 13.6, 0.58)
        row = VGroup(VGroup(num_box, num), title_m).arrange(RIGHT, buff=0.24)
        row.to_edge(UP, buff=0.16).to_edge(LEFT, buff=0.48)

        rule = Line(LEFT*7.48, RIGHT*7.48, stroke_color=LIGHT_GRAY, stroke_width=2)
        rule.next_to(row, DOWN, buff=0.07)

        words = subtitle.split()
        if len(subtitle) > 94:
            split = len(words)//2
            subtitle_m = VGroup(
                self.txt(" ".join(words[:split]), 20),
                self.txt(" ".join(words[split:]), 20),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.03)
        else:
            subtitle_m = self.txt(subtitle, 21)
        self.fit(subtitle_m, 14.3, 0.72)
        subtitle_m.next_to(rule, DOWN, buff=0.08).align_to(row, LEFT)

        new_header = VGroup(row, rule)
        if self.header_group is None:
            self.header_group = new_header
            self.add(new_header)
        else:
            old = self.header_group
            self.header_group = new_header
            self.play(ReplacementTransform(old, new_header), run_time=RUN_QUICK)

        if self.subtitle_group is None:
            self.subtitle_group = subtitle_m
            self.add(subtitle_m)
        else:
            old = self.subtitle_group
            self.subtitle_group = subtitle_m
            self.play(ReplacementTransform(old, subtitle_m), run_time=RUN_QUICK)

    def clear_stage(self, keep_header=True):
        keep = set()
        if keep_header:
            for g in (self.header_group, self.subtitle_group):
                if g is not None:
                    keep.update(id(x) for x in g.get_family())
        removable = [m for m in self.mobjects if id(m) not in keep]
        if removable:
            self.play(*[FadeOut(m) for m in removable], run_time=RUN_NORMAL)

    def tag(self, text, width, height=0.58, size=19, filled=False):
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.10,
            stroke_color=BLACK_LINE, stroke_width=1.8,
            fill_color=BLACK if filled else WHITE,
            fill_opacity=1.0,
        )
        label = Text(
            text,
            font="DejaVu Sans",
            font_size=size,
            color=WHITE if filled else BLACK_TEXT,
            weight=BOLD,
        )
        if label.width > width - 0.18:
            label.scale_to_fit_width(width - 0.18)
        return VGroup(box, label.move_to(box))

    def flow_strip(self, active):
        steps = ["PREDICT", "MODEL", "CODE", "EXECUTE", "MODIFY", "EXPLAIN"]
        parts = []
        for s in steps:
            parts.append(self.tag(s, 1.58, 0.48, 16, filled=(s == active)))
        return VGroup(*parts).arrange(RIGHT, buff=0.12).move_to(DOWN*3.72)

    def code_panel(self, lines, title, width=6.4, height=3.6, font_size=22):
        outer = RoundedRectangle(
            width=width, height=height, corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=1.8,
            fill_color=PAPER_GRAY, fill_opacity=1,
        )
        title_bar = Rectangle(
            width=width, height=0.48,
            stroke_color=BLACK_LINE, stroke_width=1.4,
            fill_color=VERY_LIGHT_GRAY, fill_opacity=1,
        ).align_to(outer, UP)
        title_bar.shift(DOWN*0.24)
        title_m = self.txt(title, 18, BOLD).move_to(title_bar)
        code_lines = VGroup(*[self.mono(line, font_size) for line in lines])
        code_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        code_lines.move_to(outer.get_center() + DOWN*0.14).align_to(outer, LEFT).shift(RIGHT*0.28)
        if code_lines.width > width - 0.5:
            code_lines.scale_to_fit_width(width - 0.5)
        if code_lines.height > height - 0.72:
            code_lines.scale_to_fit_height(height - 0.72)
        return VGroup(outer, title_bar, title_m, code_lines), code_lines

    def uml_box(self, name, attrs, ops, width=5.1, height=3.2):
        outer = Rectangle(
            width=width, height=height,
            stroke_color=BLACK_LINE, stroke_width=2,
            fill_color=WHITE, fill_opacity=1,
        )
        y1 = outer.get_top()[1] - 0.76
        y2 = outer.get_bottom()[1] + 1.03
        sep1 = Line([outer.get_left()[0], y1, 0], [outer.get_right()[0], y1, 0], color=BLACK_LINE, stroke_width=1.4)
        sep2 = Line([outer.get_left()[0], y2, 0], [outer.get_right()[0], y2, 0], color=BLACK_LINE, stroke_width=1.4)

        title = self.txt(name, 26, BOLD).move_to([outer.get_center()[0], outer.get_top()[1]-0.38, 0])
        attr_m = VGroup(*[self.mono(x, 21) for x in attrs]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        op_m = VGroup(*[self.mono(x, 21) for x in ops]).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        attr_m.move_to([outer.get_left()[0]+0.28+attr_m.width/2, (y1+y2)/2, 0])
        op_m.move_to([outer.get_left()[0]+0.28+op_m.width/2, (y2+outer.get_bottom()[1])/2, 0])
        return VGroup(outer, sep1, sep2, title, attr_m, op_m)

    def thermometer(self, value_text="20 °C", danger=False):
        bulb = Circle(radius=0.42, stroke_color=BLACK_LINE, stroke_width=2, fill_color=WHITE, fill_opacity=1)
        stem = RoundedRectangle(
            width=0.46, height=2.55, corner_radius=0.20,
            stroke_color=BLACK_LINE, stroke_width=2,
            fill_color=WHITE, fill_opacity=1,
        ).next_to(bulb, UP, buff=-0.10)
        level_h = 1.78 if not danger else 0.42
        level = Rectangle(
            width=0.16, height=level_h,
            stroke_width=0, fill_color=BLACK, fill_opacity=1,
        ).align_to(stem, DOWN).shift(UP*0.18)
        fill_bulb = Circle(radius=0.25, stroke_width=0, fill_color=BLACK, fill_opacity=1).move_to(bulb)
        label = self.txt(value_text, 27, BOLD).next_to(VGroup(stem, bulb), RIGHT, buff=0.34)
        return VGroup(stem, bulb, level, fill_bulb, label)

    def shield(self, width=2.0, height=2.4):
        pts = [
            [-width*0.5, height*0.45, 0],
            [0, height*0.62, 0],
            [width*0.5, height*0.45, 0],
            [width*0.44, -height*0.10, 0],
            [0, -height*0.58, 0],
            [-width*0.44, -height*0.10, 0],
        ]
        return Polygon(
            *pts, stroke_color=BLACK_LINE, stroke_width=2.2,
            fill_color=VERY_LIGHT_GRAY, fill_opacity=1,
        )

    # ------------------------------------------------------------------
    # CONSTRUCT
    # ------------------------------------------------------------------
    def construct(self):
        self.opening()
        self.scene_01_problem()
        self.scene_02_meaning()
        self.scene_03_uml_visibility()
        self.scene_04_python_internal_state()
        self.scene_05_property_interface()
        self.scene_06_setter_validation()
        self.scene_07_java_visibility()
        self.scene_08_not_getters_everywhere()
        self.scene_09_invariant_flow()
        self.scene_10_project_transfer()
        self.scene_11_evidence()
        self.final_exit_check()

    # ------------------------------------------------------------------
    # Opening
    # ------------------------------------------------------------------
    def opening(self):
        top = self.txt("SEMINAR 11 · THIRD PERIOD · COMMON CORE OOP + UML", 24, BOLD).move_to(UP*3.3)
        num = self.txt("CLASS 04", 58, BOLD).move_to(UP*1.75)
        title = self.txt("ENCAPSULATION & VISIBILITY", 48, BOLD).move_to(UP*0.75)
        subtitle = self.txt("Protect state behind a controlled interface.", 29).move_to(DOWN*0.15)

        chain = VGroup(
            self.tag("STATE", 1.65),
            self.txt("→", 24),
            self.tag("RULE", 1.65, filled=True),
            self.txt("→", 24),
            self.tag("CONTROLLED CHANGE", 2.55),
        ).arrange(RIGHT, buff=0.20).move_to(DOWN*1.25)

        focus = self.txt("Today: + public · - private · # protected", 25, BOLD).move_to(DOWN*2.18)
        flow = self.flow_strip("PREDICT")

        group = VGroup(top, num, title, subtitle, chain, focus, flow)
        self.assert_frame(group, "opening")
        self.play(FadeIn(top), run_time=RUN_NORMAL)
        self.play(Write(num), run_time=RUN_NORMAL)
        self.play(Write(title), run_time=RUN_SLOW)
        self.play(FadeIn(subtitle), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(m) for m in chain], lag_ratio=0.10), run_time=RUN_SLOW)
        self.play(FadeIn(focus), FadeIn(flow), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=RUN_NORMAL)

    # ------------------------------------------------------------------
    # 01 — direct mutation creates impossible state
    # ------------------------------------------------------------------
    def scene_01_problem(self):
        self.set_header(
            1,
            "WHY PROTECT STATE?",
            "If any external code can change an attribute directly, the object can be pushed into an impossible state."
        )
        flow = self.flow_strip("PREDICT")
        ok = self.thermometer("20 °C").move_to(LEFT*4.6 + UP*0.15)
        bad = self.thermometer("-500 °C", danger=True).move_to(RIGHT*4.6 + UP*0.15)

        ok_code = self.mono("temperature = 20", 26).next_to(ok, DOWN, buff=0.34)
        bad_code = self.mono("temperature = -500", 26).next_to(bad, DOWN, buff=0.34)

        arrow = Arrow(LEFT*1.25, RIGHT*1.25, stroke_width=2.4, buff=0.0, color=BLACK)
        arrow.move_to(UP*0.3)
        direct = self.tag("DIRECT WRITE", 2.15, 0.58, 18, filled=True).next_to(arrow, UP, buff=0.18)
        question = self.txt("Who stopped the invalid value?", 30, BOLD).move_to(DOWN*2.15)
        answer = self.txt("Nobody.", 34, BOLD).next_to(question, DOWN, buff=0.25)

        self.assert_content(VGroup(ok, bad, ok_code, bad_code, arrow, direct, question, answer), "scene01")
        self.play(FadeIn(flow), FadeIn(ok), Write(ok_code), run_time=RUN_NORMAL)
        self.play(GrowArrow(arrow), FadeIn(direct), run_time=RUN_NORMAL)
        self.play(FadeIn(bad), Write(bad_code), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(question), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(answer), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 02 — actual meaning of encapsulation
    # ------------------------------------------------------------------
    def scene_02_meaning(self):
        self.set_header(
            2,
            "ENCAPSULATION = CONTROL HOW STATE CHANGES",
            "Encapsulation does not mean hiding everything. It separates internal representation from the public interface used by other code."
        )
        flow = self.flow_strip("MODEL")
        shield = self.shield(2.7, 3.1).move_to(ORIGIN + UP*0.10)
        state = self.tag("INTERNAL STATE", 2.20, 0.62, 20, filled=True).move_to(shield)
        outside = VGroup(
            self.tag("READ", 1.55),
            self.tag("REQUEST CHANGE", 2.35),
            self.tag("ASK BEHAVIOR", 2.15),
        ).arrange(DOWN, buff=0.38).move_to(LEFT*4.55 + UP*0.10)
        interface = VGroup(
            self.tag("PUBLIC INTERFACE", 2.50, 0.62, 19),
            self.txt("methods / properties", 21),
        ).arrange(DOWN, buff=0.18).move_to(RIGHT*4.55 + UP*0.10)
        a1 = Arrow(outside.get_right(), shield.get_left(), buff=0.18, stroke_width=2.2, color=BLACK)
        a2 = Arrow(shield.get_right(), interface.get_left(), buff=0.18, stroke_width=2.2, color=BLACK)
        rule = self.txt("External code asks. The object decides.", 31, BOLD).move_to(DOWN*2.55)

        self.assert_content(VGroup(shield, state, outside, interface, a1, a2, rule), "scene02")
        self.play(FadeIn(flow), run_time=RUN_QUICK)
        self.play(LaggedStart(*[FadeIn(x) for x in outside], lag_ratio=0.15), run_time=RUN_SLOW)
        self.play(GrowArrow(a1), FadeIn(shield), FadeIn(state), run_time=RUN_NORMAL)
        self.play(GrowArrow(a2), FadeIn(interface), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(rule), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 03 — UML visibility
    # ------------------------------------------------------------------
    def scene_03_uml_visibility(self):
        self.set_header(
            3,
            "UML VISIBILITY MAKES ACCESS INTENT EXPLICIT",
            "Use + for public, - for private and # for protected members. Visibility is part of the design, not decoration."
        )
        flow = self.flow_strip("MODEL")
        uml = self.uml_box(
            "Thermostat",
            ["- temperature: float"],
            ["+ setTemperature(value): void", "+ getTemperature(): float"],
            width=6.6, height=3.7,
        ).move_to(LEFT*2.65 + UP*0.15)

        legend = VGroup(
            VGroup(self.mono("+", 34), self.txt("public", 25, BOLD), self.txt("intended external access", 21)).arrange(RIGHT, buff=0.26),
            VGroup(self.mono("-", 34), self.txt("private", 25, BOLD), self.txt("class-internal state", 21)).arrange(RIGHT, buff=0.26),
            VGroup(self.mono("#", 34), self.txt("protected", 25, BOLD), self.txt("subclass-oriented access", 21)).arrange(RIGHT, buff=0.26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.44).move_to(RIGHT*4.35 + UP*0.10)

        bottom = self.txt("Design question: WHO should be allowed to change this member?", 29, BOLD).move_to(DOWN*2.65)
        self.assert_content(VGroup(uml, legend, bottom), "scene03")
        self.play(FadeIn(flow), run_time=RUN_QUICK)
        self.play(Create(uml[0]), Create(uml[1]), Create(uml[2]), run_time=RUN_NORMAL)
        self.play(FadeIn(uml[3]), FadeIn(uml[4]), FadeIn(uml[5]), run_time=RUN_NORMAL)
        for item in legend:
            self.play(FadeIn(item, shift=LEFT*0.10), run_time=RUN_QUICK)
            self.wait(PAUSE_SHORT)
        self.play(FadeIn(bottom), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 04 — Python internal state convention
    # ------------------------------------------------------------------
    def scene_04_python_internal_state(self):
        self.set_header(
            4,
            "PYTHON: _ATTRIBUTE COMMUNICATES INTERNAL STATE",
            "Python encapsulation is often expressed by convention: a leading underscore says this attribute belongs to the object's internal representation."
        )
        flow = self.flow_strip("CODE")
        panel, lines = self.code_panel([
            "class Temperatura:",
            "    def __init__(self, valor):",
            "        self._valor = valor",
            "",
            "t = Temperatura(20)",
        ], "PYTHON · INTERNAL STATE", width=7.0, height=3.6, font_size=23)
        panel.move_to(LEFT*3.6 + UP*0.20)

        expl = VGroup(
            self.tag("_valor", 1.70, 0.62, 24, filled=True),
            self.txt("internal by convention", 25, BOLD),
            self.txt("Not a magic security wall.", 22),
            self.txt("It communicates design intent.", 22),
        ).arrange(DOWN, buff=0.32).move_to(RIGHT*4.3 + UP*0.15)

        warning = self.txt("Encapsulation is about controlled responsibility, not secrecy.", 27, BOLD).move_to(DOWN*2.65)
        self.assert_content(VGroup(panel, expl, warning), "scene04")

        self.play(FadeIn(flow), FadeIn(panel[0]), FadeIn(panel[1]), FadeIn(panel[2]), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[Write(x) for x in lines], lag_ratio=0.15), run_time=RUN_SLOW*1.4)
        self.wait(PAUSE_READ)
        self.play(LaggedStart(*[FadeIn(x) for x in expl], lag_ratio=0.15), run_time=RUN_SLOW)
        self.play(FadeIn(warning), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 05 — property interface
    # ------------------------------------------------------------------
    def scene_05_property_interface(self):
        self.set_header(
            5,
            "PYTHON @property EXPOSES A CONTROLLED INTERFACE",
            "A property lets other code read or assign through a familiar attribute-like interface while the object keeps control of the implementation."
        )
        flow = self.flow_strip("CODE")
        panel, lines = self.code_panel([
            "@property",
            "def valor(self):",
            "    return self._valor",
        ], "READ INTERFACE", width=5.8, height=2.7, font_size=24)
        panel.move_to(LEFT*4.1 + UP*0.55)

        call = self.mono("print(t.valor)", 29).move_to(LEFT*4.1 + DOWN*1.45)
        arrow = Arrow(LEFT*0.75, RIGHT*0.75, color=BLACK, stroke_width=2.2).move_to(ORIGIN + UP*0.20)
        internal = VGroup(
            self.tag("PUBLIC VIEW", 2.10, filled=True),
            self.mono("t.valor", 27),
            self.txt("↓", 26),
            self.tag("INTERNAL", 1.85),
            self.mono("self._valor", 27),
        ).arrange(DOWN, buff=0.20).move_to(RIGHT*4.15 + UP*0.15)

        note = self.txt("The caller sees a stable interface; the class owns the storage.", 28, BOLD).move_to(DOWN*2.65)
        self.assert_content(VGroup(panel, call, arrow, internal, note), "scene05")
        self.play(FadeIn(flow), run_time=RUN_QUICK)
        self.play(FadeIn(panel[0]), FadeIn(panel[1]), FadeIn(panel[2]), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[Write(x) for x in lines], lag_ratio=0.18), run_time=RUN_SLOW)
        self.play(Write(call), run_time=RUN_NORMAL)
        self.play(GrowArrow(arrow), LaggedStart(*[FadeIn(x) for x in internal], lag_ratio=0.12), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(note), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 06 — setter validation / absolute zero
    # ------------------------------------------------------------------
    def scene_06_setter_validation(self):
        self.set_header(
            6,
            "VALIDATION BELONGS CLOSE TO THE STATE IT PROTECTS",
            "The m10 rule is physical and explicit: a temperature below -273.15 °C must be rejected before the internal state changes."
        )
        flow = self.flow_strip("EXECUTE")
        panel, lines = self.code_panel([
            "@valor.setter",
            "def valor(self, nuevo):",
            "    if nuevo < -273.15:",
            "        raise ValueError(\"Por debajo del cero absoluto\")",
            "    self._valor = nuevo",
        ], "PYTHON · VALIDATED SETTER", width=8.1, height=3.95, font_size=21)
        panel.move_to(LEFT*3.5 + UP*0.20)

        valid = VGroup(
            self.mono("t.valor = 25", 24),
            self.tag("ACCEPT", 1.65, 0.55, 19, filled=True),
            self.txt("state → 25 °C", 22, BOLD),
        ).arrange(DOWN, buff=0.22).move_to(RIGHT*4.8 + UP*1.15)

        invalid = VGroup(
            self.mono("t.valor = -500", 24),
            self.tag("REJECT", 1.65, 0.55, 19),
            self.txt("state stays valid", 22, BOLD),
        ).arrange(DOWN, buff=0.22).move_to(RIGHT*4.8 + DOWN*1.20)

        divider = Line(RIGHT*2.4 + UP*0.05, RIGHT*7.0 + UP*0.05, color=LIGHT_GRAY, stroke_width=1.5)
        invariant = self.txt("INVARIANT: valor ≥ -273.15 °C", 26, BOLD).move_to(DOWN*2.85)

        self.assert_content(VGroup(panel, valid, invalid, divider, invariant), "scene06")
        self.play(FadeIn(flow), run_time=RUN_QUICK)
        self.play(FadeIn(panel[0]), FadeIn(panel[1]), FadeIn(panel[2]), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[Write(x) for x in lines], lag_ratio=0.15), run_time=RUN_SLOW*1.35)
        self.wait(PAUSE_READ)
        self.play(FadeIn(valid), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(Create(divider), FadeIn(invalid), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(invariant), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 07 — Java visibility modifiers
    # ------------------------------------------------------------------
    def scene_07_java_visibility(self):
        self.set_header(
            7,
            "JAVA: VISIBILITY IS ENFORCED WITH MODIFIERS",
            "private restricts direct field access; public exposes the class interface; protected is mainly for subclass-oriented access."
        )
        flow = self.flow_strip("CODE")
        panel, lines = self.code_panel([
            "class Sensor {",
            "    private double valor;",
            "",
            "    public double getValor() { return valor; }",
            "    public void setValor(double valor) {",
            "        if (valor < -273.15) throw new IllegalArgumentException();",
            "        this.valor = valor;",
            "    }",
            "}",
        ], "JAVA · PURPOSEFUL VISIBILITY", width=8.8, height=4.45, font_size=18)
        panel.move_to(LEFT*3.05 + UP*0.10)

        ladder = VGroup(
            self.tag("private", 1.80, 0.58, 21, filled=True),
            self.txt("field", 21),
            self.txt("↓", 24),
            self.tag("public", 1.80, 0.58, 21),
            self.txt("operations", 21),
            self.txt("↓", 24),
            self.tag("protected", 1.95, 0.58, 21),
            self.txt("subclass access", 21),
        ).arrange(DOWN, buff=0.14).move_to(RIGHT*5.35 + UP*0.10)

        note = self.txt("Keep the rule inside the object that owns the state.", 27, BOLD).move_to(DOWN*2.85)
        self.assert_content(VGroup(panel, ladder, note), "scene07")
        self.play(FadeIn(flow), run_time=RUN_QUICK)
        self.play(FadeIn(panel[0]), FadeIn(panel[1]), FadeIn(panel[2]), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[Write(x) for x in lines], lag_ratio=0.10), run_time=RUN_SLOW*1.5)
        self.play(LaggedStart(*[FadeIn(x) for x in ladder], lag_ratio=0.10), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(note), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 08 — getters/setters only with purpose
    # ------------------------------------------------------------------
    def scene_08_not_getters_everywhere(self):
        self.set_header(
            8,
            "DO NOT GENERATE GETTERS AND SETTERS MECHANICALLY",
            "A getter or setter is justified when it supports a useful interface, protects a rule, or controls a meaningful state transition."
        )
        flow = self.flow_strip("MODIFY")

        left_title = self.tag("WEAK DESIGN", 2.15, 0.60, 20).move_to(LEFT*4.5 + UP*1.90)
        left = VGroup(
            self.txt("public field", 26, BOLD),
            self.mono("temperature = anything", 22),
            self.txt("or", 21),
            self.txt("setter with no rule", 26, BOLD),
            self.mono("self._value = new", 22),
        ).arrange(DOWN, buff=0.22).move_to(LEFT*4.5 + DOWN*0.05)

        right_title = self.tag("PURPOSEFUL DESIGN", 2.75, 0.60, 20, filled=True).move_to(RIGHT*4.2 + UP*1.90)
        right = VGroup(
            self.txt("private/internal state", 26, BOLD),
            self.txt("+", 24),
            self.txt("controlled interface", 26, BOLD),
            self.txt("+", 24),
            self.txt("invariant validation", 26, BOLD),
        ).arrange(DOWN, buff=0.18).move_to(RIGHT*4.2 + DOWN*0.05)

        center = Line(UP*2.10, DOWN*2.10, color=LIGHT_GRAY, stroke_width=1.6)
        verdict = self.txt("Encapsulation should protect meaning, not add boilerplate.", 29, BOLD).move_to(DOWN*2.75)

        self.assert_content(VGroup(left_title, left, right_title, right, center, verdict), "scene08")
        self.play(FadeIn(flow), FadeIn(left_title), FadeIn(right_title), Create(center), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(x) for x in left], lag_ratio=0.14), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.play(LaggedStart(*[FadeIn(x) for x in right], lag_ratio=0.14), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(verdict), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 09 — invariant pipeline
    # ------------------------------------------------------------------
    def scene_09_invariant_flow(self):
        self.set_header(
            9,
            "PROTECTED STATE IS A FLOW, NOT A KEYWORD",
            "The design is complete only when every state-changing path passes through the same rule before the internal value is updated."
        )
        flow = self.flow_strip("EXECUTE")

        pipeline = VGroup(
            self.tag("REQUEST", 1.65, 0.62, 20),
            self.txt("→", 26),
            self.tag("VALIDATE", 1.85, 0.62, 20, filled=True),
            self.txt("→", 26),
            self.tag("UPDATE", 1.70, 0.62, 20),
            self.txt("→", 26),
            self.tag("VALID STATE", 2.05, 0.62, 20),
        ).arrange(RIGHT, buff=0.16).move_to(UP*1.55)

        invariant = RoundedRectangle(
            width=6.8, height=1.45, corner_radius=0.14,
            stroke_color=BLACK_LINE, stroke_width=2,
            fill_color=VERY_LIGHT_GRAY, fill_opacity=1,
        ).move_to(DOWN*0.20)
        inv_text = VGroup(
            self.txt("INVARIANT", 21, BOLD),
            self.txt("temperature ≥ -273.15 °C", 31, BOLD),
        ).arrange(DOWN, buff=0.16).move_to(invariant)

        reject = VGroup(
            self.tag("INVALID REQUEST", 2.25, 0.58, 18),
            self.txt("→", 24),
            self.tag("ERROR / REJECT", 2.25, 0.58, 18, filled=True),
            self.txt("→", 24),
            self.tag("NO STATE CHANGE", 2.40, 0.58, 18),
        ).arrange(RIGHT, buff=0.14).move_to(DOWN*1.75)

        summary = self.txt("One rule. One controlled path. Predictable objects.", 29, BOLD).move_to(DOWN*2.80)
        self.assert_content(VGroup(pipeline, invariant, inv_text, reject, summary), "scene09")
        self.play(FadeIn(flow), run_time=RUN_QUICK)
        self.play(LaggedStart(*[FadeIn(x) for x in pipeline], lag_ratio=0.10), run_time=RUN_SLOW)
        self.play(FadeIn(invariant), FadeIn(inv_text), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(LaggedStart(*[FadeIn(x) for x in reject], lag_ratio=0.10), run_time=RUN_SLOW)
        self.play(FadeIn(summary), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 10 — transfer to projects
    # ------------------------------------------------------------------
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
        ).arrange_in_grid(rows=3, cols=2, buff=(0.38, 0.28)).move_to(UP*0.20)

        question = self.txt("What rule must stay true after every public change?", 30, BOLD).move_to(DOWN*2.55)
        self.assert_content(VGroup(cards, question), "scene10")
        self.play(FadeIn(flow), run_time=RUN_QUICK)
        self.play(LaggedStart(*[FadeIn(c, shift=UP*0.08) for c in cards], lag_ratio=0.12), run_time=RUN_SLOW*1.5)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(question), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    def domain_card(self, domain, cls, state, operation):
        box = RoundedRectangle(
            width=6.15, height=1.30, corner_radius=0.12,
            stroke_color=BLACK_LINE, stroke_width=1.6,
            fill_color=WHITE, fill_opacity=1,
        )
        label = self.txt(domain, 17, BOLD).align_to(box, LEFT).align_to(box, UP).shift(RIGHT*0.20 + DOWN*0.14)
        line = VGroup(
            self.txt(cls, 22, BOLD),
            self.mono(state, 20),
            self.mono(operation, 18),
        ).arrange(RIGHT, buff=0.36).move_to(box.get_center() + DOWN*0.14)
        if line.width > 5.75:
            line.scale_to_fit_width(5.75)
        return VGroup(box, label, line)

    # ------------------------------------------------------------------
    # 11 — evidence / m10
    # ------------------------------------------------------------------
    def scene_11_evidence(self):
        self.set_header(
            11,
            "TODAY'S EVIDENCE · MODULE m10",
            "Your evidence must show protected state, one enforced rule, and correct UML visibility. Python or Java is acceptable."
        )
        flow = self.flow_strip("EXPLAIN")

        checklist = VGroup(
            self.txt("□  One internal/private field", 27, BOLD),
            self.txt("□  One public read/change interface", 27, BOLD),
            self.txt("□  One invariant validated inside the object", 27, BOLD),
            self.txt("□  UML uses + / - / # correctly", 27, BOLD),
            self.txt("□  Explain why the setter/property exists", 27, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.30).move_to(LEFT*3.15 + UP*0.20)

        module = self.tag("MODULE m10 · PYTHON OR JAVA", 4.15, 0.70, 22, filled=True).move_to(RIGHT*4.25 + UP*1.65)
        py = VGroup(
            self.tag("PYTHON", 1.55, 0.54, 18),
            self.mono("_valor · @property · @valor.setter", 18),
        ).arrange(DOWN, buff=0.18).move_to(RIGHT*4.25 + UP*0.45)
        java = VGroup(
            self.tag("JAVA", 1.55, 0.54, 18),
            self.mono("private · public · protected", 18),
        ).arrange(DOWN, buff=0.18).move_to(RIGHT*4.25 + DOWN*0.80)

        mandatory = self.txt("MANDATORY: the invalid change must be rejected.", 24, BOLD).move_to(RIGHT*4.05 + DOWN*2.05)
        self.assert_content(VGroup(checklist, module, py, java, mandatory), "scene11")
        self.play(FadeIn(flow), run_time=RUN_QUICK)
        for item in checklist:
            self.play(FadeIn(item, shift=RIGHT*0.08), run_time=RUN_QUICK)
            self.wait(0.55)
        self.play(FadeIn(module), FadeIn(py), FadeIn(java), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(mandatory), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Final
    # ------------------------------------------------------------------
    def final_exit_check(self):
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=RUN_NORMAL)
        title = self.txt("EXIT CHECK · CLASS 04", 33, BOLD).move_to(UP*3.15)
        questions = VGroup(
            self.txt("1. What state should not be freely overwritten?", 27),
            self.txt("2. Which member is public, private or protected?", 27),
            self.txt("3. What invariant does the object enforce?", 27),
            self.txt("4. Where should validation happen?", 27),
            self.txt("5. Why does this getter / setter / property exist?", 27),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).move_to(UP*0.55)

        final = self.txt("ENCAPSULATION = CONTROLLED STATE CHANGE", 38, BOLD).move_to(DOWN*1.80)
        footer = self.txt("REQUEST → VALIDATE → UPDATE → VALID STATE", 26, BOLD).move_to(DOWN*2.72)
        sentence = self.txt("Protect the rule, not just the variable.", 27).move_to(DOWN*3.38)

        self.assert_frame(VGroup(title, questions, final, footer, sentence), "final")
        self.play(FadeIn(title), run_time=RUN_NORMAL)
        for q in questions:
            self.play(FadeIn(q, shift=UP*0.05), run_time=RUN_QUICK)
            self.wait(PAUSE_READ)
        self.play(FadeIn(final), run_time=RUN_SLOW)
        self.play(FadeIn(footer), FadeIn(sentence), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=RUN_NORMAL)
