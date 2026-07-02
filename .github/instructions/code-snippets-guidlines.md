This file describes how to include code within content.md pages.

* For non-interactive code blocks, use the triple-backtick codefences (```) to format the code. The opening codedence should be followed by the name of the programming language (e.g. ```python, ```r, ```java, etc.) to allow for syntax highlighting on the platform. If the code is pseudocode, do not specify a language.
* When including code snippets or literal values (in the programming sense) in paragraphs of prose, surround it with a pair of single backticks. Where applicable, specify the language following the code snippet in a pandoc style (e.g. "`console.log("Hello, World!")`{.javascript}"). 
* File names, function names, and commands should be treated as code and surrounded with a pair of single backticks. For example, `myfile.txt`, `my_function()`, and `git commit` should all be formatted as code.
* In paragraphs of text, for numeric values, use backticks to render it as code if it is a reference to a literal value in the code, but omit it if referring to the numeric value.
* Interactive Python code cells are supported in the platform and should be surrounded with triple backticks, with the opening backticks followed by "py-cell". For example:
```py-cell
print("Hello, world!")
```
* If interactive Python cells require packages outside of the standard library, these should be added at the end of the main object in metadata.json file in a list under the key "python_packages". For example:
```json
"python_packages": [
        "numpy",
        "pandas"
    ]
}
```
* Interactive R code cells are supported in the platform and should be surrounded with triple backticks, with the opening backticks followed by "r-cell". For example:
```r-cell
print("Hello, world!")
```
* Interactive code cells should be used where it would be useful for the user to be able to run the code and see the output for themselves. In these cases, the code does not need comments preempting the output.
* When pseudocode is used to demonstrate programming concepts in a language-agnostic way, the corresponding metadata file should include the "pseudocode" tag.