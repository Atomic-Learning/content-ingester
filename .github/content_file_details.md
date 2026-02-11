This file contains a more detailed specification of the format of content that should be created, including rules on format and style which should be followed when creating the content pages.

## `content.html` file

This file contains the content as it will appear on the page. It should be written in html format. There are several rules which should be followed:

* The page should not contain a `<h1>` tag, as the title of the page will be taken from the `metadata.json` file. Instead, the highest level heading should be `<h2>`.
* The html content should avoid using `style` where possible, as styling with be handled by a global stylesheet on the platform. If styling is needed, try to use semantic html tags where possible (e.g. `<em>` for emphasis, `<strong>` for strong emphasis) rather than using `style` attributes. 
* For images, specify the width and height attributes to help with page layout, but avoid using `style` attributes to set the size of images.

## `metadata.json` file

This file contains the metadata for the page, including the title, description, and pre-requisites. It should be written in json format. The following fields should be included:

* `title`: The title of the page. This should be a short, descriptive title that accurately reflects the content of the page. Major words will often come first before minor words. For example, a page on the basic of Github might be named "GitHub: Introduction".
* `slug`: A URL-friendly version of the title, typically lowercase with words separated by hyphens. This will be used in the URL for the page. This will typically mirror the title, but with special characters removed and replaced with hyphens. Minor words may be removed. For example, a page with the title "GitHub: Introduction" might have the slug "github-introduction". The slug should be unique across all pages in the platform.
* `description`: A brief description of the content of the page. This should be a concise summary that gives an overview of what the page will cover. It will be displayed in search results on the page, and will also be used in the metadata for the page to help with search engine optimization (SEO), or parsed ny LLMs or other tools to understand the content of the page. Maximum of 500 characters.
* `authors`: A list of the authors of the page. This should include the names of the authors who contributed to the content of the page.
* `tags`: A list of tags that are relevant to the content of the page. Try to use existing tags where possible to avoid creating duplicates, but if new tags are needed, add these to the proposed structure document and highlight them as new tags. Tags will normally be fairly high-level concepts that readers can use to filter pages across the whole body of content.
* `duration`: An estimate of how long it will take to go through the content on the page. For pages which are simple descriptions, this can be estimated from the number of words. For pages that contain complex information that needs to be thought about, it may a little longer. For pages that contain exercises, an estimate based on the time to complete the exercise should be included. This should be given in minutes, and should be a single number (e.g. 10, not 5-15).
* `prerequisites`: A list of the slugs of any pages that are pre-requisites for this page. These should be the slugs of other pages that a learner should have completed before going through the content on this page.
* `related`: A list of the slugs of any pages that are related to this page. These should be the slugs of other pages that a user might want to look at next. For example, a page about the concepts of functions in programming in general might have related pages about the syntax of functions in specific programming languages, or about more complex aspects of functions such as parameters and return values.

## `resources` directory

This directory should contain any resources (e.g. images, data files) that are needed for the page. These should be referenced in the `content.html` file using relative paths. For example, if there is an image named `example.png` in the `resources` directory, it should be referenced in the `content.html` file as `<img src="resources/example.png">`.