from manim import *
import numpy as np

config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16
config.frame_height = 9
config.frame_rate = 30
config.background_color = WHITE

BLACK_TEXT = BLACK
DARK_GRAY = "#303030"
MID_GRAY = "#777777"
LIGHT_GRAY = "#D9D9D9"
PAPER = "#F7F7F7"


class Seminario11POOIntro(MovingCameraScene):
    def t(self, text, size=30, weight=NORMAL, color=BLACK_TEXT):
        return Text(text, font_size=size, weight=weight, color=color, line_spacing=0.92)

    def fit(self, mob, w=14.6, h=7.7):
        if mob.width > w:
            mob.scale_to_fit_width(w)
        if mob.height > h:
            mob.scale_to_fit_height(h)
        return mob

    def header(self, number, title, subtitle):
        box = RoundedRectangle(width=0.72, height=0.52, corner_radius=0.10,
                               stroke_color=BLACK, stroke_width=2, fill_color=WHITE, fill_opacity=1)
        num = self.t(f"{number:02d}", 23, BOLD).move_to(box)
        title_m = self.t(title, 34, BOLD)
        self.fit(title_m, 13.7, 0.55)
        row = VGroup(VGroup(box, num), title_m).arrange(RIGHT, buff=0.25)
        row.to_edge(UP, buff=0.16).to_edge(LEFT, buff=0.48)
        rule = Line(LEFT*7.48, RIGHT*7.48, stroke_color=LIGHT_GRAY, stroke_width=2)
        rule.next_to(row, DOWN, buff=0.07)
        sub = self.t(subtitle, 20)
        self.fit(sub, 14.2, 0.55)
        sub.next_to(rule, DOWN, buff=0.09).align_to(row, LEFT)
        return VGroup(row, rule, sub)

    def card(self, title, lines, width=4.1, height=2.25, title_size=27, body_size=21):
        box = RoundedRectangle(width=width, height=height, corner_radius=0.15,
                               stroke_color=BLACK, stroke_width=1.8, fill_color=WHITE, fill_opacity=1)
        title_m = self.t(title, title_size, BOLD)
        body = VGroup(*[self.t(line, body_size) for line in lines])
        body.arrange(DOWN, aligned_edge=LEFT, buff=0.10)
        content = VGroup(title_m, body).arrange(DOWN, aligned_edge=LEFT, buff=0.20)
        self.fit(content, width-0.45, height-0.35)
        content.move_to(box).align_to(box, LEFT).shift(RIGHT*0.24)
        return VGroup(box, content)

    def clear(self):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in list(self.mobjects)], run_time=0.65)
        self.camera.frame.set(width=16).move_to(ORIGIN)

    def construct(self):
        self.opening()
        self.why_oop()
        self.oop_language()
        self.code_model()
        self.semester_route()
        self.individual_projects()
        self.evidence_model()
        self.closing()

    def opening(self):
        kicker = self.t("SEMINARIO · GRADO 11°", 25, BOLD, DARK_GRAY)
        title = self.t("SEMESTRE DE PROGRAMACIÓN", 54, BOLD)
        subtitle = self.t("Programación Orientada a Objetos · POO", 34)
        rule = Line(LEFT*4.2, RIGHT*4.2, color=BLACK, stroke_width=2)
        promise = self.t("Aprender a modelar ideas y convertirlas en proyectos propios.", 25, color=DARK_GRAY)
        footer = self.t("Del concepto → al código → al proyecto funcional", 21, BOLD, MID_GRAY)
        group = VGroup(kicker, title, subtitle, rule, promise, footer).arrange(DOWN, buff=0.28).move_to(UP*0.10)
        self.play(FadeIn(kicker, shift=UP*0.15), run_time=0.8)
        self.play(Write(title), run_time=1.2)
        self.play(FadeIn(subtitle), Create(rule), run_time=0.9)
        self.play(FadeIn(promise), FadeIn(footer), run_time=0.9)
        self.wait(3.2)
        self.clear()

    def why_oop(self):
        head = self.header(1, "¿POR QUÉ PROGRAMACIÓN ORIENTADA A OBJETOS?",
                           "Un programa grande se entiende mejor cuando lo dividimos en entidades con estado y comportamiento.")
        self.add(head)
        messy = VGroup()
        labels = ["dato_1", "dato_2", "función_A", "función_B", "estado", "reglas"]
        for i, txt in enumerate(labels):
            p = RoundedRectangle(width=1.6, height=0.62, corner_radius=0.10,
                                 stroke_color=MID_GRAY, stroke_width=1.5, fill_color=PAPER, fill_opacity=1)
            lab = self.t(txt, 18).move_to(p)
            g = VGroup(p, lab)
            g.move_to(LEFT*5.0 + RIGHT*(i%2)*2.05 + UP*(1.45-(i//2)*1.25))
            messy.add(g)
        connections = VGroup(
            Line(messy[0].get_right(), messy[3].get_left(), color=LIGHT_GRAY),
            Line(messy[1].get_right(), messy[2].get_left(), color=LIGHT_GRAY),
            Line(messy[2].get_bottom(), messy[5].get_top(), color=LIGHT_GRAY),
            Line(messy[4].get_top(), messy[1].get_bottom(), color=LIGHT_GRAY),
        )
        left_label = self.t("Sin estructura", 24, BOLD).next_to(messy, UP, buff=0.30)
        class_box = RoundedRectangle(width=5.0, height=3.6, corner_radius=0.16,
                                     stroke_color=BLACK, stroke_width=2.2, fill_color=WHITE, fill_opacity=1)
        ctitle = self.t("CLASE", 29, BOLD)
        divider = Line(LEFT*2.15, RIGHT*2.15, color=LIGHT_GRAY)
        attrs = self.t("Atributos  →  datos / estado", 22)
        methods = self.t("Métodos    →  acciones / comportamiento", 22)
        ccontent = VGroup(ctitle, divider, attrs, methods).arrange(DOWN, buff=0.34).move_to(class_box)
        class_group = VGroup(class_box, ccontent).move_to(RIGHT*3.65 + DOWN*0.15)
        right_label = self.t("Modelo organizado", 24, BOLD).next_to(class_group, UP, buff=0.30)
        arrow = Arrow(LEFT*0.75, RIGHT*0.75, color=BLACK, stroke_width=3).move_to(DOWN*0.1)
        self.play(FadeIn(messy), FadeIn(connections), FadeIn(left_label), run_time=1.0)
        self.wait(1.2)
        self.play(GrowArrow(arrow), run_time=0.6)
        self.play(FadeIn(class_group, shift=LEFT*0.25), FadeIn(right_label), run_time=1.0)
        self.wait(3.0)
        self.clear()

    def oop_language(self):
        head = self.header(2, "EL LENGUAJE BÁSICO DE POO",
                           "Primero dominaremos clase, objeto, atributos y métodos; después construiremos relaciones entre objetos.")
        self.add(head)
        cards = VGroup(
            self.card("CLASE", ["La plantilla", "que define la estructura."], 3.25, 2.1),
            self.card("OBJETO", ["Una instancia real", "creada desde una clase."], 3.25, 2.1),
            self.card("ATRIBUTOS", ["Variables que guardan", "el estado del objeto."], 3.25, 2.1),
            self.card("MÉTODOS", ["Funciones que describen", "lo que el objeto hace."], 3.25, 2.1),
        ).arrange(RIGHT, buff=0.32).move_to(DOWN*0.05)
        for card in cards:
            self.play(FadeIn(card, shift=UP*0.18), run_time=0.55)
            self.wait(0.55)
        pillars = self.t("Después: encapsulación · herencia · composición · polimorfismo", 25, BOLD)
        pillars.to_edge(DOWN, buff=0.62)
        self.play(FadeIn(pillars), run_time=0.8)
        self.wait(3.0)
        self.clear()

    def code_model(self):
        head = self.header(3, "DE UNA IDEA A UN OBJETO QUE FUNCIONA",
                           "El código representará sistemas: cada clase tendrá una responsabilidad clara.")
        self.add(head)
        code_box = RoundedRectangle(width=7.3, height=4.95, corner_radius=0.14,
                                    stroke_color=BLACK, stroke_width=2, fill_color=PAPER, fill_opacity=1)
        code_lines = [
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
        code = VGroup(*[Text(line, font="DejaVu Sans Mono", font_size=22, color=BLACK) for line in code_lines])
        code.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        code.move_to(code_box).align_to(code_box, LEFT).shift(RIGHT*0.35)
        code_group = VGroup(code_box, code).move_to(LEFT*3.8 + DOWN*0.15)
        robot = RoundedRectangle(width=4.0, height=3.05, corner_radius=0.20,
                                 stroke_color=BLACK, stroke_width=2.2, fill_color=WHITE, fill_opacity=1)
        rcontent = VGroup(
            self.t("Objeto: explorer", 28, BOLD),
            self.t("name = 'A1'", 23),
            self.t("energy = 90", 23),
            self.t("move() → cambia el estado", 21, BOLD),
        ).arrange(DOWN, buff=0.27).move_to(robot)
        robot_group = VGroup(robot, rcontent).move_to(RIGHT*4.2 + DOWN*0.05)
        connector = Arrow(code_group.get_right()+RIGHT*0.15, robot_group.get_left()+LEFT*0.15,
                          buff=0.15, stroke_width=3, color=BLACK)
        self.play(FadeIn(code_group), run_time=1.0)
        self.wait(1.5)
        self.play(GrowArrow(connector), FadeIn(robot_group, shift=LEFT*0.2), run_time=1.0)
        self.wait(3.2)
        self.clear()

    def semester_route(self):
        head = self.header(4, "RUTA DEL SEMESTRE",
                           "Cada bloque agrega una capacidad nueva hasta llegar a un proyecto individual demostrable y explicable.")
        self.add(head)
        labels = [
            ("01", "BASES DE PYTHON", "control, funciones, datos"),
            ("02", "MODELADO POO", "clases, objetos, estado"),
            ("03", "DISEÑO", "responsabilidades y relaciones"),
            ("04", "PROTOTIPO", "primer sistema funcional"),
            ("05", "PRUEBAS", "errores, mejoras, refactor"),
            ("06", "ENTREGA", "demo + código + explicación"),
        ]
        cards = VGroup()
        for num, title, sub in labels:
            box = RoundedRectangle(width=4.2, height=1.65, corner_radius=0.13,
                                   stroke_color=BLACK, stroke_width=1.7, fill_color=WHITE, fill_opacity=1)
            content = VGroup(self.t(num, 21, BOLD, MID_GRAY), self.t(title, 23, BOLD), self.t(sub, 18))
            content.arrange(DOWN, aligned_edge=LEFT, buff=0.10)
            content.move_to(box).align_to(box, LEFT).shift(RIGHT*0.24)
            cards.add(VGroup(box, content))
        cards.arrange_in_grid(rows=2, cols=3, buff=(0.38, 0.42)).move_to(DOWN*0.15)
        for card in cards:
            self.play(FadeIn(card, shift=UP*0.12), run_time=0.45)
        self.wait(3.3)
        self.clear()

    def individual_projects(self):
        head = self.header(5, "UN PROYECTO DIFERENTE POR ESTUDIANTE",
                           "Cada persona elegirá un problema, lo modelará y construirá una solución propia.")
        self.add(head)
        center = RoundedRectangle(width=4.2, height=1.55, corner_radius=0.15,
                                  stroke_color=BLACK, stroke_width=2.2, fill_color=PAPER, fill_opacity=1)
        center_text = VGroup(self.t("TU PROYECTO", 31, BOLD), self.t("problema real + solución programada", 20))
        center_text.arrange(DOWN, buff=0.12).move_to(center)
        center_group = VGroup(center, center_text).move_to(UP*0.10)
        ideas = [
            ("JUEGO", LEFT*5.1+UP*1.5),
            ("SIMULADOR", LEFT*5.1+DOWN*1.45),
            ("GESTOR", RIGHT*5.1+UP*1.5),
            ("AUTOMATIZACIÓN", RIGHT*5.1+DOWN*1.45),
            ("APP DE DATOS", UP*2.35),
            ("HERRAMIENTA", DOWN*2.75),
        ]
        nodes, lines = VGroup(), VGroup()
        for label, pos in ideas:
            box = RoundedRectangle(width=2.55, height=0.95, corner_radius=0.13,
                                   stroke_color=BLACK, stroke_width=1.6, fill_color=WHITE, fill_opacity=1)
            g = VGroup(box, self.t(label, 20, BOLD).move_to(box)).move_to(pos)
            nodes.add(g)
            lines.add(Line(center_group.get_center(), g.get_center(), color=LIGHT_GRAY, stroke_width=2))
        self.play(FadeIn(center_group, scale=0.95), run_time=0.8)
        self.play(*[Create(line) for line in lines], run_time=0.8)
        self.play(LaggedStart(*[FadeIn(n, scale=0.96) for n in nodes], lag_ratio=0.12), run_time=1.6)
        self.wait(3.2)
        self.clear()

    def evidence_model(self):
        head = self.header(6, "¿QUÉ DEBE MOSTRAR UN PROYECTO?",
                           "La meta no es solo que corra: debe demostrar diseño, evolución del código y comprensión del sistema.")
        self.add(head)
        rows = VGroup(
            self.card("1 · PROBLEMA", ["Qué necesidad resuelve", "y para quién."], 4.1, 1.72),
            self.card("2 · MODELO POO", ["Clases, atributos, métodos", "y relaciones justificadas."], 4.1, 1.72),
            self.card("3 · PROTOTIPO", ["Código funcional", "con comportamiento visible."], 4.1, 1.72),
            self.card("4 · ITERACIONES", ["Errores encontrados", "y mejoras realizadas."], 4.1, 1.72),
            self.card("5 · DOCUMENTACIÓN", ["README, instrucciones", "y decisiones principales."], 4.1, 1.72),
            self.card("6 · DEMOSTRACIÓN", ["Presentar, ejecutar", "y defender el diseño."], 4.1, 1.72),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.36, 0.34)).move_to(DOWN*0.20)
        self.play(LaggedStart(*[FadeIn(c, shift=UP*0.12) for c in rows], lag_ratio=0.10), run_time=1.8)
        self.wait(3.5)
        self.clear()

    def closing(self):
        group = VGroup(
            self.t("SEMINARIO 11°", 24, BOLD, MID_GRAY),
            self.t("NO VAMOS A COPIAR UN PROYECTO.", 44, BOLD),
            self.t("VAMOS A CONSTRUIR EL NUESTRO.", 44, BOLD),
            self.t("Pensar → modelar → programar → probar → mejorar → presentar", 25),
            Line(LEFT*5.8, RIGHT*5.8, color=LIGHT_GRAY, stroke_width=2),
            self.t("POO será la herramienta. El proyecto será la evidencia.", 27, BOLD),
        ).arrange(DOWN, buff=0.27).move_to(UP*0.05)
        self.play(FadeIn(group[0]), run_time=0.6)
        self.play(Write(group[1]), run_time=1.0)
        self.play(Write(group[2]), run_time=1.0)
        self.play(FadeIn(group[3]), Create(group[4]), run_time=0.9)
        self.play(FadeIn(group[5]), run_time=0.8)
        self.wait(4.5)
