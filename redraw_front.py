from reportlab.graphics.shapes import Circle, Path as VectorPath, Rect
from reportlab.lib.colors import black, white

from card_drawing import HEIGHT, create_card, export_card, line, text


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
    drawing, layout = create_card()
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
    for team_left in [18, 250]:
        for offset in [30, 80, 102, 154, 182]:
            line(drawing, team_left + offset, 445, team_left + offset, 627)
    line(drawing, 250, 445, 250, 627)
    for row in range(7):
        for team_left in [18, 250]:
            for offset, label in [(15, "OUT"), (91, "IN"), (168, "MIN")]:
                text(drawing, label, team_left + offset, 462 + row * 26, 11.5, anchor="middle")
    logo(drawing)
    export_card(drawing, layout, "front-match-notes", "Match notes with substitution minutes")


if __name__ == "__main__":
    main()
