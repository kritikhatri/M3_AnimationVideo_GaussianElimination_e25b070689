"""
Build Storyboard.pdf (6-scene storyboard with a still from each scene).
Run after build_video.py:  python make_storyboard.py
"""
import json
import os
import subprocess

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (Image, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle, PageBreak)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
VIDS = os.path.join(HERE, "media", "videos", "gaussian_elimination", "1080p30")

SCENES = [
    ("S1_Hook", "1. Hook / Context", 0.75,
     "Spark curiosity: why do we need a method?",
     "Title card (name, ID, course). System A (all variables mixed) next to System B "
     "(triangular). Arrow labelled <i>same solution</i>; reveal (1, 2, 3).",
     "Hard vs easy system: 7z = 21 gives z = 3 instantly. Elimination turns A into B."),
    ("S2_Concept", "2. Concept Introduction", 0.85,
     "Define notation, the three row operations and the goal.",
     "Equations morph into the augmented matrix [A | b]; braces label A and b; rows "
     "R1-R3, columns x, y, z, b. Panel of row operations. Echelon template with pivots "
     "(yellow), zeros (green) and a staircase. Learning objective on screen.",
     "Swap R_i &#8596; R_j; scale R_i &#8594; kR_i (k &#8800; 0); replace R_i &#8594; R_i + cR_j. "
     "Row echelon form: zeros below each pivot."),
    ("S3_Intuition", "3. Visual Intuition", 0.85,
     "Build geometric understanding before the algebra.",
     "3D axes, three translucent planes meeting at a yellow point (1, 2, 3). Each row "
     "operation re-draws one plane; camera slowly orbits; the point never moves. Final "
     "plane 7z = 21 is horizontal (z = 3).",
     "If R1 and R2 hold then R2 - 2R1 holds; the step is reversible (add 2R1 back), so "
     "the solution set is preserved."),
    ("S4_Example", "4. Worked Example", 0.6,
     "Show every intermediate calculation.",
     "Pivots boxed in yellow. Side panel shows each row subtraction entry by entry, then "
     "the new row replaces the old one in the matrix. Staircase marks echelon form. "
     "Back-substitution bottom-up, then a check with ticks.",
     "R2 - 2R1 = [0, -1, -3 | -11];  R3 - R1 = [0, -2, 1 | -1];  R3 - 2R2 = [0, 0, 7 | 21]. "
     "z = 3, y = 2, x = 1; substitute into all three original equations."),
    ("S5_Interpretation", "5. Interpretation", 0.6,
     "Connect the algebra back to meaning.",
     "Echelon matrix with pivots circled: 3 pivots, 3 unknowns. Then three cards: "
     "unique / no solution / infinitely many, each with its tell-tale last row.",
     "Pivot in every column &#8658; unique. [0 0 0 | 5] &#8658; 0 = 5, no solution. "
     "[0 0 0 | 0] &#8658; free variable, infinitely many."),
    ("S6_Summary", "6. Summary & Credits", 0.4,
     "Reinforce takeaways and cite sources.",
     "Three numbered takeaways, then closing frame with references, tools, "
     "AI disclosure and music credit (none).",
     "Recap: [A | b] &#8594; echelon form &#8594; back-substitute &amp; check."),
]


def frame(scene, frac, out):
    d = json.load(open(os.path.join(HERE, "cues", scene + ".json")))["duration"]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{d * frac:.2f}",
                    "-i", os.path.join(VIDS, scene + ".mp4"), "-frames:v", "1",
                    "-vf", "scale=640:-1", out], check=True)
    return d


def main():
    os.makedirs(os.path.join(HERE, "frames"), exist_ok=True)
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["BodyText"], fontSize=8.5, leading=11)
    head = ParagraphStyle("h", parent=body, textColor=colors.white, fontName="Helvetica-Bold")
    doc = SimpleDocTemplate(os.path.join(ROOT, "Storyboard.pdf"), pagesize=landscape(A4),
                            leftMargin=1.2 * cm, rightMargin=1.2 * cm,
                            topMargin=1.0 * cm, bottomMargin=1.0 * cm)
    story = [
        Paragraph("Storyboard - Gaussian Elimination (M3 Animation Video)", ss["Title"]),
        Paragraph("<b>Learning objective:</b> By the end of this video, the viewer will be able to "
                  "reduce a 3 &#215; 3 system to row echelon form using elementary row operations, "
                  "solve it by back-substitution, and explain why row operations preserve the "
                  "solution set.", ss["BodyText"]),
        Paragraph("<b>Worked example:</b> x + y + z = 6,  2x + y - z = 1,  x - y + 2z = 5  "
                  "&#8594;  (x, y, z) = (1, 2, 3).   <b>Tool:</b> Manim Community Edition (Python).  "
                  "<b>Colour code:</b> yellow = pivot, blue = row operation, green = eliminated "
                  "zero, orange = right-hand side b.", ss["BodyText"]),
        Spacer(1, 8),
    ]
    rows = [[Paragraph(h, head) for h in
             ["Scene / time", "Still", "Purpose", "Visual plan", "Narration &amp; maths plan"]]]
    t = 0.0
    for scene, title, frac, purpose, visual, maths in SCENES:
        img = os.path.join(HERE, "frames", scene + ".png")
        d = frame(scene, frac, img)
        rows.append([Paragraph(f"<b>{title}</b><br/>{int(t // 60)}:{int(t % 60):02d} - "
                               f"{int((t + d) // 60)}:{int((t + d) % 60):02d}", body),
                     Image(img, width=6.4 * cm, height=3.6 * cm),
                     Paragraph(purpose, body), Paragraph(visual, body), Paragraph(maths, body)])
        t += d
    tbl = Table(rows, colWidths=[3.0 * cm, 6.8 * cm, 3.6 * cm, 6.6 * cm, 6.9 * cm], repeatRows=1)
    tbl.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0e1621")),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f2f5f9")]),
    ]))
    story += [tbl, Spacer(1, 6),
              Paragraph(f"Total running time: {int(t // 60)}:{int(t % 60):02d} "
                        "(target 5 min, limit 7 min). Full narration with timings: "
                        "Narration_Script.md.", body)]
    doc.build(story)
    print("wrote Storyboard.pdf")


if __name__ == "__main__":
    main()
