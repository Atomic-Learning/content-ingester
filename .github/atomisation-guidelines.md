# Introduction

This file describes the atomisation strategy for the content in the Atomic Learning platform.

## Guiding Goals

The atomisation strategy is guided by the following goals:
1. **Reusability**: Content should be broken down into smaller, reusable components that can be easily combined to create new learning paths.
2. **Uniqueness**: Content should be unique and not duplicated across different components.
3. **Necessity**: A learning path should only include components that are necessary for achieving the learning objectives. This means each content page should contain only one learning objective and should not include any content that is not directly related to that objective.

## Atomisation Strategy

To achieve these goals, the following atomisation strategy is recommended:

### Foundation Pages First
* **For programming content**: Create language-agnostic foundation pages before language-specific implementations. For example, a page on "Programming: For Loops" (language-agnostic) should precede "Python: For Loops" and "JavaScript: For Loops". This allows the foundation page to be reused across languages and prevents duplicating conceptual material.
* **For mathematical or scientific content**: Create conceptual/mathematical foundation pages before implementation pages. For example, "Mathematics: Complex Numbers" should precede "Python: Complex Numbers" to separate the mathematical concept from its language-specific representation.
* **Determine the appropriate level**: Ask which learners' needs you're addressing:
  - If learners from multiple languages/contexts need the concept, create a language-agnostic foundation.
  - If the concept only appears in one specific context, create that context-specific page directly.

### Single Learning Objective per Page
* Each content page should be focused on a single learning objective. This means that the content should be structured in such a way that it is clear what the learning objective is and that all content on the page is directly related to that objective. If there are multiple learning objectives, they should be broken down into separate pages.
* Content will often follow an escalating structure, starting with a high-level overview and then breaking down into more detailed components. For example, a series of pages relating to the neutron diffusion equation might start with qualitative description of the equation (requiring only minimal physics as prerequisites). The next page might introduce the mathematical form of the equation and the meaning of each term (requiring some mathematical prerequisites and more complex physics prerequisites). A further page might introduce the derivation of the equation (requiring more complex mathematical and physics prerequisites). This structure allows a learner who only needs a qualitative understanding to get it without having to navigate through more complex content.

### Granularity: When to Split vs. Combine
* **Default to splitting**: When in doubt, create separate pages rather than combining content. It is easier for users to access multiple related pages than to navigate past irrelevant content within a single page.
* **Combine only when truly inseparable**: Two concepts should be on the same page only if understanding one is impossible without simultaneously understanding the other. For example, it might be appropriate to present basic arithmetic operations (add, subtract, multiply, divide) on a single page, but "String Length" and "String Concatenation" should be separate pages with distinct learning objectives.

### Prerequisites vs Related Content
* **Prerequisite**: Content that a learner *cannot understand the main learning objective of this page without first learning*. Prerequisites are barriers—learners must satisfy them before the page makes sense.
* **Related Content**: Content that provides context, extension, or additional examples that *enhance understanding but are not strictly necessary*. Examples: a page introducing matplotlib might link to a page about open-source software, or a page on lists might link to exercises demonstrating list operations. Learners can understand the main concept without related content.
* **When in doubt, use Related Content**: If a learner can grasp the main learning objective without knowing something, it should be related content. This prevents unnecessary prerequisites from blocking access.

### Naming and Tagging Conventions
* **Language-agnostic pages**: Use the `programming` tag (e.g., "Programming: For Loops", "Programming: Objects and Types", `programming` tag). These pages may use pseudocode and should have the "pseudocode" tag if they do.
* **Language-specific pages**: Use the language name tag only (e.g., "Python: For Loops" gets tag `python`, not `programming`). Language-specific pages should have the corresponding language-agnostic foundation as a prerequisite.
* **Mathematical/conceptual foundation pages**: Use domain-specific tags (e.g., `maths`, `physics`). These precede domain-specific implementation pages.
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
