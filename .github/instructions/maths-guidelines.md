Maths can be included in the content using LaTeX syntax (it will be interpreted by KaTeX). This is some slightly customised Markdown syntax required to denote maths content.

# Inline Content

Content in the middle of a sentence can be denoted using single dollar signs. For example, $E=mc^2$.

# Equations and Equation Blocks

A single equation or a block of equations can be denoted using double dollar signs. Multiple equations in a block are separated by a double-backslash. For example:

$$
E=mc^2
$$

or 

$$
y(x=0) &= 1 \\
\frac{\textrm{d}y}{\textrm{d}x} &= 2x \\
$$

Ampersands act as alignment characters, so the equations will be aligned at the equals sign. For blocks of equations, it is good practice, but not required, to align the equations at the equals sign to make it easier to read.

You should not use the `align` environment, as this is not supported by workflow which will be used to render the content.

# Referencing Equations

All equations (but not in-line maths content) will be automatically numbered. Each equation can be labelled using the `\label{}` command, and then referenced later in the content using the `\ref{}` command. For example:

$$
E=mc^2 \label{eq:einstein}
$$

The above equation is Equation \ref{eq:einstein}.
