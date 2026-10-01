#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Seminar 11 · Class 03 · Constructors & Valid State · V2.

Curriculum-aligned ManimCE 0.20.x scene for Instituto Jorge Robledo.
Visual continuity: white background, black/gray hierarchy, persistent numbered
headers, Robot/Atlas narrative, UML boxes, thin arrows, semantic motion.
"""
from __future__ import annotations

import os
from manim import *

# -----------------------------------------------------------------------------
# Render contract
# -----------------------------------------------------------------------------
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

TIME_SCALE = float(os.getenv("LESSON_TIME_SCALE", "1.0"))

BLACK_TEXT = BLACK
DARK_GRAY = "#303030"
MID_GRAY = "#777777"
LIGHT_GRAY = "#D7D7D7"
PAPER = "#F7F7F7"
SOFT = "#EFEFEF"
WHITE_FILL = WHITE

SAFE_LEFT, SAFE_RIGHT = -7.55, 7.55
SAFE_BOTTOM, SAFE_TOP = -4.10, 2.62


class Seminar11Class03ConstructorsValidState(Scene):
    """Complete Class 03 lesson: constructors, self, valid state, UML sync, m09."""

    # ------------------------------------------------------------------
    # Core scene lifecycle
    # ------------------------------------------------------------------
    def setup(self):
        super().setup()
        self.camera.background_color = WHITE
        self.header_group = None

    def play(self, *animations, **kwargs):
        kwargs["run_time"] = kwargs.get("run_time", 1.0) * TIME_SCALE
        return super().play(*animations, **kwargs)

    def wait(self, duration=1.0, *args, **kwargs):
        return super().wait(duration * TIME_SCALE, *args, **kwargs)

    def construct(self):
        self.chapter_00_continuity()
        self.chapter_01_repair_bridge()
        self.chapter_02_problem_without_constructor()
        self.chapter_03_constructor_mental_model()
        self.chapter_04_python_init()
        self.chapter_05_self_and_parameters()
        self.chapter_06_three_objects()
        self.chapter_07_valid_state()
        self.chapter_08_constructor_vs_method()
        self.chapter_09_uml_sync()
        self.chapter_10_m09_transfer()
        self.chapter_11_exit_challenge()
        self.chapter_12_final_synthesis()

    # ------------------------------------------------------------------
    # Typography / layout helpers
    # ------------------------------------------------------------------
    def t(self, text, size=30, weight=NORMAL, color=BLACK_TEXT, font=None, **kwargs):
        opts = dict(font_size=size, color=color, weight=weight, line_spacing=0.9)
        if font:
            opts["font"] = font
        opts.update(kwargs)
        return Text(text, **opts)

    def code_t(self, text, size=24, weight=NORMAL, color=BLACK_TEXT):
        return self.t(text, size=size, weight=weight, color=color, font="DejaVu Sans Mono")

    def fit(self, mob, max_w=14.7, max_h=6.2):
        if mob.width > max_w:
            mob.scale_to_fit_width(max_w)
        if mob.height > max_h:
            mob.scale_to_fit_height(max_h)
        return mob

    def assert_safe_bounds(self, mob, label="content"):
        l, r = mob.get_left()[0], mob.get_right()[0]
        b, t = mob.get_bottom()[1], mob.get_top()[1]
        if l < SAFE_LEFT or r > SAFE_RIGHT or b < SAFE_BOTTOM or t > SAFE_TOP:
            raise ValueError(
                f"{label} outside safe content zone: left={l:.2f}, right={r:.2f}, "
                f"bottom={b:.2f}, top={t:.2f}"
            )

    def set_header(self, n, title, subtitle):
        num_box = RoundedRectangle(
            width=0.62, height=0.46, corner_radius=0.08,
            stroke_color=BLACK_TEXT, stroke_width=1.7,
            fill_color=WHITE, fill_opacity=1.0,
        )
        num = self.t(f"{n:02d}", 21, BOLD).move_to(num_box)
        title_m = self.t(title.upper(), 34, BOLD)
        title_m = self.fit(title_m, 13.7, 0.50)
        row = VGroup(VGroup(num_box, num), title_m).arrange(RIGHT, buff=0.23)
        row.to_edge(UP, buff=0.13).to_edge(LEFT, buff=0.43)

        rule = Line(LEFT * 7.47, RIGHT * 7.47, stroke_color=LIGHT_GRAY, stroke_width=1.4)
        rule.next_to(row, DOWN, buff=0.06)

        sub = self.t(subtitle, 20, color=DARK_GRAY)
        sub = self.fit(sub, 14.6, 0.46)
        sub.next_to(rule, DOWN, buff=0.07).align_to(row, LEFT)
        new = VGroup(row, rule, sub)

        if self.header_group is None:
            self.header_group = new
            self.add(new)
        else:
            # V2 QA FIX: never morph two long header strings through each other.
            # A short fade-to-clean followed by fade-in prevents the visible glyph collision
            # present in V1 around chapter changes.
            old = self.header_group
            self.play(FadeOut(old), run_time=0.22)
            self.remove(old)
            self.header_group = new
            self.play(FadeIn(new), run_time=0.28)
        return new

    def clear_content_keep_header(self, rt=0.75):
        keep_ids = set()
        if self.header_group is not None:
            keep_ids = {id(m) for m in self.header_group.get_family()}
        removable = [m for m in list(self.mobjects) if id(m) not in keep_ids]
        if removable:
            self.play(*[FadeOut(m) for m in removable], run_time=rt)

    def label_box(self, text, width=None, height=0.55, size=23, bold=False, fill=PAPER):
        txt = self.t(text, size=size, weight=BOLD if bold else NORMAL)
        w = width or max(1.5, txt.width + 0.55)
        box = RoundedRectangle(
            width=w, height=height, corner_radius=0.08,
            stroke_color=BLACK_TEXT, stroke_width=1.4,
            fill_color=fill, fill_opacity=1.0,
        )
        if txt.width > w - 0.30:
            txt.scale_to_fit_width(w - 0.30)
        txt.move_to(box)
        return VGroup(box, txt)

    def make_robot(self, label="Atlas", scale=1.0):
        head = RoundedRectangle(
            width=1.15, height=0.65, corner_radius=0.12,
            stroke_color=BLACK_TEXT, stroke_width=2,
            fill_color=WHITE, fill_opacity=1,
        ).shift(UP * 0.92)
        eye_l = Dot(head.get_center() + LEFT * 0.25 + UP * 0.03, radius=0.035, color=BLACK_TEXT)
        eye_r = Dot(head.get_center() + RIGHT * 0.25 + UP * 0.03, radius=0.035, color=BLACK_TEXT)
        mouth = Line(head.get_center() + LEFT * 0.16 + DOWN * 0.18,
                     head.get_center() + RIGHT * 0.16 + DOWN * 0.18,
                     stroke_color=MID_GRAY, stroke_width=1.3)
        antenna = Line(head.get_top(), head.get_top() + UP * 0.28, stroke_color=BLACK_TEXT, stroke_width=1.6)
        antenna_dot = Dot(antenna.get_end(), radius=0.045, color=BLACK_TEXT)

        body = RoundedRectangle(
            width=1.52, height=1.20, corner_radius=0.10,
            stroke_color=BLACK_TEXT, stroke_width=2,
            fill_color=WHITE, fill_opacity=1,
        ).shift(DOWN * 0.10)
        battery = Rectangle(width=0.62, height=0.30, stroke_color=MID_GRAY, stroke_width=1.4).move_to(body)
        bars = VGroup(*[
            Rectangle(width=0.10, height=0.18, stroke_color=MID_GRAY, fill_color=MID_GRAY, fill_opacity=0.55, stroke_width=0.8)
            for _ in range(4)
        ]).arrange(RIGHT, buff=0.035).move_to(battery)
        arm_l = Line(body.get_left() + UP * 0.25, body.get_left() + LEFT * 0.50 + DOWN * 0.10,
                     stroke_color=BLACK_TEXT, stroke_width=1.5)
        arm_r = Line(body.get_right() + UP * 0.25, body.get_right() + RIGHT * 0.50 + DOWN * 0.10,
                     stroke_color=BLACK_TEXT, stroke_width=1.5)
        wheel_l = Circle(radius=0.16, stroke_color=BLACK_TEXT, stroke_width=1.6).move_to(body.get_bottom() + LEFT * 0.48 + DOWN * 0.12)
        wheel_r = Circle(radius=0.16, stroke_color=BLACK_TEXT, stroke_width=1.6).move_to(body.get_bottom() + RIGHT * 0.48 + DOWN * 0.12)
        name = self.t(label, 24, BOLD).next_to(VGroup(wheel_l, wheel_r), DOWN, buff=0.13)
        group = VGroup(head, eye_l, eye_r, mouth, antenna, antenna_dot, body, battery, bars, arm_l, arm_r, wheel_l, wheel_r, name)
        group.scale(scale)
        return group

    def make_uml_class(self, name, attrs, methods, width=3.5, height=3.35, font_size=20):
        outer = Rectangle(width=width, height=height, stroke_color=BLACK_TEXT, stroke_width=1.5, fill_color=WHITE, fill_opacity=1)
        y_top = outer.get_top()[1]
        h1 = y_top - 0.65
        h2 = outer.get_bottom()[1] + 1.05
        div1 = Line([outer.get_left()[0], h1, 0], [outer.get_right()[0], h1, 0], stroke_color=MID_GRAY, stroke_width=1.1)
        div2 = Line([outer.get_left()[0], h2, 0], [outer.get_right()[0], h2, 0], stroke_color=MID_GRAY, stroke_width=1.1)
        title = self.t(name, font_size + 3, BOLD).move_to([0, (y_top + h1) / 2, 0])
        attr_m = VGroup(*[self.t(a, font_size, color=DARK_GRAY) for a in attrs]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        if attr_m.height > (h1 - h2) - 0.20:
            attr_m.scale_to_fit_height((h1 - h2) - 0.20)
        attr_m.move_to([0, (h1 + h2) / 2, 0]).align_to(outer, LEFT).shift(RIGHT * 0.22)
        meth_m = VGroup(*[self.t(m, font_size, color=DARK_GRAY) for m in methods]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        if meth_m.height > (h2 - outer.get_bottom()[1]) - 0.16:
            meth_m.scale_to_fit_height((h2 - outer.get_bottom()[1]) - 0.16)
        meth_m.move_to([0, (h2 + outer.get_bottom()[1]) / 2, 0]).align_to(outer, LEFT).shift(RIGHT * 0.22)
        return VGroup(outer, div1, div2, title, attr_m, meth_m)

    def make_object_card(self, var, name, energy, position, width=2.65, height=1.85):
        box = RoundedRectangle(width=width, height=height, corner_radius=0.10,
                               stroke_color=BLACK_TEXT, stroke_width=1.4,
                               fill_color=WHITE, fill_opacity=1)
        top_y = box.get_top()[1] - 0.34
        title = self.t(f"{var} : Robot", 22, BOLD).move_to([0, top_y, 0])
        divider = Line(box.get_left() + UP * 0.48, box.get_right() + UP * 0.48,
                       stroke_color=LIGHT_GRAY, stroke_width=1.0)
        state = VGroup(
            self.code_t(f'name = "{name}"', 19),
            self.code_t(f"energy = {energy}", 19),
            self.code_t(f"position = {position}", 19),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        state.next_to(divider, DOWN, buff=0.18).align_to(box, LEFT).shift(RIGHT * 0.20)
        return VGroup(box, divider, title, state)

    def make_code_panel(self, lines, width=6.4, font_size=21, title=None, padding=0.28):
        line_mobs = VGroup(*[self.code_t(line, font_size) for line in lines]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        h = max(1.25, line_mobs.height + 2 * padding + (0.45 if title else 0))
        box = RoundedRectangle(width=width, height=h, corner_radius=0.10,
                               stroke_color=MID_GRAY, stroke_width=1.25,
                               fill_color=PAPER, fill_opacity=1)
        if line_mobs.width > width - 0.46:
            line_mobs.scale_to_fit_width(width - 0.46)
        if title:
            title_m = self.t(title, 18, BOLD, color=DARK_GRAY)
            title_m.next_to(box.get_top(), DOWN, buff=0.15).align_to(box, LEFT).shift(RIGHT * 0.22)
            line_mobs.next_to(title_m, DOWN, buff=0.15).align_to(title_m, LEFT)
            return VGroup(box, title_m, line_mobs), line_mobs
        line_mobs.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.23)
        return VGroup(box, line_mobs), line_mobs

    def make_argument_token(self, text, width=1.55, height=0.55):
        return self.label_box(text, width=width, height=height, size=21, fill=WHITE)

    def make_constructor_gate(self, label="Robot(...)", subtitle="CONSTRUCTOR", width=2.35, height=1.35):
        box = RoundedRectangle(width=width, height=height, corner_radius=0.12,
                               stroke_color=BLACK_TEXT, stroke_width=1.8,
                               fill_color=PAPER, fill_opacity=1)
        top = self.code_t(label, 23, BOLD)
        sub = self.t(subtitle, 16, BOLD, color=MID_GRAY)
        VGroup(top, sub).arrange(DOWN, buff=0.14).move_to(box)
        return VGroup(box, top, sub)

    def make_state_row(self, left, right, width=5.6):
        l = self.code_t(left, 23)
        r = self.code_t(right, 23, BOLD)
        arr = Arrow(LEFT, RIGHT, buff=0, stroke_width=1.6, max_tip_length_to_length_ratio=0.12)
        group = VGroup(l, arr, r).arrange(RIGHT, buff=0.30)
        if group.width > width:
            group.scale_to_fit_width(width)
        return group

    def make_question_panel(self, question, answer=None, width=11.8):
        q = self.t(question, 29, BOLD)
        self.fit(q, width - 0.6, 1.2)
        elems = [q]
        if answer:
            a = self.t(answer, 25, color=DARK_GRAY)
            self.fit(a, width - 0.6, 0.95)
            elems.append(a)
        inner = VGroup(*elems).arrange(DOWN, buff=0.28)
        box = RoundedRectangle(width=width, height=max(1.55, inner.height + 0.65), corner_radius=0.14,
                               stroke_color=BLACK_TEXT, stroke_width=1.5,
                               fill_color=WHITE, fill_opacity=1)
        inner.move_to(box)
        return VGroup(box, inner)

    def make_pipeline(self, labels, y=-3.15, max_width=14.1):
        nodes = VGroup(*[self.label_box(x, width=max(1.45, min(2.25, 0.12 * len(x) + 1.0)), height=0.52, size=19) for x in labels])
        arrows = VGroup()
        whole = VGroup()
        for i, node in enumerate(nodes):
            whole.add(node)
            if i < len(nodes) - 1:
                whole.add(Arrow(ORIGIN, RIGHT, buff=0, stroke_width=1.35, max_tip_length_to_length_ratio=0.14).set_length(0.55))
        whole.arrange(RIGHT, buff=0.12).move_to([0, y, 0])
        if whole.width > max_width:
            whole.scale_to_fit_width(max_width)
        return whole

    # ------------------------------------------------------------------
    # CHAPTER 00 — continuity
    # ------------------------------------------------------------------
    def chapter_00_continuity(self):
        self.set_header(0, "03 · CONSTRUCTORS & VALID STATE", "An object should begin life ready to use.")

        recall = VGroup(
            self.t("MODEL THE WORLD.", 39, BOLD),
            self.t("GIVE EACH OBJECT A RESPONSIBILITY.", 39, BOLD),
        ).arrange(DOWN, buff=0.10).move_to(UP * 0.45)
        self.fit(recall, 12.8, 1.8)
        self.play(FadeIn(recall, shift=UP * 0.15), run_time=1.15)
        self.wait(2.6)

        robot = self.make_robot("Atlas", 1.0).move_to(LEFT * 2.25 + DOWN * 0.35)
        state = self.make_object_card("atlas", "Atlas", 90, 0, width=3.15, height=2.15).move_to(RIGHT * 2.6 + DOWN * 0.15)
        self.play(recall.animate.scale(0.62).to_edge(UP, buff=1.55), FadeIn(robot), FadeIn(state), run_time=1.15)
        self.wait(2.8)

        q1 = self.t("HOW DID THESE VALUES GET INSIDE ATLAS?", 34, BOLD).move_to(DOWN * 2.55)
        self.fit(q1, 12.8, 0.65)
        self.play(Write(q1), run_time=1.2)
        self.wait(3.2)
        q2 = self.t("HOW DOES AN OBJECT BEGIN ITS LIFE?", 37, BOLD).move_to(DOWN * 2.55)
        self.play(ReplacementTransform(q1, q2), run_time=1.0)
        self.wait(4.0)
        self.clear_content_keep_header()

    # ------------------------------------------------------------------
    # CHAPTER 01 — repair bridge
    # ------------------------------------------------------------------
    def chapter_01_repair_bridge(self):
        self.set_header(1, "FROM UML TO A REAL PYTHON OBJECT", "First repair the bridge: model → class → instance.")

        uml = self.make_uml_class(
            "Robot",
            ["name: str", "energy: int", "position: int"],
            ["move()", "recharge()"], width=4.00, height=3.85, font_size=21,
        ).move_to(LEFT * 4.55 + DOWN * 0.25)
        pyclass_panel, _ = self.make_code_panel(["class Robot:", "    ..."], width=4.0, font_size=25, title="PYTHON CLASS")
        pyclass_panel.move_to(DOWN * 0.35)
        call_panel, _ = self.make_code_panel(["atlas = Robot(...)"], width=4.05, font_size=25, title="INSTANCE")
        call_panel.move_to(RIGHT * 4.55 + DOWN * 0.25)

        a1 = Arrow(uml.get_right(), pyclass_panel.get_left(), buff=0.15, stroke_width=1.6, max_tip_length_to_length_ratio=0.10)
        a2 = Arrow(pyclass_panel.get_right(), call_panel.get_left(), buff=0.15, stroke_width=1.6, max_tip_length_to_length_ratio=0.10)
        captions = VGroup(
            self.t("UML CLASS", 20, BOLD, color=MID_GRAY).next_to(uml, UP, buff=0.17),
            self.t("PYTHON CLASS", 20, BOLD, color=MID_GRAY).next_to(pyclass_panel, UP, buff=0.17),
            self.t("REAL OBJECT", 20, BOLD, color=MID_GRAY).next_to(call_panel, UP, buff=0.17),
        )
        grp = VGroup(uml, pyclass_panel, call_panel, a1, a2, captions)
        self.assert_safe_bounds(grp, "repair bridge")

        self.play(Create(uml), run_time=1.0)
        self.wait(2.0)
        self.play(Create(a1), FadeIn(pyclass_panel), run_time=1.0)
        self.wait(2.2)
        self.play(Create(a2), FadeIn(call_panel), run_time=1.0)
        self.wait(3.0)

        robot = self.make_robot("Atlas", 0.88).move_to(call_panel.get_center() + DOWN * 2.0)
        create_msg = self.t("Robot(...)  means  CREATE A REAL ROBOT OBJECT", 31, BOLD).move_to(DOWN * 3.25)
        self.fit(create_msg, 12.6, 0.55)
        self.play(FadeIn(robot, shift=UP * 0.25), Write(create_msg), run_time=1.25)
        self.wait(4.2)
        self.clear_content_keep_header()

    # ------------------------------------------------------------------
    # CHAPTER 02 — object-design problem
    # ------------------------------------------------------------------
    def chapter_02_problem_without_constructor(self):
        self.set_header(2, "THE PROBLEM WITHOUT A CONSTRUCTOR", "Patching state later can leave an object incomplete or impossible.")

        robot = self.make_robot("Atlas", 0.92).move_to(LEFT * 3.45 + DOWN * 0.25)
        init_call = self.code_t("atlas = Robot()", 30, BOLD).move_to(LEFT * 3.45 + UP * 1.75)
        assign1 = self.code_t('atlas.name = "Atlas"', 25).move_to(RIGHT * 2.5 + UP * 1.15)
        assign2 = self.code_t("atlas.energy = 90", 25).move_to(RIGHT * 3.15 + DOWN * 0.05)
        assign3 = self.code_t("atlas.position = 0", 25).move_to(RIGHT * 2.45 + DOWN * 1.25)
        for a in (assign1, assign2, assign3):
            self.fit(a, 4.9, 0.45)
        self.play(FadeIn(init_call), FadeIn(robot), run_time=1.0)
        self.wait(2.0)
        self.play(FadeIn(assign1, shift=LEFT), FadeIn(assign2, shift=LEFT), FadeIn(assign3, shift=LEFT), run_time=1.25)
        self.wait(2.8)

        ask = self.t("WHAT IF WE FORGET ONE?", 34, BOLD).move_to(UP * 2.15)
        self.play(Write(ask), run_time=0.9)
        self.wait(2.2)
        self.play(FadeOut(assign2), run_time=0.7)

        incomplete = VGroup(
            self.t("name     ✓", 25, BOLD),
            self.t("position ✓", 25, BOLD),
            self.t("energy   ?", 25, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to(RIGHT * 2.9 + DOWN * 0.10)
        tag_bad = self.label_box("INCOMPLETE OBJECT", width=3.35, height=0.58, size=20, bold=True).next_to(incomplete, DOWN, buff=0.35)
        self.play(FadeOut(assign1), FadeOut(assign3), FadeIn(incomplete), FadeIn(tag_bad), run_time=1.0)
        self.wait(3.0)

        impossible = self.code_t("energy = -40", 26, BOLD).move_to(RIGHT * 2.9 + UP * 0.45)
        tag_imp = self.label_box("IMPOSSIBLE STATE", width=3.15, height=0.58, size=20, bold=True).next_to(impossible, DOWN, buff=0.35)
        self.play(FadeOut(incomplete), FadeOut(tag_bad), FadeIn(impossible), FadeIn(tag_imp), run_time=1.0)
        self.wait(2.8)

        core = self.t("CAN WE FORCE EVERY ROBOT TO BEGIN WITH THE INFORMATION IT NEEDS?", 30, BOLD).move_to(DOWN * 2.95)
        self.fit(core, 13.6, 0.62)
        self.play(Write(core), run_time=1.1)
        self.wait(4.2)
        self.clear_content_keep_header()

    # ------------------------------------------------------------------
    # CHAPTER 03 — mental model before syntax
    # ------------------------------------------------------------------
    def chapter_03_constructor_mental_model(self):
        self.set_header(3, "CONSTRUCTOR MENTAL MODEL", "Values enter; required state is initialized; a usable object comes out.")

        tokens = VGroup(
            self.make_argument_token('"Atlas"', 1.65),
            self.make_argument_token("90", 1.25),
            self.make_argument_token("0", 1.25),
        ).arrange(DOWN, buff=0.28).move_to(LEFT * 5.2 + DOWN * 0.10)
        token_label = self.t("INPUT VALUES", 21, BOLD, color=MID_GRAY).next_to(tokens, UP, buff=0.25)
        gate = self.make_constructor_gate("Robot(...)", "CONSTRUCTOR", 2.95, 1.65).move_to(LEFT * 1.25 + DOWN * 0.10)
        card = self.make_object_card("atlas", "Atlas", 90, 0, width=3.55, height=2.45).move_to(RIGHT * 4.2 + DOWN * 0.10)
        a_in = Arrow(tokens.get_right(), gate.get_left(), buff=0.25, stroke_width=1.7, max_tip_length_to_length_ratio=0.10)
        a_out = Arrow(gate.get_right(), card.get_left(), buff=0.25, stroke_width=1.7, max_tip_length_to_length_ratio=0.10)
        self.play(FadeIn(tokens), FadeIn(token_label), FadeIn(gate), Create(a_in), Create(a_out), run_time=1.25)
        self.wait(2.5)

        ghost_tokens = tokens.copy()
        self.add(ghost_tokens)
        self.play(ghost_tokens.animate.move_to(gate), run_time=1.3)
        self.play(FadeOut(ghost_tokens), FadeIn(card, shift=RIGHT * 0.15), run_time=1.0)
        self.wait(3.2)

        pipeline = self.make_pipeline(["ARGUMENTS", "CONSTRUCTOR", "INITIALIZATION", "VALID OBJECT"], y=-2.92)
        self.play(FadeIn(pipeline), run_time=1.0)
        self.wait(2.8)
        definition = self.make_question_panel(
            "CONSTRUCTOR",
            "Creates an object with its required initial state.", width=9.6,
        ).move_to(UP * 2.15)
        self.play(FadeIn(definition), run_time=1.0)
        self.wait(4.0)
        self.clear_content_keep_header()

    # ------------------------------------------------------------------
    # CHAPTER 04 — Python __init__
    # ------------------------------------------------------------------
    def chapter_04_python_init(self):
        self.set_header(4, "PYTHON __init__", "Now connect the mental model to real Python syntax, one line at a time.")

        lines = [
            "class Robot:",
            "    def __init__(self, name, energy, position):",
            "        self.name = name",
            "        self.energy = energy",
            "        self.position = position",
        ]
        panel, code_lines = self.make_code_panel(lines, width=8.75, font_size=24, title="ROBOT IMPLEMENTATION")
        panel.move_to(LEFT * 3.25 + DOWN * 0.25)
        # Hide all lines initially; keep panel chrome.
        chrome = VGroup(panel[0], panel[1])
        self.play(FadeIn(chrome), run_time=0.8)
        for i, line in enumerate(code_lines):
            self.play(FadeIn(line, shift=RIGHT * 0.08), run_time=0.75)
            self.wait(1.15 if i else 1.6)
            if i == 1:
                tag = self.label_box("INITIALIZATION METHOD", width=3.15, height=0.55, size=18, bold=True).move_to(RIGHT * 4.7 + UP * 1.35)
                arrow = Arrow(tag.get_left(), line.get_right(), buff=0.15, stroke_width=1.4, max_tip_length_to_length_ratio=0.08)
                self.play(FadeIn(tag), Create(arrow), run_time=0.8)
                self.wait(2.2)
                self.play(FadeOut(tag), FadeOut(arrow), run_time=0.6)

        robot = self.make_robot("Atlas", 0.88).move_to(RIGHT * 4.5 + DOWN * 0.20)
        self.play(FadeIn(robot), run_time=0.8)
        self.wait(1.5)

        mappings = [
            ("name", "self.name"),
            ("energy", "self.energy"),
            ("position", "self.position"),
        ]
        y_positions = [1.10, 0.00, -1.10]
        semantic_rows = VGroup()
        for (param, attr), y in zip(mappings, y_positions):
            row = self.make_state_row(param, attr, width=4.6).move_to(RIGHT * 3.9 + UP * y)
            semantic_rows.add(row)
            self.play(FadeIn(row[0]), Create(row[1]), FadeIn(row[2]), run_time=0.85)
            self.wait(1.2)
        note = self.t("parameter enters  →  attribute stays in THIS object", 22, BOLD, color=DARK_GRAY).move_to(DOWN * 2.85)
        self.fit(note, 12.2, 0.46)
        self.play(Write(note), run_time=0.9)
        self.wait(4.0)
        self.clear_content_keep_header()

    # ------------------------------------------------------------------
    # CHAPTER 05 — self + parameter vs attribute
    # ------------------------------------------------------------------
    def chapter_05_self_and_parameters(self):
        self.set_header(5, "SELF AND PARAMETERS", "self is the current object; parameters are temporary inputs to a call.")

        robots = VGroup(
            self.make_robot("Atlas", 0.68),
            self.make_robot("Explorer", 0.68),
            self.make_robot("Courier", 0.68),
        ).arrange(RIGHT, buff=1.15).move_to(UP * 0.35)
        names = ["Atlas", "Explorer", "Courier"]
        self.play(FadeIn(robots), run_time=1.0)
        self.wait(1.5)

        eq = VGroup(self.code_t("self", 30, BOLD), self.t("=", 30, BOLD), self.t("CURRENT OBJECT", 30, BOLD)).arrange(RIGHT, buff=0.35).move_to(UP * 2.15)
        self.play(Write(eq), run_time=0.9)
        self.wait(2.0)
        for robot, name in zip(robots, names):
            tag = self.label_box(f"self → {name}", width=2.35, height=0.52, size=18, bold=True).next_to(robot, DOWN, buff=0.22)
            self.play(FadeIn(tag), Indicate(robot, scale_factor=1.03, color=MID_GRAY), run_time=0.75)
            self.wait(1.25)
            self.play(FadeOut(tag), run_time=0.45)

        self.play(FadeOut(robots), FadeOut(eq), run_time=0.8)

        left_title = self.t("PARAMETER", 25, BOLD).move_to(LEFT * 3.6 + UP * 2.0)
        right_title = self.t("OBJECT STATE", 25, BOLD).move_to(RIGHT * 3.6 + UP * 2.0)
        divider = Line(UP * 1.75, DOWN * 2.15, stroke_color=LIGHT_GRAY, stroke_width=1.2)
        rows = VGroup(
            self.make_state_row("name", "self.name", 6.0),
            self.make_state_row("energy", "self.energy", 6.0),
            self.make_state_row("position", "self.position", 6.0),
        ).arrange(DOWN, buff=0.50).move_to(DOWN * 0.05)
        self.play(FadeIn(left_title), FadeIn(right_title), Create(divider), run_time=0.8)
        for row in rows:
            self.play(FadeIn(row), run_time=0.75)
            self.wait(1.1)
        self.wait(2.0)

        self.play(FadeOut(rows), FadeOut(left_title), FadeOut(right_title), FadeOut(divider), run_time=0.8)
        panel, cl = self.make_code_panel(["def recharge(self, amount):", "    self.energy += amount"], width=6.8, font_size=25, title="METHOD CALL")
        panel.move_to(LEFT * 2.7 + UP * 0.30)
        atlas_card = self.make_object_card("atlas", "Atlas", 90, 0, width=3.35, height=2.35).move_to(RIGHT * 4.1 + UP * 0.30)
        amount = self.make_argument_token("amount = 5", 2.1).move_to(LEFT * 1.2 + DOWN * 2.2)
        persistent = self.label_box("self.energy remains", width=2.6, height=0.55, size=19, bold=True).move_to(RIGHT * 4.1 + DOWN * 2.2)
        self.play(FadeIn(panel), FadeIn(atlas_card), FadeIn(amount), FadeIn(persistent), run_time=1.0)
        self.wait(2.2)
        self.play(amount.animate.move_to(panel.get_center() + DOWN * 0.35), run_time=0.9)
        self.play(FadeOut(amount), Indicate(atlas_card, scale_factor=1.02, color=MID_GRAY), run_time=0.8)
        note = self.t("amount exists for this call.   self.energy belongs to the robot.", 24, BOLD).move_to(DOWN * 3.12)
        self.fit(note, 12.7, 0.48)
        self.play(Write(note), run_time=0.9)
        self.wait(4.0)
        self.clear_content_keep_header()

    # ------------------------------------------------------------------
    # CHAPTER 06 — one class, three objects
    # ------------------------------------------------------------------
    def chapter_06_three_objects(self):
        self.set_header(6, "ONE CLASS, THREE VALID OBJECTS", "The same constructor can initialize many independent objects.")

        uml = self.make_uml_class(
            "Robot", ["name: str", "energy: int", "position: int"],
            ["Robot(name, energy, position)", "move()", "recharge(amount)"],
            width=3.85, height=3.70, font_size=19,
        ).move_to(LEFT * 5.35 + DOWN * 0.15)
        gate = self.make_constructor_gate("Robot(...)", "SAME CONSTRUCTOR", 2.35, 1.35).move_to(LEFT * 1.55 + DOWN * 0.15)
        cards = VGroup(
            self.make_object_card("atlas", "Atlas", 90, 0, 2.85, 2.00),
            self.make_object_card("explorer", "Explorer", 80, 10, 2.85, 2.00),
            self.make_object_card("courier", "Courier", 65, -4, 2.85, 2.00),
        ).arrange(DOWN, buff=0.23).move_to(RIGHT * 4.45 + DOWN * 0.18)
        a = Arrow(uml.get_right(), gate.get_left(), buff=0.20, stroke_width=1.5, max_tip_length_to_length_ratio=0.10)
        self.play(FadeIn(uml), Create(a), FadeIn(gate), run_time=1.0)
        self.wait(2.0)

        calls = [
            'Robot("Atlas", 90, 0)',
            'Robot("Explorer", 80, 10)',
            'Robot("Courier", 65, -4)',
        ]
        for i, (call, card) in enumerate(zip(calls, cards)):
            token = self.label_box(call, width=3.95, height=0.60, size=19, fill=WHITE).move_to(LEFT * 1.55 + UP * 2.00)
            self.play(FadeIn(token), run_time=0.55)
            self.play(token.animate.move_to(gate), run_time=0.85)
            self.play(FadeOut(token), FadeIn(card, shift=LEFT * 0.18), run_time=0.75)
            self.wait(1.2)

        slogan = self.t("SAME CLASS.   SAME CONSTRUCTOR.   DIFFERENT STATE.", 28, BOLD).move_to(DOWN * 3.15)
        self.fit(slogan, 13.2, 0.52)
        self.play(Write(slogan), run_time=1.0)
        self.wait(4.2)
        self.clear_content_keep_header()

    # ------------------------------------------------------------------
    # CHAPTER 07 — valid initial state
    # ------------------------------------------------------------------
    def chapter_07_valid_state(self):
        self.set_header(7, "VALID INITIAL STATE", "Reject an impossible beginning before the object enters the program.")

        bad_call = self.code_t('scout = Robot("Scout", -25, 0)', 28, BOLD).move_to(UP * 2.05)
        self.play(Write(bad_call), run_time=0.85)
        self.wait(1.8)

        bad_tokens = VGroup(
            self.make_argument_token('"Scout"', 1.65),
            self.make_argument_token("-25", 1.35),
            self.make_argument_token("0", 1.25),
        ).arrange(RIGHT, buff=0.22).move_to(LEFT * 4.6 + UP * 0.15)
        gate = self.make_constructor_gate("Robot(...)", "VALIDATION GATE", 2.65, 1.45).move_to(DOWN * 0.05)
        robot = self.make_robot("Scout", 0.72).move_to(RIGHT * 4.35 + DOWN * 0.10)
        arrow1 = Arrow(bad_tokens.get_right(), gate.get_left(), buff=0.18, stroke_width=1.6, max_tip_length_to_length_ratio=0.10)
        arrow2 = Arrow(gate.get_right(), robot.get_left(), buff=0.20, stroke_width=1.6, max_tip_length_to_length_ratio=0.10)
        self.play(FadeIn(bad_tokens), FadeIn(gate), Create(arrow1), Create(arrow2), run_time=1.0)
        self.wait(2.0)
        self.play(Indicate(bad_tokens[1], scale_factor=1.10, color=MID_GRAY), run_time=1.0)
        reject = self.label_box("INVALID INITIAL STATE", width=3.4, height=0.62, size=20, bold=True).move_to(RIGHT * 4.35 + UP * 1.35)
        cross = Cross(robot, stroke_color=BLACK_TEXT, stroke_width=3.0)
        self.play(FadeIn(reject), Create(cross), run_time=0.9)
        self.wait(3.0)

        code_panel, _ = self.make_code_panel([
            "if energy < 0 or energy > 100:",
            '    raise ValueError("energy must be between 0 and 100")',
        ], width=9.25, font_size=22, title="DOMAIN RULE FOR Robot")
        code_panel.move_to(DOWN * 2.25)
        self.play(FadeIn(code_panel), run_time=0.9)
        self.wait(3.5)

        self.play(FadeOut(cross), FadeOut(reject), FadeOut(bad_tokens), run_time=0.7)
        good = VGroup(
            self.make_argument_token('"Scout"', 1.65),
            self.make_argument_token("85", 1.35),
            self.make_argument_token("0", 1.25),
        ).arrange(RIGHT, buff=0.22).move_to(LEFT * 4.6 + UP * 0.15)
        self.play(FadeIn(good), run_time=0.6)
        self.play(good.animate.move_to(gate), run_time=0.9)
        self.play(FadeOut(good), FadeIn(robot, shift=RIGHT * 0.15), run_time=0.8)
        concept = self.t("VALIDATE EARLY  →  VALID OBJECT", 30, BOLD).move_to(UP * 2.05)
        self.play(Write(concept), run_time=0.9)
        self.wait(4.0)
        self.clear_content_keep_header()

    # ------------------------------------------------------------------
    # CHAPTER 08 — constructor vs method
    # ------------------------------------------------------------------
    def chapter_08_constructor_vs_method(self):
        self.set_header(8, "CONSTRUCTOR VS METHOD", "Initialization happens at creation; methods express behavior afterward.")

        line = Arrow(LEFT * 5.7, RIGHT * 5.7, buff=0, stroke_width=1.8, max_tip_length_to_length_ratio=0.025).move_to(DOWN * 0.10)
        create_lab = self.t("CREATE", 27, BOLD).move_to(LEFT * 4.9 + UP * 1.25)
        use_lab = self.t("USE OBJECT", 27, BOLD).move_to(RIGHT * 3.6 + UP * 1.25)
        init_tag = self.label_box("__init__()", width=2.0, height=0.58, size=21, bold=True).move_to(LEFT * 4.4 + DOWN * 0.10)
        move_tag = self.label_box("move()", width=1.75, height=0.58, size=21, bold=True).move_to(RIGHT * 1.1 + DOWN * 0.10)
        recharge_tag = self.label_box("recharge(5)", width=2.35, height=0.58, size=20, bold=True).move_to(RIGHT * 4.45 + DOWN * 0.10)
        self.play(Create(line), FadeIn(create_lab), FadeIn(use_lab), FadeIn(init_tag), FadeIn(move_tag), FadeIn(recharge_tag), run_time=1.0)
        self.wait(2.4)

        call1 = self.code_t('atlas = Robot("Atlas", 90, 0)', 28, BOLD).move_to(LEFT * 4.4 + UP * 2.15)
        call2 = self.code_t("atlas.move()", 27).move_to(RIGHT * 1.1 + DOWN * 1.35)
        call3 = self.code_t("atlas.recharge(5)", 27).move_to(RIGHT * 4.45 + DOWN * 2.15)
        self.play(Write(call1), Indicate(init_tag, color=MID_GRAY), run_time=1.0)
        self.wait(2.0)
        self.play(Write(call2), Indicate(move_tag, color=MID_GRAY), run_time=0.9)
        self.wait(1.8)
        self.play(Write(call3), Indicate(recharge_tag, color=MID_GRAY), run_time=0.9)
        self.wait(2.2)

        compare = VGroup(
            self.label_box("CONSTRUCTOR", 2.65, 0.62, 21, True),
            self.t("initial state", 22, color=DARK_GRAY),
            self.label_box("METHOD", 2.2, 0.62, 21, True),
            self.t("behavior after creation", 22, color=DARK_GRAY),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.55, 0.35)).move_to(DOWN * 2.80)
        self.play(FadeIn(compare), run_time=0.9)
        self.wait(3.7)
        exact = self.t("When Robot(...) is instantiated, Python creates the instance and __init__ initializes it.", 21, BOLD).move_to(UP * 2.82)
        self.fit(exact, 13.8, 0.42)
        self.play(FadeIn(exact), run_time=0.8)
        self.wait(3.5)
        self.clear_content_keep_header()

    # ------------------------------------------------------------------
    # CHAPTER 09 — UML ↔ code synchronization
    # ------------------------------------------------------------------
    def chapter_09_uml_sync(self):
        self.set_header(9, "UML ↔ CODE SYNCHRONIZATION", "The model and the implementation must describe the same initialization story.")

        uml = self.make_uml_class(
            "Robot",
            ["name: str", "energy: int", "position: int"],
            ["+ Robot(name, energy, position)", "+ move()", "+ recharge(amount)"],
            width=5.35, height=4.25, font_size=21,
        ).move_to(LEFT * 4.35 + DOWN * 0.35)
        code, lines = self.make_code_panel([
            "class Robot:",
            "    def __init__(self, name, energy, position):",
            "        self.name = name",
            "        self.energy = energy",
            "        self.position = position",
        ], width=7.85, font_size=22, title="PYTHON")
        code.move_to(RIGHT * 3.55 + DOWN * 0.35)
        self.play(FadeIn(uml), FadeIn(code), run_time=1.0)
        self.wait(2.8)

        mappings = [
            ("Robot(name, energy, position)", "__init__(self, name, energy, position)"),
            ("name", "self.name"),
            ("energy", "self.energy"),
            ("position", "self.position"),
        ]
        y = 2.0
        mapping_group = VGroup()
        for left, right in mappings:
            pair = VGroup(
                self.code_t(left, 18),
                Arrow(LEFT, RIGHT, buff=0, stroke_width=1.1, max_tip_length_to_length_ratio=0.12).set_length(0.55),
                self.code_t(right, 18),
            ).arrange(RIGHT, buff=0.14)
            if pair.width > 7.1:
                pair.scale_to_fit_width(7.1)
            pair.move_to(UP * y)
            y -= 0.52
            mapping_group.add(pair)
        mapping_group.move_to(DOWN * 2.80)
        self.play(FadeIn(mapping_group), run_time=1.0)
        self.wait(3.4)
        msg = self.t("MODEL AND CODE MUST TELL THE SAME STORY.", 30, BOLD).move_to(UP * 2.35)
        self.play(Write(msg), run_time=0.9)
        self.wait(4.0)
        self.clear_content_keep_header()

    # ------------------------------------------------------------------
    # CHAPTER 10 — transfer to repository m09 · V2.1 overlap-safe rebuild
    # ------------------------------------------------------------------
    def chapter_10_m09_transfer(self):
        self.set_header(
            10,
            "M09 · CONSTRUCTORS, ATTRIBUTES & METHODS",
            "Transfer the same mental model to the real technical module: Medicion.",
        )

        # LEFT: persistent UML reference, enlarged slightly for classroom readability.
        uml = self.make_uml_class(
            "Medicion",
            ["valor", "unidad"],
            ["Medicion(valor, unidad)", "escalar(factor)"],
            width=4.15,
            height=3.65,
            font_size=22,
        ).move_to(LEFT * 5.20 + DOWN * 0.20)

        # STAGE A — constructor only. Never mix constructor, method and usage in one panel.
        ctor, _ = self.make_code_panel(
            [
                "class Medicion:",
                "    def __init__(self, valor, unidad):",
                "        self.valor = valor",
                "        self.unidad = unidad",
            ],
            width=8.20,
            font_size=23,
            title="M09 · CONSTRUCTOR",
            padding=0.34,
        )
        ctor.move_to(RIGHT * 2.95 + UP * 0.78)

        self.play(FadeIn(uml), FadeIn(ctor), run_time=1.0)
        self.wait(2.8)

        flow1 = VGroup(
            self.make_argument_token("12", 1.20),
            self.t("→", 25, BOLD),
            self.code_t("valor", 23),
            self.t("→", 25, BOLD),
            self.code_t("self.valor", 23, BOLD),
        ).arrange(RIGHT, buff=0.20).move_to(RIGHT * 2.65 + DOWN * 1.20)

        flow2 = VGroup(
            self.make_argument_token('"C"', 1.20),
            self.t("→", 25, BOLD),
            self.code_t("unidad", 23),
            self.t("→", 25, BOLD),
            self.code_t("self.unidad", 23, BOLD),
        ).arrange(RIGHT, buff=0.20).move_to(RIGHT * 2.65 + DOWN * 2.05)

        self.play(FadeIn(flow1), FadeIn(flow2), run_time=0.9)
        self.wait(3.2)

        # STAGE B — method + usage in separate panels with explicit vertical separation.
        self.play(FadeOut(ctor), FadeOut(flow1), FadeOut(flow2), run_time=0.65)

        method_panel, _ = self.make_code_panel(
            [
                "def escalar(self, factor):",
                "    return self.valor * factor",
            ],
            width=7.65,
            font_size=24,
            title="METHOD",
            padding=0.36,
        )
        method_panel.move_to(RIGHT * 3.10 + UP * 0.90)

        usage_panel, _ = self.make_code_panel(
            [
                'm = Medicion(12, "C")',
                "print(m.escalar(2))",
            ],
            width=6.90,
            font_size=24,
            title="USAGE",
            padding=0.34,
        )
        usage_panel.move_to(RIGHT * 3.10 + DOWN * 1.20)

        self.play(FadeIn(method_panel), FadeIn(usage_panel), run_time=0.9)
        self.wait(2.8)

        factor = self.make_argument_token("factor = 2", 2.15).move_to(RIGHT * 0.30 + DOWN * 2.62)
        call = self.label_box("m.escalar(2)", 2.55, 0.62, 21, True).move_to(RIGHT * 3.10 + DOWN * 2.62)
        temp_note = self.t(
            "temporary parameter for this call",
            21,
            color=DARK_GRAY,
        ).move_to(RIGHT * 5.80 + DOWN * 2.62)
        self.fit(temp_note, 3.15, 0.42)

        self.play(FadeIn(factor), FadeIn(call), FadeIn(temp_note), run_time=0.8)
        self.wait(2.0)
        self.play(factor.animate.move_to(call), run_time=0.85)
        self.play(FadeOut(factor), Indicate(method_panel, color=MID_GRAY), run_time=0.65)
        self.wait(2.4)

        # STAGE C — clear explanatory canvas before the conceptual check.
        self.play(
            FadeOut(uml),
            FadeOut(method_panel),
            FadeOut(usage_panel),
            FadeOut(call),
            FadeOut(temp_note),
            run_time=0.75,
        )

        state_box = self.label_box(
            "OBJECT STATE",
            width=3.15,
            height=0.68,
            size=24,
            bold=True,
        ).move_to(LEFT * 3.55 + UP * 0.60)
        state_values = VGroup(
            self.code_t("self.valor", 28, BOLD),
            self.code_t("self.unidad", 28, BOLD),
        ).arrange(DOWN, buff=0.34).next_to(state_box, DOWN, buff=0.45)

        temp_box = self.label_box(
            "METHOD PARAMETER",
            width=3.75,
            height=0.68,
            size=24,
            bold=True,
        ).move_to(RIGHT * 3.55 + UP * 0.60)
        temp_value = self.code_t("factor", 30, BOLD).next_to(temp_box, DOWN, buff=0.60)

        divider = Line(UP * 1.65, DOWN * 1.65, stroke_color=LIGHT_GRAY, stroke_width=1.5)

        self.play(
            FadeIn(state_box),
            FadeIn(state_values),
            Create(divider),
            FadeIn(temp_box),
            FadeIn(temp_value),
            run_time=1.0,
        )
        self.wait(2.8)

        qa = self.t(
            "State stays with the object. A method parameter exists only during the call.",
            27,
            BOLD,
        ).move_to(DOWN * 2.75)
        self.fit(qa, 13.25, 0.55)
        self.play(Write(qa), run_time=0.9)
        self.wait(4.3)
        self.clear_content_keep_header()

    # ------------------------------------------------------------------
    # CHAPTER 11 — exit challenge
    # ------------------------------------------------------------------
    def chapter_11_exit_challenge(self):
        self.set_header(11, "EXIT CHALLENGE", "Predict first. Then reveal the answer from the object model.")

        code, _ = self.make_code_panel([
            "class Sensor:",
            "    def __init__(self, name, value):",
            "        self.name = name",
            "        self.value = value",
            "",
            "    def calibrate(self, offset):",
            "        return self.value + offset",
            "",
            'sensor = Sensor("S1", 12.5)',
        ], width=7.2, font_size=18, title="SENSOR")
        code.move_to(LEFT * 3.9 + DOWN * 0.35)
        self.play(FadeIn(code), run_time=1.0)
        self.wait(2.4)

        q_center = RIGHT * 3.85 + DOWN * 0.30
        questions = [
            ("A · Which values are constructor arguments?", '"S1"   and   12.5'),
            ("B · Which values become object state?", "self.name   and   self.value"),
            ("C · Which variable is temporary in calibrate()?", "offset"),
            ("D · a, b, c created from Sensor: how many objects?", "3 OBJECTS · 1 CLASS"),
            ("E · Should Sensor(\"Broken\", -999999) be accepted?", "Only if the domain rule says that value is invalid."),
        ]
        panel = None
        for i, (q, ans) in enumerate(questions):
            new_panel = self.make_question_panel(q, width=7.35).move_to(q_center)
            if panel is None:
                self.play(FadeIn(new_panel), run_time=0.75)
            else:
                self.play(ReplacementTransform(panel, new_panel), run_time=0.65)
            panel = new_panel
            self.wait(2.8 if i < 4 else 3.6)
            answer = self.t(ans, 25, BOLD, color=DARK_GRAY).next_to(panel, DOWN, buff=0.35)
            self.fit(answer, 6.8, 0.65)
            self.play(FadeIn(answer), run_time=0.65)
            self.wait(2.2 if i < 4 else 3.0)
            self.play(FadeOut(answer), run_time=0.45)

        domain = self.t("VALIDITY DEPENDS ON THE DOMAIN RULE.", 27, BOLD).move_to(DOWN * 3.20)
        self.fit(domain, 8.0, 0.50)
        self.play(Write(domain), run_time=0.85)
        self.wait(4.0)
        self.clear_content_keep_header()

    # ------------------------------------------------------------------
    # CHAPTER 12 — synthesis + bridge to class 04
    # ------------------------------------------------------------------
    def chapter_12_final_synthesis(self):
        self.set_header(12, "FINAL SYNTHESIS", "A valid object begins with coherent state and is then ready to behave.")

        labels = ["CLASS", "ARGUMENTS", "CONSTRUCTOR", "INITIAL STATE", "VALID OBJECT", "METHODS / BEHAVIOR"]
        nodes = VGroup(*[self.label_box(x, width=3.25 if i in (2, 5) else 2.75, height=0.60, size=21, bold=True) for i, x in enumerate(labels)])
        arrows = VGroup()
        flow = VGroup()
        for i, node in enumerate(nodes):
            flow.add(node)
            if i < len(nodes) - 1:
                flow.add(Arrow(UP * 0.22, DOWN * 0.22, buff=0, stroke_width=1.3, max_tip_length_to_length_ratio=0.13))
        flow.arrange(DOWN, buff=0.12).move_to(LEFT * 3.7 + DOWN * 0.25)
        if flow.height > 5.4:
            flow.scale_to_fit_height(5.4)
        self.play(FadeIn(flow), run_time=1.0)
        self.wait(3.0)

        compact = VGroup(
            self.label_box("Robot", 2.0, 0.60, 23, True),
            Arrow(LEFT, RIGHT, buff=0, stroke_width=1.5, max_tip_length_to_length_ratio=0.11).set_length(0.75),
            self.label_box('Robot("Atlas", 90, 0)', 3.7, 0.60, 19, True),
            Arrow(LEFT, RIGHT, buff=0, stroke_width=1.5, max_tip_length_to_length_ratio=0.11).set_length(0.75),
            self.make_robot("Atlas", 0.62),
        ).arrange(RIGHT, buff=0.28).move_to(RIGHT * 2.4 + UP * 0.80)
        self.play(FadeIn(compact), run_time=1.0)
        self.wait(3.0)

        three = VGroup(
            self.t("A CLASS DEFINES THE STRUCTURE.", 27, BOLD),
            self.t("A CONSTRUCTOR INITIALIZES EACH OBJECT.", 27, BOLD),
            self.t("EACH OBJECT OWNS ITS OWN STATE.", 27, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to(RIGHT * 2.75 + DOWN * 1.65)
        self.fit(three, 7.9, 1.5)
        self.play(FadeIn(three), run_time=0.9)
        self.wait(3.8)

        self.clear_content_keep_header(rt=0.85)
        atlas = self.make_robot("Atlas", 0.88).move_to(UP * 0.15)
        main = self.t("GIVE EVERY OBJECT A VALID BEGINNING.", 37, BOLD).move_to(DOWN * 2.10)
        sub = self.t("CLASS 03 · CONSTRUCTORS & VALID STATE", 20, color=DARK_GRAY).next_to(main, DOWN, buff=0.18)
        self.play(FadeIn(atlas), Write(main), FadeIn(sub), run_time=1.2)
        self.wait(5.0)

        teaser_q = self.t("IF AN OBJECT BEGINS VALID... WHO SHOULD BE ALLOWED TO CHANGE ITS STATE?", 25, BOLD).move_to(UP * 2.25)
        self.fit(teaser_q, 13.2, 0.50)
        next_box = self.label_box("NEXT: ENCAPSULATION & VISIBILITY", width=5.4, height=0.67, size=22, bold=True).move_to(DOWN * 3.15)
        self.play(FadeIn(teaser_q), FadeIn(next_box), run_time=1.0)
        self.wait(4.6)
        self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=1.1)
        self.wait(0.8)