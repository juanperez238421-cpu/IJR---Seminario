from manim import *
import importlib.util
from pathlib import Path

_BASE_PATH = Path(__file__).with_name("seminar11_oop_immersive_v8_payload.py")
_SPEC = importlib.util.spec_from_file_location("oop_v8_base", _BASE_PATH)
_BASE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_BASE)

for _name in [
    "RUN_Q", "RUN_N", "RUN_S", "PAUSE_S", "PAUSE_R", "PAUSE_E",
    "PAPER", "LIGHT_GRAY", "DARK_GRAY", "MID_GRAY",
]:
    globals()[_name] = getattr(_BASE, _name)


class Seminar11OOPImmersiveV9(_BASE.Seminar11OOPImmersiveV8):
    """QA-corrected senior immersive OOP lesson."""

    def real_object_to_model(self):
        self.set_header(
            1,
            "START WITH A REAL OBJECT",
            "OOP begins by asking two questions: what does this object know, and what can this object do?",
        )

        bot = self.robot(1.35).move_to(LEFT * 1.25 + DOWN * 0.45)
        ground = Line(LEFT * 6.6, RIGHT * 6.2, color=LIGHT_GRAY, stroke_width=2.2).move_to(DOWN * 2.65)
        name = self.label_pill("ATTRIBUTE", "name = Atlas").move_to(RIGHT * 4.45 + UP * 1.25)
        energy = self.label_pill("ATTRIBUTE", "energy = 100").move_to(RIGHT * 4.45 + UP * 0.10)
        position = self.label_pill("ATTRIBUTE", "position = 0").move_to(RIGHT * 4.45 + DOWN * 1.05)
        state_group = VGroup(name, energy, position)
        arrows = VGroup(
            Arrow(bot.get_right() + UP * 0.72, name.get_left(), buff=0.15, color=LIGHT_GRAY, stroke_width=2.5),
            Arrow(bot.get_right() + UP * 0.10, energy.get_left(), buff=0.15, color=LIGHT_GRAY, stroke_width=2.5),
            Arrow(bot.get_right() + DOWN * 0.60, position.get_left(), buff=0.15, color=LIGHT_GRAY, stroke_width=2.5),
        )
        q1 = self.text("WHAT DOES IT KNOW?", 27, BOLD, MID_GRAY).next_to(state_group, UP, buff=0.28)

        self.play(Create(ground), FadeIn(bot, shift=UP * 0.20), run_time=RUN_N)
        self.play(FadeIn(q1), run_time=RUN_Q)
        self.play(
            LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.16),
            LaggedStart(*[FadeIn(m, shift=LEFT * 0.12) for m in state_group], lag_ratio=0.16),
            run_time=RUN_S,
        )
        self.wait(PAUSE_R)
        self.play(FadeOut(arrows), run_time=RUN_Q)

        move_chip = self.chip("move()", width=2.1, height=0.72, size=25, fill=PAPER).move_to(RIGHT * 4.45 + DOWN * 2.25)
        q2 = self.text("WHAT CAN IT DO?", 25, BOLD, MID_GRAY).next_to(move_chip, LEFT, buff=0.28)
        self.play(FadeIn(q2), FadeIn(move_chip, scale=0.92), run_time=RUN_Q)

        bot_target = bot.copy().shift(RIGHT * 1.15)
        energy_new = self.label_pill("ATTRIBUTE", "energy = 90").move_to(energy)
        position_new = self.label_pill("ATTRIBUTE", "position = 1").move_to(position)
        self.play(
            Transform(bot, bot_target),
            Transform(energy, energy_new),
            Transform(position, position_new),
            Indicate(move_chip, color=BLACK),
            run_time=RUN_S,
        )
        self.wait(PAUSE_R)

        model_label = self.text("CLASS Robot", 31, BOLD)
        boundary = RoundedRectangle(
            width=6.1, height=5.15, corner_radius=0.26,
            stroke_color=BLACK, stroke_width=2.5,
            fill_color=PAPER, fill_opacity=0.40,
        ).move_to(VGroup(bot, state_group, move_chip).get_center() + LEFT * 0.15)
        model_label.next_to(boundary.get_top(), DOWN, buff=0.22)
        state_tag = self.chip("STATE", width=1.65, size=19, fill=WHITE).move_to(boundary.get_corner(UR) + LEFT * 0.95 + DOWN * 0.42)
        behavior_tag = self.chip("BEHAVIOR", width=2.05, size=19, fill=WHITE).move_to(boundary.get_corner(DR) + LEFT * 1.15 + UP * 0.45)

        self.play(Create(boundary), FadeIn(model_label), FadeIn(state_tag), FadeIn(behavior_tag), run_time=RUN_N)
        self.wait(PAUSE_R)
        model_group = VGroup(boundary, model_label, state_tag, behavior_tag, bot, name, energy, position, move_chip)
        self.camera_focus(model_group, width=7.3, pause=PAUSE_R)
        summary = self.text("A class is a reusable model of state + behavior.", 30, BOLD).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(summary, shift=UP * 0.08), run_time=RUN_N)
        self.wait(PAUSE_E)
        self.clear_all()

    def composition(self):
        self.set_header(
            6,
            "COMPOSITION: OBJECTS COOPERATE TO CREATE A SYSTEM",
            "A useful application emerges when small objects exchange messages while each one keeps a clear responsibility.",
        )

        floor = RoundedRectangle(
            width=13.9, height=5.30, corner_radius=0.20,
            stroke_color=BLACK, stroke_width=2.2,
            fill_color=PAPER, fill_opacity=0.55,
        ).move_to(DOWN * 0.45)
        title = self.text("SMART WAREHOUSE", 27, BOLD, MID_GRAY).next_to(floor.get_top(), DOWN, buff=0.20)

        order = self.order_card(0.82).move_to(LEFT * 5.35 + UP * 0.55)
        inventory = self.server("Inventory", 0.82).move_to(LEFT * 2.10 + UP * 0.45)
        robot = self.robot(0.70).move_to(RIGHT * 1.10 + DOWN * 0.85)
        package = self.package(0.85).next_to(robot, RIGHT, buff=0.12).shift(DOWN * 0.05)
        sensor = self.sensor(0.85).move_to(RIGHT * 5.15 + DOWN * 0.35)
        dock = RoundedRectangle(width=1.70, height=0.85, corner_radius=0.12, stroke_color=BLACK, stroke_width=2, fill_color=WHITE, fill_opacity=1).move_to(RIGHT * 5.05 + DOWN * 2.05)
        dock_label = self.text("DOCK", 18, BOLD, MID_GRAY).move_to(dock)

        labels = VGroup(
            self.text("receives requests", 18, color=MID_GRAY).next_to(order, DOWN, buff=0.12),
            self.text("owns stock", 18, color=MID_GRAY).next_to(inventory, DOWN, buff=0.12),
            self.text("moves products", 18, color=MID_GRAY).next_to(robot, DOWN, buff=0.14),
            self.text("reports position", 18, color=MID_GRAY).next_to(sensor, UP, buff=0.12),
        )
        self.assert_content_safe(VGroup(floor, order, inventory, robot, package, sensor, dock), "warehouse system")

        self.play(Create(floor), FadeIn(title), run_time=RUN_N)
        self.play(LaggedStart(FadeIn(order), FadeIn(inventory), FadeIn(robot), FadeIn(package), FadeIn(sensor), FadeIn(dock), lag_ratio=0.10), FadeIn(labels), run_time=RUN_S)
        self.wait(PAUSE_S)

        p_order = Dot(radius=0.11, color=BLACK).move_to(order.get_right())
        route1 = Line(order.get_right(), inventory.get_left(), color=LIGHT_GRAY, stroke_width=2.2)
        msg1 = self.chip("reserve item", width=2.05, size=17, fill=WHITE).next_to(route1, DOWN, buff=0.10)
        self.play(Create(route1), FadeIn(msg1), FadeIn(p_order), run_time=RUN_Q)
        self.play(MoveAlongPath(p_order, route1), run_time=RUN_N)
        self.play(FadeOut(p_order), Indicate(inventory, color=BLACK), run_time=RUN_Q)

        stock_new = self.text("stock = 2", 19, BOLD, DARK_GRAY).move_to(labels[1])
        self.play(Transform(labels[1], stock_new), run_time=RUN_N)

        p_task = Dot(radius=0.11, color=BLACK).move_to(inventory.get_right())
        route2 = Line(inventory.get_right(), robot.get_left() + UP * 0.30, color=LIGHT_GRAY, stroke_width=2.2)
        msg2 = self.chip("pick + deliver", width=2.15, size=17, fill=WHITE).next_to(route2, DOWN, buff=0.10)
        self.play(Create(route2), FadeIn(msg2), FadeIn(p_task), run_time=RUN_Q)
        self.play(MoveAlongPath(p_task, route2), run_time=RUN_N)
        self.play(FadeOut(p_task), Indicate(robot, color=BLACK), run_time=RUN_Q)
        self.play(FadeOut(route2), FadeOut(msg2), FadeOut(labels[2]), run_time=RUN_Q)

        moving_unit = VGroup(robot, package)
        travel = ArcBetweenPoints(moving_unit.get_center(), dock.get_center() + LEFT * 0.85 + UP * 0.20, angle=-PI / 10)
        self.play(MoveAlongPath(moving_unit, travel), run_time=2.0, rate_func=smooth)
        self.play(Indicate(dock, color=BLACK), run_time=RUN_Q)

        scan = DashedLine(sensor.get_center() + LEFT * 0.10, robot.get_center(), color=LIGHT_GRAY, dash_length=0.12)
        pos = self.chip("position = dock", width=2.30, size=18, fill=WHITE).next_to(sensor, LEFT, buff=0.25)
        self.play(Create(scan), FadeIn(pos), run_time=RUN_N)
        self.wait(PAUSE_R)

        system_summary = self.text("Order → Inventory → Robot → Sensor: four objects, one working system.", 28, BOLD).to_edge(DOWN, buff=0.38)
        self.play(FadeIn(system_summary), run_time=RUN_N)
        self.wait(PAUSE_E)
        self.clear_all()

    def think_in_objects(self):
        self.set_header(
            7,
            "THINK IN OBJECTS BEFORE YOU WRITE CODE",
            "A strong OOP project starts by identifying the things in the problem and assigning each one a clear responsibility.",
        )

        problem = self.text(
            "A smart garden reads soil moisture and turns on a pump when plants need water.",
            31, BOLD,
        )
        self.fit(problem, 13.4, 0.70)
        problem.move_to(UP * 1.50)
        prompt = self.text("What objects exist?", 24, BOLD, MID_GRAY).next_to(problem, DOWN, buff=0.30)
        self.play(Write(problem), FadeIn(prompt), run_time=RUN_S)
        self.wait(PAUSE_R)

        object_names = ["Garden", "MoistureSensor", "Pump", "Controller"]
        responsibilities = ["stores configuration", "reads moisture", "moves water", "decides what happens"]
        xs = [-5.0, -1.7, 1.7, 5.0]
        cards = VGroup()
        for x, name, resp in zip(xs, object_names, responsibilities):
            icon = Circle(radius=0.55, stroke_color=BLACK, stroke_width=2.1, fill_color=PAPER, fill_opacity=1)
            letter = self.text(name[0], 26, BOLD).move_to(icon)
            name_m = self.text(name, 23, BOLD)
            resp_m = self.text(resp, 18, color=DARK_GRAY)
            content = VGroup(VGroup(icon, letter), name_m, resp_m).arrange(DOWN, buff=0.12)
            box = RoundedRectangle(width=3.0, height=2.45, corner_radius=0.18, stroke_color=BLACK, stroke_width=1.9, fill_color=WHITE, fill_opacity=1)
            content.move_to(box)
            card = VGroup(box, content).move_to([x, -0.55, 0])
            cards.add(card)

        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.16) for c in cards], lag_ratio=0.18), run_time=RUN_S)
        self.wait(PAUSE_S)

        def bus(source, target, y_bus):
            p1 = source.get_bottom()
            p2 = target.get_bottom()
            leg1 = Line(p1, [p1[0], y_bus, 0], color=LIGHT_GRAY, stroke_width=2.0)
            mid = Arrow([p1[0], y_bus, 0], [p2[0], y_bus, 0], buff=0.08, color=LIGHT_GRAY, stroke_width=2.2)
            leg2 = Line([p2[0], y_bus, 0], p2, color=LIGHT_GRAY, stroke_width=2.0)
            return VGroup(leg1, mid, leg2)

        sensor_to_controller = bus(cards[1], cards[3], -2.10)
        controller_to_pump = bus(cards[3], cards[2], -2.38)
        pump_to_garden = bus(cards[2], cards[0], -2.66)
        connections = VGroup(sensor_to_controller, controller_to_pump, pump_to_garden)
        connection_labels = VGroup(
            self.text("moisture data", 17, BOLD, MID_GRAY).move_to([-0.05, -2.03, 0]),
            self.text("pump command", 17, BOLD, MID_GRAY).move_to([3.35, -2.31, 0]),
            self.text("water flow", 17, BOLD, MID_GRAY).move_to([-1.65, -2.59, 0]),
        )
        self.play(
            LaggedStart(*[Create(c) for c in connections], lag_ratio=0.18),
            LaggedStart(*[FadeIn(l) for l in connection_labels], lag_ratio=0.18),
            run_time=RUN_S,
        )

        flow = self.text("PROBLEM → OBJECTS → RESPONSIBILITIES → RELATIONSHIPS → CODE", 27, BOLD).to_edge(DOWN, buff=0.34)
        self.play(FadeIn(flow, shift=UP * 0.08), run_time=RUN_N)
        self.wait(PAUSE_E)
        self.clear_all()
