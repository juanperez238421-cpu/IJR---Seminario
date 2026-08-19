from manim import *

# =============================================================================
# JP CLASSROOM / MANIMCE 0.20.x RENDER CONTRACT
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
PAPER = "#F8F8F8"
VERY_LIGHT = "#F0F0F0"

SAFE_W = 14.7
SAFE_H = 7.6


class Seminar11OOPVisualConcepts(MovingCameraScene):
    """Visual OOP lesson for Grade 11 Seminar.

    QA contract:
    - 100% English visible instructional content.
    - 1920x1080, 30 fps, white classroom background.
    - Main concepts are explained through evolving UML-like rectangles,
      not static vocabulary cards.
    - OOP usefulness is demonstrated through reuse, independent object state,
      inheritance, polymorphism, and composition.
    - Typography and objects remain inside a conservative 16:9 safe zone.
    """

    def txt(self, text, size=30, weight=NORMAL, color=BLACK_TEXT, font=None):
        kw = dict(font_size=size, weight=weight, color=color, line_spacing=0.92)
        if font:
            kw["font"] = font
        return Text(text, **kw)

    def fit(self, mob, max_w=SAFE_W, max_h=SAFE_H):
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
        n = self.txt(f"{number:02d}", 24, BOLD).move_to(badge)
        title_m = self.txt(title, 35, BOLD)
        self.fit(title_m, 13.4, 0.62)
        row = VGroup(VGroup(badge, n), title_m).arrange(RIGHT, buff=0.28)
        row.to_edge(UP, buff=0.17).to_edge(LEFT, buff=0.48)
        rule = Line(LEFT * 7.42, RIGHT * 7.42, color=LIGHT_GRAY, stroke_width=2)
        rule.next_to(row, DOWN, buff=0.07)
        sub = self.txt(subtitle, 21, color=DARK_GRAY)
        self.fit(sub, 14.1, 0.60)
        sub.next_to(rule, DOWN, buff=0.09).align_to(row, LEFT)
        return VGroup(row, rule, sub)

    def clear_scene(self, run_time=0.55):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=run_time)
        self.camera.frame.set(width=16).move_to(ORIGIN)

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

        attr_label = self.txt("ATTRIBUTES", 18, BOLD, MID_GRAY)
        attr_label.move_to([x_l + 0.72, title_div_y - 0.27, 0])
        attr_group = VGroup(*[self.txt(a, body_size, color=DARK_GRAY) for a in attributes])
        attr_group.arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        self.fit(attr_group, width - 0.55, 1.05)
        attr_group.move_to([box.get_center()[0], title_div_y - 0.98, 0]).align_to(box, LEFT).shift(RIGHT * 0.28)

        method_label = self.txt("METHODS", 18, BOLD, MID_GRAY)
        method_label.move_to([x_l + 0.57, attr_div_y - 0.27, 0])
        method_group = VGroup(*[self.txt(m, body_size, color=DARK_GRAY) for m in methods])
        method_group.arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        self.fit(method_group, width - 0.55, 1.45)
        method_group.move_to([box.get_center()[0], attr_div_y - 1.05, 0]).align_to(box, LEFT).shift(RIGHT * 0.28)

        return VGroup(box, line1, line2, title, attr_label, attr_group, method_label, method_group)

    def object_card(self, name, state_lines, method_text="move()", width=3.6, height=2.35):
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.14,
            stroke_color=BLACK, stroke_width=2,
            fill_color=WHITE, fill_opacity=1,
        )
        title = self.txt(name, 25, BOLD)
        state = VGroup(*[self.txt(s, 21, color=DARK_GRAY) for s in state_lines]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08
        )
        method = self.txt(method_text, 20, BOLD, MID_GRAY)
        content = VGroup(title, state, method).arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        self.fit(content, width - 0.45, height - 0.28)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.24)
        return VGroup(box, content)

    def simple_box(self, title, body, width=3.5, height=1.55):
        box = RoundedRectangle(
            width=width, height=height, corner_radius=0.13,
            stroke_color=BLACK, stroke_width=1.8,
            fill_color=WHITE, fill_opacity=1,
        )
        t = self.txt(title, 24, BOLD)
        b = self.txt(body, 20, color=DARK_GRAY)
        self.fit(b, width - 0.40, 0.52)
        content = VGroup(t, b).arrange(DOWN, buff=0.12).move_to(box)
        return VGroup(box, content)

    def construct(self):
        self.opening()
        self.class_blueprint()
        self.objects_from_class()
        self.encapsulation_usefulness()
        self.inheritance()
        self.polymorphism()
        self.composition_system()
        self.project_path()
        self.closing()

    def opening(self):
        kicker = self.txt("SEMINAR · GRADE 11", 26, BOLD, MID_GRAY)
        title = self.txt("WHY OBJECT-ORIENTED PROGRAMMING?", 53, BOLD)
        subtitle = self.txt("Build software by modeling objects, responsibilities, and relationships.", 29, color=DARK_GRAY)
        route = self.txt("CLASS  →  OBJECTS  →  INHERITANCE  →  SYSTEM", 25, BOLD, MID_GRAY)
        rule = Line(LEFT * 4.65, RIGHT * 4.65, color=BLACK, stroke_width=2.2)
        group = VGroup(kicker, title, subtitle, rule, route).arrange(DOWN, buff=0.34).move_to(UP * 0.05)
        self.fit(group, 14.4, 6.6)

        self.play(FadeIn(kicker, shift=UP * 0.12), run_time=0.7)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle), Create(rule), run_time=0.9)
        self.play(FadeIn(route, shift=UP * 0.08), run_time=0.8)
        self.wait(2.5)
        self.clear_scene()

    def class_blueprint(self):
        head = self.section_header(
            1,
            "A CLASS IS A BLUEPRINT",
            "A class puts data and behavior in one model so the program has a clear structure.",
        )
        self.add(head)

        outer = RoundedRectangle(
            width=6.0, height=4.95, corner_radius=0.14,
            stroke_color=BLACK, stroke_width=2.4,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(LEFT * 1.25 + DOWN * 0.18)
        class_name = self.txt("Robot", 36, BOLD).move_to(outer.get_top() + DOWN * 0.52)
        name_hint = self.txt("WHAT IT IS", 19, BOLD, MID_GRAY).next_to(class_name, RIGHT, buff=0.35)

        div1 = Line(outer.get_left() + UP * 1.48, outer.get_right() + UP * 1.48, color=BLACK, stroke_width=1.8)
        div2 = Line(outer.get_left() + DOWN * 0.15, outer.get_right() + DOWN * 0.15, color=BLACK, stroke_width=1.8)

        attr_title = self.txt("ATTRIBUTES", 22, BOLD)
        attrs = VGroup(
            self.txt("name", 25),
            self.txt("energy", 25),
            self.txt("position", 25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        attr_group = VGroup(attr_title, attrs).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        attr_group.move_to(outer.get_center() + UP * 0.70).align_to(outer, LEFT).shift(RIGHT * 0.40)
        attr_hint = self.txt("WHAT IT HAS", 19, BOLD, MID_GRAY).move_to(outer.get_center() + RIGHT * 1.70 + UP * 0.72)

        method_title = self.txt("METHODS", 22, BOLD)
        methods = VGroup(
            self.txt("move()", 25),
            self.txt("recharge()", 25),
            self.txt("report_status()", 25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        method_group = VGroup(method_title, methods).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        method_group.move_to(outer.get_center() + DOWN * 1.40).align_to(outer, LEFT).shift(RIGHT * 0.40)
        method_hint = self.txt("WHAT IT CAN DO", 19, BOLD, MID_GRAY).move_to(outer.get_center() + RIGHT * 1.55 + DOWN * 1.35)

        right_note = VGroup(
            self.txt("ONE RECTANGLE", 28, BOLD),
            self.txt("one responsibility", 24, color=DARK_GRAY),
            self.txt("state + behavior", 24, color=DARK_GRAY),
        ).arrange(DOWN, buff=0.18).move_to(RIGHT * 4.65)
        arrow = Arrow(outer.get_right() + RIGHT * 0.25, right_note.get_left() + LEFT * 0.20, buff=0.18, color=BLACK)

        self.play(Create(outer), FadeIn(class_name), FadeIn(name_hint), run_time=0.9)
        self.wait(0.7)
        self.play(Create(div1), FadeIn(attr_group, shift=UP * 0.08), FadeIn(attr_hint), run_time=0.9)
        self.wait(0.8)
        self.play(Create(div2), FadeIn(method_group, shift=UP * 0.08), FadeIn(method_hint), run_time=0.9)
        self.wait(1.0)
        self.play(GrowArrow(arrow), FadeIn(right_note, shift=LEFT * 0.18), run_time=0.9)
        self.wait(2.2)
        self.clear_scene()

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
            width=3.8, height=4.2, title_size=29, body_size=21, fill=PAPER,
        ).move_to(LEFT * 5.25 + DOWN * 0.25)
        bp_label = self.txt("CLASS", 20, BOLD, MID_GRAY).next_to(blueprint, UP, buff=0.18)

        objs = VGroup(
            self.object_card("explorer", ["energy = 100", "position = 0"], width=3.25),
            self.object_card("courier", ["energy = 65", "position = 12"], width=3.25),
            self.object_card("scout", ["energy = 80", "position = 4"], width=3.25),
        ).arrange(DOWN, buff=0.26).move_to(RIGHT * 3.15 + DOWN * 0.23)

        arrows = VGroup(*[
            Arrow(blueprint.get_right() + RIGHT * 0.1, obj.get_left() + LEFT * 0.1, buff=0.18, color=LIGHT_GRAY, stroke_width=2.5)
            for obj in objs
        ])
        caption = self.txt("Same methods. Different data. Independent objects.", 25, BOLD)
        caption.to_edge(DOWN, buff=0.50)

        self.play(FadeIn(blueprint), FadeIn(bp_label), run_time=0.9)
        self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.18), run_time=1.1)
        self.play(LaggedStart(*[FadeIn(o, shift=LEFT * 0.15) for o in objs], lag_ratio=0.18), run_time=1.4)
        self.wait(1.0)

        ex_energy = objs[0][1][1][0]
        changed = self.txt("energy = 90", 21, color=DARK_GRAY).move_to(ex_energy)
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

        left_title = self.txt("WITHOUT A MODEL", 24, BOLD, MID_GRAY).move_to(LEFT * 4.55 + UP * 2.0)
        raw = VGroup(
            self.simple_box("robot_energy", "variable", 2.65, 1.12),
            self.simple_box("robot_position", "variable", 2.65, 1.12),
            self.simple_box("move_robot()", "function", 2.65, 1.12),
            self.simple_box("charge_robot()", "function", 2.65, 1.12),
        ).arrange_in_grid(rows=2, cols=2, buff=(0.28, 0.28)).move_to(LEFT * 4.25 + DOWN * 0.05)
        tangle = VGroup(
            Line(raw[0].get_right(), raw[3].get_left(), color=LIGHT_GRAY),
            Line(raw[1].get_right(), raw[2].get_left(), color=LIGHT_GRAY),
            Line(raw[0].get_bottom(), raw[2].get_top(), color=LIGHT_GRAY),
        )

        right_title = self.txt("WITH OOP", 24, BOLD, MID_GRAY).move_to(RIGHT * 4.25 + UP * 2.0)
        robot = self.uml_class(
            "Robot",
            ["energy", "position"],
            ["move()", "recharge()"],
            width=4.8, height=4.0, body_size=23, fill=PAPER,
        ).move_to(RIGHT * 4.1 + DOWN * 0.10)
        arrow = Arrow(LEFT * 0.72, RIGHT * 0.72, color=BLACK, stroke_width=3).move_to(DOWN * 0.10)
        result = self.txt("The object owns its data and the actions that change it.", 24, BOLD)
        self.fit(result, 12.8, 0.55)
        result.to_edge(DOWN, buff=0.48)

        self.play(FadeIn(left_title), FadeIn(raw), FadeIn(tangle), run_time=1.0)
        self.wait(1.1)
        self.play(GrowArrow(arrow), run_time=0.55)
        self.play(FadeIn(right_title), FadeIn(robot, shift=LEFT * 0.18), run_time=1.0)
        self.play(FadeIn(result), run_time=0.75)
        self.wait(2.4)
        self.clear_scene()

    def inheritance(self):
        head = self.section_header(
            4,
            "INHERITANCE: REUSE A GENERAL MODEL",
            "A child class receives shared attributes and methods, then adds only what makes it different.",
        )
        self.add(head)

        parent = self.uml_class(
            "Vehicle",
            ["speed", "position"],
            ["move()", "stop()"],
            width=4.55, height=4.25, body_size=22, fill=PAPER,
        ).move_to(LEFT * 4.35 + DOWN * 0.20)
        parent_tag = self.txt("PARENT CLASS", 20, BOLD, MID_GRAY).next_to(parent, UP, buff=0.16)

        robot = self.simple_box(
            "Robot", "adds: energy + recharge()", 4.45, 1.65
        ).move_to(RIGHT * 3.65 + UP * 1.10)
        drone = self.simple_box(
            "Drone", "adds: altitude + take_off()", 4.45, 1.65
        ).move_to(RIGHT * 3.65 + DOWN * 1.42)

        robot_tag = self.txt("CHILD CLASS", 18, BOLD, MID_GRAY).next_to(robot, UP, buff=0.11)
        drone_tag = self.txt("CHILD CLASS", 18, BOLD, MID_GRAY).next_to(drone, UP, buff=0.11)

        ar1 = Arrow(parent.get_right() + UP * 0.65, robot.get_left(), buff=0.15, color=BLACK, stroke_width=2.6)
        ar2 = Arrow(parent.get_right() + DOWN * 0.65, drone.get_left(), buff=0.15, color=BLACK, stroke_width=2.6)

        inherited1 = self.txt("inherits: speed · position · move() · stop()", 19, BOLD, MID_GRAY)
        inherited1.next_to(robot, DOWN, buff=0.10)
        inherited2 = self.txt("inherits: speed · position · move() · stop()", 19, BOLD, MID_GRAY)
        inherited2.next_to(drone, DOWN, buff=0.10)
        self.fit(inherited1, 5.3, 0.40)
        self.fit(inherited2, 5.3, 0.40)

        benefit = self.txt("Write shared behavior once. Extend only what changes.", 24, BOLD)
        benefit.to_edge(DOWN, buff=0.45)

        self.play(FadeIn(parent), FadeIn(parent_tag), run_time=0.9)
        self.wait(0.8)
        self.play(GrowArrow(ar1), GrowArrow(ar2), run_time=0.8)
        self.play(
            FadeIn(robot, shift=LEFT * 0.15), FadeIn(drone, shift=LEFT * 0.15),
            FadeIn(robot_tag), FadeIn(drone_tag), run_time=1.0
        )
        self.play(FadeIn(inherited1), FadeIn(inherited2), FadeIn(benefit), run_time=0.9)
        self.wait(2.5)
        self.clear_scene()

    def polymorphism(self):
        head = self.section_header(
            5,
            "POLYMORPHISM: ONE COMMAND, DIFFERENT BEHAVIOR",
            "The program can call the same method on different objects without knowing every implementation detail.",
        )
        self.add(head)

        command = RoundedRectangle(
            width=3.4, height=1.25, corner_radius=0.15,
            stroke_color=BLACK, stroke_width=2.2,
            fill_color=PAPER, fill_opacity=1,
        ).move_to(UP * 1.85)
        command_text = self.txt("vehicle.move()", 28, BOLD, font="Monospace").move_to(command)
        command_group = VGroup(command, command_text)

        robot = self.simple_box("Robot", "rolls on the floor", 4.1, 1.55).move_to(LEFT * 3.8 + DOWN * 0.45)
        drone = self.simple_box("Drone", "flies through the air", 4.1, 1.55).move_to(RIGHT * 3.8 + DOWN * 0.45)
        arrows = VGroup(
            Arrow(command_group.get_bottom() + LEFT * 0.55, robot.get_top(), buff=0.15, color=BLACK),
            Arrow(command_group.get_bottom() + RIGHT * 0.55, drone.get_top(), buff=0.15, color=BLACK),
        )
        same = self.txt("SAME INTERFACE", 22, BOLD, MID_GRAY).next_to(command_group, RIGHT, buff=0.35)
        different = self.txt("DIFFERENT IMPLEMENTATIONS", 24, BOLD).to_edge(DOWN, buff=0.85)
        benefit = self.txt("Useful when a project grows: new child classes can plug into existing code.", 22, color=DARK_GRAY)
        benefit.to_edge(DOWN, buff=0.40)

        self.play(FadeIn(command_group), FadeIn(same), run_time=0.8)
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), run_time=0.8)
        self.play(FadeIn(robot, shift=UP * 0.12), FadeIn(drone, shift=UP * 0.12), run_time=1.0)
        self.play(FadeIn(different), FadeIn(benefit), run_time=0.8)
        self.wait(2.5)
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
            fill_color=PAPER, fill_opacity=1,
        ).move_to(DOWN * 0.22)
        system_title = self.txt("SMART WAREHOUSE PROJECT", 29, BOLD).move_to(system.get_top() + DOWN * 0.40)
        system_rule = Line(system.get_left() + UP * 1.60, system.get_right() + UP * 1.60, color=LIGHT_GRAY, stroke_width=2)

        boxes = VGroup(
            self.simple_box("Robot", "moves products", 2.55, 1.55),
            self.simple_box("Inventory", "tracks stock", 2.55, 1.55),
            self.simple_box("Order", "stores requests", 2.55, 1.55),
            self.simple_box("Sensor", "reports position", 2.55, 1.55),
        ).arrange(RIGHT, buff=0.34).move_to(DOWN * 0.10)

        links = VGroup(
            Arrow(boxes[0].get_right(), boxes[1].get_left(), buff=0.12, color=BLACK, stroke_width=2.2),
            Arrow(boxes[1].get_right(), boxes[2].get_left(), buff=0.12, color=BLACK, stroke_width=2.2),
            Arrow(boxes[3].get_top(), boxes[0].get_bottom(), buff=0.16, color=LIGHT_GRAY, stroke_width=2.2),
        )
        responsibility = self.txt("Small classes cooperate → a larger useful system emerges.", 25, BOLD)
        responsibility.next_to(system, DOWN, buff=0.20)

        self.play(Create(system), FadeIn(system_title), Create(system_rule), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.12) for b in boxes], lag_ratio=0.16), run_time=1.5)
        self.play(LaggedStart(*[GrowArrow(a) for a in links], lag_ratio=0.18), run_time=1.1)
        self.play(FadeIn(responsibility), run_time=0.75)
        self.wait(2.5)
        self.clear_scene()

    def project_path(self):
        head = self.section_header(
            7,
            "TURN A REAL PROBLEM INTO AN OOP PROJECT",
            "Start from responsibilities, not from a giant file full of unrelated functions.",
        )
        self.add(head)

        stages = [
            ("1", "PROBLEM", "What should it solve?"),
            ("2", "NOUNS", "What objects exist?"),
            ("3", "CLASSES", "What belongs together?"),
            ("4", "RELATIONSHIPS", "How do classes connect?"),
            ("5", "PROTOTYPE", "Code, test, improve."),
        ]
        cards = VGroup()
        for num, title, body in stages:
            box = RoundedRectangle(
                width=2.72, height=2.25, corner_radius=0.14,
                stroke_color=BLACK, stroke_width=1.8,
                fill_color=WHITE, fill_opacity=1,
            )
            n = self.txt(num, 22, BOLD, MID_GRAY)
            t = self.txt(title, 22, BOLD)
            b = self.txt(body, 18, color=DARK_GRAY)
            self.fit(b, 2.28, 0.84)
            content = VGroup(n, t, b).arrange(DOWN, buff=0.12).move_to(box)
            cards.add(VGroup(box, content))
        cards.arrange(RIGHT, buff=0.18).move_to(DOWN * 0.10)

        arrows = VGroup(*[
            Arrow(cards[i].get_right(), cards[i + 1].get_left(), buff=0.10, color=LIGHT_GRAY, stroke_width=2.1)
            for i in range(len(cards) - 1)
        ])
        final = self.txt("Your individual project should have its own problem, model, code, and evidence.", 24, BOLD)
        self.fit(final, 13.6, 0.55)
        final.to_edge(DOWN, buff=0.58)

        for i, card in enumerate(cards):
            self.play(FadeIn(card, shift=UP * 0.10), run_time=0.48)
            if i < len(arrows):
                self.play(GrowArrow(arrows[i]), run_time=0.28)
        self.play(FadeIn(final), run_time=0.8)
        self.wait(2.8)
        self.clear_scene()

    def closing(self):
        kicker = self.txt("OBJECT-ORIENTED PROGRAMMING", 25, BOLD, MID_GRAY)
        line1 = self.txt("MODEL THE WORLD.", 51, BOLD)
        line2 = self.txt("GIVE EACH OBJECT A RESPONSIBILITY.", 42, BOLD)
        rule = Line(LEFT * 4.8, RIGHT * 4.8, color=BLACK, stroke_width=2.2)
        summary = self.txt("Class → objects → inheritance → polymorphism → composition", 25, BOLD, DARK_GRAY)
        outcome = self.txt("Then use those ideas to build a project that is uniquely yours.", 27, color=DARK_GRAY)
        group = VGroup(kicker, line1, line2, rule, summary, outcome).arrange(DOWN, buff=0.30).move_to(UP * 0.05)
        self.fit(group, 14.2, 7.0)

        self.play(FadeIn(kicker), run_time=0.6)
        self.play(Write(line1), run_time=1.0)
        self.play(Write(line2), run_time=1.0)
        self.play(Create(rule), FadeIn(summary), run_time=0.8)
        self.play(FadeIn(outcome, shift=UP * 0.08), run_time=0.8)
        self.wait(4.0)
