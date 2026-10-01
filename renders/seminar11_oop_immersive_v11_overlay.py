from manim import *
import importlib.util
from pathlib import Path

_BASE_PATH = Path(__file__).with_name("seminar11_oop_immersive_v10_overlay.py")
_SPEC = importlib.util.spec_from_file_location("oop_v10_base", _BASE_PATH)
_BASE = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_BASE)

for _name in [
    "RUN_Q", "RUN_N", "RUN_S", "PAUSE_S", "PAUSE_R", "PAUSE_E",
    "PAPER", "LIGHT_GRAY", "DARK_GRAY", "MID_GRAY",
]:
    globals()[_name] = getattr(_BASE, _name)


class Seminar11OOPImmersiveV11(_BASE.Seminar11OOPImmersiveV10):
    """Final composition QA: dedicated message monitor and visible dock label."""

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
        title = self.text("SMART WAREHOUSE", 27, BOLD, MID_GRAY).next_to(
            floor.get_top(), DOWN, buff=0.20
        )

        order = self.order_card(0.82).move_to(LEFT * 5.35 + UP * 0.55)
        inventory = self.server("Inventory", 0.82).move_to(LEFT * 2.10 + UP * 0.45)
        robot = self.robot(0.70).move_to(RIGHT * 1.10 + DOWN * 0.85)
        package = self.package(0.85).next_to(robot, RIGHT, buff=0.12).shift(DOWN * 0.05)
        sensor = self.sensor(0.85).move_to(RIGHT * 5.15 + DOWN * 0.35)
        dock = RoundedRectangle(
            width=1.70, height=0.85, corner_radius=0.12,
            stroke_color=BLACK, stroke_width=2,
            fill_color=WHITE, fill_opacity=1,
        ).move_to(RIGHT * 5.05 + DOWN * 2.05)
        dock_label = self.text("DOCK", 18, BOLD, MID_GRAY).move_to(dock)

        labels = VGroup(
            self.text("receives requests", 18, color=MID_GRAY).next_to(order, DOWN, buff=0.12),
            self.text("owns stock", 18, color=MID_GRAY).next_to(inventory, DOWN, buff=0.12),
            self.text("moves products", 18, color=MID_GRAY).next_to(robot, DOWN, buff=0.14),
            self.text("reports position", 18, color=MID_GRAY).next_to(sensor, UP, buff=0.12),
        )
        self.assert_content_safe(
            VGroup(floor, order, inventory, robot, package, sensor, dock),
            "warehouse system",
        )

        self.play(Create(floor), FadeIn(title), run_time=RUN_N)
        self.play(
            LaggedStart(
                FadeIn(order),
                FadeIn(inventory),
                FadeIn(robot),
                FadeIn(package),
                FadeIn(sensor),
                FadeIn(dock),
                FadeIn(dock_label),
                lag_ratio=0.09,
            ),
            FadeIn(labels),
            run_time=RUN_S,
        )
        self.wait(PAUSE_S)

        p_order = Dot(radius=0.11, color=BLACK).move_to(order.get_right())
        route1 = Line(
            order.get_right(), inventory.get_left(),
            color=LIGHT_GRAY, stroke_width=2.2,
        )
        msg1 = self.chip(
            "message: reserve()", width=2.75, height=0.58,
            size=16, fill=WHITE,
        ).move_to(RIGHT * 1.15 + UP * 1.15)
        self.play(Create(route1), FadeIn(msg1), FadeIn(p_order), run_time=RUN_Q)
        self.play(MoveAlongPath(p_order, route1), run_time=RUN_N)
        self.play(FadeOut(p_order), Indicate(inventory, color=BLACK), run_time=RUN_Q)

        stock_new = self.text("stock = 2", 19, BOLD, DARK_GRAY).move_to(labels[1])
        self.play(Transform(labels[1], stock_new), run_time=RUN_N)
        self.play(FadeOut(route1), FadeOut(msg1), run_time=RUN_Q)

        p_task = Dot(radius=0.11, color=BLACK).move_to(inventory.get_right())
        route2 = Line(
            inventory.get_right(), robot.get_left() + UP * 0.30,
            color=LIGHT_GRAY, stroke_width=2.2,
        )
        msg2 = self.chip(
            "message: deliver()", width=2.75, height=0.58,
            size=16, fill=WHITE,
        ).move_to(RIGHT * 1.15 + UP * 1.15)
        self.play(Create(route2), FadeIn(msg2), FadeIn(p_task), run_time=RUN_Q)
        self.play(MoveAlongPath(p_task, route2), run_time=RUN_N)
        self.play(FadeOut(p_task), Indicate(robot, color=BLACK), run_time=RUN_Q)
        self.play(
            FadeOut(route2), FadeOut(msg2), FadeOut(labels[2]),
            run_time=RUN_Q,
        )

        moving_unit = VGroup(robot, package)
        travel = ArcBetweenPoints(
            moving_unit.get_center(),
            dock.get_center() + LEFT * 0.85 + UP * 0.20,
            angle=-PI / 10,
        )
        self.play(MoveAlongPath(moving_unit, travel), run_time=2.0, rate_func=smooth)
        self.play(Indicate(dock, color=BLACK), run_time=RUN_Q)

        scan = DashedLine(
            sensor.get_center() + LEFT * 0.10,
            robot.get_center(),
            color=LIGHT_GRAY,
            dash_length=0.12,
        )
        pos = self.chip(
            "position = dock", width=2.30, size=18, fill=WHITE
        ).next_to(sensor, LEFT, buff=0.25)
        self.play(Create(scan), FadeIn(pos), run_time=RUN_N)
        self.wait(PAUSE_R)

        system_summary = self.text(
            "Order → Inventory → Robot → Sensor: four objects, one working system.",
            28, BOLD,
        ).to_edge(DOWN, buff=0.38)
        self.play(FadeIn(system_summary), run_time=RUN_N)
        self.wait(PAUSE_E)
        self.clear_all()
