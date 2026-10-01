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
    text(drawing, title, 250, heading_top + 19, 19, True, "middle")
    label_top = heading_top + 24
    line(drawing, 18, label_top, 482, label_top)
    text(drawing, "GOALS (PLAYER / MIN)", 25, label_top + 15)
    text(drawing, "GOALS (PLAYER / MIN)", 257, label_top + 15)
    grid_top = label_top + 20
    for row in range(5):
        line(drawing, 18, grid_top + row * 22, 482, grid_top + row * 22, 1.2 if row == 2 else 0.7)
    for column in range(1, 16):
        line(drawing, 18 + column * 29, grid_top, 18 + column * 29, grid_top + 88)
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


def substitutions(drawing, heading_top):
    text(drawing, "SUBSTITUTIONS", 250, heading_top + 20, 21, True, "middle")
    header_top = heading_top + 26
    grid_top = header_top + 18
    grid_bottom = grid_top + 7 * 22
    line(drawing, 18, header_top, 482, header_top)
    for row in range(8):
        line(drawing, 18, grid_top + row * 22, 482, grid_top + row * 22)
    for team_left in [18, 250]:
        for column in range(1, 3):
            boundary = team_left + column * 232 / 3
            line(drawing, boundary, header_top, boundary, grid_bottom)
        for column, label in enumerate(["OUT", "IN", "MIN"]):
            text(drawing, label, team_left + (column + 0.5) * 232 / 3, header_top + 13, 11.5, anchor="middle")
    line(drawing, 250, header_top, 250, grid_bottom)


def main():
    drawing, layout = create_card()
    text(drawing, "MATCH NOTES", 250, 42, 24, True, "middle")
    for horizontal in [55, 115, 139, 164]:
        line(drawing, 18, horizontal, 482, horizontal)
    line(drawing, 250, 55, 250, 164)
    for vertical in [190, 422]:
        line(drawing, vertical, 55, vertical, 115)
    text(drawing, "HOME TEAM:", 25, 72)
    text(drawing, "AWAY TEAM:", 257, 72)
    for center in [220, 452]:
        text(drawing, "KICK-", center, 72, anchor="middle")
        text(drawing, "OFF", center, 86, anchor="middle")
    for start in [25, 257]:
        text(drawing, "JERSEY COLOUR:", start, 131)
    for position, label, state in [(18, "KO:", 0), (134, "HT:", 1), (250, "2.H:", 1), (366, "FT:", 1)]:
        if position in [134, 366]:
            line(drawing, position, 139, position, 164)
        stopwatch(drawing, position + 4, 143, state)
        text(drawing, label, position + 23, 157)
    goals(drawing, 164, "1. HALF")
    goals(drawing, 296, "2. HALF")
    substitutions(drawing, 428)
    logo(drawing)
    export_card(drawing, layout, "front-match-notes", "Match notes with two goal-entry rows per half")


if __name__ == "__main__":
    main()
