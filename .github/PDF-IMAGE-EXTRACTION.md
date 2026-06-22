# PDF Processing for Content-Ingester: Text and Images

## Overview
When processing PDF source material for content-ingester, extract both text and images in a coordinated workflow. Preserve background intent for images and organize both assets for integration into atomic learning pages.

## Workflow

### Phase 1: Text Extraction

#### Step 1.1: Extract Text from PDF
```bash
pdftotext <pdf_path> -
```
Output to stdout for inspection, or redirect to a file for storage.

#### Step 1.2: Review and Summarize
- Skim the extracted text to understand the document structure and main concepts.
- Identify key sections, learning objectives, and hierarchies.
- Note any specialized terms or prerequisite concepts that may need separate pages.

#### Step 1.3: Plan Content Atomization
Based on the text, determine:
- What constitutes a single learning objective per page?
- Are there natural breaks for separate pages?
- What prerequisites might be missing from the platform?
- Which sections should be omitted (already covered elsewhere)?

### Phase 2: Image Extraction

#### Step 2.1: Identify Images in the PDF
```bash
pdfimages -list <pdf_path>
```
Shows all embedded images, their dimensions, color type, and whether they have soft masks.

#### Step 2.2: Ask the User About Background Intent
**Before extracting**, clarify the desired background for each image:
- **Transparent**: Use the soft mask to create RGBA with alpha channel. Best for logos, diagrams, infographics.
- **White**: Fill masked areas with white instead of preserving transparency.
- **Opaque**: Extract without mask processing (standard RGB).

Default assumption: **Transparent** for technical diagrams and project overviews.

#### Step 2.3: Initial Extraction
```bash
pdfimages -png <pdf_path> <output_prefix>
```
Creates numbered files: `<prefix>-000.png`, `<prefix>-001.png`, etc.

#### Step 2.4: Inspect Extracted Layers
```bash
file <prefix>-*.png
view_image <prefix>-000.png
view_image <prefix>-001.png
```
Identify which is the RGB layer (usually `-000.png`) and which is the soft mask if present (usually `-001.png` as grayscale).

#### Step 2.5: Process Images to Desired Background
**For Transparent Background:**
Use a standard-library Python script to combine the RGB layer with its soft mask:
- Parse both PNG files using struct/zlib/PIL-free methods
- Apply PNG filtering per row (Paeth, Sub, Up, Average)
- Create RGBA by concatenating RGB bytes with mask alpha channel
- Write a new PNG with IHDR (RGBA), IDAT, IEND chunks

If PIL/Pillow is available, use it directly instead; this avoids a dependency.

**For White Background:**
Use PIL or similar to fill transparent areas with white, or extract RGB only and paste on white canvas.

**For Opaque:**
Use RGB extraction directly.

#### Step 2.6: Verify Output
```bash
file <final_asset>
view_image <final_asset>
```
Confirm the result displays correctly with the intended background (transparent, white, or opaque).

#### Step 2.7: Clean Up
Remove intermediate extraction files and unused layers. Keep only the final assets.

### Phase 3: Integration into Content-Ingester

#### Step 3.1: Create Proposed Structure
Based on text extraction and planned atomization, create `outputs/proposed_structure.json` following `.github/proposed-structure-format.md` and `.github/atomisation-guidelines.md`.

#### Step 3.2: Generate Pages
For each page in the proposed structure:
1. Create `outputs/<slug>/` folder structure
2. Add extracted images to `resources/`
3. Create `content.html` incorporating text and image references
4. Create `metadata.json` with extracted metadata
5. Create `license.md` and `resources/.gitkeep`

#### Step 3.3: Reference Images in Content
In `content.html`, use relative paths:
```html
<img src="resources/<image_filename>" alt="description" width="x" height="y">
```

## Common Issues

- **Black background instead of transparent**: The tool extracted RGB only, missing the soft mask. Re-run with mask combining.
- **Mismatched dimensions**: RGB and mask have different sizes. Check PDF extraction; may need to re-export from source.
- **Grayscale image mistaken for mask**: Verify color type with `file` before discarding.
- **Text is incomplete**: PDF may use embedded fonts or unusual encoding. Try alternative extraction tools or manual review.

## Tools Used
- `pdftotext` (command-line): Extract text from PDF
- `pdfimages` (command-line): List and extract images from PDF
- `view_image` (copilot tool): Inspect extracted PNG visually
- `file` (command-line): Verify PNG format and color type
- `python3` with standard library (struct, zlib): Combine layers if PIL unavailable
- `run_in_terminal` (copilot tool): Execute extraction commands

## Example Workflow
```bash
# Extract text
pdftotext inputs/summary.pdf - | head -100

# List images
pdfimages -list inputs/summary.pdf

# Extract as PNG
pdfimages -png inputs/summary.pdf resources/extracted

# Verify and view
file resources/extracted-*.png
view_image resources/extracted-000.png

# Then follow content-ingester workflow to create pages
```
