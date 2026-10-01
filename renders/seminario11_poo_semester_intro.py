from manim import *
import numpy as np

# =============================================================================
# JP CLASSROOM RENDER CONTRACT
# =============================================================================
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

BLACK_TEXT = BLACK
DARK_GRAY = "#303030"
MID_GRAY = "#787878"
LIGHT_GRAY = "#D7D7D7"
VERY_LIGHT_GRAY = "#F0F0F0"
PAPER = "#F8F8F8"

SAFE_WIDTH = 14.75
SAFE_HEIGHT = 7.65
CONTENT_TOP_Y = 2.55
CONTENT_BOTTOM_Y = -3.95


class Seminario11POOIntro(MovingCameraScene):
    """English-first OOP semester introduction for Seminar 11.

    QA goals implemented in this version:
    - 100% English visible instructional text.
    - Full-HD 16:9 at 30 fps.
    - Classroom-readable typography: body text >= 20 pt wherever practical.
    - No dependency on unavailable custom fonts; uses Manim/Pango generic fonts.
    - Every section fits the safe 16:9 classroom frame before animation.
    - More explanatory transformations and less static card dumping.
    """

    def txt(self, text, size=30, weight=NORMAL, color=BLACK_TEXT, font=None):
        kwargs = dict(font_size=size, weight=weight, color=color, line_spacing=0.92)
        if font:
            kwargs["font"] = font
        return Text(text, **kwargs)

    def fit(self, mob, max_w=SAFE_WIDTH, max_h=SAFE_HEIGHT):
        if mob.width > max_w:
            mob.scale_to_fit_width(max_w)
        if mob.height > max_h:
            mob.scale_to_fit_height(max_h)
        return mob

    def section_header(self, number, title, subtitle):
        badge = RoundedRectangle(
            width=0.78, height=0.56, corner_radius=0.10,
            stroke_color=BLACK, stroke_width=2,
            fill_color=WHITE, fill_opacity=1,
        )
        badge_num = self.txt(f"{number:02d}", 24, BOLD).move_to(badge)

        title_m = self.txt(title, 35, BOLD)
        self.fit(title_m, 13.55, 0.62)
        title_row = VGroup(VGroup(badge, badge_num), title_m).arrange(RIGHT, buff=0.28)
        title_row.to_edge(UP, buff=0.18).to_edge(LEFT, buff=0.48)

        rule = Line(LEFT * 7.42, RIGHT * 7.42, color=LIGHT_GRAY, stroke_width=2)
        rule.next_to(title_row, DOWN, buff=0.07)

        subtitle_m = self.txt(subtitle, 21, color=DARK_GRAY)
        self.fit(subtitle_m, 14.15, 0.62)
        subtitle_m.next_to(rule, DOWN, buff=0.10).align_to(title_row, LEFT)

        return VGroup(title_row, rule, subtitle_m)

    def card(self, title, lines, width=4.2, height=2.0, title_size=27, body_size=21):
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.16,
            stroke_color=BLACK, stroke_width=1.8,
            fill_color=WHITE, fill_opacity=1,
        )
        title_m = self.txt(title, title_size, BOLD)
        body = VGroup(*[self.txt(line, body_size, color=DARK_GRAY) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.11)
        content = VGroup(title_m, body).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        self.fit(content, width - 0.48, height - 0.36)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.25)
        return VGroup(box, content)

    def divider_label(self, text, y):
        label = self.txt(text, 22, BOLD, MID_GRAY).move_to(UP * y)
        line_l = Line(LEFT * 6.5, LEFT * 1.1, color=LIGHT_GRAY, stroke_width=2).next_to(label, LEFT, buff=0.25)
        line_r = Line(RIGHT * 1.1, RIGHT * 6.5, color=LIGHT_GRAY, stroke_width=2).next_to(label, RIGHT, buff=0.25)
        return VGroup(line_l, label, line_r)

    def clear_scene(self, run_time=0.55):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=run_time)
        self.camera.frame.set(width=16).move_to(ORIGIN)

    def construct(self):
        self.opening()
        self.why_oop()
        self.core_language()
        self.code_to_object()
        self.oop_pillars()
        self.semester_route()
        self.individual_projects()
        self.project_evidence()
        self.closing()

    def opening(self):
        kicker = self.txt("SEMINAR · GRADE 11", 26, BOLD, MID_GRAY)
        title = self.txt("PROGRAMMING SEMESTER", 58, BOLD)
        subtitle = self.txt("Object-Oriented Programming · OOP", 38)
        rule = Line(LEFT * 4.4, RIGHT * 4.4, color=BLACK, stroke_width=2.2)
        promise = self.txt("Model real ideas. Build your own software project.", 28, color=DARK_GRAY)
        route = self.txt("idea  →  model  →  code  →  test  →  improve  →  present", 23, BOLD, MID_GRAY)

        group = VGroup(kicker, title, subtitle, rule, promise, route).arrange(DOWN, buff=0.28)
        group.move_to(UP * 0.10)
        self.fit(group, 14.2, 7.0)

        self.play(FadeIn(kicker, shift=UP * 0.15), run_time=0.7)
        self.play(Write(title), run_time=1.1)
        self.play(FadeIn(subtitle), Create(rule), run_time=0.8)
        self.play(FadeIn(promise, shift=UP * 0.08), FadeIn(route), run_time=0.9)
        self.wait(2.8)
        self.clear_scene()

    def why_oop(self):
        head = self.section_header(
            1,
            "WHY OBJECT-ORIENTED PROGRAMMING?",
            "OOP organizes a larger program as objects that combine state with behavior.",
        )
        self.add(head)

        messy = VGroup()
        raw_items = ["data_1", "data_2", "function_A", "function_B", "state", "rules"]
        positions = [
            LEFT * 5.25 + UP * 1.40,
            LEFT * 3.25 + UP * 1.40,
            LEFT * 5.25 + UP * 0.15,
            LEFT * 3.25 + UP * 0.15,
            LEFT * 5.25 + DOWN * 1.10,
            LEFT * 3.25 + DOWN * 1.10,
        ]
        for label, pos in zip(raw_items, positions):
            box = RoundedRectangle(
                width=1.65, height=0.64, corner_radius=0.10,
                stroke_color=MID_GRAY, stroke_width=1.5,
                fill_color=PAPER, fill_opacity=1,
            )
            text = self.txt(label, 18).move_to(box)
            messy.add(VGroup(box, text).move_to(pos))

        links = VGroup(
            Line(messy[0].get_right(), messy[3].get_left(), color=LIGHT_GRAY),
            Line(messy[1].get_left(), messy[2].get_right(), color=LIGHT_GRAY),
            Line(messy[2].get_bottom(), messy[5].get_top(), color=LIGHT_GRAY),
            Line(messy[4].get_top(), messy[1].get_bottom(), color=LIGHT_GRAY),
        )
        left_label = self.txt("Scattered pieces", 25, BOLD).next_to(messy, UP, buff=0.30)

        class_box = RoundedRectangle(
            width=5.2, height=3.6, corner_radius=0.18,
            stroke_color=BLACK, stroke_width=2.2,
            fill_color=WHITE, fill_opacity=1,
        )
        class_title = self.txt("CLASS", 31, BOLD)
        divider = Line(LEFT * 2.15, RIGHT * 2.15, color=LIGHT_GRAY)
        attrs = self.txt("Attributes  →  data / state", 23)
        methods = self.txt("Methods  →  actions / behavior", 23)
        class_content = VGroup(class_title, divider, attrs, methods).arrange(DOWN, buff=0.35).move_to(class_box)
        organized = VGroup(class_box, class_content).move_to(RIGHT * 3.65 + DOWN * 0.12)
        right_label = self.txt("One coherent model", 25, BOLD).next_to(organized, UP, buff=0.30)
        arrow = Arrow(LEFT * 0.78, RIGHT * 0.78, color=BLACK, stroke_width=3).move_to(DOWN * 0.06)

        self.play(FadeIn(messy), FadeIn(links), FadeIn(left_label), run_time=0.9)
        self.wait(1.1)
        self.play(GrowArrow(arrow), run_time=0.55)
        self.play(FadeIn(organized, shift=LEFT * 0.22), FadeIn(right_label), run_time=0.9)
        self.wait(2.8)
        self.clear_scene()

    def core_language(self):
        head = self.section_header(
            2,
            "THE FOUR BUILDING BLOCKS",
            "Start with four precise ideas: class, object, attributes, and methods.",
        )
        self.add(head)

        cards = VGroup(
            self.card("CLASS", ["A blueprint that defines", "structure and behavior."], 6.15, 2.05, 29, 22),
            self.card("OBJECT", ["A concrete instance created", "from a class."], 6.15, 2.05, 29, 22),
            self.card("ATTRIBUTES", ["Variables that store the", "object's current state."], 6.15, 2.05, 29, 22),
            self.card("METHODS", ["Functions that define what", "the object can do."], 6.15, 2.05, 29, 22),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.48, 0.40)).move_to(DOWN * 0.20)

        for card in cards:
            self.play(FadeIn(card, shift=UP * 0.15), run_time=0.50)
            self.wait(0.45)
        self.wait(2.2)
        self.clear_scene()

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
            fill_color=PAPER, fill_opacity=1,
        ).move_to(LEFT * 3.75 + DOWN * 0.18)

        code_lines_text = [
            "class Robot:",
            "    def __init__(self, name):",
            "        self.name = name",
            "        self.energy = 100",
            "",
            "    def move(self):",
            "        self.energy -= 10",
            "",
            "explorer = Robot('A1')",
            "explorer.move()",
        ]
        code_lines = VGroup(*[
            Text(line, font="Monospace", font_size=23, color=BLACK)
            for line in code_lines_text
        ]).arrange(DOWN, aligned_edge=LEFT, buff=0.085)
        code_lines.move_to(code_box).align_to(code_box, LEFT).shift(RIGHT * 0.34)
        code_group = VGroup(code_box, code_lines)

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
        status = self.txt("ready to move()", 22, BOLD, MID_GRAY)
        object_content = VGroup(object_title, name_line, energy_row, status).arrange(DOWN, buff=0.31).move_to(object_box)
        object_group = VGroup(object_box, object_content)

        connector = Arrow(
            code_group.get_right() + RIGHT * 0.15,
            object_group.get_left() + LEFT * 0.15,
            buff=0.15, stroke_width=3, color=BLACK,
        )

        create_highlight = SurroundingRectangle(code_lines[8], color=BLACK, buff=0.08, stroke_width=2)
        move_highlight = SurroundingRectangle(code_lines[9], color=BLACK, buff=0.08, stroke_width=2)

        self.play(FadeIn(code_group), run_time=0.9)
        self.play(Create(create_highlight), run_time=0.5)
        self.play(GrowArrow(connector), FadeIn(object_group, shift=LEFT * 0.22), run_time=0.9)
        self.wait(1.0)

        self.play(Transform(create_highlight, move_highlight), run_time=0.55)
        energy_90 = self.txt("90", 24, BOLD).move_to(energy_100)
        moved_status = self.txt("move() changed the state", 22, BOLD).move_to(status)
        self.play(Transform(energy_100, energy_90), Transform(status, moved_status), run_time=0.8)
        self.wait(2.5)
        self.clear_scene()

    def oop_pillars(self):
        head = self.section_header(
            4,
            "THE FOUR OOP PILLARS",
            "These ideas help us control complexity as projects grow.",
        )
        self.add(head)

        center = RoundedRectangle(
            width=3.15, height=1.35, corner_radius=0.16,
            stroke_color=BLACK, stroke_width=2.2,
            fill_color=PAPER, fill_opacity=1,
        )
        center_text = VGroup(self.txt("OBJECT MODEL", 28, BOLD), self.txt("state + behavior", 21)).arrange(DOWN, buff=0.12).move_to(center)
        center_group = VGroup(center, center_text).move_to(DOWN * 0.18)

        pillar_specs = [
            ("ENCAPSULATION", ["Protect internal state", "through clear interfaces."], LEFT * 4.70 + UP * 1.55),
            ("INHERITANCE", ["Reuse a common base", "when an is-a relation fits."], RIGHT * 4.70 + UP * 1.55),
            ("COMPOSITION", ["Build objects from other", "objects with has-a relations."], LEFT * 4.70 + DOWN * 1.95),
            ("POLYMORPHISM", ["Use one interface with", "different implementations."], RIGHT * 4.70 + DOWN * 1.95),
        ]

        cards = VGroup()
        connectors = VGroup()
        for title, lines, pos in pillar_specs:
            c = self.card(title, lines, 4.45, 1.75, 24, 20).move_to(pos)
            cards.add(c)
            connectors.add(Line(center_group.get_center(), c.get_center(), color=LIGHT_GRAY, stroke_width=2))

        self.play(FadeIn(center_group, scale=0.95), run_time=0.7)
        self.play(*[Create(line) for line in connectors], run_time=0.7)
        self.play(LaggedStart(*[FadeIn(c, scale=0.97) for c in cards], lag_ratio=0.14), run_time=1.5)
        self.wait(3.0)
        self.clear_scene()

    def semester_route(self):
        head = self.section_header(
            5,
            "SEMESTER ROADMAP",
            "Each stage adds one capability until you can explain and demonstrate your own working project.",
        )
        self.add(head)

        steps = [
            ("01", "PYTHON BASICS", "control · functions · data"),
            ("02", "OOP MODELING", "classes · objects · state"),
            ("03", "DESIGN", "responsibilities · relations"),
            ("04", "PROTOTYPE", "first working system"),
            ("05", "TEST & IMPROVE", "bugs · refactor · iteration"),
            ("06", "DEMO", "code · explanation · defense"),
        ]

        cards = VGroup()
        for number, title, sub in steps:
            box = RoundedRectangle(
                width=4.25, height=1.70, corner_radius=0.14,
                stroke_color=BLACK, stroke_width=1.7,
                fill_color=WHITE, fill_opacity=1,
            )
            content = VGroup(
                self.txt(number, 21, BOLD, MID_GRAY),
                self.txt(title, 24, BOLD),
                self.txt(sub, 19, color=DARK_GRAY),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.10)
            content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.25)
            cards.add(VGroup(box, content))

        cards.arrange_in_grid(rows=2, cols=3, buff=(0.40, 0.43)).move_to(DOWN * 0.18)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in cards], lag_ratio=0.12), run_time=1.8)
        self.wait(3.0)
        self.clear_scene()

    def individual_projects(self):
        head = self.section_header(
            6,
            "ONE DIFFERENT PROJECT PER STUDENT",
            "You will choose a problem, model it, and build an original solution instead of copying one common exercise.",
        )
        self.add(head)

        center = RoundedRectangle(
            width=4.35, height=1.62, corner_radius=0.16,
            stroke_color=BLACK, stroke_width=2.2,
            fill_color=PAPER, fill_opacity=1,
        )
        center_text = VGroup(
            self.txt("YOUR PROJECT", 32, BOLD),
            self.txt("real problem + programmed solution", 21),
        ).arrange(DOWN, buff=0.12).move_to(center)
        center_group = VGroup(center, center_text).move_to(DOWN * 0.12)

        ideas = [
            ("GAME", LEFT * 5.15 + UP * 1.50),
            ("SIMULATOR", LEFT * 5.15 + DOWN * 1.55),
            ("MANAGER", RIGHT * 5.15 + UP * 1.50),
            ("AUTOMATION", RIGHT * 5.15 + DOWN * 1.55),
            ("DATA APP", UP * 2.20),
            ("TOOL", DOWN * 2.70),
        ]

        nodes = VGroup()
        lines = VGroup()
        for label, pos in ideas:
            box = RoundedRectangle(
                width=2.62, height=0.96, corner_radius=0.13,
                stroke_color=BLACK, stroke_width=1.6,
                fill_color=WHITE, fill_opacity=1,
            )
            node = VGroup(box, self.txt(label, 21, BOLD).move_to(box)).move_to(pos)
            nodes.add(node)
            lines.add(Line(center_group.get_center(), node.get_center(), color=LIGHT_GRAY, stroke_width=2))

        self.play(FadeIn(center_group, scale=0.95), run_time=0.75)
        self.play(*[Create(line) for line in lines], run_time=0.75)
        self.play(LaggedStart(*[FadeIn(n, scale=0.97) for n in nodes], lag_ratio=0.12), run_time=1.6)
        self.wait(3.0)
        self.clear_scene()

    def project_evidence(self):
        head = self.section_header(
            7,
            "WHAT MUST YOUR PROJECT PROVE?",
            "A strong submission shows both a working result and the engineering process behind it.",
        )
        self.add(head)

        top_label = self.divider_label("DESIGN", 2.02)
        bottom_label = self.divider_label("ENGINEERING EVIDENCE", -0.63)

        design_cards = VGroup(
            self.card("1 · PROBLEM", ["Who needs it?", "What does it solve?"], 4.10, 1.55, 24, 20),
            self.card("2 · OOP MODEL", ["Classes · attributes", "methods · relations"], 4.10, 1.55, 24, 20),
            self.card("3 · PROTOTYPE", ["A visible behavior", "that actually works"], 4.10, 1.55, 24, 20),
        ).arrange(RIGHT, buff=0.40).move_to(UP * 0.85)

        evidence_cards = VGroup(
            self.card("4 · ITERATIONS", ["Bugs found", "changes made"], 4.10, 1.55, 24, 20),
            self.card("5 · DOCUMENTATION", ["README · instructions", "design decisions"], 4.10, 1.55, 24, 20),
            self.card("6 · DEMONSTRATION", ["Run it · explain it", "defend your design"], 4.10, 1.55, 24, 20),
        ).arrange(RIGHT, buff=0.40).move_to(DOWN * 1.78)

        self.play(FadeIn(top_label), run_time=0.45)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in design_cards], lag_ratio=0.12), run_time=1.1)
        self.play(FadeIn(bottom_label), run_time=0.45)
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.12) for c in evidence_cards], lag_ratio=0.12), run_time=1.1)
        self.wait(3.1)
        self.clear_scene()

    def closing(self):
        kicker = self.txt("SEMINAR · GRADE 11", 25, BOLD, MID_GRAY)
        title = self.txt("DO NOT COPY A PROJECT.", 47, BOLD)
        title2 = self.txt("BUILD YOUR OWN.", 52, BOLD)
        route = self.txt("Think  →  model  →  code  →  test  →  improve  →  present", 27)
        rule = Line(LEFT * 5.9, RIGHT * 5.9, color=LIGHT_GRAY, stroke_width=2)
        end = self.txt("OOP is the tool. Your project is the evidence.", 30, BOLD)
        group = VGroup(kicker, title, title2, route, rule, end).arrange(DOWN, buff=0.30).move_to(UP * 0.05)
        self.fit(group, 14.2, 7.0)

        self.play(FadeIn(kicker), run_time=0.55)
        self.play(Write(title), run_time=0.9)
        self.play(Write(title2), run_time=0.9)
        self.play(FadeIn(route), Create(rule), run_time=0.8)
        self.play(FadeIn(end), run_time=0.75)
        self.wait(4.0)
