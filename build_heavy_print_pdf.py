import json

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas

from build_print_pdf import DIRECTORY, draw_card, draw_cut_marks


def main():
    layout = json.loads((DIRECTORY / "card-layout.json").read_text(encoding="utf-8"))
    calibration = json.loads((DIRECTORY / "printer-calibration.json").read_text(encoding="utf-8"))
    vertical_scale = calibration["reference_height_mm"] / calibration["measured_height_mm"]
    width = layout["width_mm"] * mm
    height = layout["height_mm"] * vertical_scale * mm
    gap = 10 * mm
    left_margin = (A4[0] - 2 * width - gap) / 2
    bottom_margin = (A4[1] - 2 * height - gap) / 2
    if min(left_margin, bottom_margin) < 5 * mm:
        raise ValueError("The compensated cards do not fit this A4 layout.")
    output = DIRECTORY / "print" / "referee-cards-A4-duplex-HP135w-extra-heavy.pdf"
    output.parent.mkdir(exist_ok=True)
    sheet = canvas.Canvas(str(output), pagesize=A4)
    sheet.setTitle("Referee cards - HP MFP 135w Extra Heavy compensation")
    for side in ["front_jpeg", "back_jpeg"]:
        for row in range(2):
            for column in range(2):
                left = left_margin + column * (width + gap)
                bottom = bottom_margin + row * (height + gap)
                draw_card(sheet, DIRECTORY / layout[side], left, bottom, width, height, layout)
                draw_cut_marks(sheet, left, bottom, width, height)
        sheet.setStrokeColorRGB(0, 0, 0)
        sheet.setLineWidth(0.5)
        sheet.line(80 * mm, 14 * mm, 130 * mm, 14 * mm)
        for horizontal in [80, 130]:
            sheet.line(horizontal * mm, 13 * mm, horizontal * mm, 15 * mm)
        sheet.setFont("Helvetica", 8)
        sheet.drawCentredString(A4[0] / 2, 9 * mm, "HP MFP 135w | EXTRA HEAVY | Actual size / 100% | Long-edge duplex")
        sheet.drawCentredString(A4[0] / 2, 5 * mm,
                               f"50 mm check | Target card: {layout['width_mm']:g} x {layout['height_mm']:g} mm"
                               f" | Height correction: {calibration['reference_height_mm']:g} / {calibration['measured_height_mm']:g}")
        sheet.showPage()
    sheet.save()
    print(f"Compensated PDF card: {width / mm:.4f} x {height / mm:.4f} mm")
    print(output)


if __name__ == "__main__":
    main()
