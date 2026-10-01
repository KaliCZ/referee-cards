# Printable referee cards

Football referee cards sized **77 x 114 mm**, with rounded cutting borders and layouts designed for black-and-white printing.

**[Download the A4 print PDF](https://github.com/KaliCZ/referee-cards/raw/refs/heads/main/print/referee-cards-A4-duplex.pdf)**

No software setup is needed to print. The PDFs are already included in the repository.

## Print and cut

1. Open [`print/referee-cards-A4-duplex.pdf`](print/referee-cards-A4-duplex.pdf).
2. Select **A4, portrait, Actual size / 100%**, with one PDF page per paper side.
3. Enable **duplex printing, flip on long edge**. Disable Fit, Shrink, booklet mode and borderless enlargement.
4. Print one test sheet. The scale bar should measure **50 mm**, and each card's outer border should measure **77 x 114 mm**.
5. Cut along the outside of the rounded black border. One duplex A4 sheet makes **four cards**.

If front/back registration is offset, adjust the printer's duplex alignment. The PDF positions are symmetric.

[`print/referee-card-front-back.pdf`](print/referee-card-front-back.pdf) contains two individual card-sized pages for a print shop or other layouts.

## HP MFP 135w: Extra Heavy profile

Use [`print/referee-cards-A4-duplex-HP135w-extra-heavy.pdf`](print/referee-cards-A4-duplex-HP135w-extra-heavy.pdf) with **Extra Heavy**, **A4 portrait**, **Actual size / 100%**, and **long-edge duplex** (manually refeed if needed).

This separate version compensates for Pavel's measured result: a 114 mm card printed 110 mm tall with Extra Heavy, while its width remained correct. It stretches only the card height by **114 / 110 = 1.03636**, making the PDF borders **77 x 118.145 mm**. After the same printer compression, they should measure **77 x 114 mm**. Both sides use matching positions. Test one sheet and measure both sides before printing a batch; the correction has not yet been physically verified.

Use the standard PDF for Plain Paper, other printers or a print shop. The **Heavy** profile needs a separate measurement; this correction is specifically for **Extra Heavy**. Compensation does not change the printer's supported paper-weight range.

Rebuild the compensated PDF with `python build_heavy_print_pdf.py`. The reference and measured heights are stored in `printer-calibration.json`; card masters and standard dimensions stay unchanged.

## Clone and print

```sh
git clone https://github.com/KaliCZ/referee-cards.git
cd referee-cards
```

Open the A4 PDF in the `print` folder and use the settings above.

## Card layouts

| Match notes | Penalties and sending off |
| --- | --- |
| ![Match-notes front](docs/front-preview.png) | ![Penalties back](docs/back-preview.png) |

The front has compact Home/Away and Ball fields, jersey colours, **two player/minute goal-entry rows per team per half**, and **seven substitution rows per team** beneath Out, In and Min column headers. Each goal-entry row is a pair of thin rows: player number above, minute below. The back has 16 unnumbered rows with a compact Number column for handwritten player numbers, Yellow, Second Yellow, Red and a wide **Notes column** with matching horizontal rules for handwritten reasons.

## Edit and rebuild

The current JPEG masters are [`cards/front-match-notes.jpg`](cards/front-match-notes.jpg) and [`cards/back-disciplinary.jpg`](cards/back-disciplinary.jpg). The fixed dimensions and border settings are in [`card-layout.json`](card-layout.json). Both sides have lossless PNG companions and editable vector exports.

Printing needs no Python. Rebuilding requires **Python 3.12+**:

```sh
python -m pip install -r requirements.txt
python build_print_pdf.py
python build_heavy_print_pdf.py
python -m unittest discover -s tests
```

The standard builder reads the JPEGs and overwrites the two standard files in `print`. The heavy-paper builder writes only the separate compensated A4 PDF. Both add vector cutting borders without altering the JPEG masters.

For a clean redesign, edit `redraw_front.py` or `redraw_back.py`, then run:

```sh
python redraw_front.py
python redraw_back.py
python build_print_pdf.py
python build_heavy_print_pdf.py
python -m unittest discover -s tests
```

This regenerates both sides' JPEGs, lossless PNGs, SVGs and vector PDFs. The shared drawing code uses Arial fonts when available on Windows and built-in Helvetica elsewhere, so regenerated lettering can differ slightly across platforms. The checked-in PDFs print identically on any platform.

See [editing and size notes](docs/editing.md) for source-file roles and scan measurements.

For future agent sessions, [AGENTS.md](AGENTS.md) defines the editing, rebuilding,
validation and printer-calibration workflow.

## Project contents

- `print/`: ready-to-print PDFs.
- `cards/`: current JPEG masters, lossless companions, initial snapshots and vector exports of both sides.
- `sources/`: original PNG and PDF scans used as the layout reference.
- `docs/`: previews and editing notes.
- `build_print_pdf.py`: portable PDF builder.
- `build_heavy_print_pdf.py`: separate HP Extra Heavy compensation builder.
- `printer-calibration.json`: measured printer-profile height correction.
- `redraw_front.py`: vector front drawing and raster export.
- `redraw_back.py`: vector penalties drawing and raster export.
- `card_drawing.py`: shared drawing, fonts, sizing and export functions.
- `tests/`: checks for physical sizes, complete borders and duplex positioning.

The layout was adapted from scanned SELECT referee cards. The current front omits the logo and large title to give more room to handwriting. Goal and substitution writing rows are equally tall (5.32 mm); team and jersey rows remain compact.
