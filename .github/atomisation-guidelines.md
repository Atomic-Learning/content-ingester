# Introduction

This file describes the atomisation strategy for the content in the Atomic Learning platform.

## Guiding Goals

The atomisation strategy is guided by the following goals:
1. **Reusability**: Content should be broken down into smaller, reusable components that can be easily combined to create new learning paths. Smaller, more focused pages are more reusable than larger pages covering multiple concepts.
2. **Uniqueness**: Content should be unique and not duplicated across different components. When similar content might appear in multiple pages, language-agnostic foundation pages should be created to prevent duplication.
3. **Necessity**: A learning path should only include components that are necessary for achieving the learning objectives. This means each content page should contain only one learning objective and should not include any content that is not directly related to that objective. If a page contains multiple related objectives (e.g., "append AND insert in relation to lists in programming"), consider splitting them.

## Key Principles

### Explicit vs. Implicit Prerequisites

When creating pages, distinguish between:
* **Explicit prerequisites** (to be listed in metadata): Concepts that learners absolutely must have learned first for this page to make sense.
* **Prerequisite discoveries**: During content creation, you may realize a page references concepts that aren't yet in the platform. Consider whether these should be created as new prerequisite pages. Ask yourself: "Would a learner unfamiliar with this concept be unable to understand the main learning objective of this page if they skipped the new prerequisite?"

## Atomisation Strategy

To achieve these goals, the following atomisation strategy is recommended:

### Foundation Pages First
* **For programming content**: Create language-agnostic foundation pages before language-specific implementations. For example, a page on "Programming: For Loops" (language-agnostic) should precede "Python: For Loops" and "JavaScript: For Loops". This allows the foundation page to be reused across languages and prevents duplicating conceptual material.
  - This applies not only to control structures but also to **concepts about functions** (e.g., "Programming: Calling Functions" before "Python: Calling Functions", "Programming: Defining Functions" before "Python: Defining Functions") to separate conceptual understanding from language-specific syntax.
  - This also applies to **operations and methods** where the underlying operation is language-agnostic even if syntax varies, to avoid duplicating similar explanations across multiple language-specific pages.
* **For mathematical or scientific content**: Create conceptual/mathematical foundation pages before implementation pages. For example, "Mathematics: Complex Numbers" should precede "Python: Complex Numbers" to separate the mathematical concept from its language-specific representation.
* **Determine the appropriate level**: Ask which learners' needs you're addressing:
  - If learners from multiple languages/contexts need the concept, create a language-agnostic foundation.
  - If the concept only appears in one specific context, create that context-specific page directly.
* **Discovering missing prerequisites**: During content creation, you may realize that content refers to prerequisites that don't yet exist in the platform. This is expected and normal. When this happens, consider creating the missing prerequisite page. The prerequisite may be a language-agnostic foundation, a more basic explanation, or a foundational concept that the new content depends on. If you do this, inform the user.

### Single Learning Objective per Page
* Each content page should be focused on a single learning objective. This means that the content should be structured in such a way that it is clear what the learning objective is and that all content on the page is directly related to that objective. If there are multiple learning objectives, they should be broken down into separate pages.
* Content will often follow an escalating structure, starting with a high-level overview and then breaking down into more detailed components. For example, a series of pages relating to the neutron diffusion equation might start with qualitative description of the equation (requiring only minimal physics as prerequisites). The next page might introduce the mathematical form of the equation and the meaning of each term (requiring some mathematical prerequisites and more complex physics prerequisites). A further page might introduce the derivation of the equation (requiring more complex mathematical and physics prerequisites). This structure allows a learner who only needs a qualitative understanding to get it without having to navigate through more complex content.

### Granularity: When to Split vs. Combine
* **Default to splitting**: When in doubt, create separate pages rather than combining content. It is easier for users to access multiple related pages than to navigate past irrelevant content within a single page. This is especially true for:
  - **Methods/Functions**: Each distinct method or function (e.g., `append`, `insert`, `pop`) should generally have its own page focused on its specific purpose and usage. Avoid combining multiple methods unless they are truly complementary operations with a shared conceptual foundation.
  - **Related operations**: Variations of a concept (e.g., "String Concatenation", "String Multiplication", "String Length") should be on separate pages with distinct learning objectives, not grouped on a single page.
  - **Different aspects of a concept**: If a concept has multiple facets (e.g., defining functions vs. calling functions, shallow copy vs. deep copy), each should have its own page with clear naming to distinguish them.
* **Combine only when truly inseparable**: Two concepts should be on the same page only if understanding one is impossible without simultaneously understanding the other. For example, basic arithmetic operations (add, subtract, multiply, divide) might reasonably be on a single page when teaching a single foundational concept, but operations like string concatenation and string multiplication should each have distinct pages with their own learning objectives.

### Prerequisites vs Related Content
* **Prerequisite**: Content that a learner *cannot understand the main learning objective of this page without first learning*. Prerequisites are barriers—learners must satisfy them before the page makes sense.
* **Related Content**: Content that provides context, extension, or additional examples that *enhance understanding but are not strictly necessary*. Examples: a page introducing matplotlib might link to a page about open-source software, or a page on lists might link to exercises demonstrating list operations. Learners can understand the main concept without related content. When Page A has Page B as a prerequisite, consider whether Page B should note Page A as a piece of related content to help learners discover it.
* **When in doubt, use Related Content**: If a learner can grasp the main learning objective without knowing something, it should be related content. This prevents unnecessary prerequisites from blocking access.

### Naming and Tagging Conventions
* **Language-agnostic pages**: Use the `programming` tag (e.g., "Programming: For Loops", "Programming: Calling Functions", `programming` tag). These pages may use pseudocode and should have the "pseudocode" tag if they do.
* **Language-specific pages**: Use the language name tag only (e.g., "Python: For Loops" gets tag `python`, not `programming`). Language-specific pages should have the corresponding language-agnostic foundation as a prerequisite when one exists.
* **Mathematical/conceptual foundation pages**: Use domain-specific tags (e.g., `maths`, `physics`). These precede domain-specific implementation pages.
* **Related pages with consistent patterns**: When creating multiple pages that cover variations of a concept (e.g., string operations, list methods), use a consistent naming pattern in the slug to make relationships clear. For example:
  - `python-strings-concatenation`, `python-strings-multiplication`, `python-strings-length` all follow the pattern `python-strings-<operation>`
  - Choose a consistent pattern and apply it throughout a content area to help users recognize related pages.
* **Exercise and Sample Solution naming**:
  - Exercises should have the prefix "Exercise: " in the title and be language/context-specific when appropriate (e.g., "Exercise: Python List Operations").
  - Use consistent slug naming: `exercise-<language>-<topic>` and `sample-solution-<language>-<topic>` for language-specific exercises.
  - Sample solutions should have the prefix "Sample Solution: " and list the related exercise as a prerequisite.
  - When possible, extract concrete exercises directly from the source material rather than creating generic placeholders.
  - If an exercise relates to a particular piece of content, it should be noted as a related piece of content on that page. The sample solution need not be noted as related content on the main content page, but should have the main content page as a prerequisite.

### Examples and Example Pages
* Some pages will be examples that demonstrate an application of a concept. If these contain specific content fabricated for the example (e.g. showing how to solve a particular abstract ODE), then the page title should begin with the prefix "Example: ". Generally, other pages will not use Examples as a prerequisite.
* If an example might be used as a prerequisite for another topic, it should not have the prefix "Example: " in the title, and other pages may use it as a prerequisite. For example, if the series of ODEs being solved are the Lorenz Equations, then the page might be titled "The Lorenz Equations" and other pages might use it as a prerequisite. This allows the content to be more easily reused in different contexts.
* Some pages will require a basic example to demonstrate a point or concept. These should generally be simple, abstract and discipline-agnostic, such as a simple ODE or a simple example of a particular programming concept. More complex examples that are specific to a particular discipline or context should generally be reserved for example pages, which can be linked to as "Related Content" from the main content page. This allows the main content page to remain focused on the learning objective.
