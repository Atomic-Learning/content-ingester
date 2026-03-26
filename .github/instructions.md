# Introduction
This workspace is designed to support the creation of content for an online learning platform named Atomic Learning. The platform organises its content into a large number of small "atomic" pages which each teach "one thing". This means the smallest meaningful and complete concept. for instance, when teaching functions for a programming language, there might be a page introducing the functions on a conceptual level, then one introducing the basic syntax for a programming language, then another for each more complex aspect of functions (e.g. parameters, return values, variable scope, etc.). 

This workspace is designed to support the creation of these pages from pre-existing content. The goal is to break down the content into small, digestible pieces that can be easily consumed by learners. The pages are related to each other through noting which are pre-requisites for which other pages.

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

You should write this structure into a file named `proposed_structure.json` in the `outputs` directory. This JSON file is the canonical Step 2 output and should contain the full proposal details, including inputs reviewed, user preferences applied, proposed pages, proposed missing prerequisites, omitted source sections, tag review, and checkpoint review.

Highlight any new tags to add to the platform in a separate section.

In some cases, there may be content which might be expected to be in the platform as a pre-requisite of the new content, but which is not yet in the platform. In this case, you should also propose the creation of this pre-requisite content and include it in the `proposed_missing_prerequisites` section of `proposed_structure.json`.

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
You should share the `proposed_structure.json` file with the user and discuss it with them. They may have suggestions for how to improve the structure, or they may want to change the proposed pre-requisites. You should work with them to refine the structure until you are both happy with it. The user may prompt you to make changes or edit the file directly. 

Before concluding this step, remind the user of the key atomisation principles (language-agnostic foundations, single learning objectives, concrete exercises, tagging conventions) to check whether they want any final refinements. 

## 4. Create the content pages.
Once the structure is agreed, re-check `proposed_structure.json` as the user may have edited it directly. Use this opportunity to verify that the structure aligns with the key atomisation principles: language-agnostic foundations precede language-specific implementations (if applicable), pages have single learning objectives, exercises are concrete and extracted from source material, and tagging conventions are followed. If there are pages which you have proposed as pre-requisites but which are not yet in the platform, you should also ask if the user would like to create these themselves or if they would like you to create them. You should also ask the user who should be credited as the author for the pages as it appears in the metadata for the page. The user will judge who should be the author.

The format of the files is specified in the GitHub repo https://github.com/Atomic-Learning/content-template . You can download this to the `/templates` directory in this repo and use it as a reference for how to create the content pages using tools/github_downloader.py to download the template repo and copy the relevant files. This should be done once before creating the first page's content. At a basic level, `content.html` contains the content of the page, `metadata.json` contains the metadata for the page (including the title, description, and pre-requisites). The resources directory is where any resources (e.g. images, data files) for the page should be stored. Further instructions on the format of the content can be found in `.github/content_file_details.md`. You should follow these instructions when creating the content pages.

**Required files for each page:**
* `metadata.json` - Page metadata
* `content.html` - Page content
* `license.md` - License file (copy from `templates/license.md`)
* `resources/` directory (can be empty or contain images/data files)
* `resources/placeholder.txt` - Empty placeholder file (copy from `templates/resources/placeholder.txt`)

You should create the content pages according to the agreed structure and fill in the content and metadata for each page. Each new page should go in its own directory in the `outputs` directory, titled by its slug. Where possible, you should try to reuse text and examples from the `inputs` directory, but you may need to rewrite it to fit the format of the atomic pages. You should also make sure to include any resources that are needed for the page, along with the required `license.md` and `resources/placeholder.txt` files mentioned above.

## Iterate the new content pages with the user.
Report to the user when the pages have been created. Highlight any area where you've added substantial new content or made significant changes to the original content. Ask the user to review the new pages and provide feedback. You should be prepared to make changes to the pages based on the user's feedback, and you should work with them to refine the pages until they are happy with them. When creating new content, periodically review `content_file_details.md` to ensure you are following the guidelines for how to format the content in the revised pages.

## Step 5. Check for consistency

In the above process, many pages may have been added, removed, renamed, edited, etc. You should check each metadata file to ensure that the pre-requisites and related content are consistent with the new structure and page names. Recall page names may be pages created in this workflow, or pages that already existed in the platform, specified in `current_content.md`. Also check that the slug in each metadata file matches the directory name of the page. You should also check that any new tags proposed are consistent across pages and with the existing tags in `tags_current.md`. Generate a dependency graph using `tools/generate_prerequisite_graph.py` and share this with the user to help identify any inconsistencies or circular dependencies. You should work with the user to resolve any issues that are identified. Also check each page has a license file and that the license file is consistent with that in the `sample_content_structure` directory. Also check that each page has a `resources/placeholder.txt` file. You should work with the user to resolve any inconsistencies that you find.

## 6. Recommend related content for existing pages.
Finally, you should check the existing pages in `current_content.md` to see if any of the newly created pages should be added as related content to any of the existing pages. You should create a file named `related_content_recommendations.md` in the `outputs` directory where you list any recommendations for related content to be added to existing pages. You should share this file with the user and work with them to refine it until they are happy with it. The user may then choose to update the existing pages in the platform to include the new related content.

## 7. Upload pages to GitHub repositories.
Once the content pages have been created and reviewed, they should be uploaded to individual repositories in the Atomic Learning GitHub organization. Each page will have its own repository with the page content, metadata, and resources.

To upload the pages, use the `tools/github_uploader.py` script. This script:
* Discovers all pages in the `outputs` directory (identified by the presence of a `metadata.json` file)
* Creates new repositories in the specified GitHub organization if they don't already exist (named using the page slug, e.g., `python-methods`)
* Initializes each page directory as its own git repository and pushes content to the remote
* Leaves the `.git` directory in place in each page directory, making them immediately usable as local repositories

Before uploading, ensure:
* Your GitHub Personal Access Token (PAT) is stored in a `.env` file in the project root: `GITHUB_PAT=your_token_here`
* Your PAT has permissions to create repositories in the target organization
* The organization name is correct (e.g., `Atomic-Learning`)
* Your Python virtual environment is activated (created in Step 0)

**Usage:**

First, do a dry run to see what would be uploaded without making any changes:
```bash
python tools/github_uploader.py Atomic-Learning --dry-run
```

If there are significant problems, pause and report these to the user to fix before proceeding. Once you're ready, you can perform the actual upload with the `--force` flag:

```bash
python tools/github_uploader.py Atomic-Learning --force
```

You can also specify a different output directory if needed:
```bash
python tools/github_uploader.py Atomic-Learning -d path/to/outputs --force
```

**What the script does:**
* Creates a repository for each page using the page slug as the repository name (e.g., `python-methods`)
* Initializes a git repository in each page directory (outputs/page_slug/.git)
* Stages all page content and pushes it to the remote repository
* Uses the `main` branch for new repositories and pushes content to `main`
* Reports on successfully created repositories, skipped repositories (already exist), and any errors
* Generates `upload_summary.txt` in the outputs directory with a summary of the upload results
* Leaves the page directories with their own `.git` folder, ready to be used as local repositories immediately

If a repository already exists with the same name, the script will skip it and report it as skipped. To re-upload to an existing repository, you would need to manually handle that or remove the repository from the organization first.

**Post-Upload: Set Up Local Git Repositories**

After uploading, you should set up local git repositories in each page directory. This allows you to iterate on pages locally and push changes back to GitHub. Use the `tools/github_setup_local_repos.py` script:

First, do a dry run to preview:
```bash
python tools/github_setup_local_repos.py Atomic-Learning --dry-run
```

Then set up the local repositories:
```bash
python tools/github_setup_local_repos.py Atomic-Learning --force
```

This script will:
* Discover all pages in the `outputs` directory
* Initialize a local git repository in each page directory (if not already present)
* Configure the GitHub repository as the `origin` remote
* Fetch the latest content from GitHub
* Check out the master branch

After this step, each page directory will be a fully functional git repository with the GitHub repository configured as the origin remote. You can now make local edits, commit changes, and push them back to GitHub using standard git commands.