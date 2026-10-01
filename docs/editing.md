# Editing and dimensions

## Which files to edit

The PDF builder reads the current JPEGs in `cards/` and `card-layout.json`. Commit changes to the relevant masters and the rebuilt PDFs together. Keep the `*-current-lossless.png` companions synchronized if editing them. The `*-initial-lossless.png` files are historical snapshots, not the latest artwork.

`redraw_front.py` and `redraw_back.py` are the editable drawing sources. Both use `card_drawing.py` for shared fonts, physical sizing and exports. Each creates its side's JPEG, PNG, SVG and vector PDF. An SVG edit is not imported into the Python drawing script. Include any newer JPEG-only edits in the corresponding script before regenerating, or they will be overwritten. The normal print builder never runs the redraw automatically.

The front has a compact Home/Away and Ball header, a jersey-colour row and no match-timing row, giving more height to the goals grid. It has seven blank substitution rows per team beneath Out, In and Min column headers. Each half has two goal-entry rows per team; each entry row pairs a player-number row with a minute row below it. The heavier horizontal rule separates the two pairs. The penalties table has 16 unnumbered rows and five columns: Number, Yellow, Second Yellow, Red and Notes. The Number column is compact and blank for handwritten player numbers, leaving more width for Notes. All notes rows align with the penalty rows. Both sides use black vector artwork on white.

Use lossless working files during edits and export the finished JPEG once at maximum quality. JPEG DPI metadata does not control the print size; the JSON dimensions do.

## Physical dimensions

The original card was measured by its owner: **77 mm wide by 114 mm tall**. That measurement supersedes the earlier scan-crop estimate of approximately 78.62 x 118 mm, which included white margins.

The original PDF page is 595 x 842 points, or 209.9028 x 297.0389 mm. Its embedded image is 4962 x 7014 pixels. At that scale, a 77 x 114 mm rectangle corresponds to approximately 1820.24 x 2691.89 pixels. An outline overlay fits the visible card edges well. Some edges disappear into the white scanner background, so the scan alone cannot confirm them precisely. The crop coordinates retained in the JSON document the initial extraction only.

Each printed card's border has an outer extent of exactly 77 x 114 mm. The 0.35-point stroke is placed inward. Cut along its outer edge. The 3 mm corner radius is an approximation; it was not measured.

The builder clips a rounded inset of 1.5 mm from the JPEG edges to suppress older outlines before adding a common vector border. Keep important artwork inside that area. Both sides share the same border and page positions.

## Validate a revision

The separate HP MFP 135w Extra Heavy PDF is built by `build_heavy_print_pdf.py` from the same JPEGs. `printer-calibration.json` records the standard card's 114 mm reference height and its measured 110 mm output with Extra Heavy. The builder applies 114/110 to card heights only, producing 77 x 118.145 mm PDF borders intended to print at 77 x 114 mm with that profile. The standard PDFs and artwork retain their original dimensions. A different driver profile needs its own measured calibration, and the compensated output still needs a physical test on both sides.

Run both builders and tests, then visually inspect both sides of each PDF for legible labels, row counts, clipping and border visibility. Print a test sheet at 100%, measure the 50 mm scale bar and 77 x 114 mm border, and check the front/back registration before a batch.

The automated checks run for pushes and pull requests. They inspect committed PDFs and rebuild the project on Linux to check portability. They do not replace visual inspection or a physical printer check.
