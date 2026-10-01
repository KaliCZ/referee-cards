# Referee cards

Read [README.md](README.md) for printing and build commands, and
[docs/editing.md](docs/editing.md) for the current layout, source-file roles,
measurements and printer calibration. Keep those documents current when the
design or printing workflow changes.

## Editing sources

- Make layout changes in `redraw_front.py` or `redraw_back.py`; shared drawing
  and export code is in `card_drawing.py`. Use clean black-on-white vector
  artwork rather than reproducing scan artifacts.
- The print builders consume `cards/front-match-notes.jpg` and
  `cards/back-disciplinary.jpg`. These are the current print masters; the
  Python drawing sources make the design reproducible. Before redrawing,
  check for newer JPEG-only edits and incorporate them into the drawing code
  so they are not lost. SVG changes are not imported by the redraw scripts.
- Preserve the originals in `sources/` and the `*-initial-lossless.png`
  snapshots. Keep current JPEG, lossless PNG, SVG and vector PDF exports
  synchronized with any side that is redrawn.
- Preserve the current layout described in `docs/editing.md` unless the
  requested change affects it. Goal and substitution writing rows have equal
  heights; the compact team and jersey rows have their own fixed heights.

## Physical size and printer compensation

- `card-layout.json` defines the standard card size: **77 x 114 mm**, measured
  at the outside of the cutting border. Preserve visible rounded cutting
  borders and matching front/back placement. Scan crop dimensions and JPEG
  DPI metadata do not define the print size.
- Keep `build_print_pdf.py` and its two standard PDFs independent of printer
  compensation. The A4 layout contains four cards per side for long-edge
  duplex printing at Actual size / 100%.
- `build_heavy_print_pdf.py` creates the separate HP MFP 135w **Extra Heavy**
  PDF using `printer-calibration.json`. This profile's measured reduction
  from 114 mm to 110 mm is compensated vertically only. Do not apply that
  correction to the standard artwork, other printers or the Heavy profile.
- Physical confirmation of the compensated print remains pending until the
  user reports measurements. Automated geometry checks cannot establish a
  printer's actual output size. Record new measurements in the calibration
  data and editing documentation when supplied.

## Rebuild and verify

Use Python 3.12+ from the repository root:

```sh
python -m pip install -r requirements.txt
```

Run the relevant redraw command only for a side whose design changed:

```sh
python redraw_front.py
python redraw_back.py
```

After artwork or print-generation changes, rebuild all print variants and
run the geometry checks:

```sh
python build_print_pdf.py
python build_heavy_print_pdf.py
python -m unittest discover -s tests -v
```

Render and inspect both sides of each changed printable PDF for legibility,
clipping, row counts, borders and placement. Refresh `docs/front-preview.png`
or `docs/back-preview.png` from the standard card PDF when that side changes.
Commit affected sources, exports, printable PDFs and previews together.
Do not regenerate artwork or PDFs for documentation-only changes.

Arial fonts are used when available on Windows, with Helvetica fallbacks
elsewhere. Check for unintended typography changes when rebuilding on a
different platform. CI validates committed PDFs and rebuilds on Linux.

## Delivery

For new work, fetch the latest `main` and branch from it; continue an existing
open feature branch when updating its PR. Preserve unrelated local changes.
Commit and push completed work to the feature branch and keep its PR targeting
`main`. Never merge or push to `main` without an explicit user request.
Report local validation and any pending physical print checks. Do not block
the session waiting for CI; use background monitoring when available.
