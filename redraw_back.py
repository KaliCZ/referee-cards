from reportlab.graphics.shapes import Group, String
from reportlab.lib.colors import black
from reportlab.pdfbase.pdfmetrics import stringWidth

from card_drawing import HEIGHT, create_card, export_card, line, text


def vertical_label(drawing, value, center_x, center_y):
    label = Group(String(0, 0, value, fontName="CardHeading", fontSize=12, textAnchor="middle", fillColor=black))
    label.transform = (0, 1, -1, 0, center_x, HEIGHT - center_y)
    drawing.add(label)


def main():
    drawing, layout = create_card()
    title = "WARNINGS, TIME PENALTIES AND SENDINGS OFF"
    title_size = min(20, 464 * 20 / stringWidth(title, "CardHeading", 20))
    text(drawing, title, 250, 30, title_size, True, "middle")
    line(drawing, 18, 38, 482, 38)
    text(drawing, "NUMBER", 50.5, 57, 11.5, anchor="middle")
    text(drawing, "NOTES", 341, 57, 13, anchor="middle")
    vertical_label(drawing, "YELLOW", 106, 74)
    vertical_label(drawing, "SECOND", 140, 74)
    vertical_label(drawing, "YELLOW", 153, 74)
    vertical_label(drawing, "RED", 185, 74)
    for boundary in [83, 122, 161, 200]:
        line(drawing, boundary, 38, boundary, 716)
    for row in range(17):
        line(drawing, 18, 108 + row * 38, 482, 108 + row * 38)
    export_card(drawing, layout, "back-disciplinary", "Penalties with a notes column")


if __name__ == "__main__":
    main()
