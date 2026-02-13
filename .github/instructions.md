# Introduction
This workspace is designed to support the creation of content for an online learning platform named Atomic Learning. The platform organises its content into a large number of small "atomic" pages which each teach "one thing". This means the smallest meaningful and complete concept. for instance, when teaching functions for a programming language, there might be a page introducing the functions on a conceptual level, then one introducing the basic syntax for a programming language, then another for each more complex aspect of functions (e.g. parameters, return values, variable scope, etc.). 

This workspace is designed to support the creation of these pages from pre-existing content. The goal is to break down the content into small, digestible pieces that can be easily consumed by learners. The pages are related to each other through noting which are pre-requisites for which other pages.

Your goal is to work with the user to process content from the `inputs` directory and create the corresponding "atomic" pages in the `outputs` directory. This will follow a number of steps, which you should guide the user through. At any step, if something is unclear, ask the user. The steps are as follows:

## 1. Understand existing content and user preferences.
In the `inputs` directory there will be a file named `current_content.md` or some variant on that name. This file contains a list of the content that currently exists in the platform, along with a description, and the pre-requisites for each piece of content. You should read through this file and understand the content that currently exists. The file `tags_current.md` (or similarly named filed) describes the names of tags which currently exist in the platform, which you should also read through and understand.

## 2. Identify new content and propose structure.
Other files in the `inputs` directory will contain content that is not yet in the platform. This could be in a number of formats:
* Markdown file: You can read this with no special steps.
* Jupyter notebook: You can read this with no special steps.
If an unsupported file format is present, ask the user.

You should read through this content and propose a structure for how it could be broken down into atomic pages. Detailed guidelines are presented in the file `.github/atomisation-guidelines.md`. You should write this structure into a file named `proposed_structure.md` in the `outputs` directory. This structure should include the title of each proposed page, a description of what it will cover, the pre-requisites for each page, the related content for each page, and proposed tags for each page. Highlight any new tags to add to the platform in a separate section.

In some cases, there may be content which might be expected to be in the platform as a pre-requisite of the new content, but which is not yet in the platform. In this case, you should also propose the creation of this pre-requisite content and include it in a separate section of the `proposed_structure.md` file.

If content in the content being converted overlaps existing content, the existing content should not be updated - it can left as-is. Summarise sections of the provided files which will not be included in the new pages in the `proposed_structure.md` file, and explain why they will not be included.

Circular dependencies should be avoided in your proposed structure.

For large collections of input file, the process may produce dozens of new pages.

### Proposed Structure Checkpoints
Before finalizing the proposed structure, verify:
* **Language-agnostic foundations**: If the content includes programming language features, have you created language-agnostic foundation pages before language-specific implementation pages (based on the user's stated preference from Step 1)?
* **Mathematical/conceptual foundations**: If the content involves mathematical or scientific concepts with implementation pages, are conceptual foundations separated from implementation (e.g., "Mathematics: Complex Numbers" before "Python: Complex Numbers")?
* **Single learning objectives**: Does each page have one clear, focused learning objective? If any page contains "and also...", consider splitting it.
* **Concrete exercises**: For exercises referenced in the source material, have you proposed concrete exercises extracted from that material (with descriptions of what learners will actually do) rather than generic placeholder exercises?
* **Exercise naming conventions**: Are exercises slugged as `exercise-<language>-<topic>` and sample solutions as `sample-solution-<language>-<topic>`?
* **Tags**: Are language-agnostic pages tagged `programming`, language-specific pages tagged with the language name only, and conceptual foundations tagged appropriately (e.g., `maths`)?

## 3. Iterate with the user to refine the proposed structure.
You should share the `proposed_structure.md` file with the user and discuss it with them. They may have suggestions for how to improve the structure, or they may want to change the proposed pre-requisites. You should work with them to refine the structure until you are both happy with it. The user may prompt you to make changes or edit the file directly. 

Before concluding this step, remind the user of the key atomisation principles (language-agnostic foundations, single learning objectives, concrete exercises, tagging conventions) to check whether they want any final refinements. 

## 4. Create the content pages.
Once the structure is agreed, re-check `proposed_structure.md` as the user may have edited it directly. Use this opportunity to verify that the structure aligns with the key atomisation principles: language-agnostic foundations precede language-specific implementations (if applicable), pages have single learning objectives, exercises are concrete and extracted from source material, and tagging conventions are followed. If there are pages which you have proposed as pre-requisites but which are not yet in the platform, you should also ask if the user would like to create these themselves or if they would like you to create them. You should also ask the user who should be credited as the author for the pages as it appears in the metadata for the page. The user will judge who should be the author.

The format of the files is specified in the GitHub repo https://github.com/Atomic-Learning/content-template . You can download this to the `/templates` directory in this repo and use it as a reference for how to create the content pages using tools/github_downloader.py to download the template repo and copy the relevant files. This should be done once before creating the first page's content. At a basic level, `content.html` contains the content of the page, `metadata.json` contains the metadata for the page (including the title, description, and pre-requisites). The resources directory is where any resources (e.g. images, data files) for the page should be stored. Further instructions on the format of the content can be found in `.github/content_file_details.md`. You should follow these instructions when creating the content pages.

You should create the content pages according to the agreed structure and fill in the content and metadata for each page. Each new page should go in its own directory in the `outputs` directory, titled by its slug. Where possible, you should try to reuse text and examples from the `inputs` directory, but you may need to rewrite it to fit the format of the atomic pages. You should also make sure to include any resources that are needed for the page.

## Iterate the new content pages with the user.
Report to the user when the pages have been created. Highlight any area where you've added substantial new content or made significant changes to the original content. Ask the user to review the new pages and provide feedback. You should be prepared to make changes to the pages based on the user's feedback, and you should work with them to refine the pages until they are happy with them.