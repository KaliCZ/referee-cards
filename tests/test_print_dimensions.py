import unittest
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parents[1]
POINTS_PER_MM = 72 / 25.4


def cutting_borders(page):
    paths = []
    coordinates = []
    curves = 0
    stroke_width = 1
    for operands, operator in page.get_contents().operations:
        if operator == b"w":
            stroke_width = float(operands[0])
        elif operator == b"m":
            coordinates = [tuple(map(float, operands))]
            curves = 0
        elif operator == b"l":
            coordinates.append(tuple(map(float, operands)))
        elif operator == b"c":
            curves += 1
            coordinates.extend((float(operands[index]), float(operands[index + 1])) for index in range(0, 6, 2))
        elif operator == b"S" and curves == 4:
            horizontal = [point[0] for point in coordinates]
            vertical = [point[1] for point in coordinates]
            paths.append((min(horizontal) - stroke_width / 2, min(vertical) - stroke_width / 2,
                          max(horizontal) + stroke_width / 2, max(vertical) + stroke_width / 2))
            curves = 0
        elif operator == b"n":
            coordinates = []
            curves = 0
    return paths


class PrintDimensions(unittest.TestCase):
    def test_extra_heavy_compensation_restores_measured_height_on_both_sides(self):
        pages = PdfReader(ROOT / "print/referee-cards-A4-duplex-HP135w-extra-heavy.pdf").pages
        self.assertEqual(len(pages), 2)
        positions = []
        for page in pages:
            self.assertAlmostEqual(float(page.mediabox.width) / POINTS_PER_MM, 210, places=3)
            self.assertAlmostEqual(float(page.mediabox.height) / POINTS_PER_MM, 297, places=3)
            self.assertIn("EXTRA HEAVY", page.extract_text())
            borders = cutting_borders(page)
            self.assertEqual(len(borders), 4)
            self.assertEqual(sum(operator == b"Do" for _, operator in page.get_contents().operations), 4)
            for left, bottom, right, top in borders:
                self.assertAlmostEqual((right - left) / POINTS_PER_MM, 77, places=3)
                self.assertAlmostEqual((top - bottom) / POINTS_PER_MM * 110 / 114, 114, places=3)
                self.assertGreater(left, 5 * POINTS_PER_MM)
                self.assertGreater(bottom, 20 * POINTS_PER_MM)
                self.assertLess(right, float(page.mediabox.width) - 5 * POINTS_PER_MM)
                self.assertLess(top, float(page.mediabox.height) - 5 * POINTS_PER_MM)
                reflected = (float(page.mediabox.width) - right, bottom,
                             float(page.mediabox.width) - left, top)
                self.assertTrue(any(all(abs(actual - expected) < 0.001 for actual, expected in zip(candidate, reflected))
                                    for candidate in borders))
            positions.append(borders)
        self.assertEqual(positions[0], positions[1])

    def test_individual_cards_are_measured_size_with_full_cutting_borders(self):
        pages = PdfReader(ROOT / "print/referee-card-front-back.pdf").pages
        self.assertEqual(len(pages), 2)
        for page in pages:
            self.assertAlmostEqual(float(page.mediabox.width) / POINTS_PER_MM, 77, places=3)
            self.assertAlmostEqual(float(page.mediabox.height) / POINTS_PER_MM, 114, places=3)
            borders = cutting_borders(page)
            self.assertEqual(len(borders), 1)
            for actual, expected in zip(borders[0], [0, 0, 77 * POINTS_PER_MM, 114 * POINTS_PER_MM]):
                self.assertAlmostEqual(actual, expected, places=3)

    def test_a4_has_four_measured_cards_and_matching_duplex_positions(self):
        pages = PdfReader(ROOT / "print/referee-cards-A4-duplex.pdf").pages
        self.assertEqual(len(pages), 2)
        positions = []
        for page in pages:
            self.assertAlmostEqual(float(page.mediabox.width) / POINTS_PER_MM, 210, places=3)
            self.assertAlmostEqual(float(page.mediabox.height) / POINTS_PER_MM, 297, places=3)
            borders = cutting_borders(page)
            self.assertEqual(len(borders), 4)
            self.assertEqual(sum(operator == b"Do" for _, operator in page.get_contents().operations), 4)
            for left, bottom, right, top in borders:
                self.assertAlmostEqual((right - left) / POINTS_PER_MM, 77, places=3)
                self.assertAlmostEqual((top - bottom) / POINTS_PER_MM, 114, places=3)
                self.assertGreater(left, 0)
                self.assertGreater(bottom, 0)
                self.assertLess(right, float(page.mediabox.width))
                self.assertLess(top, float(page.mediabox.height))
            positions.append(borders)
        self.assertEqual(positions[0], positions[1])
        for left, bottom, right, top in positions[0]:
            reflected = (float(pages[0].mediabox.width) - right, bottom,
                         float(pages[0].mediabox.width) - left, top)
            self.assertTrue(any(all(abs(actual - expected) < 0.001 for actual, expected in zip(candidate, reflected))
                                for candidate in positions[1]))


if __name__ == "__main__":
    unittest.main()
