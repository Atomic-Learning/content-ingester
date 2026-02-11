This file contains a more detailed specification of the format of content that should be created, including rules on format and style which should be followed when creating the content pages.

## `content.html` file

This file contains the content as it will appear on the page. It should be written in html format. There are several rules which should be followed:

* The page must not contain a `<h1>` tag, as the title of the page will be taken from the `metadata.json` file and inserted as a `<h1>` automatically by the platform. 
* Do not repeat the page title as a heading in the content. 
* The html content should avoid using `style` where possible, as styling with be handled by a global stylesheet on the platform. If styling is needed, try to use semantic html tags where possible (e.g. `<em>` for emphasis, `<strong>` for strong emphasis) rather than using `style` attributes. 
* For images, specify the width and height attributes to help with page layout, but avoid using `style` attributes to set the size of images.
* For non-interactive code blocks, use the `<pre><code>` tags to format the code. If the code is in a specific programming language, include the language as a class on the `<code>` tag (e.g. `<code class="python">` for Python code). This will allow for syntax highlighting on the platform.
* Interactive Python code cells are supported in the platform and should be included inside the `<py-cell>` tag. For example:
```html<py-cell>
print("Hello, world!")
</py-cell>
```
* Interactive R code cells are supported in the platform and should be included inside the `<r-cell>` tag. For example:
```html<r-cell>
print("Hello, world!")
</r-cell>
```

### Guidance for Sample Solutions for Coding Problems

* Aim to break the solution into a sequence of logical steps, each with a short explanatory paragraph (`<p>`) before a code cell.
* Each code cell should focus on a single operation or concept, and the explanation should help the learner understand what to expect or why the step is important.
* Avoid including output comments in code cells—users can run the code to see the output themselves.
* Avoid summary sections at the end; instead, weave key insights into the explanations between code cells.
* This approach helps learners follow the reasoning and see the solution unfold step by step, but you do not need to be overly prescriptive—use your judgment to keep the solution clear and concise.

## `metadata.json` file

This file contains the metadata for the page, including the title, description, and pre-requisites. It should be written in json format. The following fields should be included:

* `title`: The title of the page. This should be a short, descriptive title that accurately reflects the content of the page. Major words will often come first before minor words. For example, a page on the basic of Github might be named "GitHub: Introduction".
* `slug`: A URL-friendly version of the title, typically lowercase with words separated by hyphens. This will be used in the URL for the page. This will typically mirror the title, but with special characters removed and replaced with hyphens. Minor words may be removed. For example, a page with the title "GitHub: Introduction" might have the slug "github-introduction". The slug should be unique across all pages in the platform.
* `description`: A brief description of the content of the page. This should be a concise summary that gives an overview of what the page will cover. It will be displayed in search results on the page, and will also be used in the metadata for the page to help with search engine optimization (SEO), or parsed ny LLMs or other tools to understand the content of the page. Maximum of 500 characters.
* `authors`: A list of the authors of the page. This should include the names of the authors who contributed to the content of the page. **If there are multiple authors, each entry should be on a separate line, as in the template.**
* `tags`: A list of tags that are relevant to the content of the page. Try to use existing tags where possible to avoid creating duplicates, but if new tags are needed, add these to the proposed structure document and highlight them as new tags. Tags will normally be fairly high-level concepts that readers can use to filter pages across the whole body of content. **If there are multiple tags, each entry should be on a separate line, as in the template.**
* `duration`: An estimate of how long it will take to go through the content on the page. For pages which are simple descriptions, this can be estimated from the number of words. For pages that contain complex information that needs to be thought about, it may a little longer. For pages that contain exercises, an estimate based on the time to complete the exercise should be included. This should be given in minutes, and should be a single number (e.g. 10, not 5-15).
* `prerequisites`: A list of the slugs of any pages that are pre-requisites for this page. These should be the slugs of other pages that a learner should have completed before going through the content on this page. **If there are multiple prerequisites, each entry should be on a separate line, as in the template.**
* `related`: A list of the slugs of any pages that are related to this page. These should be the slugs of other pages that a user might want to look at next. For example, a page about the concepts of functions in programming in general might have related pages about the syntax of functions in specific programming languages, or about more complex aspects of functions such as parameters and return values. **If there are multiple related pages, each entry should be on a separate line, as in the template.**

## `resources` directory

This directory should contain any resources (e.g. images, data files) that are needed for the page. These should be referenced in the `content.html` file using relative paths. For example, if there is an image named `example.png` in the `resources` directory, it should be referenced in the `content.html` file as `<img src="resources/example.png">`.