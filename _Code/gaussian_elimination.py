"""
M3 Internal Assessment - Animation Video
Topic: Gaussian Elimination (solving a 3x3 system step by step)

Render all scenes at 1080p, 30 fps:
    manim -r 1920,1080 --frame_rate 30 gaussian_elimination.py S1_Hook S2_Concept S3_Intuition S4_Example S5_Interpretation S6_Summary
Then join them with build_video.py.

Every scene is split into narration "cues". Each cue holds the narration line
and the animations shown while it is spoken; the helper pads with a wait so
the picture stays on screen long enough to read the line aloud. The cue times
are saved to cues/<Scene>.json, which build_video.py turns into the
narration script / subtitle file.

Worked example used throughout:
     x +  y +  z =  6
    2x +  y -  z =  1
     x -  y + 2z =  5        solution (x, y, z) = (1, 2, 3)
"""
import json
import os

from manim import *

# ---------------------------------------------------------------- settings
STUDENT_NAME = "Kritika Khatri"
STUDENT_ID = "e25b070689"
BATCH = "Ramanujan"
COURSE = "Linear Algebra and Calculus (M3) - Internal Assessment"

WORDS_PER_SECOND = 2.5                   # fallback if a line has no audio yet
try:                                     # spoken length of each line (make_voiceover.py)
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "audio", "durations.json")) as _f:
        SPEECH = json.load(_f)
except FileNotFoundError:
    SPEECH = {}

BG = "#0e1621"
PIVOT = YELLOW
OP = "#58C4DD"        # row-operation colour (blue)
ZERO = "#83C167"      # entries we have eliminated (green)
RHS = "#FF8C69"       # right-hand-side column b (orange)
DIM = GREY_B
PLANE_COLORS = ["#58C4DD", "#83C167", "#C77DFF"]   # R1, R2, R3

config.background_color = BG


# ---------------------------------------------------------------- helpers
class Narrated:
    """Mixin: self.cue("text") starts a narration segment."""

    def setup_cues(self):
        self._cues, self._cur = [], None

    def _t(self):
        return self.renderer.time

    def cue(self, text):
        self._close()
        self._cur = (self._t(), text)

    def _close(self):
        if self._cur is None:
            return
        start, text = self._cur
        if text.strip() in SPEECH:
            need = SPEECH[text.strip()] + 0.35
        else:
            need = len(text.split()) / WORDS_PER_SECOND + 0.4
        elapsed = self._t() - start
        if elapsed < need:
            self.wait(need - elapsed)
        self._cues.append({"start": start, "end": self._t(), "text": text})
        self._cur = None

    def finish(self, tail=0.6):
        self._close()
        self.wait(tail)
        os.makedirs("cues", exist_ok=True)
        with open(f"cues/{type(self).__name__}.json", "w") as f:
            json.dump({"duration": self._t(), "cues": self._cues}, f, indent=1)


class NScene(Narrated, Scene):
    def setup(self):
        self.setup_cues()


class N3DScene(Narrated, ThreeDScene):
    def setup(self):
        super().setup()
        self.setup_cues()


def T(s, fs=36, color=WHITE, alignment="center", **kw):
    if "\n" in s:   # multi-line text
        lines = [Text(l, font_size=fs, color=color, **kw) for l in s.split("\n")]
        return VGroup(*lines).arrange(DOWN, buff=0.14,
                                      aligned_edge=LEFT if alignment == "left" else ORIGIN)
    return Text(s, font_size=fs, color=color, **kw)


def M(s, fs=44, color=WHITE):
    return MathTex(s, font_size=fs, color=color)


def heading(s):
    return T(s, 40, WHITE, weight=BOLD).to_edge(UP, buff=0.45)


def bracket(top, bot, x, left=True, arm=0.16):
    d = arm if left else -arm
    return VMobject(stroke_width=3, color=WHITE).set_points_as_corners(
        [[x + d, top, 0], [x, top, 0], [x, bot, 0], [x + d, bot, 0]])


class AugMatrix(VGroup):
    """3 x 4 augmented matrix with a dashed bar before the last column."""

    def __init__(self, rows, col_gap=1.2, row_gap=0.85, fs=46, labels=True):
        super().__init__()
        self.col_gap, self.row_gap, self.fs = col_gap, row_gap, fs
        self.anchor = Dot(ORIGIN, radius=0.001).set_opacity(0)
        self.add(self.anchor)
        self.cells = []
        for i, r in enumerate(rows):
            line = []
            for j, s in enumerate(r):
                m = M(s, fs, RHS if j == 3 else WHITE).move_to(self.offset(i, j))
                line.append(m)
            self.cells.append(line)
        self.entries = VGroup(*[c for line in self.cells for c in line])
        top, bot = row_gap + 0.45, -row_gap - 0.45
        xl = self.offset(0, 0)[0] - 0.65
        xr = self.offset(0, 3)[0] + 0.75
        xbar = (self.offset(0, 2)[0] + self.offset(0, 3)[0]) / 2
        self.brackets = VGroup(bracket(top, bot, xl, True), bracket(top, bot, xr, False))
        self.bar = DashedLine([xbar, top - 0.05, 0], [xbar, bot + 0.05, 0],
                              dash_length=0.1, color=GREY_B)
        self.add(self.entries, self.brackets, self.bar)
        if labels:
            self.rlabels = VGroup(*[
                M(f"R_{i+1}", 36, DIM).move_to([xl - 0.55, self.offset(i, 0)[1], 0])
                for i in range(3)])
            self.add(self.rlabels)

    def offset(self, i, j):
        x = (j - 1.5) * self.col_gap + (0.3 if j == 3 else 0)
        return np.array([x, (1 - i) * self.row_gap, 0])

    def pos(self, i, j):
        return self.anchor.get_center() + self.offset(i, j)

    def row(self, i):
        return VGroup(*self.cells[i])

    def set_row(self, i, values, colors=None):
        """Animations that morph row i into new values (same mobjects kept)."""
        anims = []
        for j, s in enumerate(values):
            c = colors[j] if colors else (RHS if j == 3 else WHITE)
            new = M(s, self.fs, c).move_to(self.pos(i, j))
            anims.append(Transform(self.cells[i][j], new))
        return anims


def calc_rows(label_lines, rows, x0, y0, gap=1.0, dy=0.7, fs=40):
    """Small table: label + 4 numbers per line, used for the side calculation."""
    g = VGroup()
    for k, (lab, vals, col) in enumerate(zip(label_lines, rows,
                                               [WHITE, OP, ZERO])):
        y = y0 - k * dy
        line = VGroup(M(lab, fs, col).move_to([x0, y, 0]).align_to([x0 + 0.6, 0, 0], RIGHT))
        for j, v in enumerate(vals):
            line.add(M(v, fs, col).move_to([x0 + 1.25 + j * gap + (0.25 if j == 3 else 0), y, 0]))
        g.add(line)
    return g


# ======================================================================
# Scene 1 - Hook / context
# ======================================================================
class S1_Hook(NScene):
    def construct(self):
        # opening frame: title, concept, name, ID
        title = T("Gaussian Elimination", 72, WHITE, weight=BOLD).shift(UP * 1.3)
        sub = T("Solving a 3 × 3 system, one step at a time", 36, OP).next_to(title, DOWN, 0.4)
        who = VGroup(T(STUDENT_NAME, 32),
                     T(f"Student ID: {STUDENT_ID}   ·   Batch: {BATCH}", 28, GREY_B),
                     T(COURSE, 24, GREY_B)).arrange(DOWN, buff=0.2).shift(DOWN * 1.6)
        self.cue("Hi! In this video we'll learn Gaussian elimination, a step-by-step "
                 "method for solving systems of linear equations.")
        self.play(Write(title), FadeIn(sub, shift=UP * 0.2), run_time=1.5)
        self.play(FadeIn(who), run_time=0.8)
        self.cue("")
        self.play(FadeOut(VGroup(title, sub, who)), run_time=0.6)

        hard = VGroup(M(r"x + y + z = 6"), M(r"2x + y - z = 1"), M(r"x - y + 2z = 5")
                      ).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        easy = VGroup(M(r"x + y + z = 6"), M(r"-y - 3z = -11"), M(r"7z = 21")
                      ).arrange(DOWN, buff=0.35, aligned_edge=RIGHT)
        hard.move_to(LEFT * 3.5 + DOWN * 0.2)
        easy.move_to(RIGHT * 3.5 + DOWN * 0.2)
        box_h = SurroundingRectangle(hard, color=GREY_B, buff=0.35, corner_radius=0.15)
        box_e = SurroundingRectangle(easy, color=GREY_B, buff=0.35, corner_radius=0.15)
        lab_h = T("System A", 30, GREY_B).next_to(box_h, UP)
        lab_e = T("System B", 30, GREY_B).next_to(box_e, UP)

        self.cue("Here are three equations in three unknowns, x, y and z. Can you see the "
                 "solution just by looking? Not really: every equation mixes all three variables.")
        self.play(FadeIn(lab_h), Create(box_h), Write(hard), run_time=2)
        q = T("?", 96, PIVOT).next_to(box_h, DOWN, 0.3)
        self.play(FadeIn(q, scale=0.5))

        self.cue("Now look at this system. The last equation says seven z equals twenty-one, "
                 "so z is three. Plug that in above, and y and x follow straight away.")
        self.play(FadeIn(lab_e), Create(box_e), Write(easy), run_time=2)
        self.play(Indicate(easy[2], color=PIVOT, scale_factor=1.2))
        zsol = M("z = 3", 44, PIVOT).next_to(box_e, DOWN, 0.4)
        self.play(Write(zsol))

        self.cue("Here's the surprise: both systems have exactly the same solution. Gaussian "
                 "elimination is the recipe that turns the hard system into the easy one. "
                 "Let's see how, and why it works.")
        arrow = Arrow(box_h.get_right(), box_e.get_left(), buff=0.15, color=OP, stroke_width=6)
        same = T("same solution", 28, OP).next_to(arrow, UP, 0.15)
        self.play(FadeOut(q), GrowArrow(arrow), FadeIn(same))
        sol = M(r"(x, y, z) = (1, 2, 3)", 48, PIVOT).to_edge(DOWN, buff=0.5)
        self.play(ReplacementTransform(zsol, sol))
        self.finish()


# ======================================================================
# Scene 2 - Concept introduction: augmented matrix, row operations, goal
# ======================================================================
class S2_Concept(NScene):
    def construct(self):
        h = heading("The augmented matrix  [ A | b ]")
        eqs = VGroup(M(r"1x + 1y + 1z = 6"), M(r"2x + 1y - 1z = 1"), M(r"1x - 1y + 2z = 5")
                     ).arrange(DOWN, buff=0.35, aligned_edge=LEFT).shift(UP * 0.2)
        aug = AugMatrix([["1", "1", "1", "6"], ["2", "1", "-1", "1"], ["1", "-1", "2", "5"]])
        aug.shift(DOWN * 0.1)

        self.cue("First, some notation. Only the numbers matter, not the letters. So we write the "
                 "system as an augmented matrix: the coefficient matrix A, then a bar, then "
                 "the right-hand-side column b.")
        self.play(FadeIn(h), Write(eqs), run_time=1.5)
        self.wait(0.8)
        self.play(ReplacementTransform(eqs, VGroup(aug.entries)), run_time=1.6)
        self.play(Create(aug.brackets), Create(aug.bar))
        A_brace = Brace(VGroup(*[aug.cells[i][j] for i in range(3) for j in range(3)]), DOWN, buff=0.45)
        A_lab = M("A", 44).next_to(A_brace, DOWN, 0.15)
        b_brace = Line(aug.pos(2, 3) + DOWN * 0.6 + LEFT * 0.25, aug.pos(2, 3) + DOWN * 0.6 + RIGHT * 0.25,
                       color=RHS, stroke_width=3)
        b_lab = M("b", 44, RHS).move_to([b_brace.get_center()[0], A_lab.get_center()[1], 0])
        self.play(GrowFromCenter(A_brace), FadeIn(A_lab), Create(b_brace), FadeIn(b_lab))

        self.cue("Each row is one equation: we'll call them R one, R two and R three. Each column "
                 "belongs to one variable, x, y and z, and the last column holds the constants.")
        heads = VGroup(*[M(s, 36, c).move_to(aug.pos(0, j) + UP * 0.8)
                         for j, (s, c) in enumerate(zip("xyzb", [GREY_B] * 3 + [RHS]))])
        self.play(FadeIn(aug.rlabels, shift=RIGHT * 0.2), FadeIn(heads, shift=DOWN * 0.2))

        mat = VGroup(aug, heads, A_brace, A_lab, b_brace, b_lab)
        self.play(mat.animate.scale(0.75).to_edge(LEFT, buff=0.7), run_time=1)

        ops_title = T("Elementary row operations", 32, OP, weight=BOLD)
        ops = VGroup(
            VGroup(T("1. Swap", 30), M(r"R_i \leftrightarrow R_j", 40)),
            VGroup(T("2. Scale", 30), M(r"R_i \to k\,R_i,\quad k \neq 0", 40)),
            VGroup(T("3. Replace", 30), M(r"R_i \to R_i + c\,R_j", 40)),
        )
        for o in ops:
            o.arrange(RIGHT, buff=0.4)
        ops.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        panel = VGroup(ops_title, ops).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        panel.to_edge(RIGHT, buff=0.7).shift(DOWN * 0.2)
        self.cue("We are allowed three elementary row operations. One: swap two rows. Two: "
                 "multiply a row by a non-zero number k. Three: replace a row by itself plus "
                 "c times another row.")
        self.play(FadeIn(ops_title))
        for o in ops:
            self.play(FadeIn(o, shift=LEFT * 0.3), run_time=0.8)
            self.wait(1.6)

        # goal: echelon form template
        self.cue("Our goal is row echelon form, a staircase shape. The first non-zero entry in "
                 "each row is called a pivot, and every entry below a pivot is zero.")
        self.play(FadeOut(VGroup(mat, panel)), run_time=0.7)
        h2 = heading("Goal: row echelon form")
        self.play(Transform(h, h2))
        templ = AugMatrix([[r"\blacksquare", "*", "*", "*"], ["0", r"\blacksquare", "*", "*"],
                           ["0", "0", r"\blacksquare", "*"]], labels=False, fs=50)
        for i in range(3):
            templ.cells[i][i].set_color(PIVOT)
            for j in range(i):
                templ.cells[i][j].set_color(ZERO)
        templ.shift(DOWN * 0.2)
        self.play(FadeIn(templ))
        stair = VMobject(color=PIVOT, stroke_width=4).set_points_as_corners([
            templ.pos(0, 0) + [-0.45, -0.45, 0], templ.pos(0, 0) + [0.6, -0.45, 0],
            templ.pos(1, 1) + [-0.6, -0.45, 0], templ.pos(1, 1) + [0.6, -0.45, 0],
            templ.pos(2, 2) + [-0.6, -0.45, 0], templ.pos(2, 2) + [0.6, -0.45, 0]])
        self.play(Create(stair), run_time=1.5)
        leg = VGroup(
            VGroup(M(r"\blacksquare", 36, PIVOT), T("pivot (non-zero)", 26)).arrange(RIGHT),
            VGroup(M("0", 36, ZERO), T("zeros below each pivot", 26)).arrange(RIGHT),
            VGroup(M("*", 36), T("any number", 26)).arrange(RIGHT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(templ, DOWN, 0.6)
        self.play(FadeIn(leg))

        self.cue("By the end of this video, you'll be able to reduce a three by three system to "
                 "echelon form, solve it by back-substitution, and explain why row operations "
                 "never change the solution.")
        self.play(FadeOut(VGroup(templ, stair, leg)))
        obj_t = T("Learning objective", 34, OP, weight=BOLD)
        obj = Paragraph("By the end, you will be able to reduce a 3 × 3 system",
                        "to echelon form, solve it by back-substitution, and",
                        "explain why row operations preserve the solution set.",
                        font_size=32, alignment="center", line_spacing=0.9)
        box = VGroup(obj_t, obj).arrange(DOWN, buff=0.5)
        self.play(Transform(h, heading("What you'll learn")), FadeIn(box, shift=UP * 0.3))
        self.finish()


# ======================================================================
# Scene 3 - Visual intuition: three planes and a fixed meeting point
# ======================================================================
class S3_Intuition(N3DScene):
    def fixed(self, mob):
        """Register a 2D overlay (stays flat on screen while the camera turns)."""
        self.add_fixed_in_frame_mobjects(mob)
        self.remove(mob)
        return mob

    def swap(self, old, new, run_time=0.6):
        self.fixed(new)
        self.play(FadeOut(old), FadeIn(new), run_time=run_time)
        return new

    def construct(self):
        axes = ThreeDAxes(x_range=[-1, 4, 1], y_range=[-1, 5, 1], z_range=[-2, 8, 2],
                          x_length=5.5, y_length=6, z_length=5.5,
                          axis_config={"color": GREY_B, "stroke_width": 2})
        axes.shift(-axes.c2p(1, 2, 3))          # put the solution point at the centre
        labels = axes.get_axis_labels(M("x", 36), M("y", 36), M("z", 36))
        self.set_camera_orientation(phi=65 * DEGREES, theta=-20 * DEGREES, zoom=0.85)

        def plane(f, color, opacity=0.55):
            return Surface(lambda u, v: axes.c2p(u, v, f(u, v)),
                           u_range=[-0.6, 2.6], v_range=[0.4, 3.6], resolution=(6, 6),
                           fill_opacity=opacity, checkerboard_colors=[color, color],
                           stroke_color=color, stroke_width=0.6)

        f1 = lambda x, y: 6 - x - y            # x + y + z = 6
        f2 = lambda x, y: 2 * x + y - 1        # 2x + y - z = 1
        f3 = lambda x, y: (5 - x + y) / 2      # x - y + 2z = 5
        f2b = lambda x, y: (11 - y) / 3        # -y - 3z = -11
        f3b = lambda x, y: 2 * y - 1           # -2y + z = -1
        f3c = lambda x, y: 3 + 0 * x           # 7z = 21

        P = [plane(f1, PLANE_COLORS[0]), plane(f2, PLANE_COLORS[1]), plane(f3, PLANE_COLORS[2])]
        pt = Dot3D(axes.c2p(1, 2, 3), radius=0.11, color=PIVOT)

        def eq(i, tex):
            m = M(rf"R_{i+1}:\; {tex}", 38, PLANE_COLORS[i])
            m.to_corner(UL, buff=0.45).shift(DOWN * 0.55 * i)
            return self.fixed(m)

        def bottom(tex, color=OP):
            return self.fixed(M(tex, 40, color).to_edge(DOWN, buff=0.5))

        eqs = [eq(0, "x + y + z = 6"), eq(1, "2x + y - z = 1"), eq(2, "x - y + 2z = 5")]
        sol = self.fixed(M(r"\text{meeting point } (1, 2, 3)", 36, PIVOT).to_corner(UR, buff=0.45))

        self.cue("Before calculating, let's picture it. An equation in three variables is a plane "
                 "in space. Our three planes meet at a single point, and that point is the solution.")
        self.play(Create(axes), FadeIn(labels), run_time=1.2)
        for k in range(3):
            self.play(FadeIn(P[k]), FadeIn(eqs[k]), run_time=0.9)
        self.play(FadeIn(pt, scale=2), FadeIn(sol))
        self.begin_ambient_camera_rotation(rate=0.012)

        self.cue("Now apply our first row operation: R two becomes R two minus two R one. "
                 "Watch the green plane.")
        low = bottom(r"R_2 \to R_2 - 2R_1")
        self.play(FadeIn(low), run_time=0.4)
        new = eq(1, "-y - 3z = -11")
        self.play(Transform(P[1], plane(f2b, PLANE_COLORS[1])),
                  FadeOut(eqs[1]), FadeIn(new), run_time=2.5)
        eqs[1] = new
        self.play(Flash(pt, color=PIVOT, line_length=0.3))

        self.cue("It tilts to a new position, but it still passes through the same point. Why? "
                 "If a point satisfies both R one and R two, it automatically satisfies "
                 "R two minus two R one.")
        low = self.swap(low, bottom(r"R_1, R_2 \text{ true } \Rightarrow R_2 - 2R_1 \text{ true}", WHITE))

        self.cue("And the step can be undone: just add two R one back. So no solutions are "
                 "gained, and none are lost. The solution set is preserved.")
        low = self.swap(low, bottom(r"\text{undo: } R_2 \to R_2 + 2R_1 \;\Rightarrow\; "
                                    r"\text{same solution set}", ZERO))

        self.cue("Next, R three minus R one, and then R three minus two R two. "
                 "Look at the final plane: it is perfectly flat. Seven z equals twenty-one, "
                 "which is the plane z equals three.")
        low = self.swap(low, bottom(r"R_3 \to R_3 - R_1"), run_time=0.4)
        new = eq(2, "-2y + z = -1")
        self.play(Transform(P[2], plane(f3b, PLANE_COLORS[2])), FadeOut(eqs[2]), FadeIn(new),
                  run_time=2)
        eqs[2] = new
        low = self.swap(low, bottom(r"R_3 \to R_3 - 2R_2"), run_time=0.4)
        new = eq(2, "7z = 21")
        self.play(Transform(P[2], plane(f3c, PLANE_COLORS[2])), FadeOut(eqs[2]), FadeIn(new),
                  run_time=2)
        eqs[2] = new
        self.play(Flash(pt, color=PIVOT, line_length=0.3))

        self.cue("Every step moved the planes, but never the meeting point. That is the whole idea "
                 "behind Gaussian elimination.")
        low = self.swap(low, bottom(r"\text{planes move} \;\;\cdot\;\; \text{solution stays}", PIVOT))
        self.finish(tail=0.8)
        self.stop_ambient_camera_rotation()


# ======================================================================
# Scene 4 - Worked example: elimination + back-substitution + check
# ======================================================================
class S4_Example(NScene):
    def construct(self):
        h = heading("Worked example")
        aug = AugMatrix([["1", "1", "1", "6"], ["2", "1", "-1", "1"], ["1", "-1", "2", "5"]],
                        col_gap=1.05, fs=44)
        aug.to_edge(LEFT, buff=1.4).shift(UP * 0.6)
        X0, Y0 = 0.9, 1.6        # side calculation panel origin

        self.cue("Now let's do the algebra carefully. Here is our augmented matrix.")
        self.play(FadeIn(h), FadeIn(aug))

        # ---- step 1: pivot 1
        step = T("Step 1: clear column 1 below pivot 1", 30, OP).to_edge(DOWN, buff=0.5)
        p1 = SurroundingRectangle(aug.cells[0][0], color=PIVOT, buff=0.15)
        self.cue("Step one. The first pivot is the one in the top-left corner. We use it to "
                 "create zeros below it, in column one.")
        self.play(FadeIn(step), Create(p1))
        self.play(Indicate(VGroup(aug.cells[1][0], aug.cells[2][0]), color=OP))

        # R2 - 2R1
        op = M(r"R_2 \to R_2 - 2R_1", 42, OP).move_to([X0 + 2.6, Y0 + 0.9, 0])
        calc = calc_rows([r"R_2", r"-2R_1", r"\text{new } R_2"],
                         [["2", "1", "-1", "1"], ["-2", "-2", "-2", "-12"], ["0", "-1", "-3", "-11"]],
                         X0, Y0)
        rule = Line([X0 + 0.7, Y0 - 1.05, 0], [X0 + 5.7, Y0 - 1.05, 0], color=GREY_B)
        self.cue("To clear the two in row two, subtract two times row one. Two minus two is zero, "
                 "one minus two is minus one, minus one minus two is minus three, and one minus "
                 "twelve is minus eleven.")
        self.play(FadeIn(op), Indicate(aug.row(1), color=OP), Indicate(aug.row(0), color=OP))
        self.play(FadeIn(calc[0]), FadeIn(calc[1]))
        self.play(Create(rule))
        for j in range(5):
            self.play(FadeIn(calc[2][j], shift=DOWN * 0.15), run_time=0.45)
            self.wait(0.9)

        self.cue("The new row two replaces the old one.")
        self.play(*aug.set_row(1, ["0", "-1", "-3", "-11"], [ZERO, WHITE, WHITE, RHS]),
                  Indicate(calc[2], color=ZERO), run_time=1.3)
        self.play(FadeOut(VGroup(op, calc, rule)))

        # R3 - R1
        op = M(r"R_3 \to R_3 - R_1", 42, OP).move_to([X0 + 2.6, Y0 + 0.9, 0])
        calc = calc_rows([r"R_3", r"-R_1", r"\text{new } R_3"],
                         [["1", "-1", "2", "5"], ["-1", "-1", "-1", "-6"], ["0", "-2", "1", "-1"]],
                         X0, Y0)
        rule = Line([X0 + 0.7, Y0 - 1.05, 0], [X0 + 5.7, Y0 - 1.05, 0], color=GREY_B)
        self.cue("For row three, the leading entry is one, so we simply subtract row one. "
                 "That gives zero, minus two, one, and minus one.")
        self.play(FadeIn(op), FadeIn(calc[0]), FadeIn(calc[1]), Create(rule))
        self.play(FadeIn(calc[2], shift=DOWN * 0.15))
        self.play(*aug.set_row(2, ["0", "-2", "1", "-1"], [ZERO, WHITE, WHITE, RHS]), run_time=1.3)
        self.play(FadeOut(VGroup(op, calc, rule)))

        # ---- step 2: pivot 2
        self.cue("Column one is now clear. Step two: our next pivot is minus one, "
                 "in row two, column two.")
        step2 = T("Step 2: clear column 2 below pivot 2", 30, OP).to_edge(DOWN, buff=0.5)
        p2 = SurroundingRectangle(aug.cells[1][1], color=PIVOT, buff=0.15)
        self.play(Transform(step, step2), Create(p2))

        op = M(r"R_3 \to R_3 - 2R_2", 42, OP).move_to([X0 + 2.6, Y0 + 0.9, 0])
        calc = calc_rows([r"R_3", r"-2R_2", r"\text{new } R_3"],
                         [["0", "-2", "1", "-1"], ["0", "2", "6", "22"], ["0", "0", "7", "21"]],
                         X0, Y0)
        rule = Line([X0 + 0.7, Y0 - 1.05, 0], [X0 + 5.7, Y0 - 1.05, 0], color=GREY_B)
        self.cue("To eliminate the minus two below it, use R three minus two R two. Minus two "
                 "plus two is zero, one plus six is seven, and minus one plus twenty-two is "
                 "twenty-one.")
        self.play(FadeIn(op), FadeIn(calc[0]), FadeIn(calc[1]), Create(rule))
        for j in range(5):
            self.play(FadeIn(calc[2][j], shift=DOWN * 0.15), run_time=0.45)
            self.wait(0.7)
        self.play(*aug.set_row(2, ["0", "0", "7", "21"], [ZERO, ZERO, WHITE, RHS]), run_time=1.3)
        self.play(FadeOut(VGroup(op, calc, rule)))

        # ---- echelon form reached
        self.cue("And there it is: row echelon form. Three pivots on a staircase, "
                 "and zeros below every pivot.")
        p3 = SurroundingRectangle(aug.cells[2][2], color=PIVOT, buff=0.15)
        stair = VMobject(color=PIVOT, stroke_width=4).set_points_as_corners([
            aug.pos(0, 0) + [-0.4, -0.42, 0], aug.pos(0, 0) + [0.52, -0.42, 0],
            aug.pos(1, 1) + [-0.52, -0.42, 0], aug.pos(1, 1) + [0.52, -0.42, 0],
            aug.pos(2, 2) + [-0.52, -0.42, 0], aug.pos(2, 2) + [0.52, -0.42, 0]])
        done = T("Row echelon form ✓", 30, PIVOT).to_edge(DOWN, buff=0.5)
        self.play(Create(p3), Create(stair), Transform(step, done), run_time=1.5)

        # ---- back substitution
        self.play(FadeOut(VGroup(p1, p2, p3, stair)), Transform(h, heading("Back-substitution")),
                  FadeOut(step))
        bx = 0.9
        eqs = VGroup(M(r"x + y + z = 6"), M(r"-y - 3z = -11"), M(r"7z = 21"))
        for i, e in enumerate(eqs):
            e.move_to([bx + 2.3, aug.pos(i, 0)[1], 0])
        self.cue("Now solve from the bottom up. This is called back-substitution. "
                 "The last row says seven z equals twenty-one, so z equals three.")
        self.play(*[TransformFromCopy(aug.row(i), eqs[i]) for i in range(3)], run_time=1.5)
        arrow = Arrow(eqs[2].get_right() + RIGHT * 0.2 + DOWN * 0.1,
                      eqs[0].get_right() + RIGHT * 0.2 + UP * 0.1,
                      path_arc=1.2, color=OP, buff=0.1).shift(RIGHT * 1.0)
        self.play(Create(arrow))
        res = VGroup(
            M(r"7z = 21 \;\Rightarrow\; z = 3", 42),
        ).move_to([0, -1.9, 0])
        self.play(Indicate(eqs[2], color=PIVOT))
        self.play(Write(res[0]))

        self.cue("Row two says minus y minus three z equals minus eleven. Substituting z equals "
                 "three: minus y minus nine equals minus eleven, so y equals two.")
        r2 = M(r"-y - 3(3) = -11 \;\Rightarrow\; -y = -2 \;\Rightarrow\; y = 2", 42
               ).next_to(res[0], DOWN, 0.3)
        self.play(Indicate(eqs[1], color=PIVOT))
        self.play(Write(r2), run_time=1.6)

        self.cue("Row one: x plus two plus three equals six, so x equals one.")
        r1 = M(r"x + 2 + 3 = 6 \;\Rightarrow\; x = 1", 42).next_to(r2, DOWN, 0.3)
        self.play(Indicate(eqs[0], color=PIVOT))
        self.play(Write(r1))

        # ---- check
        self.cue("Always check in the original equations. One plus two plus three is six. "
                 "Two plus two minus three is one. One minus two plus six is five. "
                 "All three check out.")
        self.play(FadeOut(VGroup(aug, eqs, arrow, res, r2, r1)), Transform(h, heading("Check")))
        sol = M(r"(x, y, z) = (1, 2, 3)", 52, PIVOT).shift(UP * 1.8)
        self.play(Write(sol))
        checks = VGroup(
            M(r"1 + 2 + 3 = 6"), M(r"2(1) + 2 - 3 = 1"), M(r"1 - 2 + 2(3) = 5"),
        ).arrange(DOWN, buff=0.4).shift(DOWN * 0.5)
        for c in checks:
            tick = M(r"\checkmark", 48, ZERO).next_to(c, RIGHT, 0.4)
            self.play(Write(c), run_time=0.9)
            self.play(FadeIn(tick, scale=1.5), run_time=0.4)
            self.wait(0.8)
        self.finish()


# ======================================================================
# Scene 5 - Interpretation: what the echelon form tells us
# ======================================================================
class S5_Interpretation(NScene):
    def construct(self):
        h = heading("What does echelon form tell us?")
        aug = AugMatrix([["1", "1", "1", "6"], ["0", "-1", "-3", "-11"], ["0", "0", "7", "21"]],
                        col_gap=1.05, fs=44, labels=False)
        for i in range(3):
            for j in range(i):
                aug.cells[i][j].set_color(ZERO)
        aug.shift(LEFT * 3.3 + UP * 0.4)
        piv = VGroup(*[Circle(radius=0.38, color=PIVOT).move_to(aug.pos(i, i)) for i in range(3)])
        info = VGroup(
            T("3 pivots, 3 unknowns", 34),
            T("pivot in every column of A", 30, GREY_B),
            T("→ no free variables", 30, GREY_B),
            T("→ exactly one solution", 34, PIVOT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).shift(RIGHT * 3 + UP * 0.4)

        self.cue("So what do these numbers mean? x equals one, y equals two, z equals three is the "
                 "single point where all three planes meet.")
        self.play(FadeIn(h), FadeIn(aug))
        pt = M(r"(1, 2, 3) = \text{the one point where the 3 planes meet}", 38, PIVOT
               ).to_edge(DOWN, buff=1.0)
        self.play(Write(pt), run_time=1.5)

        self.cue("Echelon form also reveals the structure. Here every column of A has a pivot, "
                 "so there are no free variables, and the solution is unique.")
        self.play(LaggedStart(*[Create(c) for c in piv], lag_ratio=0.3))
        self.play(LaggedStart(*[FadeIn(i, shift=LEFT * 0.2) for i in info], lag_ratio=0.5),
                  run_time=2.5)

        # three possible endings
        self.play(FadeOut(VGroup(aug, piv, info, pt)), Transform(h, heading("Three possible endings")))

        def card(title, rowtex, meaning, col):
            r = M(rowtex, 36)
            body = VGroup(T(title, 30, col, weight=BOLD), T("last row:", 22, GREY_B), r,
                          T(meaning, 24)).arrange(DOWN, buff=0.3)
            box = RoundedRectangle(width=4.1, height=3.6, corner_radius=0.2, color=col)
            body.move_to(box)
            return VGroup(box, body)

        c1 = card("Unique", r"[\,0\;\;0\;\;7 \mid 21\,]", "pivot in every column\none point", PIVOT)
        c2 = card("No solution", r"[\,0\;\;0\;\;0 \mid 5\,]", "says 0 = 5: impossible\nplanes share no point",
                  "#FC6255")
        c3 = card("Infinitely many", r"[\,0\;\;0\;\;0 \mid 0\,]", "a free variable\nplanes meet in a line",
                  OP)
        cards = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.35).shift(DOWN * 0.3)

        self.cue("But elimination can end differently. Ours ended with a pivot in every column. "
                 "If instead a row becomes zero, zero, zero, bar five, it says zero equals five. "
                 "That's impossible, so there is no solution: the planes share no common point.")
        self.play(FadeIn(c1, shift=UP * 0.3))
        self.wait(2.5)
        self.play(FadeIn(c2, shift=UP * 0.3))

        self.cue("And if a row becomes all zeros, including the right-hand side, that equation "
                 "added no new information. A variable is then free, and there are infinitely "
                 "many solutions, like planes meeting along a line.")
        self.play(FadeIn(c3, shift=UP * 0.3))

        self.cue("So after elimination, the pivots tell you everything: one solution, none, "
                 "or infinitely many.")
        self.play(Indicate(VGroup(c1[1][0], c2[1][0], c3[1][0]), color=WHITE, scale_factor=1.1))
        self.finish()


# ======================================================================
# Scene 6 - Summary & credits (closing frame)
# ======================================================================
class S6_Summary(NScene):
    def construct(self):
        h = heading("Three takeaways")
        items = VGroup(
            VGroup(T("1", 40, PIVOT, weight=BOLD),
                   VGroup(T("Write the system as an augmented matrix", 32), M(r"[\,A \mid b\,]", 40))
                   .arrange(RIGHT, buff=0.3)),
            VGroup(T("2", 40, PIVOT, weight=BOLD),
                   T("Row operations reach echelon form without\nchanging the solution set", 32, alignment="left")),
            VGroup(T("3", 40, PIVOT, weight=BOLD),
                   T("Back-substitute, check, and read the pivots:\nunique, none, or infinitely many", 32, alignment="left")),
        )
        for it in items:
            it.arrange(RIGHT, buff=0.5, aligned_edge=UP)
        items.arrange(DOWN, aligned_edge=LEFT, buff=0.6).shift(DOWN * 0.2)

        self.cue("Let's recap three key takeaways.")
        self.play(FadeIn(h))
        self.cue("One: write the system as an augmented matrix, A bar b.")
        self.play(FadeIn(items[0], shift=RIGHT * 0.3))
        self.cue("Two: use row operations to reach echelon form. They change the equations, "
                 "but never the solution set.")
        self.play(FadeIn(items[1], shift=RIGHT * 0.3))
        self.cue("Three: solve by back-substitution, check in the original equations, and read "
                 "the pivots to know if the solution is unique, impossible, or infinite.")
        self.play(FadeIn(items[2], shift=RIGHT * 0.3))

        self.cue("Thanks for watching! References, tools and the AI disclosure are on screen now.")
        self.play(FadeOut(VGroup(h, items)))
        credits = VGroup(
            T("Gaussian Elimination", 44, WHITE, weight=BOLD),
            T(f"{STUDENT_NAME}  ·  {STUDENT_ID}  ·  Batch {BATCH}", 28, GREY_B),
            T("References", 28, OP, weight=BOLD),
            T("G. Strang, Introduction to Linear Algebra, 5th ed., Ch. 2\n"
              "D. C. Lay, Linear Algebra and Its Applications, Ch. 1\n"
              "M3 lecture notes, Newton School of Technology", 24),
            T("Tools", 28, OP, weight=BOLD),
            T("Manim Community Edition (Python) · ffmpeg", 24),
            T("AI disclosure", 28, OP, weight=BOLD),
            T("Script, storyboard and Manim code drafted with help from Claude (Anthropic).\n"
              "Voice-over: AI text-to-speech (Kokoro). All mathematics checked by hand.\n"
              "Music: none.", 24),
        ).arrange(DOWN, buff=0.22)
        credits.scale_to_fit_height(7.2)
        if credits.width > 13:
            credits.scale_to_fit_width(13)
        self.play(FadeIn(credits, shift=UP * 0.3), run_time=1.2)
        self.wait(4)
        self.finish(tail=1.0)
