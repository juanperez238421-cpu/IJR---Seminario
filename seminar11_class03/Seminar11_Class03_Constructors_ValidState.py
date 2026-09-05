#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Seminar 11 · Class 03 · Constructors & Valid State.

Senior ManimCE lesson for the OOP + UML Common Core.
Continuity contract: the previous class ended with
"MODEL THE WORLD. GIVE EACH OBJECT A RESPONSIBILITY."
This class answers the next question: how does a valid object begin its life?

Curriculum lock:
- constructors initialize required state
- parameters communicate what an object needs to exist
- Python __init__ + self + instance attributes
- early validation rejects impossible initial state
- one class creates many independent valid objects
- UML constructor signature must match implementation
- m09 transfer: Medicion(valor, unidad), self.valor vs method parameter factor

Target: ManimCE 0.20.1 · 1920x1080 · 30 fps · white background.
"""

from __future__ import annotations

from dataclasses import dataclass

from jp_classroom_style import *


@dataclass(frozen=True)
class RobotData:
    variable: str
    name: str
    energy: int
    position: int


ROBOTS = (
    RobotData("atlas", "Atlas", 90, 0),
    RobotData("explorer", "Explorer", 75, 4),
    RobotData("courier", "Courier", 60, 10),
)


class Seminar11Class03ConstructorsValidState(JPClassroomScene):
    """Problem -> constructor -> parameters -> self -> validation -> objects -> UML -> transfer."""

    # ------------------------------------------------------------------
    # Lesson data / guardrails
    # ------------------------------------------------------------------
    def validate_lesson_data(self) -> None:
        assert len(ROBOTS) == 3
        assert [r.variable for r in ROBOTS] == ["atlas", "explorer", "courier"]
        assert [r.energy for r in ROBOTS] == [90, 75, 60]
        assert all(0 <= r.energy <= 100 for r in ROBOTS)
        assert 12 * 2 == 24

    # ------------------------------------------------------------------
    # Reusable visual helpers
    # ------------------------------------------------------------------
    def mono(self, content: str, size: int = 25, weight=NORMAL) -> Text:
        return Text(content, font="DejaVu Sans Mono", font_size=size, color=BLACK_TEXT, weight=weight)

    def tag(self, label: str, width: float = 2.0, height: float = 0.52, size: int = 20, *, filled: bool = False) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.09,
            stroke_color=BLACK_LINE,
            stroke_width=1.8,
            fill_color=VERY_LIGHT_GRAY if filled else WHITE,
            fill_opacity=1,
        )
        txt = self.text(label, size, BOLD if filled else MEDIUM)
        self.fit(txt, width - 0.20, height - 0.12)
        txt.move_to(box)
        return VGroup(box, txt)

    def concept_arrow(self, start, end, *, width: float = 1.7) -> Arrow:
        return Arrow(
            start,
            end,
            buff=0.10,
            color=BLACK_LINE,
            stroke_width=width,
            max_tip_length_to_length_ratio=0.14,
        )

    def state_row(self, label: str, value: str, *, width: float = 3.45, size: int = 21) -> VGroup:
        left = self.text(label, size, MEDIUM)
        right = self.mono(value, size)
        row = VGroup(left, right).arrange(RIGHT, buff=0.22)
        if row.width > width:
            row.scale_to_fit_width(width)
        return row

    def object_card(
        self,
        variable: str,
        name: str,
        energy: str | int,
        position: str | int,
        *,
        width: float = 3.65,
        height: float = 2.55,
        compact: bool = False,
    ) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.8,
            fill_color=WHITE,
            fill_opacity=1,
        )
        title = self.text(f"{variable} : Robot", 22 if not compact else 19, BOLD)
        divider = Line(LEFT * (width / 2 - 0.22), RIGHT * (width / 2 - 0.22), color=LIGHT_GRAY, stroke_width=1.4)
        rows = VGroup(
            self.state_row("name =", f'"{name}"' if name != "?" else "?", width=width - 0.55, size=20 if not compact else 17),
            self.state_row("energy =", str(energy), width=width - 0.55, size=20 if not compact else 17),
            self.state_row("position =", str(position), width=width - 0.55, size=20 if not compact else 17),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12 if not compact else 0.08)
        content = VGroup(title, divider, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.17 if not compact else 0.11)
        self.fit(content, width - 0.42, height - 0.34)
        content.move_to(box)
        return VGroup(box, content)

    def measurement_card(self, *, width: float = 3.75, height: float = 2.05) -> VGroup:
        box = RoundedRectangle(width=width, height=height, corner_radius=0.12, stroke_color=BLACK_LINE, stroke_width=1.8, fill_color=WHITE, fill_opacity=1)
        title = self.text("m : Medicion", 22, BOLD)
        divider = Line(LEFT * (width / 2 - 0.22), RIGHT * (width / 2 - 0.22), color=LIGHT_GRAY, stroke_width=1.4)
        rows = VGroup(
            self.state_row("valor =", "12", width=width - 0.55, size=20),
            self.state_row("unidad =", '"C"', width=width - 0.55, size=20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.13)
        content = VGroup(title, divider, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        content.move_to(box)
        return VGroup(box, content)

    def robot_icon(self, label: str = "Atlas", energy: int | None = 90, *, scale: float = 1.0, incomplete: bool = False) -> VGroup:
        head = RoundedRectangle(width=1.45, height=0.88, corner_radius=0.15, stroke_color=BLACK_LINE, stroke_width=2.0, fill_color=WHITE, fill_opacity=1)
        eye_l = Dot(radius=0.055, color=BLACK_LINE).move_to(head.get_center() + LEFT * 0.35)
        eye_r = Dot(radius=0.055, color=BLACK_LINE).move_to(head.get_center() + RIGHT * 0.35)
        antenna = Line(head.get_top(), head.get_top() + UP * 0.30, color=BLACK_LINE, stroke_width=1.8)
        tip = Dot(radius=0.055, color=BLACK_LINE).move_to(antenna.get_end())
        body = RoundedRectangle(width=1.75, height=1.35, corner_radius=0.12, stroke_color=BLACK_LINE, stroke_width=2.0, fill_color=WHITE, fill_opacity=1).next_to(head, DOWN, buff=0.12)
        arm_l = Line(body.get_left() + UP * 0.20, body.get_left() + LEFT * 0.48 + DOWN * 0.10, color=BLACK_LINE, stroke_width=2.0)
        arm_r = Line(body.get_right() + UP * 0.20, body.get_right() + RIGHT * 0.48 + DOWN * 0.10, color=BLACK_LINE, stroke_width=2.0)
        leg_l = Line(body.get_bottom() + LEFT * 0.42, body.get_bottom() + LEFT * 0.42 + DOWN * 0.48, color=BLACK_LINE, stroke_width=2.0)
        leg_r = Line(body.get_bottom() + RIGHT * 0.42, body.get_bottom() + RIGHT * 0.42 + DOWN * 0.48, color=BLACK_LINE, stroke_width=2.0)
        name_text = self.text("?" if incomplete else label, 18, BOLD).move_to(head.get_center() + DOWN * 0.02)
        battery_box = RoundedRectangle(width=1.10, height=0.42, corner_radius=0.06, stroke_color=BLACK_LINE, stroke_width=1.5, fill_color=WHITE, fill_opacity=1).move_to(body.get_center() + UP * 0.13)
        battery_text = self.text("?" if incomplete or energy is None else f"{energy}%", 16, BOLD).move_to(battery_box)
        pos_text = self.text("position: ?" if incomplete else "position: 0", 15).move_to(body.get_center() + DOWN * 0.39)
        group = VGroup(head, eye_l, eye_r, antenna, tip, body, arm_l, arm_r, leg_l, leg_r, name_text, battery_box, battery_text, pos_text)
        group.scale(scale)
        return group

    def validation_gate(self, *, width: float = 2.85, height: float = 2.10) -> VGroup:
        box = RoundedRectangle(width=width, height=height, corner_radius=0.14, stroke_color=BLACK_LINE, stroke_width=2.1, fill_color=VERY_LIGHT_GRAY, fill_opacity=1)
        title = self.text("VALIDATION", 24, BOLD)
        rule = self.mono("0 <= energy <= 100", 18)
        content = VGroup(title, rule).arrange(DOWN, buff=0.20).move_to(box)
        return VGroup(box, content)

    def uml_robot(self, *, include_constructor: bool = True, width: float = 5.15, height: float = 4.05) -> VGroup:
        box = Rectangle(width=width, height=height, stroke_color=BLACK_LINE, stroke_width=1.8, fill_color=WHITE, fill_opacity=1)
        top_y = box.get_top()[1]
        bottom_y = box.get_bottom()[1]
        left_x = box.get_left()[0]
        right_x = box.get_right()[0]
        y1 = top_y - 0.78
        y2 = top_y - 2.30
        d1 = Line([left_x, y1, 0], [right_x, y1, 0], color=BLACK_LINE, stroke_width=1.4)
        d2 = Line([left_x, y2, 0], [right_x, y2, 0], color=BLACK_LINE, stroke_width=1.4)
        title = self.text("Robot", 28, BOLD).move_to([0, (top_y + y1) / 2, 0])
        attrs = VGroup(
            self.text("- name: String", 21),
            self.text("- energy: int", 21),
            self.text("- position: int", 21),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        attrs.move_to([left_x + 0.35 + attrs.width / 2, (y1 + y2) / 2, 0])
        op_lines = []
        if include_constructor:
            op_lines.append(self.text("+ Robot(name, energy, position)", 20, BOLD))
        op_lines.extend([
            self.text("+ move(step): void", 20),
            self.text("+ recharge(amount): void", 20),
        ])
        ops = VGroup(*op_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        ops.move_to([left_x + 0.35 + ops.width / 2, (y2 + bottom_y) / 2, 0])
        return VGroup(box, d1, d2, title, attrs, ops)

    def code_panel(self, lines: list[str], *, width: float = 7.2, height: float = 4.15, font_size: int = 24, title: str | None = None) -> tuple[VGroup, VGroup]:
        box = RoundedRectangle(width=width, height=height, corner_radius=0.12, stroke_color=BLACK_LINE, stroke_width=1.7, fill_color=PAPER_GRAY, fill_opacity=1)
        line_mobs = VGroup(*[self.mono(line, font_size) for line in lines])
        line_mobs.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        if title:
            title_mob = self.text(title, 19, BOLD)
            title_mob.next_to(box.get_top(), DOWN, buff=0.18).align_to(box, LEFT).shift(RIGHT * 0.28)
            self.fit(line_mobs, width - 0.55, height - 1.00)
            line_mobs.next_to(title_mob, DOWN, buff=0.22).align_to(title_mob, LEFT)
            return VGroup(box, title_mob, line_mobs), line_mobs
        self.fit(line_mobs, width - 0.55, height - 0.44)
        line_mobs.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.28)
        return VGroup(box, line_mobs), line_mobs

    def safe_fade(self, *mobs: Mobject, run_time: float = RUN_NORMAL) -> None:
        items = [mob for mob in mobs if mob is not None]
        if items:
            self.play(*[FadeOut(mob) for mob in items], run_time=run_time)

    def clear_scene(self) -> None:
        self.clear_stage()

    # ------------------------------------------------------------------
    # Orchestration
    # ------------------------------------------------------------------
    def construct(self) -> None:
        self.opening_00()
        self.scene_01_recall_atlas()
        self.scene_02_creation_problem()
        self.scene_03_constructor_model()
        self.scene_04_python_init()
        self.scene_05_self()
        self.scene_06_three_objects()
        self.scene_07_valid_state()
        self.scene_08_constructor_vs_method()
        self.scene_09_uml_sync()
        self.scene_10_medicion_transfer()
        self.scene_11_common_mistake()
        self.scene_12_exit_check()
        self.final_synthesis()

    # ------------------------------------------------------------------
    # 00 — opening continuity
    # ------------------------------------------------------------------
    def opening_00(self) -> None:
        callback = VGroup(
            self.text("MODEL THE WORLD.", 44, BOLD),
            self.text("GIVE EACH OBJECT A RESPONSIBILITY.", 38, BOLD),
        ).arrange(DOWN, buff=0.20).move_to(UP * 0.35)
        self.fit(callback, 13.8, 2.0)
        self.play(FadeIn(callback, shift=UP * 0.10), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)

        but = self.text("BUT...", 30, BOLD).move_to(UP * 1.45)
        question = VGroup(
            self.text("HOW DOES AN OBJECT", 44, BOLD),
            self.text("BEGIN ITS LIFE?", 44, BOLD),
        ).arrange(DOWN, buff=0.13).move_to(DOWN * 0.15)
        self.play(ReplacementTransform(callback, question), FadeIn(but), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.safe_fade(but, question)

        course = self.text("SEMINAR · GRADE 11", 25, BOLD).move_to(UP * 3.30)
        oop = self.text("OBJECT-ORIENTED PROGRAMMING", 24, MEDIUM).move_to(UP * 2.78)
        cls = self.tag("CLASS 03", 2.05, 0.60, 22, filled=True).move_to(UP * 1.95)
        title = self.text("CONSTRUCTORS & VALID STATE", 49, BOLD).move_to(UP * 0.85)
        subtitle = self.text("A good object is valid from the moment it exists.", 28).move_to(DOWN * 0.05)
        line = Line(LEFT * 5.8, RIGHT * 5.8, color=LIGHT_GRAY, stroke_width=2.0).move_to(DOWN * 0.70)
        core = VGroup(
            self.text("A CLASS defines what an object can be.", 25),
            self.text("A CONSTRUCTOR defines how that object begins.", 25, BOLD),
        ).arrange(DOWN, buff=0.18).move_to(DOWN * 1.55)
        self.assert_within_frame(VGroup(course, oop, cls, title, subtitle, line, core), "opening title")
        self.play(FadeIn(course), FadeIn(oop), run_time=RUN_NORMAL)
        self.play(FadeIn(cls, shift=UP * 0.08), Write(title), run_time=RUN_SLOW)
        self.play(FadeIn(subtitle), Create(line), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(core), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=RUN_NORMAL)

    # ------------------------------------------------------------------
    # 01 — recall Atlas
    # ------------------------------------------------------------------
    def scene_01_recall_atlas(self) -> None:
        self.set_header(1, "REMEMBER ATLAS", "A class defines the structure. An object carries its own state.")
        robot = self.robot_icon("Atlas", 90, scale=1.18).move_to(LEFT * 4.55 + DOWN * 0.05)
        atlas_label = self.text("Atlas", 25, BOLD).next_to(robot, DOWN, buff=0.30)
        card = self.object_card("atlas", "Atlas", 90, 0, width=4.10, height=2.85).move_to(RIGHT * 2.65 + UP * 0.25)
        state_tag = self.tag("STATE", 1.55, 0.52, 20, filled=True).next_to(card, DOWN, buff=0.25)
        behavior = VGroup(self.tag("move()", 1.65, 0.52, 19), self.tag("recharge()", 2.10, 0.52, 19)).arrange(RIGHT, buff=0.20).next_to(state_tag, DOWN, buff=0.22)
        self.assert_content_safe(VGroup(robot, atlas_label, card, state_tag, behavior), "scene01")
        self.play(Create(robot), FadeIn(atlas_label), run_time=RUN_SLOW)
        self.play(FadeIn(card, shift=RIGHT * 0.12), run_time=RUN_NORMAL)
        self.play(FadeIn(state_tag), FadeIn(behavior), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        rows = card[1][2]
        for row in rows:
            self.play(Indicate(row, color=BLACK_LINE, scale_factor=1.04), run_time=RUN_QUICK)
        self.wait(PAUSE_READ)

        question = self.text("WHERE DID THESE INITIAL VALUES COME FROM?", 29, BOLD).move_to(DOWN * 2.75)
        values = VGroup(self.mono('"Atlas"', 28, BOLD), self.mono("90", 28, BOLD), self.mono("0", 28, BOLD)).arrange(RIGHT, buff=0.90).next_to(question, DOWN, buff=0.32)
        self.play(FadeIn(question), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[TransformFromCopy(row, val) for row, val in zip(rows, values)], lag_ratio=0.20), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 02 — empty-object problem
    # ------------------------------------------------------------------
    def scene_02_creation_problem(self) -> None:
        self.set_header(2, "AN OBJECT SHOULD NOT BE BORN EMPTY", "If data is required for the object to work, do not create it first and repair it later.")
        call = self.mono("atlas = Robot()", 31, BOLD).move_to(LEFT * 3.85 + UP * 1.65)
        robot = self.robot_icon("", None, scale=0.90, incomplete=True).move_to(LEFT * 4.20 + DOWN * 0.45)
        empty = self.object_card("atlas", "?", "?", "?", width=3.65, height=2.55).move_to(RIGHT * 3.40 + UP * 0.55)
        warn = self.tag("OBJECT EXISTS · STATE INCOMPLETE", 4.25, 0.58, 19, filled=True).next_to(empty, DOWN, buff=0.24)
        self.assert_content_safe(VGroup(call, robot, empty, warn), "scene02 initial")
        self.play(Write(call), run_time=RUN_NORMAL)
        self.play(FadeIn(robot), FadeIn(empty, shift=RIGHT * 0.10), run_time=RUN_NORMAL)
        self.play(FadeIn(warn), run_time=RUN_QUICK)
        self.wait(PAUSE_EXPLAIN)

        assigns = VGroup(
            self.mono('atlas.name = "Atlas"', 24),
            self.mono("atlas.energy = 90", 24),
            self.mono("atlas.position = 0", 24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to(LEFT * 3.50 + DOWN * 2.15)
        patched_cards = [
            self.object_card("atlas", "Atlas", "?", "?", width=3.65, height=2.55).move_to(empty),
            self.object_card("atlas", "Atlas", 90, "?", width=3.65, height=2.55).move_to(empty),
            self.object_card("atlas", "Atlas", 90, 0, width=3.65, height=2.55).move_to(empty),
        ]
        current = empty
        for line, next_card in zip(assigns, patched_cards):
            self.play(Write(line), ReplacementTransform(current, next_card), run_time=RUN_NORMAL)
            current = next_card
            self.wait(PAUSE_READ)
        self.safe_fade(warn)
        self.wait(PAUSE_READ)

        self.safe_fade(call, robot, assigns, current)
        flow = VGroup(
            self.tag("CREATE", 1.45, 0.55, 19), self.text("→", 27),
            self.tag("PATCH", 1.45, 0.55, 19), self.text("→", 27),
            self.tag("PATCH", 1.45, 0.55, 19), self.text("→", 27),
            self.tag("PATCH", 1.45, 0.55, 19), self.text("→", 27),
            self.tag("HOPE", 1.45, 0.55, 19, filled=True),
        ).arrange(RIGHT, buff=0.12).move_to(UP * 0.35)
        problem = VGroup(
            self.text("Between creation and the last assignment,", 27),
            self.text("the object is incomplete.", 30, BOLD),
        ).arrange(DOWN, buff=0.16).move_to(DOWN * 0.85)
        can_move = self.text("CAN THIS OBJECT SAFELY MOVE?", 28, BOLD).move_to(DOWN * 2.05)
        answer = self.tag("NOT YET", 2.00, 0.62, 22, filled=True).move_to(DOWN * 2.85)
        rule = self.text("WE NEED A CREATION RULE.", 31, BOLD).move_to(DOWN * 2.85)
        self.play(FadeIn(flow), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.play(FadeIn(problem), run_time=RUN_NORMAL)
        self.play(FadeIn(can_move), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(answer), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(ReplacementTransform(answer, rule), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 03 — constructor mental model
    # ------------------------------------------------------------------
    def scene_03_constructor_model(self) -> None:
        self.set_header(3, "THE CONSTRUCTOR DEFINES HOW AN OBJECT BEGINS", "Required input enters one creation rule and leaves as a ready object.")
        inputs_title = self.text("INPUT DATA", 22, BOLD).move_to(LEFT * 5.15 + UP * 1.55)
        inputs = VGroup(self.tag('"Atlas"', 1.70, 0.60, 22), self.tag("90", 1.35, 0.60, 22), self.tag("0", 1.35, 0.60, 22)).arrange(DOWN, buff=0.30).move_to(LEFT * 5.15 + DOWN * 0.05)
        gate = RoundedRectangle(width=3.25, height=2.60, corner_radius=0.15, stroke_color=BLACK_LINE, stroke_width=2.2, fill_color=VERY_LIGHT_GRAY, fill_opacity=1).move_to(ORIGIN + DOWN * 0.05)
        gate_text = VGroup(self.text("CONSTRUCTOR", 27, BOLD), self.mono("Robot(...)", 23)).arrange(DOWN, buff=0.22).move_to(gate)
        gate_group = VGroup(gate, gate_text)
        card = self.object_card("atlas", "Atlas", 90, 0, width=3.65, height=2.55).move_to(RIGHT * 4.55 + DOWN * 0.05)
        valid = self.tag("VALID OBJECT", 2.15, 0.56, 20, filled=True).next_to(card, DOWN, buff=0.24)
        arr_in = [self.concept_arrow(item.get_right(), gate.get_left() + UP * y, width=1.45) for item, y in zip(inputs, [0.60, 0.0, -0.60])]
        arr_out = self.concept_arrow(gate.get_right(), card.get_left(), width=1.9)
        self.assert_content_safe(VGroup(inputs_title, inputs, gate_group, card, valid, *arr_in, arr_out), "scene03")
        self.play(FadeIn(inputs_title), FadeIn(inputs), run_time=RUN_NORMAL)
        self.play(FadeIn(gate_group), run_time=RUN_NORMAL)
        for arrow, item in zip(arr_in, inputs):
            self.play(GrowArrow(arrow), TransformFromCopy(item, gate_text[1]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(GrowArrow(arr_out), FadeIn(card, shift=RIGHT * 0.10), run_time=RUN_NORMAL)
        self.play(FadeIn(valid), run_time=RUN_QUICK)
        self.wait(PAUSE_EXPLAIN)

        self.safe_fade(inputs_title, inputs, gate_group, card, valid, *arr_in, arr_out)
        pipeline = VGroup(
            self.tag("ARGUMENTS", 2.05, 0.62, 21),
            self.text("↓", 31),
            self.tag("CONSTRUCTOR", 2.35, 0.62, 21, filled=True),
            self.text("↓", 31),
            self.tag("INITIALIZATION", 2.55, 0.62, 21),
            self.text("↓", 31),
            self.tag("READY OBJECT", 2.25, 0.62, 21, filled=True),
        ).arrange(DOWN, buff=0.12).move_to(DOWN * 0.25)
        statement = self.text("OBJECT CREATION IS A PROCESS.", 30, BOLD).move_to(UP * 2.10)
        self.play(Write(statement), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(item, shift=UP * 0.06) for item in pipeline], lag_ratio=0.10), run_time=RUN_SLOW)
        self.wait(PAUSE_WORK)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 04 — Python __init__ and parameter -> attribute
    # ------------------------------------------------------------------
    def scene_04_python_init(self) -> None:
        self.set_header(4, "PYTHON: __init__ BUILDS THE INITIAL STATE", "Syntax now follows the mental model: receive required data, then store object state.")
        lines = [
            "class Robot:",
            "    def __init__(self, name, energy, position):",
            "        self.name = name",
            "        self.energy = energy",
            "        self.position = position",
        ]
        # Build a large projector-readable code panel and reveal it progressively.
        panel, code = self.code_panel(lines, width=8.60, height=4.35, font_size=25, title="PYTHON")
        panel.move_to(LEFT * 2.55 + DOWN * 0.15)
        for line in code:
            line.set_opacity(0)
        self.add(panel[0], panel[1], code)
        self.play(code[0].animate.set_opacity(1), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(code[1].animate.set_opacity(1), run_time=RUN_NORMAL)
        init_tag = self.tag("RUNS WHEN AN INSTANCE IS CREATED", 4.15, 0.58, 18, filled=True).move_to(RIGHT * 4.20 + UP * 1.05)
        params_tag = VGroup(
            self.text("name · energy · position", 23, BOLD),
            self.text("required creation information", 20),
        ).arrange(DOWN, buff=0.10).move_to(RIGHT * 4.20 + UP * 0.05)
        self.play(FadeIn(init_tag), run_time=RUN_NORMAL)
        self.play(FadeIn(params_tag), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)

        mapping_box = RoundedRectangle(width=4.35, height=2.65, corner_radius=0.12, stroke_color=BLACK_LINE, stroke_width=1.6, fill_color=WHITE, fill_opacity=1).move_to(RIGHT * 4.20 + DOWN * 1.85)
        left = VGroup(self.mono("name", 23, BOLD), self.text("PARAMETER", 18)).arrange(DOWN, buff=0.10).move_to(mapping_box.get_center() + LEFT * 1.20)
        right = VGroup(self.mono("self.name", 23, BOLD), self.text("OBJECT ATTRIBUTE", 18)).arrange(DOWN, buff=0.10).move_to(mapping_box.get_center() + RIGHT * 1.10)
        arrow = self.concept_arrow(left.get_right(), right.get_left(), width=1.7)
        self.play(FadeIn(mapping_box), FadeIn(left), FadeIn(right), GrowArrow(arrow), run_time=RUN_NORMAL)
        self.play(code[2].animate.set_opacity(1), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(code[3].animate.set_opacity(1), run_time=RUN_NORMAL)
        self.play(code[4].animate.set_opacity(1), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 05 — self means this object
    # ------------------------------------------------------------------
    def scene_05_self(self) -> None:
        self.set_header(5, "self MEANS ‘THIS OBJECT’", "The same constructor runs for different instances; self points to the instance being initialized.")
        calls = VGroup(
            self.mono('atlas = Robot("Atlas", 90, 0)', 23, BOLD),
            self.mono('explorer = Robot("Explorer", 75, 4)', 23),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to(UP * 1.70)
        class_box = RoundedRectangle(width=3.10, height=1.45, corner_radius=0.12, stroke_color=BLACK_LINE, stroke_width=1.8, fill_color=VERY_LIGHT_GRAY, fill_opacity=1).move_to(ORIGIN + UP * 0.25)
        class_text = VGroup(self.text("ROBOT CLASS", 22, BOLD), self.mono("same __init__", 20)).arrange(DOWN, buff=0.15).move_to(class_box)
        atlas = self.object_card("atlas", "Atlas", 90, 0, width=3.30, height=2.10, compact=True).move_to(LEFT * 3.55 + DOWN * 1.70)
        explorer = self.object_card("explorer", "Explorer", 75, 4, width=3.30, height=2.10, compact=True).move_to(RIGHT * 3.55 + DOWN * 1.70)
        a1 = self.concept_arrow(class_box.get_bottom() + LEFT * 0.55, atlas.get_top(), width=1.5)
        a2 = self.concept_arrow(class_box.get_bottom() + RIGHT * 0.55, explorer.get_top(), width=1.5)
        self.play(Write(calls[0]), run_time=RUN_NORMAL)
        self.play(FadeIn(class_box), FadeIn(class_text), run_time=RUN_NORMAL)
        self.play(GrowArrow(a1), FadeIn(atlas), run_time=RUN_NORMAL)
        self_tag = self.tag("self → atlas", 2.25, 0.56, 20, filled=True).next_to(atlas, UP, buff=0.18)
        self.play(FadeIn(self_tag), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        map_lines = VGroup(
            self.mono("self.name     → atlas.name", 20),
            self.mono("self.energy   → atlas.energy", 20),
            self.mono("self.position → atlas.position", 20),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.10).move_to(LEFT * 4.55 + DOWN * 3.15)
        self.play(FadeIn(map_lines), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)

        self.play(Write(calls[1]), run_time=RUN_NORMAL)
        self.play(GrowArrow(a2), FadeIn(explorer), run_time=RUN_NORMAL)
        self_tag_2 = self.tag("self → explorer", 2.45, 0.56, 20, filled=True).next_to(explorer, UP, buff=0.18)
        self.play(ReplacementTransform(self_tag, self_tag_2), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.safe_fade(map_lines)
        final = VGroup(self.text("SAME CREATION RULE.", 27, BOLD), self.text("DIFFERENT INITIAL STATE.", 27, BOLD)).arrange(DOWN, buff=0.10).move_to(DOWN * 3.05)
        self.play(FadeIn(final), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 06 — one class, three valid objects
    # ------------------------------------------------------------------
    def scene_06_three_objects(self) -> None:
        self.set_header(6, "ONE CLASS → MANY VALID OBJECTS", "The constructor states what every Robot needs; the arguments supply each object's initial state.")
        signature = self.tag("Robot(name, energy, position)", 4.65, 0.66, 22, filled=True).move_to(UP * 1.80)
        cards = VGroup(*[
            self.object_card(r.variable, r.name, r.energy, r.position, width=3.55, height=2.15, compact=True)
            for r in ROBOTS
        ]).arrange(RIGHT, buff=0.55).move_to(DOWN * 0.15)
        calls = VGroup(*[
            self.mono(f'{r.variable} = Robot("{r.name}", {r.energy}, {r.position})', 18)
            for r in ROBOTS
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to(DOWN * 2.65)
        self.play(FadeIn(signature), run_time=RUN_NORMAL)
        for call, card in zip(calls, cards):
            self.play(Write(call), run_time=RUN_NORMAL)
            self.play(FadeIn(card, shift=UP * 0.10), run_time=RUN_NORMAL)
            self.wait(PAUSE_READ)
        compare = VGroup(
            self.text("SAME CLASS", 25, BOLD),
            self.text("DIFFERENT IDENTITY + DIFFERENT STATE", 25, BOLD),
        ).arrange(DOWN, buff=0.10).move_to(DOWN * 3.55)
        self.play(FadeIn(compare), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 07 — initial-state validation
    # ------------------------------------------------------------------
    def scene_07_valid_state(self) -> None:
        self.set_header(7, "NOT EVERY INITIAL STATE SHOULD BE ALLOWED", "A constructor can reject impossible state before the object enters the system.")
        valid_call = self.mono('Robot("Atlas", 90, 0)', 29, BOLD).move_to(LEFT * 3.80 + UP * 1.70)
        valid_energy = self.tag("ENERGY = 90", 2.25, 0.60, 21).next_to(valid_call, DOWN, buff=0.32)
        valid_mark = self.text("VALID", 29, BOLD).next_to(valid_energy, DOWN, buff=0.25)
        self.play(Write(valid_call), FadeIn(valid_energy), FadeIn(valid_mark), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)

        invalid_call = self.mono('Robot("Scout", -25, 0)', 29, BOLD).move_to(RIGHT * 3.80 + UP * 1.70)
        invalid_energy = self.tag("ENERGY = -25", 2.35, 0.60, 21, filled=True).next_to(invalid_call, DOWN, buff=0.32)
        question = self.text("SHOULD THIS OBJECT EXIST?", 24, BOLD).next_to(invalid_energy, DOWN, buff=0.25)
        no = self.tag("NO", 1.20, 0.58, 22, filled=True).next_to(question, DOWN, buff=0.22)
        self.play(Write(invalid_call), FadeIn(invalid_energy), run_time=RUN_NORMAL)
        self.play(FadeIn(question), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(no), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.safe_fade(valid_call, valid_energy, valid_mark, invalid_call, invalid_energy, question, no)

        lines = [
            "class Robot:",
            "    def __init__(self, name, energy, position):",
            "        if energy < 0 or energy > 100:",
            "            raise ValueError(\"energy must be between 0 and 100\")",
            "        self.name = name",
            "        self.energy = energy",
            "        self.position = position",
        ]
        panel, code = self.code_panel(lines, width=8.10, height=4.90, font_size=20, title="EARLY VALIDATION")
        panel.move_to(LEFT * 3.50 + DOWN * 0.35)
        gate = self.validation_gate().move_to(RIGHT * 4.40 + UP * 0.20)
        bad = self.tag('Robot("Scout", -25, 0)', 3.35, 0.62, 18).next_to(gate, UP, buff=0.34)
        cross = self.text("REJECTED", 25, BOLD).next_to(gate, DOWN, buff=0.26)
        good = self.tag('Robot("Scout", 85, 0)', 3.25, 0.62, 18).move_to(RIGHT * 4.40 + DOWN * 2.65)
        created = self.tag("OBJECT CREATED", 2.55, 0.56, 19, filled=True).next_to(good, DOWN, buff=0.20)
        self.play(FadeIn(panel), run_time=RUN_NORMAL)
        self.play(Circumscribe(code[2], color=BLACK_LINE), Circumscribe(code[3], color=BLACK_LINE), run_time=RUN_SLOW)
        self.play(FadeIn(bad), FadeIn(gate), run_time=RUN_NORMAL)
        self.play(FadeIn(cross), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(good), FadeIn(created), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.safe_fade(good, created)
        message = self.text("THE CONSTRUCTOR PROTECTS THE INITIAL STATE.", 27, BOLD).move_to(DOWN * 3.35)
        self.play(FadeIn(message), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 08 — constructor vs method
    # ------------------------------------------------------------------
    def scene_08_constructor_vs_method(self) -> None:
        self.set_header(8, "CREATE FIRST. BEHAVE SECOND.", "A constructor establishes initial state; methods work with an object that already exists.")
        left = RoundedRectangle(width=6.05, height=4.60, corner_radius=0.13, stroke_color=BLACK_LINE, stroke_width=1.7, fill_color=WHITE, fill_opacity=1).move_to(LEFT * 3.35 + DOWN * 0.25)
        right = left.copy().move_to(RIGHT * 3.35 + DOWN * 0.25)
        ltitle = self.text("CREATION", 25, BOLD).next_to(left.get_top(), DOWN, buff=0.28)
        rtitle = self.text("BEHAVIOR", 25, BOLD).next_to(right.get_top(), DOWN, buff=0.28)
        lflow = VGroup(
            self.mono('Robot("Atlas", 90, 0)', 22), self.text("↓", 28), self.mono("__init__()", 23, BOLD), self.text("↓", 28), self.tag("atlas exists", 2.15, 0.58, 20, filled=True)
        ).arrange(DOWN, buff=0.14).move_to(left.get_center() + DOWN * 0.15)
        before = self.state_row("position =", "0", width=2.6, size=21)
        call = self.mono("atlas.move(3)", 22, BOLD)
        after = self.state_row("position =", "3", width=2.6, size=21)
        rflow = VGroup(before, self.text("↓", 28), call, self.text("↓", 28), after).arrange(DOWN, buff=0.15).move_to(right.get_center() + DOWN * 0.10)
        self.play(FadeIn(left), FadeIn(right), FadeIn(ltitle), FadeIn(rtitle), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(m) for m in lflow], lag_ratio=0.12), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.play(LaggedStart(*[FadeIn(m) for m in rflow], lag_ratio=0.12), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        timeline = VGroup(
            self.tag("CREATE OBJECT", 2.30, 0.56, 19), self.text("→", 27), self.tag("OBJECT EXISTS", 2.25, 0.56, 19, filled=True), self.text("→", 27), self.tag("CALL METHODS", 2.20, 0.56, 19), self.text("→", 27), self.tag("STATE CHANGES", 2.35, 0.56, 19)
        ).arrange(RIGHT, buff=0.13).move_to(DOWN * 3.45)
        self.play(FadeIn(timeline), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 09 — UML synchronization
    # ------------------------------------------------------------------
    def scene_09_uml_sync(self) -> None:
        self.set_header(9, "THE DESIGN MUST SHOW HOW OBJECTS ARE CREATED", "UML and code should tell the same initialization story.")
        uml_without = self.uml_robot(include_constructor=False).move_to(LEFT * 3.55 + DOWN * 0.10)
        uml_with = self.uml_robot(include_constructor=True).move_to(uml_without)
        self.play(FadeIn(uml_without), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(ReplacementTransform(uml_without, uml_with), run_time=RUN_SLOW)
        constructor_line = uml_with[5][0]
        constructor_tag = self.tag("CONSTRUCTOR", 1.95, 0.54, 19, filled=True).move_to(RIGHT * 1.15 + UP * 0.75)
        arrow = self.concept_arrow(constructor_tag.get_left(), constructor_line.get_right(), width=1.4)
        self.play(FadeIn(constructor_tag), GrowArrow(arrow), Circumscribe(constructor_line, color=BLACK_LINE), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)

        code_box = RoundedRectangle(width=5.65, height=2.05, corner_radius=0.12, stroke_color=BLACK_LINE, stroke_width=1.6, fill_color=PAPER_GRAY, fill_opacity=1).move_to(RIGHT * 4.20 + DOWN * 1.15)
        code_line = self.mono("def __init__(self, name, energy, position):", 19, BOLD).move_to(code_box)
        uml_sig = self.mono("+ Robot(name, energy, position)", 21, BOLD).move_to(RIGHT * 4.20 + UP * 1.55)
        connect = self.concept_arrow(uml_sig.get_bottom(), code_line.get_top(), width=1.5)
        self.play(FadeIn(uml_sig), FadeIn(code_box), FadeIn(code_line), GrowArrow(connect), run_time=RUN_NORMAL)
        statement = VGroup(self.text("THE UML MODEL AND THE CODE", 24, BOLD), self.text("MUST TELL THE SAME STORY.", 24, BOLD)).arrange(DOWN, buff=0.08).move_to(RIGHT * 4.20 + DOWN * 3.05)
        self.play(FadeIn(statement), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 10 — Medicion transfer / m09
    # ------------------------------------------------------------------
    def scene_10_medicion_transfer(self) -> None:
        self.set_header(10, "TRANSFER THE IDEA TO A NEW CLASS", "A measurement needs a numeric value and a unit before it can do useful work.")
        problem = VGroup(
            self.text("NEW PROBLEM", 22, BOLD),
            self.text("A measurement has:", 25),
            self.text("• a numeric value", 24),
            self.text("• a unit", 24),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(LEFT * 4.70 + UP * 0.55)
        question = self.text("What does a Medicion need to exist?", 25, BOLD).move_to(LEFT * 4.15 + DOWN * 1.25)
        reveal = VGroup(self.tag("valor", 1.55, 0.55, 20), self.tag("unidad", 1.70, 0.55, 20)).arrange(RIGHT, buff=0.28).next_to(question, DOWN, buff=0.28)
        self.play(FadeIn(problem), run_time=RUN_NORMAL)
        self.play(FadeIn(question), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(reveal), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.safe_fade(problem, question, reveal)

        lines = [
            "class Medicion:",
            "    def __init__(self, valor, unidad):",
            "        self.valor = valor",
            "        self.unidad = unidad",
            "",
            "    def escalar(self, factor):",
            "        return self.valor * factor",
            "",
            "m = Medicion(12, \"C\")",
            "print(m.escalar(2))",
        ]
        panel, code = self.code_panel(lines, width=8.20, height=5.30, font_size=20, title="m09 · PYTHON")
        panel.move_to(LEFT * 3.55 + DOWN * 0.40)
        card = self.measurement_card().move_to(RIGHT * 4.35 + UP * 0.45)
        self.play(FadeIn(panel), run_time=RUN_NORMAL)
        self.play(Circumscribe(code[2], color=BLACK_LINE), Circumscribe(code[3], color=BLACK_LINE), run_time=RUN_NORMAL)
        self.play(FadeIn(card, shift=RIGHT * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)

        stored = VGroup(self.mono("self.valor", 24, BOLD), self.text("STORED STATE", 18)).arrange(DOWN, buff=0.08).move_to(RIGHT * 3.55 + DOWN * 1.45)
        temp = VGroup(self.mono("factor", 24, BOLD), self.text("METHOD PARAMETER", 18)).arrange(DOWN, buff=0.08).move_to(RIGHT * 5.50 + DOWN * 1.45)
        calc = self.mono("12 × 2 = 24", 28, BOLD).move_to(RIGHT * 4.55 + DOWN * 2.45)
        self.play(FadeIn(stored), FadeIn(temp), run_time=RUN_NORMAL)
        self.play(Circumscribe(code[6], color=BLACK_LINE), run_time=RUN_NORMAL)
        self.play(FadeIn(calc), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.safe_fade(panel, card, calc)
        transfer_q = VGroup(
            self.text("WHY DOES self.valor REMAIN AFTER __init__ FINISHES,", 21, BOLD),
            self.text("BUT factor DOES NOT?", 22, BOLD),
        ).arrange(DOWN, buff=0.08).move_to(UP * 0.45)
        self.play(FadeIn(transfer_q), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        answer = self.text("self.valor belongs to the object · factor belongs to one method call", 20, BOLD).move_to(UP * 0.45)
        self.play(ReplacementTransform(transfer_q, answer), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 11 — common mistake
    # ------------------------------------------------------------------
    def scene_11_common_mistake(self) -> None:
        self.set_header(11, "AVOID ‘EMPTY OBJECT + PATCH LATER’", "Ask for required data when the object is created, then centralize initialization in one place.")
        left = RoundedRectangle(width=6.20, height=4.75, corner_radius=0.13, stroke_color=BLACK_LINE, stroke_width=1.7, fill_color=WHITE, fill_opacity=1).move_to(LEFT * 3.35 + DOWN * 0.20)
        right = left.copy().move_to(RIGHT * 3.35 + DOWN * 0.20)
        frag = self.tag("FRAGILE", 1.70, 0.56, 20, filled=True).next_to(left.get_top(), DOWN, buff=0.25)
        coh = self.tag("COHERENT", 1.95, 0.56, 20, filled=True).next_to(right.get_top(), DOWN, buff=0.25)
        left_lines = VGroup(
            self.mono("Robot()", 24, BOLD),
            self.text("↓", 27),
            self.text("scattered initialization", 21),
            self.text("↓", 27),
            self.text("repeated logic", 21),
            self.text("↓", 27),
            self.text("possible invalid state", 21, BOLD),
        ).arrange(DOWN, buff=0.12).move_to(left.get_center() + DOWN * 0.15)
        right_lines = VGroup(
            self.mono('Robot("Atlas", 90, 0)', 22, BOLD),
            self.text("↓", 27),
            self.text("required data", 21),
            self.text("↓", 27),
            self.text("constructor + validation", 21),
            self.text("↓", 27),
            self.text("ready object", 21, BOLD),
        ).arrange(DOWN, buff=0.12).move_to(right.get_center() + DOWN * 0.15)
        self.play(FadeIn(left), FadeIn(right), FadeIn(frag), FadeIn(coh), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[FadeIn(m) for m in left_lines], lag_ratio=0.08), run_time=RUN_SLOW)
        self.play(LaggedStart(*[FadeIn(m) for m in right_lines], lag_ratio=0.08), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        rule = VGroup(
            self.text("IF AN OBJECT NEEDS DATA TO EXIST,", 25, BOLD),
            self.text("ASK FOR THAT DATA WHEN IT IS CREATED.", 25, BOLD),
        ).arrange(DOWN, buff=0.08).move_to(DOWN * 3.50)
        self.play(FadeIn(rule), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_scene()

    # ------------------------------------------------------------------
    # 12 — exit check
    # ------------------------------------------------------------------
    def scene_12_exit_check(self) -> None:
        self.set_header(12, "CAN YOU EXPLAIN IT?", "Answer each question before the keywords appear.")
        questions = [
            "WHEN DOES __init__ RUN?",
            "WHAT IS THE DIFFERENCE BETWEEN energy AND self.energy?",
            'WHY IS Robot("Atlas", 90, 0) SAFER THAN Robot() + PATCHES?',
            'WHAT SHOULD HAPPEN WITH Robot("Scout", -25, 0)?',
        ]
        qmob = self.text(questions[0], 31, BOLD).move_to(UP * 0.60)
        self.play(FadeIn(qmob), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        for q in questions[1:]:
            next_q = self.text(q, 28 if len(q) < 58 else 25, BOLD).move_to(UP * 0.60)
            self.fit(next_q, 13.2, 0.85)
            self.play(ReplacementTransform(qmob, next_q), run_time=RUN_NORMAL)
            qmob = next_q
            self.wait(PAUSE_WORK)
        keywords = VGroup(
            self.tag("CREATION", 1.85, 0.60, 21),
            self.tag("STATE", 1.65, 0.60, 21),
            self.tag("PARAMETERS", 2.25, 0.60, 21),
            self.tag("VALIDATION", 2.25, 0.60, 21, filled=True),
        ).arrange(RIGHT, buff=0.35).move_to(DOWN * 1.10)
        self.play(FadeOut(qmob), FadeIn(keywords), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.clear_scene()

    # ------------------------------------------------------------------
    # Final synthesis / evidence handoff / next class teaser
    # ------------------------------------------------------------------
    def final_synthesis(self) -> None:
        if self.header_group is not None:
            self.play(FadeOut(self.header_group), run_time=RUN_QUICK)
            self.header_group = None
        if self.subtitle_group is not None:
            self.play(FadeOut(self.subtitle_group), run_time=RUN_QUICK)
            self.subtitle_group = None

        pipeline = VGroup(
            self.tag("REQUIREMENTS", 2.25, 0.58, 19), self.text("↓", 25),
            self.tag("PARAMETERS", 2.10, 0.58, 19), self.text("↓", 25),
            self.tag("CONSTRUCTOR", 2.20, 0.58, 19, filled=True), self.text("↓", 25),
            self.tag("VALIDATION", 2.10, 0.58, 19), self.text("↓", 25),
            self.tag("INITIAL STATE", 2.25, 0.58, 19), self.text("↓", 25),
            self.tag("VALID OBJECT", 2.20, 0.58, 19, filled=True), self.text("↓", 25),
            self.tag("BEHAVIOR", 1.85, 0.58, 19),
        ).arrange(DOWN, buff=0.05).move_to(LEFT * 4.65 + DOWN * 0.20)
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.04) for m in pipeline], lag_ratio=0.05), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)

        first = VGroup(
            self.text("A GOOD OBJECT", 33, BOLD),
            self.text("DOES NOT BEGIN AS", 28),
            self.text("A COLLECTION OF MISSING VALUES.", 28, BOLD),
        ).arrange(DOWN, buff=0.13).move_to(RIGHT * 2.25 + UP * 1.05)
        second = VGroup(
            self.text("A GOOD OBJECT", 33, BOLD),
            self.text("BEGINS READY TO DO ITS JOB.", 30, BOLD),
        ).arrange(DOWN, buff=0.14).move_to(RIGHT * 2.25 + UP * 1.05)
        durable = VGroup(
            self.text("A CLASS DEFINES WHAT AN OBJECT CAN BE.", 24),
            self.text("A CONSTRUCTOR DEFINES HOW THAT OBJECT BEGINS.", 24, BOLD),
            self.text("CREATE VALID OBJECTS. THEN LET THEM BEHAVE.", 24, BOLD),
        ).arrange(DOWN, buff=0.15).move_to(RIGHT * 2.25 + DOWN * 1.35)
        self.play(FadeIn(first), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(ReplacementTransform(first, second), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(durable), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)

        self.safe_fade(pipeline, second, durable)
        evidence_title = self.text("CLASSROOM EVIDENCE", 28, BOLD).move_to(UP * 2.45)
        evidence = VGroup(
            self.text("1 · THREE valid objects", 23),
            self.text("2 · Justify each constructor parameter", 23),
            self.text("3 · UML consistent with implementation", 23),
            self.text("4 · One rejected invalid initial state", 23),
            self.text("5 · Explain self.valor vs factor", 23),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(UP * 0.25)
        self.play(FadeIn(evidence_title), FadeIn(evidence), run_time=RUN_NORMAL)
        self.wait(PAUSE_SUMMARY)
        self.safe_fade(evidence_title, evidence)

        footer = self.text("SEMINAR 11 · OOP + UML", 22, BOLD).move_to(UP * 2.95)
        cls = self.text("CLASS 03 · CONSTRUCTORS & VALID STATE", 31, BOLD).move_to(UP * 2.25)
        next_label = self.tag("NEXT", 1.30, 0.54, 19, filled=True).move_to(UP * 1.25)
        next_title = self.text("ENCAPSULATION & VISIBILITY", 29, BOLD).move_to(UP * 0.55)
        bridge = VGroup(
            self.text("THE CONSTRUCTOR CREATES VALID STATE.", 25, BOLD),
            self.text("BUT AFTER CREATION...", 25),
            self.text("WHO SHOULD BE ALLOWED TO CHANGE IT?", 27, BOLD),
        ).arrange(DOWN, buff=0.18).move_to(DOWN * 1.15)
        self.play(FadeIn(footer), FadeIn(cls), run_time=RUN_NORMAL)
        self.play(FadeIn(next_label), FadeIn(next_title), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(bridge), run_time=RUN_NORMAL)
        self.wait(PAUSE_FINAL)
        self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=RUN_SLOW)
