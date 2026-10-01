# Editing and dimensions

## Which files to edit

The PDF builder reads the current JPEGs in `cards/` and `card-layout.json`. Commit changes to the relevant masters and the rebuilt PDFs together. Keep the `*-current-lossless.png` companions synchronized if editing them. The `*-initial-lossless.png` files are historical snapshots, not the latest artwork.

For the front, `redraw_front.py` is the editable drawing source. It creates the JPEG, PNG, SVG and vector PDF. An SVG edit is not imported into the Python drawing script. Include any newer JPEG-only edits in the script before regenerating, or they will be overwritten. The normal print builder never runs the redraw automatically.

Use lossless working files during edits and export the finished JPEG once at maximum quality. JPEG DPI metadata does not control the print size; the JSON dimensions do.

## Physical dimensions

The original card was measured by its owner: **77 mm wide by 114 mm tall**. That measurement supersedes the earlier scan-crop estimate of approximately 78.62 x 118 mm, which included white margins.

The original PDF page is 595 x 842 points, or 209.9028 x 297.0389 mm. Its embedded image is 4962 x 7014 pixels. At that scale, a 77 x 114 mm rectangle corresponds to approximately 1820.24 x 2691.89 pixels. An outline overlay fits the visible card edges well. Some edges disappear into the white scanner background, so the scan alone cannot confirm them precisely. The crop coordinates retained in the JSON document the initial extraction only.

Each printed card's border has an outer extent of exactly 77 x 114 mm. The 0.35-point stroke is placed inward. Cut along its outer edge. The 3 mm corner radius is an approximation; it was not measured.

The builder clips a rounded inset of 1.5 mm from the JPEG edges to suppress older outlines before adding a common vector border. Keep important artwork inside that area. Both sides share the same border and page positions.

## Validate a revision

Run the builder and tests, then visually inspect both PDF pages for legible labels, row counts, clipping and border visibility. Print a test sheet at 100%, measure the 50 mm scale bar and 77 x 114 mm border, and check the front/back registration before a batch.

The automated checks run for pushes and pull requests. They inspect committed PDFs and rebuild the project on Linux to check portability. They do not replace visual inspection or a physical printer check.
