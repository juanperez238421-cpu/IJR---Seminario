from manim import *
from renders.seminario11_poo_semester_intro import Seminario11POOIntro as BaseSeminario11POOIntro


class Seminario11POOIntroV3(BaseSeminario11POOIntro):
    """QA overlay that fixes the code-panel line layout from V2."""

    def code_to_object(self):
        head = self.section_header(
            3,
            "FROM CODE TO A WORKING OBJECT",
            "A class defines the model; an object stores a real state that changes when a method runs.",
        )
        self.add(head)

        code_box = RoundedRectangle(
            width=7.45, height=5.05, corner_radius=0.15,
            stroke_color=BLACK, stroke_width=2,
            fill_color=self.PAPER if hasattr(self, "PAPER") else "#F8F8F8",
            fill_opacity=1,
        ).move_to(LEFT * 3.75 + DOWN * 0.18)

        code_label = self.txt("PYTHON", 19, BOLD, "#787878")
        code_label.move_to(code_box.get_top() + DOWN * 0.28 + RIGHT * (-2.85))

        source_lines = {
            0: "class Robot:",
            1: "    def __init__(self, name):",
            2: "        self.name = name",
            3: "        self.energy = 100",
            5: "    def move(self):",
            6: "        self.energy -= 10",
            8: "explorer = Robot('A1')",
            9: "explorer.move()",
        }

        line_map = {}
        anchor_x = code_box.get_left()[0] + 0.36
        start_y = code_box.get_center()[1] + 1.47
        line_step = 0.385
        visible_code = VGroup()

        for source_index, line_text in source_lines.items():
            line = Text(line_text, font="Monospace", font_size=22, color=BLACK)
            y = start_y - source_index * line_step
            line.move_to([anchor_x + line.width / 2, y, 0])
            line_map[source_index] = line
            visible_code.add(line)

        code_group = VGroup(code_box, code_label, visible_code)

        object_box = RoundedRectangle(
            width=4.35, height=3.45, corner_radius=0.18,
            stroke_color=BLACK, stroke_width=2.2,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(RIGHT * 4.25 + DOWN * 0.10)

        object_title = self.txt("OBJECT: explorer", 29, BOLD)
        name_line = self.txt("name = 'A1'", 24)
        energy_label = self.txt("energy =", 24)
        energy_100 = self.txt("100", 24, BOLD)
        energy_row = VGroup(energy_label, energy_100).arrange(RIGHT, buff=0.12)
        status = self.txt("ready to move()", 22, BOLD, "#787878")
        object_content = VGroup(object_title, name_line, energy_row, status).arrange(DOWN, buff=0.31).move_to(object_box)
        object_group = VGroup(object_box, object_content)

        connector = Arrow(
            code_group.get_right() + RIGHT * 0.15,
            object_group.get_left() + LEFT * 0.15,
            buff=0.15, stroke_width=3, color=BLACK,
        )

        create_highlight = SurroundingRectangle(line_map[8], color=BLACK, buff=0.08, stroke_width=2)
        move_highlight = SurroundingRectangle(line_map[9], color=BLACK, buff=0.08, stroke_width=2)

        self.play(FadeIn(code_group), run_time=0.9)
        self.wait(0.7)
        self.play(Create(create_highlight), run_time=0.5)
        self.play(GrowArrow(connector), FadeIn(object_group, shift=LEFT * 0.22), run_time=0.9)
        self.wait(0.9)

        self.play(Transform(create_highlight, move_highlight), run_time=0.55)
        energy_90 = self.txt("90", 24, BOLD).move_to(energy_100)
        moved_status = self.txt("move() changed the state", 22, BOLD).move_to(status)
        self.play(Transform(energy_100, energy_90), Transform(status, moved_status), run_time=0.8)
        self.wait(2.4)
        self.clear_scene()
