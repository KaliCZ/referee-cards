import json
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


DIRECTORY = Path(__file__).resolve().parent


def draw_card(document, image, left, bottom, width, height, layout):
    document.saveState()
    inset = 1.5 * mm
    radius = layout["corner_radius_mm"] * mm
    content_clip = document.beginPath()
    content_clip.roundRect(left + inset, bottom + inset, width - 2 * inset, height - 2 * inset, radius)
    document.clipPath(content_clip, stroke=0, fill=0)
    document.drawImage(str(image), left, bottom, width=width, height=height)
    document.restoreState()
    stroke_width = layout["cut_border_width_pt"]
    half_stroke = stroke_width / 2
    document.setStrokeColorRGB(0, 0, 0)
    document.setLineWidth(stroke_width)
    document.roundRect(left + half_stroke, bottom + half_stroke, width - stroke_width, height - stroke_width, radius - half_stroke, stroke=1, fill=0)


def draw_cut_marks(document, left, bottom, width, height):
    document.setStrokeColorRGB(0.55, 0.55, 0.55)
    document.setLineWidth(0.25)
    gap = 1 * mm
    length = 3 * mm
    for horizontal in (left, left + width):
        document.line(horizontal, bottom - gap, horizontal, bottom - gap - length)
        document.line(horizontal, bottom + height + gap, horizontal, bottom + height + gap + length)
    for vertical in (bottom, bottom + height):
        document.line(left - gap, vertical, left - gap - length, vertical)
        document.line(left + width + gap, vertical, left + width + gap + length, vertical)


def main():
    layout = json.loads((DIRECTORY / "card-layout.json").read_text(encoding="utf-8"))
    width = layout["width_mm"] * mm
    height = layout["height_mm"] * mm
    images = [DIRECTORY / layout[side] for side in ("front_jpeg", "back_jpeg")]
    for image in images:
        if not image.is_file():
            raise FileNotFoundError(image)
    output_directory = DIRECTORY / "print"
    output_directory.mkdir(exist_ok=True)

    individual = canvas.Canvas(str(output_directory / "referee-card-front-back.pdf"), pagesize=(width, height))
    individual.setTitle("Referee card - 77 x 114 mm, front and back")
    for image in images:
        draw_card(individual, image, 0, 0, width, height, layout)
        individual.showPage()
    individual.save()

    sheet = canvas.Canvas(str(output_directory / "referee-cards-A4-duplex.pdf"), pagesize=A4)
    sheet.setTitle("Referee cards - A4 duplex, actual size, long-edge binding")
    gap = 10 * mm
    left_margin = (A4[0] - 2 * width - gap) / 2
    bottom_margin = (A4[1] - 2 * height - gap) / 2
    if min(left_margin, bottom_margin) < 5 * mm:
        raise ValueError("The configured cards do not fit this A4 layout.")
    for image in images:
        for row in range(2):
            for column in range(2):
                left = left_margin + column * (width + gap)
                bottom = bottom_margin + row * (height + gap)
                draw_card(sheet, image, left, bottom, width, height, layout)
                draw_cut_marks(sheet, left, bottom, width, height)
        sheet.setStrokeColorRGB(0, 0, 0)
        sheet.setLineWidth(0.5)
        sheet.line(80 * mm, 12 * mm, 130 * mm, 12 * mm)
        for horizontal in (80, 130):
            sheet.line(horizontal * mm, 11 * mm, horizontal * mm, 13 * mm)
        sheet.setFont("Helvetica", 8)
        sheet.drawCentredString(A4[0] / 2, 7 * mm, "50 mm check | Print 100% / Actual size | Duplex: flip on long edge")
        sheet.showPage()
    sheet.save()
    print(f"Card canvas: {layout['width_mm']:.4f} x {layout['height_mm']:.4f} mm")
    print(output_directory / "referee-card-front-back.pdf")
    print(output_directory / "referee-cards-A4-duplex.pdf")


if __name__ == "__main__":
    main()
