from manim import *
import importlib.util
from pathlib import Path

_BASE_PATH = Path(__file__).with_name("seminario11_oop_visual_concepts_v5.py")
_SPEC = importlib.util.spec_from_file_location("seminar11_oop_v5", _BASE_PATH)
_BASE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_BASE)
BaseScene = _BASE.Seminar11OOPVisualConceptsV5

# Constants are defined in the original V4 module loaded by V5.
ROOT = _BASE._BASE


class Seminar11OOPVisualConceptsV6(BaseScene):
    """Final proportional-UML QA pass.

    The class rectangle is split by measured compartment heights instead of
    fixed absolute text offsets. This keeps headings, attributes, and methods
    clear of borders for every class size used in the lesson.
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
            width=width,
            height=height,
            corner_radius=0.12,
            stroke_color=BLACK,
            stroke_width=2.2,
            fill_color=fill,
            fill_opacity=1,
        )

        top = box.get_top()[1]
        bottom = box.get_bottom()[1]
        left = box.get_left()[0]
        right = box.get_right()[0]

        title_h = min(0.92, height * 0.23)
        remaining_h = height - title_h
        attr_h = remaining_h * 0.50
        method_h = remaining_h - attr_h

        line1_y = top - title_h
        line2_y = line1_y - attr_h

        line1 = Line([left, line1_y, 0], [right, line1_y, 0], color=BLACK, stroke_width=1.7)
        line2 = Line([left, line2_y, 0], [right, line2_y, 0], color=BLACK, stroke_width=1.7)

        title = self.txt(class_name, title_size, BOLD)
        self.fit(title, width - 0.45, title_h - 0.16)
        title.move_to([box.get_center()[0], top - title_h / 2, 0])

        attr_label = self.txt("ATTRIBUTES", 17, BOLD, ROOT.MID_GRAY)
        attr_lines = VGroup(*[self.txt(a, body_size, color=ROOT.DARK_GRAY) for a in attributes])
        attr_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        attr_content = VGroup(attr_label, attr_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        self.fit(attr_content, width - 0.52, attr_h - 0.28)
        attr_center_y = (line1_y + line2_y) / 2
        attr_content.move_to([box.get_center()[0], attr_center_y, 0])
        attr_content.align_to(box, LEFT).shift(RIGHT * 0.28)

        method_label = self.txt("METHODS", 17, BOLD, ROOT.MID_GRAY)
        method_lines = VGroup(*[self.txt(m, body_size, color=ROOT.DARK_GRAY) for m in methods])
        method_lines.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        method_content = VGroup(method_label, method_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        self.fit(method_content, width - 0.52, method_h - 0.28)
        method_center_y = (line2_y + bottom) / 2
        method_content.move_to([box.get_center()[0], method_center_y, 0])
        method_content.align_to(box, LEFT).shift(RIGHT * 0.28)

        return VGroup(box, line1, line2, title, attr_content, method_content)
