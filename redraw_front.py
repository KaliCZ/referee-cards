import json
import os
from pathlib import Path

import pypdfium2 as pdfium
from reportlab.graphics import renderPDF, renderSVG
from reportlab.graphics.shapes import Circle, Drawing, Line, Path as VectorPath, Rect, String
from reportlab.lib.colors import black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import Font


DIRECTORY = Path(__file__).resolve().parent
HEIGHT = 750


def line(drawing, left, top, right, bottom, weight=0.7):
    drawing.add(Line(left, HEIGHT - top, right, HEIGHT - bottom, strokeColor=black, strokeWidth=weight))


def text(drawing, value, left, baseline, size=11.5, bold=False, anchor="start"):
    drawing.add(String(left, HEIGHT - baseline, value, fontName="CardHeading" if bold else "CardRegular", fontSize=size, textAnchor=anchor, fillColor=black))


def stopwatch(drawing, left, top, state):
    center_x = left + 7
    center_y = HEIGHT - top - 9
    drawing.add(Circle(center_x, center_y, 6.5, fillColor=white, strokeColor=black, strokeWidth=1.2))
    drawing.add(Rect(center_x - 2.3, center_y + 7.2, 4.6, 2, fillColor=black, strokeColor=None))
    if state:
        line(drawing, center_x, top + 9, center_x, top + 4, 1)
        line(drawing, center_x, top + 9, center_x + 3.5, top + 10.5, 1)


def goals(drawing, heading_top, title):
    text(drawing, title, 250, heading_top + 21, 19, True, "middle")
    label_top = heading_top + 29
    line(drawing, 18, label_top, 482, label_top)
    text(drawing, "GOALS (MIN)", 25, label_top + 18)
    text(drawing, "GOALS (MIN)", 257, label_top + 18)
    grid_top = label_top + 26
    for row in range(3):
        line(drawing, 18, grid_top + row * 26, 482, grid_top + row * 26)
    for column in range(1, 16):
        line(drawing, 18 + column * 29, grid_top, 18 + column * 29, grid_top + 52)
    line(drawing, 250, label_top, 250, grid_top)


def logo(drawing):
    origin_x = 420
    origin_y = 650
    paths = [
        ((28, 0), [(27, 25, 17, 41, 0, 49), (24, 43, 30, 30, 28, 0)]),
        ((31, 0), [(31, 30, 39, 41, 57, 49), (41, 36, 36, 22, 31, 0)]),
        ((3, 51), [(22, 38, 35, 37, 55, 51), (35, 45, 23, 45, 3, 51)]),
    ]
    for start, curves in paths:
        path = VectorPath(fillColor=black, strokeColor=None)
        path.moveTo(origin_x + start[0], HEIGHT - origin_y - start[1])
        for curve in curves:
            path.curveTo(origin_x + curve[0], HEIGHT - origin_y - curve[1], origin_x + curve[2], HEIGHT - origin_y - curve[3], origin_x + curve[4], HEIGHT - origin_y - curve[5])
        path.closePath()
        drawing.add(path)
    text(drawing, "SELECT", 449, 717, 18, True, "middle")


def main():
    layout = json.loads((DIRECTORY / "card-layout.json").read_text())
    fonts = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
    if (fonts / "arial.ttf").is_file() and (fonts / "ARIALNB.TTF").is_file():
        pdfmetrics.registerFont(TTFont("CardRegular", str(fonts / "arial.ttf")))
        pdfmetrics.registerFont(TTFont("CardHeading", str(fonts / "ARIALNB.TTF")))
    else:
        pdfmetrics.registerFont(Font("CardRegular", "Helvetica", "WinAnsiEncoding"))
        pdfmetrics.registerFont(Font("CardHeading", "Helvetica-Bold", "WinAnsiEncoding"))
    drawing = Drawing(500, HEIGHT)
    drawing.add(Rect(0, 0, 500, HEIGHT, fillColor=white, strokeColor=None))
    border_width = layout["cut_border_width_pt"] / (layout["width_mm"] * 72 / 25.4 / 500)
    border_inset = border_width / 2
    radius_x = layout["corner_radius_mm"] * 500 / layout["width_mm"]
    radius_y = layout["corner_radius_mm"] * HEIGHT / layout["height_mm"]
    drawing.add(Rect(border_inset, border_inset, 500 - border_width, HEIGHT - border_width, rx=radius_x - border_inset, ry=radius_y - border_inset, fillColor=None, strokeColor=black, strokeWidth=border_width))
    text(drawing, "MATCH NOTES", 250, 62, 24, True, "middle")
    for horizontal in [75, 145, 171, 198]:
        line(drawing, 18, horizontal, 482, horizontal)
    line(drawing, 250, 75, 250, 198)
    for vertical in [190, 422]:
        line(drawing, vertical, 75, vertical, 145)
    text(drawing, "HOME TEAM:", 25, 92)
    text(drawing, "AWAY TEAM:", 257, 92)
    for center in [220, 452]:
        text(drawing, "KICK-", center, 92, anchor="middle")
        text(drawing, "OFF", center, 106, anchor="middle")
    for start in [25, 257]:
        text(drawing, "JERSEY COLOUR:", start, 163)
    for position, label, state in [(18, "KO:", 0), (134, "HT:", 1), (250, "2.H:", 1), (366, "FT:", 1)]:
        if position in [134, 366]:
            line(drawing, position, 171, position, 198)
        stopwatch(drawing, position + 4, 175, state)
        text(drawing, label, position + 23, 189)
    goals(drawing, 198, "1. HALF")
    goals(drawing, 305, "2. HALF")
    text(drawing, "SUBSTITUTIONS", 250, 438, 21, True, "middle")
    for row in range(8):
        line(drawing, 18, 445 + row * 26, 482, 445 + row * 26)
    for column in range(1, 8):
        line(drawing, 18 + column * 58, 445, 18 + column * 58, 627)
    for row in range(7):
        for column, label in [(0, "OUT"), (2, "IN"), (4, "OUT"), (6, "IN")]:
            text(drawing, label, 18 + (column + 0.5) * 58, 462 + row * 26, 11.5, anchor="middle")
    logo(drawing)

    scale_x = layout["width_mm"] * 72 / 25.4 / 500
    scale_y = layout["height_mm"] * 72 / 25.4 / HEIGHT
    drawing.scale(scale_x, scale_y)
    drawing.width = 500 * scale_x
    drawing.height = HEIGHT * scale_y
    vector_path = DIRECTORY / "cards/front-match-notes-vector.pdf"
    renderPDF.drawToFile(drawing, str(vector_path), title="Clean vector match-notes card")
    renderSVG.drawToFile(drawing, str(DIRECTORY / "cards/front-match-notes.svg"))
    document = pdfium.PdfDocument(str(vector_path))
    rendered = document[0].render(scale=600 / 72).to_pil().convert("RGB")
    rendered.save(DIRECTORY / "cards/front-match-notes-current-lossless.png", dpi=(600, 600))
    rendered.save(DIRECTORY / "cards/front-match-notes.jpg", quality=100, subsampling=0, dpi=(600, 600))
    print(vector_path)
    print("JPEG and PNG exported at", rendered.size)


if __name__ == "__main__":
    main()
