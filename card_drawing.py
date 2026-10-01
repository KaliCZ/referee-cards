import json
import os
from pathlib import Path

import pypdfium2 as pdfium
from reportlab.graphics import renderPDF, renderSVG
from reportlab.graphics.shapes import Drawing, Line, Rect, String
from reportlab.lib.colors import black, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import Font
from reportlab.pdfbase.ttfonts import TTFont


DIRECTORY = Path(__file__).resolve().parent
HEIGHT = 750


def line(drawing, left, top, right, bottom, weight=0.7):
    drawing.add(Line(left, HEIGHT - top, right, HEIGHT - bottom, strokeColor=black, strokeWidth=weight))


def text(drawing, value, left, baseline, size=11.5, bold=False, anchor="start"):
    drawing.add(String(left, HEIGHT - baseline, value, fontName="CardHeading" if bold else "CardRegular", fontSize=size, textAnchor=anchor, fillColor=black))


def create_card():
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
    return drawing, layout


def export_card(drawing, layout, name, title):
    scale_x = layout["width_mm"] * 72 / 25.4 / 500
    scale_y = layout["height_mm"] * 72 / 25.4 / HEIGHT
    drawing.scale(scale_x, scale_y)
    drawing.width = 500 * scale_x
    drawing.height = HEIGHT * scale_y
    vector_path = DIRECTORY / "cards" / f"{name}-vector.pdf"
    renderPDF.drawToFile(drawing, str(vector_path), title=title)
    renderSVG.drawToFile(drawing, str(DIRECTORY / "cards" / f"{name}.svg"))
    document = pdfium.PdfDocument(str(vector_path))
    rendered = document[0].render(scale=600 / 72).to_pil().convert("RGB")
    rendered.save(DIRECTORY / "cards" / f"{name}-current-lossless.png", dpi=(600, 600))
    rendered.save(DIRECTORY / "cards" / f"{name}.jpg", quality=100, subsampling=0, dpi=(600, 600))
    print(vector_path)
    print("JPEG and PNG exported at", rendered.size)
