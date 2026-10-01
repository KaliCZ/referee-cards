from card_drawing import create_card, export_card, line, text


CONTENT_TOP = 26.5
ENTRY_ROW_HEIGHT = 33.6
TEAM_DIVIDER_WIDTH = 2.1


def goals(drawing, heading_top, title):
    text(drawing, title, 250, heading_top + 19, 19, True, "middle")
    label_top = heading_top + 24
    line(drawing, 18, label_top, 482, label_top)
    text(drawing, "GOALS (PLAYER / MIN)", 25, label_top + 15)
    text(drawing, "GOALS (PLAYER / MIN)", 257, label_top + 15)
    grid_top = label_top + 20
    for row in range(5):
        line(drawing, 18, grid_top + row * ENTRY_ROW_HEIGHT, 482, grid_top + row * ENTRY_ROW_HEIGHT, 1.2 if row == 2 else 0.7)
    for column in range(1, 16):
        if column != 8:
            line(drawing, 18 + column * 29, grid_top, 18 + column * 29, grid_top + 4 * ENTRY_ROW_HEIGHT)
    line(drawing, 250, label_top, 250, grid_top + 4 * ENTRY_ROW_HEIGHT, TEAM_DIVIDER_WIDTH)


def substitutions(drawing, heading_top):
    text(drawing, "SUBSTITUTIONS", 250, heading_top + 20, 21, True, "middle")
    header_top = heading_top + 26
    grid_top = header_top + 18
    grid_bottom = grid_top + 7 * ENTRY_ROW_HEIGHT
    line(drawing, 18, header_top, 482, header_top)
    for row in range(8):
        line(drawing, 18, grid_top + row * ENTRY_ROW_HEIGHT, 482, grid_top + row * ENTRY_ROW_HEIGHT)
    for team_left in [18, 250]:
        for column in range(1, 3):
            boundary = team_left + column * 232 / 3
            line(drawing, boundary, header_top, boundary, grid_bottom)
        for column, label in enumerate(["OUT", "IN", "MIN"]):
            text(drawing, label, team_left + (column + 0.5) * 232 / 3, header_top + 13, 11.5, anchor="middle")
    line(drawing, 250, header_top, 250, grid_bottom, TEAM_DIVIDER_WIDTH)


def main():
    drawing, layout = create_card()
    for horizontal in [CONTENT_TOP, CONTENT_TOP + 37, CONTENT_TOP + 61]:
        line(drawing, 18, horizontal, 482, horizontal)
    line(drawing, 250, CONTENT_TOP, 250, CONTENT_TOP + 61, TEAM_DIVIDER_WIDTH)
    for vertical in [190, 422]:
        line(drawing, vertical, CONTENT_TOP, vertical, CONTENT_TOP + 37)
    text(drawing, "HOME:", 25, CONTENT_TOP + 17)
    text(drawing, "AWAY:", 257, CONTENT_TOP + 17)
    for center in [220, 452]:
        text(drawing, "BALL", center, CONTENT_TOP + 17, anchor="middle")
    for start in [25, 257]:
        text(drawing, "JERSEY COLOUR:", start, CONTENT_TOP + 53)
    first_half_top = CONTENT_TOP + 61
    second_half_top = first_half_top + 44 + 4 * ENTRY_ROW_HEIGHT
    substitutions_top = second_half_top + 44 + 4 * ENTRY_ROW_HEIGHT
    goals(drawing, first_half_top, "1. HALF")
    goals(drawing, second_half_top, "2. HALF")
    substitutions(drawing, substitutions_top)
    export_card(drawing, layout, "front-match-notes", "Match notes with two goal-entry rows per half")


if __name__ == "__main__":
    main()
