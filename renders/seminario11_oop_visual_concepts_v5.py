from manim import *
import importlib.util
from pathlib import Path

# Load the V4 scene by sibling file path so Manim can execute this scene as a
# standalone module inside the pinned Docker image.
_BASE_PATH = Path(__file__).with_name("seminario11_oop_visual_concepts_v4.py")
_SPEC = importlib.util.spec_from_file_location("seminar11_oop_v4", _BASE_PATH)
_BASE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_BASE)
BaseScene = _BASE.Seminar11OOPVisualConcepts


class Seminar11OOPVisualConceptsV5(BaseScene):
    """Final QA overlay for the visual OOP lesson.

    Fixes discovered by post-render frame inspection:
    - compact object cards remain below the persistent header/subtitle;
    - UML compartment labels no longer touch divider lines;
    - tangled non-OOP connectors render behind opaque cards;
    - composition connectors never cross class text.
    """

    def uml_class(
        self,
        class_name,
        attributes,
        methods,
        width=5.0,
        height=4.7,
        title_size=30,
        body_size=23,
        fill=WHITE,
    ):
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.12,
            stroke_color=BLACK, stroke_width=2.2,
            fill_color=fill, fill_opacity=1,
        )
        y_top = box.get_top()[1]
        x_l = box.get_left()[0]
        x_r = box.get_right()[0]
        title_div_y = y_top - 0.92
        attr_div_y = y_top - 2.55

        line1 = Line([x_l, title_div_y, 0], [x_r, title_div_y, 0], color=BLACK, stroke_width=1.7)
        line2 = Line([x_l, attr_div_y, 0], [x_r, attr_div_y, 0], color=BLACK, stroke_width=1.7)

        title = self.txt(class_name, title_size, BOLD)
        title.move_to([box.get_center()[0], y_top - 0.46, 0])

        attr_label = self.txt("ATTRIBUTES", 18, BOLD, _BASE.MID_GRAY)
        attr_label.move_to([x_l + 0.72, title_div_y - 0.40, 0])
        attr_group = VGroup(*[self.txt(a, body_size, color=_BASE.DARK_GRAY) for a in attributes])
        attr_group.arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        self.fit(attr_group, width - 0.55, 1.02)
        attr_group.move_to([box.get_center()[0], title_div_y - 1.08, 0]).align_to(box, LEFT).shift(RIGHT * 0.28)

        method_label = self.txt("METHODS", 18, BOLD, _BASE.MID_GRAY)
        method_label.move_to([x_l + 0.57, attr_div_y - 0.40, 0])
        method_group = VGroup(*[self.txt(m, body_size, color=_BASE.DARK_GRAY) for m in methods])
        method_group.arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        self.fit(method_group, width - 0.55, 1.38)
        method_group.move_to([box.get_center()[0], attr_div_y - 1.12, 0]).align_to(box, LEFT).shift(RIGHT * 0.28)

        return VGroup(box, line1, line2, title, attr_label, attr_group, method_label, method_group)

    def object_card(self, name, state_lines, method_text="move()", width=3.6, height=1.75):
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.14,
            stroke_color=BLACK, stroke_width=2,
            fill_color=WHITE, fill_opacity=1,
        )
        title = self.txt(name, 23, BOLD)
        state = VGroup(*[self.txt(s, 19, color=_BASE.DARK_GRAY) for s in state_lines]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.07
        )
        method = self.txt(method_text, 18, BOLD, _BASE.MID_GRAY)
        content = VGroup(title, state, method).arrange(DOWN, aligned_edge=LEFT, buff=0.09)
        self.fit(content, width - 0.45, height - 0.25)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.24)
        return VGroup(box, content)

    def objects_from_class(self):
        head = self.section_header(
            2,
            "ONE CLASS → MANY OBJECTS",
            "Each object follows the same blueprint but keeps its own independent state.",
        )
        self.add(head)

        blueprint = self.uml_class(
            "Robot",
            ["name", "energy", "position"],
            ["move()", "recharge()"],
            width=3.8, height=4.2, title_size=29, body_size=21, fill=_BASE.PAPER,
        ).move_to(LEFT * 5.25 + DOWN * 0.25)
        bp_label = self.txt("CLASS", 20, BOLD, _BASE.MID_GRAY).next_to(blueprint, UP, buff=0.18)

        objs = VGroup(
            self.object_card("explorer", ["energy = 100", "position = 0"], width=3.35),
            self.object_card("courier", ["energy = 65", "position = 12"], width=3.35),
            self.object_card("scout", ["energy = 80", "position = 4"], width=3.35),
        ).arrange(DOWN, buff=0.25).move_to(RIGHT * 3.20 + DOWN * 0.55)

        arrows = VGroup(*[
            Arrow(
                blueprint.get_right() + RIGHT * 0.10,
                obj.get_left() + LEFT * 0.10,
                buff=0.18,
                color=_BASE.LIGHT_GRAY,
                stroke_width=2.5,
            )
            for obj in objs
        ])
        caption = self.txt("Same methods. Different data. Independent objects.", 25, BOLD)
        caption.to_edge(DOWN, buff=0.48)

        self.play(FadeIn(blueprint), FadeIn(bp_label), run_time=0.9)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.18), run_time=1.1)
        self.play(LaggedStart(*[FadeIn(o, shift=LEFT * 0.15) for o in objs], lag_ratio=0.18), run_time=1.4)
        self.wait(1.0)

        ex_energy = objs[0][1][1][0]
        changed = self.txt("energy = 90", 19, color=_BASE.DARK_GRAY).move_to(ex_energy)
        highlight = SurroundingRectangle(objs[0], color=BLACK, stroke_width=2.2, buff=0.07)
        self.play(Create(highlight), run_time=0.45)
        self.play(Transform(ex_energy, changed), run_time=0.7)
        self.play(FadeIn(caption), run_time=0.7)
        self.wait(2.2)
        self.clear_scene()

    def encapsulation_usefulness(self):
        head = self.section_header(
            3,
            "WHY KEEP ATTRIBUTES AND METHODS TOGETHER?",
            "Encapsulation gives each object control over its own state and reduces scattered code.",
        )
        self.add(head)

        left_title = self.txt("WITHOUT A MODEL", 24, BOLD, _BASE.MID_GRAY).move_to(LEFT * 4.55 + UP * 2.0)
        raw = VGroup(
            self.simple_box("robot_energy", "variable", 2.65, 1.12),
            self.simple_box("robot_position", "variable", 2.65, 1.12),
            self.simple_box("move_robot()", "function", 2.65, 1.12),
            self.simple_box("charge_robot()", "function", 2.65, 1.12),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.28, 0.28)).move_to(LEFT * 4.25 + DOWN * 0.05)
        tangle = VGroup(
            Line(raw[0].get_right(), raw[3].get_left(), color=_BASE.LIGHT_GRAY),
            Line(raw[1].get_right(), raw[2].get_left(), color=_BASE.LIGHT_GRAY),
            Line(raw[0].get_bottom(), raw[2].get_top(), color=_BASE.LIGHT_GRAY),
        ).set_z_index(-1)

        right_title = self.txt("WITH OOP", 24, BOLD, _BASE.MID_GRAY).move_to(RIGHT * 4.25 + UP * 2.0)
        robot = self.uml_class(
            "Robot",
            ["energy", "position"],
            ["move()", "recharge()"],
            width=4.8, height=4.0, body_size=23, fill=_BASE.PAPER,
        ).move_to(RIGHT * 4.1 + DOWN * 0.10)
        arrow = Arrow(LEFT * 0.72, RIGHT * 0.72, color=BLACK, stroke_width=3).move_to(DOWN * 0.10)
        result = self.txt("The object owns its data and the actions that change it.", 24, BOLD)
        self.fit(result, 12.8, 0.55)
        result.to_edge(DOWN, buff=0.48)

        self.add(tangle)
        self.play(FadeIn(left_title), FadeIn(raw), run_time=1.0)
        self.wait(1.1)
        self.play(GrowArrow(arrow), run_time=0.55)
        self.play(FadeIn(right_title), FadeIn(robot, shift=LEFT * 0.18), run_time=1.0)
        self.play(FadeIn(result), run_time=0.75)
        self.wait(2.4)
        self.clear_scene()

    def composition_system(self):
        head = self.section_header(
            6,
            "COMPOSITION: BUILD A SYSTEM FROM SMALL OBJECTS",
            "A real project is easier to design when each class has one clear responsibility.",
        )
        self.add(head)

        system = RoundedRectangle(
            width=12.8, height=4.75, corner_radius=0.18,
            stroke_color=BLACK, stroke_width=2.3,
            fill_color=_BASE.PAPER, fill_opacity=1,
        ).move_to(DOWN * 0.22)
        system_title = self.txt("SMART WAREHOUSE PROJECT", 29, BOLD).move_to(system.get_top() + DOWN * 0.40)
        system_rule = Line(system.get_left() + UP * 1.60, system.get_right() + UP * 1.60, color=_BASE.LIGHT_GRAY, stroke_width=2)

        boxes = VGroup(
            self.simple_box("Robot", "moves products", 2.55, 1.55),
            self.simple_box("Inventory", "tracks stock", 2.55, 1.55),
            self.simple_box("Order", "stores requests", 2.55, 1.55),
            self.simple_box("Sensor", "reports position", 2.55, 1.55),
        ).arrange(RIGHT, buff=0.55).move_to(DOWN * 0.10)

        links = VGroup(
            Arrow(boxes[0].get_right(), boxes[1].get_left(), buff=0.06, color=BLACK, stroke_width=2.2),
            Arrow(boxes[1].get_right(), boxes[2].get_left(), buff=0.06, color=BLACK, stroke_width=2.2),
            Arrow(boxes[2].get_right(), boxes[3].get_left(), buff=0.06, color=BLACK, stroke_width=2.2),
        )
        interface_note = self.txt("clear interfaces", 20, BOLD, _BASE.MID_GRAY).next_to(boxes, DOWN, buff=0.30)
        responsibility = self.txt("Small classes cooperate → a larger useful system emerges.", 25, BOLD)
        responsibility.next_to(system, DOWN, buff=0.20)

        self.play(Create(system), FadeIn(system_title), Create(system_rule), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.12) for b in boxes], lag_ratio=0.16), run_time=1.5)
        self.play(LaggedStart(*[GrowArrow(a) for a in links], lag_ratio=0.18), FadeIn(interface_note), run_time=1.1)
        self.play(FadeIn(responsibility), run_time=0.75)
        self.wait(2.5)
        self.clear_scene()
