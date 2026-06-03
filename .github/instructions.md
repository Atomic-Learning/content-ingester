# Introduction

This workspace is designed to support the creation of content for an online learning platform named Atomic Learning. The platform organises its content into a large number of small "atomic" pages which each teach "one thing". This means the smallest meaningful and complete concept. for instance, when teaching functions for a programming language, there might be a page introducing the functions on a conceptual level, then one introducing the basic syntax for a programming language, then another for each more complex aspect of functions (e.g. parameters, return values, variable scope, etc.). 

This workspace is designed to support the creation of these pages from pre-existing content. The goal is to break down the content into small, digestible pieces that can be easily consumed by learners. The pages are related to each other through noting which are pre-requisites for which other pages.

If the user asks to "run validation tests" (or equivalent regression validation wording), follow `.github/validation-workflow.instructions.md`.

## Directory Scope Rule

Ignore anything in the `workflow-validation/` directory by default. Do not use files from `workflow-validation/` as source inputs, references, or validation targets unless the user explicitly asks you to work with that directory.

Your goal is to work with the user to process content from the `inputs` directory and create the corresponding "atomic" pages in the `outputs` directory. This will follow a number of steps, which you should guide the user through. At any step, if something is unclear, ask the user. The steps are as follows:

## 0. Set up the Python environment.

There may already be a Python virtual environment set up for this workspace (likely in `.venv` or `venv`). If this environment exists, verify it has the packages specified in `requirements.txt` installed. 

If it exists but lacks required packages, install them.

If no virtual environment exists in the workspace, create one:

```bash
python -m venv venv
```

Activate the virtual environment:

* On Windows: `.\venv\Scripts\activate`
* On macOS/Linux: `source venv/bin/activate`

Install the required dependencies:

```bash
pip install -r requirements.txt
```

You should keep the virtual environment activated throughout your work session, as it will be needed for tools like `github_downloader.py` and `github_uploader.py`.

## 1. Understand existing content.

In the `inputs` directory there will be a file named `current_content.md` or some variant on that name. This file contains a list of the content that currently exists in the platform, along with a description, and the pre-requisites for each piece of content. You should read through this file and understand the content that currently exists. Some pieces of content may have Related Content slugs which do not correspond to existing content slugs - these are placeholders that indicate content that is expected to be added at some point in the future (possibly but no necessarily while this tool is running). The file `tags_current.md` (or similarly named filed) describes the names of tags which currently exist in the platform, which you should also read through and understand.

## 2. Identify new content and propose structure.

Other files in the `inputs` directory will contain content that is not yet in the platform. This could be in a number of formats:

* Markdown file: You can read this with no special steps.
* Jupyter notebook: You can read this with no special steps.
If an unsupported file format is present, ask the user.

You should read through this content and propose a structure for how it could be broken down into atomic pages. Detailed guidelines are presented in the file `.github/atomisation-guidelines.md`. The required Step 2 output format is defined in `.github/proposed-structure-format.md`.

You should write this structure into a file named `proposed_structure.json` in the `outputs` directory. This JSON file is the canonical Step 2 output and should contain the full proposal details, including inputs reviewed, user preferences applied, proposed pages, omitted source sections, tag review, and checkpoint review.

Highlight any new tags to add to the platform in a separate section.

In some cases, there may be content which might be expected to be in the platform as a pre-requisite of the new content, but which is not yet in the platform. In this case, you should also propose the creation of this pre-requisite content and include it in the `pages` list of `proposed_structure.json`, with `status` set to `"missing"`. Pages derived directly from the provided source content should use `status` `"new"`.

If content in the content being converted overlaps existing content, the existing content should not be updated - it can left as-is. Summarise sections of the provided files which will not be included in the new pages in `proposed_structure.json`, and explain why they will not be included.

Circular dependencies should be avoided in your proposed structure.

For large collections of input file, the process may produce dozens of new pages.

After producing `proposed_structure.json`, generate the Step 2 dependency graph using:

```bash
python tools/generate_prerequisite_graph.py --source proposed_structure
```

Point out the existence of `proposed_structure.json` and the generated dependency graph to the user for their review.

### Proposed Structure Checkpoints

Before finalizing the proposed structure, verify:

* **Language-agnostic foundations**: If the content includes programming language features, have you created language-agnostic foundation pages before language-specific implementation pages (based on the user's stated preference from Step 1)?
* **Mathematical/conceptual foundations**: If the content involves mathematical or scientific concepts with implementation pages, are conceptual foundations separated from implementation (e.g., "Mathematics: Complex Numbers" before "Python: Complex Numbers")?
* **Single learning objectives**: Does each page have one clear, focused learning objective? If any page contains "and also...", consider splitting it.
* **Concrete exercises**: For exercises referenced in the source material, have you proposed concrete exercises extracted from that material (with descriptions of what learners will actually do) rather than generic placeholder exercises?
* **Exercise naming conventions**: Are exercises slugged as `exercise-<language>-<topic>` and sample solutions as `sample-solution-<language>-<topic>`?
* **Tags**: Are language-agnostic pages tagged `programming`, language-specific pages tagged with the language name only, and conceptual foundations tagged appropriately (e.g., `maths`)?

## 3. Iterate with the user to refine the proposed structure.

You should share the `proposed_structure.json` file with the user and discuss it with them. They may have suggestions for how to improve the structure, or they may want to change the proposed pre-requisites. You should work with them to refine the structure until you are both happy with it. The user may prompt you to make changes or they may edit the file directly. If you add new pages, consider if these should be prerequisites for any proposed pages, and if so, update the structure accordingly. Regenerate the dependency graph after any changes to the structure and share this with the user to help them understand the structure and identify any issues.

Before concluding this step, remind the user of the key atomisation principles (language-agnostic foundations, single learning objectives, concrete exercises, tagging conventions) to check whether they want any final refinements. You should also check that the proposed structure does not contain any circular dependencies.

## 4. Create and review content pages one at a time.

Once the structure is agreed, re-check `proposed_structure.json` as the user may have edited it directly. Use this opportunity to verify that the structure aligns with the key atomisation principles: language-agnostic foundations precede language-specific implementations (if applicable), pages have single learning objectives, exercises are concrete and extracted from source material, and tagging conventions are followed. If there are pages with `status` `"missing"` (proposed as prerequisites that are not yet in the platform), you should also ask if the user would like to create these themselves or if they would like you to create them. You should also ask the user who should be credited as the author for the pages as it appears in the metadata for the page. The user will judge who should be the author.

The format of the files is specified in the GitHub repo https://github.com/Atomic-Learning/content-template . You can download this to the `/templates` directory in this repo and use it as a reference for how to create the content pages using tools/github_downloader.py to download the template repo and copy the relevant files. This should be done once before creating the first page's content. At a basic level, `content.html` contains the content of the page, `metadata.json` contains the metadata for the page (including the title, description, and pre-requisites). The resources directory is where any resources (e.g. images, data files) for the page should be stored. Further instructions on the format of the content can be found in `.github/content_file_details.md`. You should follow these instructions when creating the content pages.

**Required files for each page:**

* `metadata.json` - Page metadata
* `content.html` - Page content
* `license.md` - License file (copy from `templates/license.md`)
* `resources/` directory (can be empty or contain images/data files)
* `resources/.gitkeep` - Empty placeholder file (copy from `templates/resources/.gitkeep`)

**Dependency ordering:** Pages must be created in dependency order — prerequisites before the pages that depend on them. To determine which page to work on next, inspect `proposed_structure.json` and check which pages in the `pages` list do not yet have a corresponding folder in `outputs/`. Among those remaining, choose the one whose prerequisites are all already present either in `outputs/` or in `current_content.md`. Announce to the user which page you are working on next and why (i.e. its prerequisites are satisfied).

Create one page at a time. For each page:

1. Create the page folder `outputs/<slug>/` and all required files.
2. Fill in the content and metadata, reusing source material from `inputs/` where possible.
3. Highlight to the user any areas where you have added substantial new content or made significant changes to the original material.
4. Ask the user to review the page and provide feedback. Work with the user to refine the page until they are satisfied. When creating or editing content, periodically review `content_file_details.md` to ensure you are following the formatting guidelines.
5. Once the user approves the page, confirm it is complete and ask whether to proceed to the next page or stop for now.

If the user decides a page does not make sense, they may ask you to delete it. Remove the page folder and mark it as omitted in `proposed_structure.json`. If new pages are needed, add them to `proposed_structure.json` and regenerate the dependency graph before continuing. The user may return to Step 3 to revise the overall structure at any point.

Continue until all pages in `proposed_structure.json` with `status` `"new"` or `"missing"` have been created and approved, or the user decides to stop.

## Step 5. Check for consistency

In the above process, many pages may have been added, removed, renamed, edited, etc. You should check each metadata file to ensure that the pre-requisites and related content are consistent with the new structure and page names. Recall page names may be pages created in this workflow, or pages that already existed in the platform, specified in `current_content.md`. Also check that the slug in each metadata file matches the directory name of the page. You should also check that any new tags proposed are consistent across pages and with the existing tags in `tags_current.md`. Generate a dependency graph using `tools/generate_prerequisite_graph.py` and share this with the user to help identify any inconsistencies or circular dependencies. You should work with the user to resolve any issues that are identified. Also check each page has a license file and that the license file is consistent with that in the `sample_content_structure` directory. Also check that each page has a `resources/.gitkeep` file. You should work with the user to resolve any inconsistencies that you find.

## Step 6. Recommend related content for existing pages.

Finally, you should check the existing pages in `current_content.md` to see if any of the newly created pages should be added as related content to any of the existing pages. You should create a file named `related_content_recommendations.md` in the `outputs` directory where you list any recommendations for related content to be added to existing pages. You should share this file with the user and work with them to refine it until they are happy with it. The user may then choose to update the existing pages in the platform to include the new related content.

## Step 7. Upload pages to GitHub repositories and sync to the site, one at a time.

Pages are published in the same dependency order used during content creation. Upload each page individually, then ask the user to coordinate manual registration/sync with the Atomic Learning admin team before moving on to the next.

To upload a page, use the `tools/github_uploader.py` script. This script:

* Creates a new repository in the specified GitHub organization if one does not already exist (named using the page slug, e.g., `python-methods`)
* Initialises the page directory as its own git repository and pushes content to the remote
* Leaves the `.git` directory in place, making the page directory immediately usable as a local repository

Before uploading, ensure:

* Your GitHub Personal Access Token (PAT) is stored in a `.env` file in the project root: `GITHUB_PAT=your_token_here`
* Your PAT has permissions to create repositories in the target organization
* The organisation name is correct (e.g., `Atomic-Learning`)
* Your Python virtual environment is activated (created in Step 0)

If the user does not have permission to create repositories in the organisation, they should ask the admin team (contact: Chris Cooling, `c.cooling10@imperial.ac.uk`) to perform the upload or create the repository and grant access.

**Per-page upload workflow:**

For each page (in dependency order):

1. Do a dry run for the single page to confirm what will be uploaded:
```bash
python tools/github_uploader.py Atomic-Learning -d outputs/<slug> --dry-run
```
2. If the dry run looks correct, perform the upload:
```bash
python tools/github_uploader.py Atomic-Learning -d outputs/<slug> --force
```
3. Update `outputs/upload_summary.txt` to reflect the current state of all uploads so far. The file should list every page that has been attempted, grouped as: created, skipped, and failed. Replace the file contents each time so it always reflects the full up-to-date picture.
4. Ask the user to register the new repository name with the Atomic Learning site and trigger a content sync manually. Inform them they will need site admin permissions, or they will need to contact Chris Cooling at `c.cooling10@imperial.ac.uk`.
5. Share the live URL of the new page with the user for review.
6. Work with the user to fix any issues that appear on the live site (content rendering, broken links, missing resources, etc.).
7. Once the user approves the page on the site, confirm it is complete and proceed to the next page.

If a repository already exists with the same name, the script will skip it and report it as skipped. To re-upload to an existing repository, you would need to manually handle that or remove the repository from the organisation first.

If GitHub upload steps fail for permission or organisation-policy reasons, tell the user to contact Chris Cooling at `c.cooling10@imperial.ac.uk`.

After all pages have been uploaded, do a final update of `outputs/upload_summary.txt` with the complete results.