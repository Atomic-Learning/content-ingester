# PPTX Data Extraction (Current Workflow)

## Purpose

This guide defines the current, cross-platform process for extracting PPTX text and images for content-ingester.

Use the script-based workflow only. Do not rely on OS-specific tools such as LibreOffice.

Default paths are resolved from `.env`:

- `CONTENT_INGESTER_INPUTS_DIR` (default: `inputs`)
- `CONTENT_INGESTER_OUTPUTS_DIR` (default: `outputs`)

## Canonical Tool

Run extraction with:

- `tools/extract_pptx_assets.py`

This script handles:

- text extraction via `python-pptx`, one entry per slide
- embedded raster image extraction via `python-pptx` and `Pillow` (any format converted to PNG)
- background policy for exported images (`transparent`, `white`, `opaque`)
- output directory collision handling

## Standard Run Procedure

1. Ensure dependencies are installed from `requirements.txt`.
2. Put source PPTX files in `<input-dir>/content-to-ingest/` (default `inputs/content-to-ingest/`).
3. Run the extractor script.
4. Confirm artifacts exist under `<output-dir>/pptx-processing/<file-name>/` (default `outputs/pptx-processing/<file-name>/`).
5. Use extracted text/image assets to generate or update page content under `<output-dir>/<slug>/`.

### Mandatory Image Embedding Rule For Page Generation

When creating `<output-dir>/<slug>/content.html` from PPTX inputs, do not stop at extraction output.

You must:

1. Copy each image actually used by the page from `<output-dir>/pptx-processing/<file-name>/resources/` into `<output-dir>/<slug>/resources/`.
2. Reference it in `content.html` with a relative path such as `resources/<image-name>.png`.
3. Include `width` and `height` attributes on each `<img>`.
4. Confirm the referenced files exist in `<output-dir>/<slug>/resources/` (not only in `<output-dir>/pptx-processing/...`).

If no images are embedded in `content.html` while source PPTX images exist, treat this as an incomplete page build.

## Operational Commands

Basic run:

```bash
python tools/extract_pptx_assets.py
```

Run with explicit output path:

```bash
python tools/extract_pptx_assets.py --output-dir outputs/pptx-processing
```

Override background when the user requests a specific mode:

```bash
python tools/extract_pptx_assets.py --background transparent
```

Allow in-place overwrite of existing extraction folders when intentionally re-running:

```bash
python tools/extract_pptx_assets.py --overwrite
```

## Output Contract

For each `<input-dir>/content-to-ingest/<name>.pptx`, expect:

- `<output-dir>/pptx-processing/<name>/text.md`
- `<output-dir>/pptx-processing/<name>/resources/*.png`

Text is organised by slide, with a `## Slide N: <title>` header per slide and `---` separators between slides.

Image filenames follow the pattern `s<slide>_img<index>.png` (for example `s002_img001.png`).

If folder-name collisions occur and `--overwrite` is not set, the script writes to suffixed folders (for example `slides-2`).

## Background Rules

Always use `white` background unless the user explicitly requests a different mode.

Available modes (pass via `--background`):

- `white` (**default**): flattened white-background export
- `transparent`: preserves alpha channel; use only when the user asks for it
- `opaque`: non-alpha export without white fill; use only when the user asks for it

## Blocker Questions

When the workflow is blocked or ambiguous, ask concise user questions before proceeding:

1. Should slides with only vector shapes and no raster images be noted as visual gaps in the page content?
2. If output folders already exist, should extraction overwrite them (`--overwrite`) or create new suffixed folders?

## Consistency Checks After Extraction

1. `text.md` is present and readable.
2. Expected images exist in `resources/`.
3. No unexpected temporary extraction files remain.
4. Referenced resources in generated page `content.html` resolve correctly.
5. If PPTX images exist and are relevant, they are copied into `<output-dir>/<slug>/resources/` and embedded in `content.html`.

## Known Limitations

- Vector shapes, SmartArt, charts, and drawn shapes are not rasterised. Their text content (if any) is extracted; their visual appearance is not. The extraction result reports a `skipped_vector_shapes` count so you know how many were encountered.
- Slide background images are not extracted; only shapes with image fills and picture placeholders are captured.
- A future `--render-vector-slides` option may address vector rendering via an optional LibreOffice fallback.

## Related References

- `tools/extract_pptx_assets.py`
- `.github/instructions/content-ingestion.instructions.md`
- `.github/instructions/updating-proposed-structure.md`
- `.github/instructions/atomisation-guidelines.md`
