#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Seminar 11 · Class 03 · Constructors & Valid State.

Curricular ground truth:
- t3/common/index.html — Session 3: Constructors / Initialization / 3 valid objects
- t3/oop-uml/course-data.js — Constructors & Valid State
- t3/data/modules/m09.json — Python __init__, Java constructor, self/this, early validation
- t3/README.md — Common Core OOP + UML + project-studio engineering workflow

Visual continuity:
- white 16:9 classroom canvas
- black / charcoal typography
- thin UML and mapping lines
- numbered sections and generous whitespace
- restrained causal animation, no decorative color

Target: ManimCE 0.20.1, 1920x1080, 30 fps.
Preview:
  manim -pql Seminar11_Class03_Constructors_ValidState.py Seminar11Class03ConstructorsValidState --disable_caching
Final:
  manim -pqh Seminar11_Class03_Constructors_ValidState.py Seminar11Class03ConstructorsValidState --fps 30 --disable_caching
"""

from __future__ import annotations

from dataclasses import dataclass

from jp_classroom_style import *


@dataclass(frozen=True)
class MeasurementData:
    name: str
    value: str
    unit: str


MEASUREMENTS = (
    MeasurementData("temperature", "12", '"C"'),
    MeasurementData("distance", "5.2", '"m"'),
    MeasurementData("mass", "70", '"kg"'),
)


class Seminar11Class03ConstructorsValidState(JPClassroomScene):
    """One continuous lesson: constructor parameters -> initialization -> valid object state."""

    # ------------------------------------------------------------------
    # Validation
    # ------------------------------------------------------------------
    def validate_lesson_data(self) -> None:
        assert len(MEASUREMENTS) == 3
        assert [item.name for item in MEASUREMENTS] == ["temperature", "distance", "mass"]
        assert MEASUREMENTS[0].value == "12"
        assert 12 * 2 == 24
        assert all(item.unit.strip('"') for item in MEASUREMENTS)

    # ------------------------------------------------------------------
    # Generic visual builders
    # ------------------------------------------------------------------
    def tag(self, label: str, width: float = 2.0, height: float = 0.50, size: int = 20, *, filled: bool = False) -> VGroup:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.09,
            stroke_color=BLACK_LINE,
            stroke_width=2.0 if filled else 1.5,
            fill_color=VERY_LIGHT_GRAY if filled else WHITE,
            fill_opacity=1,
        )
        txt = self.text(label, size, BOLD if filled else MEDIUM)
        self.fit(txt, width - 0.20, height - 0.12)
        txt.move_to(box)
        return VGroup(box, txt)

    def simple_arrow(self, start, end, *, width: float = 1.8) -> Arrow:
        return Arrow(
            start,
            end,
            buff=0.12,
            color=BLACK_LINE,
            stroke_width=width,
            max_tip_length_to_length_ratio=0.13,
        )

    def flow_strip(self, active: str) -> VGroup:
        labels = ["PREDICT", "MODEL", "CODE", "EXECUTE", "MODIFY", "EXPLAIN"]
        cards = VGroup()
        for label in labels:
            cards.add(self.tag(label, 1.72, 0.46, 17, filled=(label == active)))
        cards.arrange(RIGHT, buff=0.16)
        arrows = VGroup()
        for left, right in zip(cards[:-1], cards[1:]):
            arrows.add(self.simple_arrow(left.get_right(), right.get_left(), width=1.2))
        group = VGroup(cards, arrows)
        group.move_to(DOWN * 3.50)
        self.fit(group, 14.25, 0.68)
        return group

    def instance_card(
        self,
        name: str,
        value: str,
        unit: str,
        *,
        width: float = 3.15,
        height: float = 2.05,
        question_value: bool = False,
        question_unit: bool = False,
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
        title = self.text(f"{name} : Measurement", 22, BOLD)
        v = "?" if question_value else value
        u = "?" if question_unit else unit
        state = VGroup(
            self.text(f"value = {v}", 21),
            self.text(f"unit = {u}", 21),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        divider = Line(LEFT * (width / 2 - 0.22), RIGHT * (width / 2 - 0.22), color=LIGHT_GRAY, stroke_width=1.5)
        content = VGroup(title, divider, state).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        self.fit(content, width - 0.48, height - 0.38)
        content.move_to(box)
        return VGroup(box, content)

    def uml_measurement(self, *, compact: bool = False) -> VGroup:
        width = 4.20 if not compact else 3.35
        height = 3.75 if not compact else 2.70
        box = Rectangle(width=width, height=height, stroke_color=BLACK_LINE, stroke_width=1.8, fill_color=WHITE, fill_opacity=1)
        top_y = box.get_top()[1]
        bottom_y = box.get_bottom()[1]
        left_x = box.get_left()[0]
        right_x = box.get_right()[0]

        y1 = top_y - (0.80 if not compact else 0.62)
        y2 = top_y - (2.00 if not compact else 1.42)
        d1 = Line([left_x, y1, 0], [right_x, y1, 0], color=BLACK_LINE, stroke_width=1.4)
        d2 = Line([left_x, y2, 0], [right_x, y2, 0], color=BLACK_LINE, stroke_width=1.4)

        title = self.text("Measurement", 27 if not compact else 22, BOLD).move_to([0, (top_y + y1) / 2, 0])
        attrs = VGroup(
            self.text("- value : float", 23 if not compact else 18),
            self.text("- unit  : String", 23 if not compact else 18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.14 if not compact else 0.08)
        attrs.move_to([left_x + 0.34 + attrs.width / 2, (y1 + y2) / 2, 0])

        ops = VGroup(
            self.text("+ Measurement(value, unit)", 22 if not compact else 17, BOLD),
            self.text("+ scale(factor) : float", 22 if not compact else 17),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15 if not compact else 0.08)
        ops.move_to([left_x + 0.34 + ops.width / 2, (y2 + bottom_y) / 2, 0])
        return VGroup(box, d1, d2, title, attrs, ops)

    def code_panel(
        self,
        lines: list[str],
        *,
        width: float = 7.20,
        height: float = 3.55,
        font_size: int = 25,
        title: str | None = None,
    ) -> tuple[VGroup, VGroup]:
        box = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.12,
            stroke_color=BLACK_LINE,
            stroke_width=1.7,
            fill_color=PAPER_GRAY,
            fill_opacity=1,
        )
        line_mobs = VGroup(*[
            Text(
                line,
                font="DejaVu Sans Mono",
                font_size=font_size,
                color=BLACK_TEXT,
                weight=NORMAL,
            )
            for line in lines
        ])
        line_mobs.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        self.fit(line_mobs, width - 0.55, height - (0.90 if title else 0.45))
        line_mobs.move_to(box)
        line_mobs.align_to(box, LEFT).shift(RIGHT * 0.28)
        if title:
            title_mob = self.text(title, 20, BOLD).next_to(box.get_top(), DOWN, buff=0.18).align_to(box, LEFT).shift(RIGHT * 0.28)
            line_mobs.next_to(title_mob, DOWN, buff=0.22).align_to(title_mob, LEFT)
            return VGroup(box, title_mob, line_mobs), line_mobs
        return VGroup(box, line_mobs), line_mobs

    def small_blueprint(self) -> VGroup:
        box = RoundedRectangle(width=2.75, height=1.55, corner_radius=0.10, stroke_color=BLACK_LINE, stroke_width=1.7, fill_color=WHITE, fill_opacity=1)
        title = self.text("Measurement", 23, BOLD)
        sub = self.text("constructor(value, unit)", 17)
        content = VGroup(title, sub).arrange(DOWN, buff=0.16).move_to(box)
        return VGroup(box, content)

    def project_domain_card(self, track: str, signature: str, width: float = 4.10) -> VGroup:
        box = RoundedRectangle(width=width, height=1.05, corner_radius=0.10, stroke_color=BLACK_LINE, stroke_width=1.4, fill_color=WHITE, fill_opacity=1)
        title = self.text(track, 17, BOLD)
        sig = Text(signature, font="DejaVu Sans Mono", font_size=18, color=BLACK_TEXT)
        content = VGroup(title, sig).arrange(DOWN, buff=0.10)
        self.fit(content, width - 0.32, 0.78)
        content.move_to(box)
        return VGroup(box, content)

    # ------------------------------------------------------------------
    # Lesson orchestration
    # ------------------------------------------------------------------
    def construct(self) -> None:
        self.opening_00()
        self.scene_01_half_built()
        self.scene_02_constructor_birth()
        self.scene_03_uml_initialization()
        self.scene_04_python_init()
        self.scene_05_parameter_vs_attribute()
        self.scene_06_three_objects()
        self.scene_07_java_connection()
        self.scene_08_valid_state()
        self.scene_09_behavior_after_init()
        self.scene_10_project_transfer()
        self.scene_11_evidence()
        self.final_exit_check()

    # ------------------------------------------------------------------
    # 00 — conceptual bridge
    # ------------------------------------------------------------------
    def opening_00(self) -> None:
        course = self.text("SEMINAR · GRADE 11", 28, BOLD).move_to(UP * 3.25)
        title = self.text("CONSTRUCTORS & VALID STATE", 51, BOLD).move_to(UP * 2.25)
        subtitle = self.text("OBJECTS SHOULD BE BORN READY TO WORK", 28, MEDIUM).move_to(UP * 1.43)
        rule = Line(LEFT * 5.6, RIGHT * 5.6, color=BLACK_LINE, stroke_width=2.0).move_to(UP * 0.90)
        last = self.text("Last time:   object = identity + state + behavior", 25).move_to(UP * 0.15)
        today = self.text("Today:   How does the state get there?", 25, BOLD).move_to(DOWN * 0.42)

        trio = VGroup(
            self.tag("identity", 2.00, 0.58, 22),
            self.tag("state", 2.00, 0.58, 22, filled=True),
            self.tag("behavior", 2.00, 0.58, 22),
        ).arrange(RIGHT, buff=0.36).move_to(DOWN * 1.35)
        state_big = self.text("STATE", 42, BOLD).move_to(DOWN * 1.35)
        initial = self.text("INITIAL STATE", 42, BOLD).move_to(DOWN * 1.35)
        constructor = self.text("CONSTRUCTOR", 42, BOLD).move_to(DOWN * 1.35)
        question = self.text("WHEN AND HOW IS THAT STATE CREATED?", 24, MEDIUM).move_to(DOWN * 2.25)

        self.assert_within_frame(VGroup(course, title, subtitle, rule, last, today, trio, question), "opening")
        self.play(FadeIn(course, shift=UP * 0.14), run_time=RUN_NORMAL)
        self.play(Write(title), run_time=RUN_SLOW)
        self.play(Create(rule), FadeIn(subtitle), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(last), FadeIn(today), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(LaggedStart(*[FadeIn(item, shift=UP * 0.08) for item in trio], lag_ratio=0.15), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.play(FadeOut(trio[0]), FadeOut(trio[2]), ReplacementTransform(trio[1], state_big), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(ReplacementTransform(state_big, initial), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(ReplacementTransform(initial, constructor), FadeIn(question), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=RUN_NORMAL)

    # ------------------------------------------------------------------
    # 01 — predict the problem
    # ------------------------------------------------------------------
    def scene_01_half_built(self) -> None:
        self.set_header(1, "AN OBJECT SHOULD NOT BEGIN HALF-BUILT", "Predict the engineering problem before writing constructor syntax.")
        flow = self.flow_strip("PREDICT")

        call = Text("m = Measurement()", font="DejaVu Sans Mono", font_size=30, color=BLACK_TEXT).move_to(LEFT * 3.6 + UP * 1.45)
        card_empty = self.instance_card("m", "", "", question_value=True, question_unit=True).move_to(RIGHT * 3.20 + UP * 0.65)
        assign_value = Text("m.value = 12", font="DejaVu Sans Mono", font_size=28, color=BLACK_TEXT).move_to(LEFT * 3.55 + UP * 0.30)
        card_half = self.instance_card("m", "12", "", question_unit=True).move_to(card_empty)
        incomplete = self.tag("INCOMPLETE STATE", 2.65, 0.58, 20, filled=True).next_to(card_half, DOWN, buff=0.26)
        assign_unit = Text('m.unit = "C"', font="DejaVu Sans Mono", font_size=28, color=BLACK_TEXT).move_to(LEFT * 3.55 + DOWN * 0.85)
        card_full = self.instance_card("m", "12", '"C"').move_to(card_empty)
        question = VGroup(
            self.text("If an object requires value and unit,", 25, BOLD),
            self.text("why allow it to exist without them?", 25, BOLD),
        ).arrange(DOWN, buff=0.12).move_to(DOWN * 2.30)

        patch_flow = VGroup(
            self.tag("CREATE", 1.65, 0.54, 19),
            self.text("→", 28),
            self.tag("PATCH", 1.65, 0.54, 19),
            self.text("→", 28),
            self.tag("PATCH", 1.65, 0.54, 19),
        ).arrange(RIGHT, buff=0.14).move_to(DOWN * 2.25)
        correct = self.tag("CREATE CORRECTLY", 3.55, 0.72, 25, filled=True).move_to(DOWN * 2.25)

        self.assert_content_safe(VGroup(call, card_empty, assign_value, assign_unit, question), "scene01 main")
        self.assert_within_frame(flow, "scene01 flow")
        self.play(FadeIn(flow), run_time=RUN_QUICK)
        self.play(Write(call), run_time=RUN_NORMAL)
        self.play(FadeIn(card_empty, shift=RIGHT * 0.10), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(Write(assign_value), ReplacementTransform(card_empty, card_half), run_time=RUN_NORMAL)
        self.play(FadeIn(incomplete), run_time=RUN_QUICK)
        self.wait(PAUSE_EXPLAIN)
        self.play(Write(assign_unit), FadeOut(incomplete), ReplacementTransform(card_half, card_full), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(question), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.play(FadeOut(call), FadeOut(assign_value), FadeOut(assign_unit), FadeOut(card_full), FadeOut(question), run_time=RUN_NORMAL)
        self.play(FadeIn(patch_flow), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(ReplacementTransform(patch_flow, correct), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 02 — constructor as birth gate
    # ------------------------------------------------------------------
    def scene_02_constructor_birth(self) -> None:
        self.set_header(2, "CONSTRUCTOR = CONTROLLED INITIALIZATION", "The constructor receives required information and establishes the initial state.")

        call = Text('Measurement(12, "C")', font="DejaVu Sans Mono", font_size=31, color=BLACK_TEXT).move_to(UP * 1.88)
        left_title = self.text("INPUT PARAMETERS", 21, BOLD).move_to(LEFT * 4.55 + UP * 0.95)
        inputs = VGroup(self.tag("12", 1.55, 0.62, 24), self.tag('"C"', 1.55, 0.62, 24)).arrange(DOWN, buff=0.30).move_to(LEFT * 4.55 + DOWN * 0.20)
        gate = RoundedRectangle(width=3.15, height=2.55, corner_radius=0.15, stroke_color=BLACK_LINE, stroke_width=2.2, fill_color=VERY_LIGHT_GRAY, fill_opacity=1).move_to(ORIGIN + DOWN * 0.20)
        gate_label = self.text("CONSTRUCTOR", 26, BOLD).move_to(gate.get_center() + UP * 0.42)
        gate_sub = self.text("controlled initialization", 18).move_to(gate.get_center() + DOWN * 0.25)
        gate_group = VGroup(gate, gate_label, gate_sub)
        result = self.instance_card("measurement", "12", '"C"', width=3.55, height=2.30).move_to(RIGHT * 4.50 + DOWN * 0.20)

        a1 = self.simple_arrow(inputs[0].get_right(), gate.get_left() + UP * 0.38)
        a2 = self.simple_arrow(inputs[1].get_right(), gate.get_left() + DOWN * 0.38)
        b1 = self.simple_arrow(gate.get_right() + UP * 0.38, result.get_left() + UP * 0.32)
        b2 = self.simple_arrow(gate.get_right() + DOWN * 0.38, result.get_left() + DOWN * 0.32)
        map1 = self.text("12 → value", 18, BOLD).next_to(b1, UP, buff=0.10)
        map2 = self.text('"C" → unit', 18, BOLD).next_to(b2, DOWN, buff=0.10)

        ladder = VGroup(
            self.text("parameters", 22),
            self.text("↓", 27),
            self.text("constructor", 22, BOLD),
            self.text("↓", 27),
            self.text("initial state", 22, BOLD),
        ).arrange(DOWN, buff=0.05).move_to(DOWN * 2.55)

        self.assert_content_safe(VGroup(call, left_title, inputs, gate_group, result, a1, a2, b1, b2, map1, map2, ladder), "scene02")
        self.play(Write(call), run_time=RUN_NORMAL)
        self.play(FadeIn(left_title), FadeIn(inputs), FadeIn(gate_group), run_time=RUN_NORMAL)
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(GrowArrow(b1), TransformFromCopy(inputs[0], result), run_time=RUN_NORMAL)
        self.play(GrowArrow(b2), FadeIn(result), run_time=RUN_NORMAL)
        self.play(FadeIn(map1), FadeIn(map2), run_time=RUN_QUICK)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(ladder), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 03 — UML model before code
    # ------------------------------------------------------------------
    def scene_03_uml_initialization(self) -> None:
        self.set_header(3, "UML: SHOW WHAT AN OBJECT NEEDS TO EXIST", "Model required state and initialization before implementation details.")
        flow = self.flow_strip("MODEL")
        uml = self.uml_measurement().move_to(LEFT * 2.25 + DOWN * 0.25)
        # Progressive groups from the final UML object.
        base = VGroup(uml[0], uml[3])
        attrs = VGroup(uml[1], uml[4])
        ops = VGroup(uml[2], uml[5])

        call = Text("Measurement(value, unit)", font="DejaVu Sans Mono", font_size=26, color=BLACK_TEXT).move_to(RIGHT * 4.10 + UP * 1.10)
        value_tag = self.tag("value", 1.60, 0.52, 19).move_to(RIGHT * 4.10 + UP * 0.15)
        unit_tag = self.tag("unit", 1.60, 0.52, 19).move_to(RIGHT * 4.10 + DOWN * 0.70)
        mapping = VGroup(
            self.simple_arrow(call.get_left() + DOWN * 0.05, value_tag.get_left() + LEFT * 0.20, width=1.3),
            self.simple_arrow(call.get_left() + DOWN * 0.15, unit_tag.get_left() + LEFT * 0.20, width=1.3),
        )
        note = VGroup(
            self.text("The constructor communicates the information", 23, BOLD),
            self.text("required when the object is created.", 23, BOLD),
            self.text("Constructor → initialization", 19),
        ).arrange(DOWN, buff=0.12).move_to(RIGHT * 3.65 + DOWN * 2.15)

        self.assert_content_safe(VGroup(uml, call, value_tag, unit_tag, mapping, note), "scene03")
        self.assert_within_frame(flow, "scene03 flow")
        self.play(FadeIn(flow), run_time=RUN_QUICK)
        self.play(Create(base[0]), FadeIn(base[1]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(Create(attrs[0]), FadeIn(attrs[1]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(Create(ops[0]), FadeIn(ops[1]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        constructor_line = ops[1][0]
        self.play(Circumscribe(constructor_line, color=BLACK_LINE, time_width=1.0), run_time=RUN_NORMAL)
        self.play(Write(call), FadeIn(value_tag), FadeIn(unit_tag), run_time=RUN_NORMAL)
        self.play(*[GrowArrow(a) for a in mapping], run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(note), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 04 — Python __init__
    # ------------------------------------------------------------------
    def scene_04_python_init(self) -> None:
        self.set_header(4, "PYTHON: __init__ BUILDS THE INSTANCE STATE", "Read the code as data movement: parameters enter, attributes persist.")
        flow = self.flow_strip("CODE")
        lines = [
            "class Measurement:",
            "    def __init__(self, value, unit):",
            "        self.value = value",
            "        self.unit = unit",
        ]
        panel, code_lines = self.code_panel(lines, width=7.65, height=3.65, font_size=25, title="PYTHON")
        panel.move_to(LEFT * 3.55 + UP * 0.05)

        params_label = self.tag("PARAMETERS", 2.25, 0.52, 19, filled=True).move_to(RIGHT * 2.85 + UP * 1.70)
        params = VGroup(self.tag("value", 1.50, 0.52, 19), self.tag("unit", 1.50, 0.52, 19)).arrange(RIGHT, buff=0.22).next_to(params_label, DOWN, buff=0.24)
        stored_label = self.tag("OBJECT STATE", 2.25, 0.52, 19, filled=True).move_to(RIGHT * 2.85 + DOWN * 0.25)
        stored = VGroup(self.tag("self.value", 1.90, 0.52, 18), self.tag("self.unit", 1.90, 0.52, 18)).arrange(RIGHT, buff=0.22).next_to(stored_label, DOWN, buff=0.24)
        arrows = VGroup(
            self.simple_arrow(params[0].get_bottom(), stored[0].get_top(), width=1.5),
            self.simple_arrow(params[1].get_bottom(), stored[1].get_top(), width=1.5),
        )
        call = Text('m = Measurement(12, "C")', font="DejaVu Sans Mono", font_size=24, color=BLACK_TEXT).move_to(RIGHT * 3.40 + DOWN * 2.10)
        card = self.instance_card("m", "12", '"C"', width=3.25, height=1.90).move_to(RIGHT * 5.25 + DOWN * 1.55)
        call_arrow = self.simple_arrow(call.get_right(), card.get_left(), width=1.6)

        self.assert_content_safe(VGroup(panel, params_label, params, stored_label, stored, arrows, call, card, call_arrow), "scene04")
        self.assert_within_frame(flow, "scene04 flow")
        self.play(FadeIn(flow), FadeIn(panel[0]), FadeIn(panel[1]), run_time=RUN_NORMAL)
        # Progressive code construction: never dump all code at once.
        self.play(Write(code_lines[0]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(Write(code_lines[1]), FadeIn(params_label), FadeIn(params), run_time=RUN_NORMAL)
        self.play(Circumscribe(code_lines[1], color=BLACK_LINE, time_width=0.9), run_time=RUN_QUICK)
        self.wait(PAUSE_EXPLAIN)
        self.play(Write(code_lines[2]), FadeIn(stored_label), FadeIn(stored[0]), GrowArrow(arrows[0]), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(Write(code_lines[3]), FadeIn(stored[1]), GrowArrow(arrows[1]), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(Write(call), FadeIn(card), GrowArrow(call_arrow), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 05 — parameter vs attribute
    # ------------------------------------------------------------------
    def scene_05_parameter_vs_attribute(self) -> None:
        self.set_header(5, "SAME WORD — DIFFERENT RESPONSIBILITY", "A constructor parameter delivers a value; an object attribute remembers it.")

        center_line = Line(UP * 2.10, DOWN * 2.45, color=LIGHT_GRAY, stroke_width=1.8)
        left_title = self.text("value", 40, BOLD).move_to(LEFT * 3.60 + UP * 1.45)
        left_role = self.text("Constructor parameter", 24, BOLD).move_to(LEFT * 3.60 + UP * 0.65)
        left_note = self.text("exists during the call", 22).move_to(LEFT * 3.60 + UP * 0.10)

        right_title = self.text("self.value", 40, BOLD).move_to(RIGHT * 3.60 + UP * 1.45)
        right_role = self.text("Object attribute", 24, BOLD).move_to(RIGHT * 3.60 + UP * 0.65)
        right_note = self.text("remains in the instance", 22).move_to(RIGHT * 3.60 + UP * 0.10)

        line1 = Text("def __init__(self, value, unit):", font="DejaVu Sans Mono", font_size=23, color=BLACK_TEXT)
        line2 = Text("    self.value = value", font="DejaVu Sans Mono", font_size=23, color=BLACK_TEXT)
        code = VGroup(line1, line2).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(UP * -0.90)
        param_box = SurroundingRectangle(line1, color=BLACK_LINE, stroke_width=1.8, buff=0.08)
        attribute_box = SurroundingRectangle(line2, color=BLACK_LINE, stroke_width=1.8, buff=0.08)

        temporary = self.tag("temporary: value", 2.45, 0.54, 19, filled=True).move_to(LEFT * 3.60 + DOWN * 2.05)
        card = self.instance_card("m", "12", '"C"', width=3.25, height=1.90).move_to(RIGHT * 3.60 + DOWN * 1.80)
        takeaway = self.text("The parameter delivers the value.  The attribute remembers it.", 25, BOLD).move_to(DOWN * 3.15)

        self.assert_content_safe(VGroup(center_line, left_title, left_role, left_note, right_title, right_role, right_note, code, param_box, attribute_box, temporary, card), "scene05")
        self.assert_within_frame(takeaway, "scene05 takeaway")
        self.play(Create(center_line), FadeIn(left_title), FadeIn(right_title), run_time=RUN_NORMAL)
        self.play(FadeIn(left_role), FadeIn(left_note), FadeIn(right_role), FadeIn(right_note), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(Write(code), run_time=RUN_NORMAL)
        self.play(Create(param_box), run_time=RUN_QUICK)
        self.wait(PAUSE_READ)
        self.play(ReplacementTransform(param_box, attribute_box), FadeIn(temporary), FadeIn(card), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        # Constructor call ends: parameter fades, object state remains.
        self.play(FadeOut(temporary), FadeOut(left_note), run_time=RUN_SLOW)
        self.wait(PAUSE_READ)
        self.play(FadeIn(takeaway), run_time=RUN_NORMAL)
        self.wait(2.4)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 06 — three valid objects
    # ------------------------------------------------------------------
    def scene_06_three_objects(self) -> None:
        self.set_header(6, "ONE CONSTRUCTOR → MANY VALID OBJECTS", "The constructor is reused; each instance owns independent state.")
        flow = self.flow_strip("EXECUTE")
        blueprint = self.small_blueprint().move_to(LEFT * 5.20 + UP * 0.25)
        calls = VGroup(*[
            Text(f'{item.name} = Measurement({item.value}, {item.unit})', font="DejaVu Sans Mono", font_size=20, color=BLACK_TEXT)
            for item in MEASUREMENTS
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.30).move_to(LEFT * 1.75 + UP * 0.15)
        cards = VGroup(*[
            self.instance_card(item.name, item.value, item.unit, width=3.25, height=1.62)
            for item in MEASUREMENTS
        ]).arrange(DOWN, buff=0.18).move_to(RIGHT * 4.75 + DOWN * 0.38)
        arrows = VGroup(*[
            self.simple_arrow(blueprint.get_right(), card.get_left(), width=1.25)
            for card in cards
        ])
        same = self.text("SAME CLASS · SAME CONSTRUCTOR STRUCTURE", 21, BOLD).move_to(LEFT * 0.85 + DOWN * 2.10)
        different = self.text("DIFFERENT STATE", 27, BOLD).move_to(LEFT * 0.85 + DOWN * 2.67)
        evidence = self.tag("3 VALID OBJECTS", 2.75, 0.62, 22, filled=True).move_to(LEFT * 0.85 + DOWN * 3.30)

        self.assert_content_safe(VGroup(blueprint, calls, cards, arrows, same, different), "scene06")
        self.assert_within_frame(VGroup(flow, evidence), "scene06 lower")
        self.play(FadeIn(flow), FadeIn(blueprint), run_time=RUN_NORMAL)
        for call, card, arrow in zip(calls, cards, arrows):
            self.play(Write(call), run_time=RUN_NORMAL)
            self.play(GrowArrow(arrow), FadeIn(card, shift=RIGHT * 0.10), run_time=RUN_NORMAL)
            self.wait(PAUSE_READ)
        # The narrative strip has completed EXECUTE; remove it before the evidence
        # summary so the lower-third remains spacious and overlap-free.
        self.play(FadeOut(flow), run_time=RUN_QUICK)
        self.play(FadeIn(same), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(FadeIn(different), FadeIn(evidence), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 07 — Java semantic correspondence
    # ------------------------------------------------------------------
    def scene_07_java_connection(self) -> None:
        self.set_header(7, "SAME IDEA, DIFFERENT SYNTAX", "The Common Core object model is language-independent: Python self corresponds to Java this.")

        py_lines = [
            "def __init__(self, value, unit):",
            "    self.value = value",
            "    self.unit = unit",
        ]
        java_lines = [
            "public Measurement(double value, String unit) {",
            "    this.value = value;",
            "    this.unit = unit;",
            "}",
        ]
        py_panel, py_code = self.code_panel(py_lines, width=6.55, height=2.65, font_size=21, title="PYTHON")
        java_panel, java_code = self.code_panel(java_lines, width=6.55, height=2.65, font_size=21, title="JAVA")
        py_panel.move_to(LEFT * 3.60 + UP * 0.35)
        java_panel.move_to(RIGHT * 3.60 + UP * 0.35)

        correspondence = VGroup(
            self.text("self", 28, BOLD), self.text("↔", 28), self.text("this", 28, BOLD),
            self.text("__init__", 24, BOLD), self.text("↔", 28), self.text("Measurement(...) constructor", 22, BOLD),
            self.text("parameter", 22), self.text("→", 24), self.text("object field", 22, BOLD),
        ).arrange_in_grid(rows=3, cols=3, buff=(0.28, 0.22)).move_to(DOWN * 1.80)
        sentence = self.text("Different syntax.  Same object-modeling idea.", 27, BOLD).move_to(DOWN * 3.10)

        self.assert_content_safe(VGroup(py_panel, java_panel, correspondence), "scene07")
        self.assert_within_frame(sentence, "scene07 sentence")
        self.play(FadeIn(py_panel[0]), FadeIn(py_panel[1]), FadeIn(java_panel[0]), FadeIn(java_panel[1]), run_time=RUN_NORMAL)
        self.play(LaggedStart(*[Write(line) for line in py_code], lag_ratio=0.15), run_time=RUN_SLOW)
        self.play(LaggedStart(*[Write(line) for line in java_code], lag_ratio=0.12), run_time=RUN_SLOW)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(correspondence), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.play(FadeIn(sentence), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 08 — constructor validation
    # ------------------------------------------------------------------
    def scene_08_valid_state(self) -> None:
        self.set_header(8, "DO NOT CREATE IMPOSSIBLE OBJECTS", "Early constructor validation can reject an invalid initial state before the object enters the system.")
        flow = self.flow_strip("MODIFY")

        invalid_call = Text('Measurement(12, "")', font="DejaVu Sans Mono", font_size=30, color=BLACK_TEXT).move_to(LEFT * 3.80 + UP * 1.30)
        invalid = self.instance_card("candidate", "12", '""', width=3.50, height=2.05).move_to(RIGHT * 3.80 + UP * 0.65)
        question = self.text("Is this object ready to work?", 28, BOLD).move_to(DOWN * 0.60)
        no = self.tag("NO — REQUIRED STATE IS MISSING", 4.75, 0.66, 22, filled=True).move_to(DOWN * 1.38)

        conceptual, conceptual_lines = self.code_panel([
            "if unit is empty:",
            "    reject creation",
        ], width=4.80, height=1.55, font_size=22, title="CONCEPTUAL RULE")
        conceptual.move_to(LEFT * 3.65 + DOWN * 2.15)
        python_rule, py_lines = self.code_panel([
            "if not unit:",
            '    raise ValueError("unit is required")',
        ], width=5.55, height=1.55, font_size=20, title="OPTIONAL PYTHON")
        python_rule.move_to(RIGHT * 3.60 + DOWN * 2.15)

        pipeline = VGroup(
            self.tag("INPUT", 1.55, 0.54, 18), self.text("→", 24),
            self.tag("VALIDATE", 1.75, 0.54, 18, filled=True), self.text("→", 24),
            self.tag("CONSTRUCT", 1.90, 0.54, 18), self.text("→", 24),
            self.tag("VALID OBJECT", 2.25, 0.54, 18),
        ).arrange(RIGHT, buff=0.14).move_to(DOWN * 3.18)
        reject_mark = Cross(invalid, stroke_color=BLACK_LINE, stroke_width=2.2).scale(0.85)

        self.assert_content_safe(VGroup(invalid_call, invalid, question, no, conceptual, python_rule), "scene08")
        self.assert_within_frame(VGroup(flow, pipeline), "scene08 lower")
        self.play(FadeIn(flow), Write(invalid_call), FadeIn(invalid), run_time=RUN_NORMAL)
        self.play(FadeIn(question), run_time=RUN_NORMAL)
        self.wait(2.5)
        self.play(FadeIn(no), Create(reject_mark), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(conceptual[0]), FadeIn(conceptual[1]), LaggedStart(*[Write(line) for line in conceptual_lines], lag_ratio=0.18), run_time=RUN_NORMAL)
        self.play(FadeIn(python_rule[0]), FadeIn(python_rule[1]), LaggedStart(*[Write(line) for line in py_lines], lag_ratio=0.18), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(pipeline), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 09 — behavior depends on initialized state
    # ------------------------------------------------------------------
    def scene_09_behavior_after_init(self) -> None:
        self.set_header(9, "FIRST INITIALIZE — THEN BEHAVE", "Methods can rely on the state established by the constructor.")

        card = self.instance_card("temperature", "12", '"C"', width=3.45, height=2.05).move_to(LEFT * 4.65 + UP * 0.25)
        method_panel, method_lines = self.code_panel([
            "def scale(self, factor):",
            "    return self.value * factor",
        ], width=5.90, height=1.80, font_size=23, title="METHOD")
        method_panel.move_to(RIGHT * 2.15 + UP * 1.05)
        call = Text("temperature.scale(2)", font="DejaVu Sans Mono", font_size=27, color=BLACK_TEXT).move_to(RIGHT * 2.15 + DOWN * 0.30)
        factors = VGroup(self.tag("self.value = 12", 2.35, 0.56, 19), self.tag("factor = 2", 2.05, 0.56, 19)).arrange(RIGHT, buff=0.30).move_to(RIGHT * 2.15 + DOWN * 1.25)
        arrow = self.simple_arrow(factors.get_bottom(), factors.get_bottom() + DOWN * 0.65, width=1.6)
        result = self.tag("24", 1.55, 0.65, 26, filled=True).next_to(arrow, DOWN, buff=0.10)
        ordering = VGroup(
            self.tag("1. CONSTRUCT", 2.15, 0.58, 19),
            self.text("→", 25),
            self.tag("2. INITIALIZE STATE", 2.75, 0.58, 19, filled=True),
            self.text("→", 25),
            self.tag("3. CALL METHODS", 2.35, 0.58, 19),
        ).arrange(RIGHT, buff=0.15).move_to(DOWN * 3.12)

        self.assert_content_safe(VGroup(card, method_panel, call, factors, arrow, result), "scene09")
        self.assert_within_frame(ordering, "scene09 ordering")
        self.play(FadeIn(card), run_time=RUN_NORMAL)
        self.play(FadeIn(method_panel[0]), FadeIn(method_panel[1]), LaggedStart(*[Write(line) for line in method_lines], lag_ratio=0.18), run_time=RUN_NORMAL)
        self.wait(PAUSE_READ)
        self.play(Write(call), FadeIn(factors), run_time=RUN_NORMAL)
        self.play(GrowArrow(arrow), FadeIn(result), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(ordering), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 10 — transfer to project tracks
    # ------------------------------------------------------------------
    def scene_10_project_transfer(self) -> None:
        self.set_header(10, "DEFINE WHAT YOUR OBJECT NEEDS TO EXIST", "Transfer the constructor question to your own project domain without changing the Common Core model.")

        cards = VGroup(
            self.project_domain_card("WEB", "Product(name, price)"),
            self.project_domain_card("DATA SCIENCE", "Dataset(path, label)"),
            self.project_domain_card("DEFENSIVE CYBERSECURITY", "LogEvent(timestamp, source)"),
            self.project_domain_card("3D PROGRAMMING", "Mesh(name, scale)"),
            self.project_domain_card("ROBOTICS", "Robot(name, battery)"),
        ).arrange_in_grid(rows=3, cols=2, buff=(0.40, 0.32)).move_to(UP * 0.05)
        question = VGroup(
            self.text("What information must your object have", 29, BOLD),
            self.text("the moment it is created?", 29, BOLD),
        ).arrange(DOWN, buff=0.12).move_to(DOWN * 2.35)
        answer = self.text("Those values become constructor parameters.", 24, BOLD).next_to(question, DOWN, buff=0.30)

        self.assert_content_safe(VGroup(cards, question), "scene10")
        self.assert_within_frame(answer, "scene10 answer")
        self.play(LaggedStart(*[FadeIn(card, shift=UP * 0.08) for card in cards], lag_ratio=0.12), run_time=RUN_SLOW * 1.5)
        self.wait(PAUSE_READ)
        self.play(FadeIn(question), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(answer), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # 11 — evidence / m09 handoff
    # ------------------------------------------------------------------
    def scene_11_evidence(self) -> None:
        self.set_header(11, "TODAY'S EVIDENCE", "Module m09 turns the constructor mental model into Python or Java practice and a Git commit.")
        flow = self.flow_strip("EXPLAIN")

        checklist = VGroup(
            self.text("□  ONE class with a clear responsibility", 27, BOLD),
            self.text("□  ONE constructor", 27, BOLD),
            self.text("□  THREE valid objects", 27, BOLD),
            self.text("□  UML updated with initialization", 27, BOLD),
            self.text("□  Explain parameter vs attribute / field", 27, BOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to(LEFT * 2.90 + UP * 0.25)
        module = self.tag("MODULE m09 · PYTHON OR JAVA", 4.00, 0.68, 22, filled=True).move_to(RIGHT * 4.40 + UP * 1.60)
        workflow = VGroup(
            self.tag("MODEL", 1.55, 0.52, 18), self.text("→", 23),
            self.tag("IMPLEMENT", 1.90, 0.52, 18), self.text("→", 23),
            self.tag("RUN", 1.35, 0.52, 18), self.text("→", 23),
            self.tag("EXPLAIN", 1.80, 0.52, 18, filled=True), self.text("→", 23),
            self.tag("COMMIT", 1.70, 0.52, 18),
        ).arrange(RIGHT, buff=0.10).move_to(RIGHT * 2.70 + DOWN * 0.15)
        mandatory = self.text("THREE VALID OBJECTS is mandatory.", 25, BOLD).move_to(RIGHT * 4.00 + DOWN * 1.35)
        optional = self.text("Optional extension: reject one invalid initial state.", 20).next_to(mandatory, DOWN, buff=0.25)

        self.assert_content_safe(VGroup(checklist, module, workflow, mandatory, optional), "scene11")
        self.assert_within_frame(flow, "scene11 flow")
        self.play(FadeIn(flow), run_time=RUN_QUICK)
        for item in checklist:
            self.play(FadeIn(item, shift=RIGHT * 0.08), run_time=RUN_QUICK)
            self.wait(0.55)
        self.play(FadeIn(module), run_time=RUN_NORMAL)
        self.play(FadeIn(workflow), run_time=RUN_NORMAL)
        self.wait(PAUSE_EXPLAIN)
        self.play(FadeIn(mandatory), FadeIn(optional), run_time=RUN_NORMAL)
        self.wait(PAUSE_WORK)
        self.clear_stage()

    # ------------------------------------------------------------------
    # Final — exit check
    # ------------------------------------------------------------------
    def final_exit_check(self) -> None:
        # Remove persistent header first.
        self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=RUN_NORMAL)
        title = self.text("EXIT CHECK", 31, BOLD).move_to(UP * 3.10)
        questions = VGroup(
            self.text("What information does the object need to exist?", 28),
            self.text("Which values belong to the object?", 28),
            self.text("Which values are only constructor parameters?", 28),
            self.text("Can the object ever be created in an invalid state?", 28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to(UP * 0.65)
        final = self.text("GOOD OBJECTS BEGIN WITH GOOD STATE.", 37, BOLD).move_to(DOWN * 1.60)
        footer = self.text("CLASS → CONSTRUCTOR → VALID OBJECT → BEHAVIOR", 24, MEDIUM).move_to(DOWN * 2.55)
        sentence = self.text("An object should be born ready to work.", 26, BOLD).move_to(DOWN * 3.25)

        self.assert_within_frame(VGroup(title, questions, final, footer, sentence), "final")
        self.play(FadeIn(title), run_time=RUN_NORMAL)
        for q in questions:
            self.play(FadeIn(q, shift=UP * 0.06), run_time=RUN_NORMAL)
            self.wait(PAUSE_READ)
        self.play(FadeIn(final), run_time=RUN_SLOW)
        self.play(FadeIn(footer), FadeIn(sentence), run_time=RUN_NORMAL)
        self.wait(3.2)
        self.play(*[FadeOut(mob) for mob in list(self.mobjects)], run_time=RUN_NORMAL)
