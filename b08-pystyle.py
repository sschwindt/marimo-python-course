import marimo

__generated_with = "0.25.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Code Style and Conventions

    Make your code consistent through style conventions: Take a deep breath, take off, and look at what you have learned so far from a new perspective. After this chapter, it will be worth having another look at your old code and formatting it robustly. The style guidelines presented here go beyond visual aesthetics and aid in writing effective code.

    ## Background and PEP

    This style guide highlights parts of the [PEP 8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/) by Guido van Rossum, Barry Warsaw, and Nick Coghlan. The full document is available at [python.org](https://www.python.org/dev/peps/pep-0008/) and only aspects with relevance for the applications shown in this eBook are featured in this chapter.

    **What is a PEP?** PEP stands for **Python Enhancement Proposal**. A PEP is a design document that provides information to the Python community or describes a proposed feature, process, or related change. There are many PEPs, including standards-track, informational, and process proposals. This chapter highlights recommendations from PEP 8, the style guide for Python code, by Guido van Rossum, Barry Warsaw, and Alyssa Coghlan.

    Many IDEs, including PyCharm or VS Code, provide auto-completion and tooltips with PEP-style guidance to aid consistent programming. Thus, when your IDE underlines anything in your script, check the reason for that and consider modifying the code accordingly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The Zen of Python

    Are we getting spiritual? Far from it. [The Zen of Python](https://www.python.org/dev/peps/pep-0020/) is an informational *PEP* (20) by Tim Peters to guide programmers. It is a couple of lines summarizing good practice in coding. Python's *Easter Egg* `import this` prints the Zen of Python in any Python interpreter:
    """)
    return


@app.cell
def _():
    import this

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Code Layout

    ### Maximum Line Length

    PEP 8 recommends limiting code lines to 79 characters. Flowing text in comments and [docstrings](https://hydro-informatics.com/pystyle#docstrings) should be limited to 72 characters. A team may agree on a code-line limit of up to 99 characters, provided that comments and docstrings remain limited to 72 characters.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Indentation
    Indentation groups statements into suites controlled by constructs such as `for`, `if`, `while`, `try`, `with`, `def`, and `class`. PEP 8 recommends four spaces per indentation level. Indentation does not by itself create a new variable scope: names assigned in an `if` or `for` suite remain in the surrounding scope. Functions, classes, modules, and some comprehensions have their own scoping rules.
    """)
    return


@app.cell
def _():
    for i in range(1, 2):
      print("I'm one level indented.")
      if i == 1:
    	  print("I'm two levels indented.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Because long lines of code are bad practice, we sometimes need to use line breaks when assigning, for example, a *list*, or calling a function. In these cases, the next, continuing line is also indented and there are different options to indent multi-line assignments. Here, we want to use the style code of using an opening delimiter for indentation:
    """)
    return


@app.cell
def _():
    a_too_long_word_list = ["Do", "not", "hard-code", "something", "like", "this.",
                            "There", "are", "better", "ways."]
    a_better_indented_list = [
        "Do",
        "not",
        "hard-code",
        "something",
        "like",
        "this.",
        "...",
    ]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Recall: PyCharm, VS Code, and many other IDEs automatically layout indentation.**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Line Breaks of Expressions with Binary Operators
    When binary operators are part of an expression that exceeds the maximum line length of 79 characters, the line break should be before the binary operators.
    """)
    return


@app.cell
def _():
    import pandas as pd

    dummy_df = pd.get_dummies(
      pd.Series(["variable1", "parameter2", "sensor3"]),
      dtype=int,
    )
    print(dummy_df.head(3))

    dum_sum = (
      dummy_df["variable1"]
      + dummy_df["parameter2"]
      - dummy_df["sensor3"]
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Blank Lines

    To separate code blocks, hitting the *Enter* key many times is a very inviting option. However, the random and mood-driven use of blank lines results in unstructured code. This is why *PEP* 8 authors provide guidance also on the use of blank lines:

    * Surround class definitions and top-level functions (i.e., functions where the `def`-line is not indented) with two blank lines.
    * Surround methods (e.g., functions within a class) with one blank line.
    * Use blank lines sparsely in all other code to indicate logical sections.
    """)
    return


@app.cell
def _():
    # blank 1 before top-level function
    # blank 2 before top-level function
    def top_level_function():
        pass
    # blank 1 after top-level function
    # blank 2 after top-level function
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Blanks (Whitespaces)

    Avoid unnecessary whitespace immediately inside parentheses, brackets, or braces; before commas, semicolons, and ordinary colons; or between a function name and its argument list. Write `function(e1, e2)`, `(1,)`, `a_dict = {a_key: a_value}`, and `def fun(arg=0.0):`.

    Use spaces around assignment, comparison, and Boolean operators. For arithmetic expressions, add spaces around the lowest-precedence operators and use judgment to make precedence clear; for instance, `hypot2 = x*x + y*y`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Packages and Modules

    ### Imports
    Imports normally appear after the module docstring and before module globals. Group them in this order, with a blank line between groups: standard library, related third-party packages, and local application or library imports. Put ordinary imports on separate lines and avoid wildcard imports. Every import should have its own line and avoid using the comma sign for multiple imports:
    """)
    return


@app.cell
def _():
    import os
    import sys

    import numpy as np

    from my_package import my_module

    return (np,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Naming Packages and Script
    New, custom packages or modules should have short and all-lowercase names, where underscores may be used to improve readability (discouraged for packages).

    > **Never use a minus `-` sign in a Python file name**, because the minus sign may cause import errors.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Comments

    ### Block and Inline Comments
    Block comments are indented to the same level as the code they describe, and each line begins with `# `. Use inline comments sparingly. An inline comment appears on the same line as a statement, is separated from it by at least two spaces, and begins with `# `.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Docstrings

    A docstring is a string literal that occurs as the first statement in a module, function, class, or method. It becomes available through the object's `__doc__` attribute. PEP 257 recommends triple double quotes. For example:
    """)
    return


@app.cell
def _():
    a_list = [1, 2]
    print(a_list.__doc__)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When writing a Python function, docstrings are introduced immediately after the `def ...` line with triple double-quotes:
    """)
    return


@app.cell
def _():
    def let_there_be_light(*args, **kwargs):
      """Print a sunrise message and return `True`.

      Args:
    	  *args: Positional arguments accepted but not used.
    	  **kwargs: Keyword arguments accepted but not used.

      Returns:
    	  `True` in all cases.
      """
      print("Sunrise")
      return True

    print(let_there_be_light.__doc__)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note that the recommendations on docstrings are provided with [*PEP* 257](https://www.python.org/dev/peps/pep-0257/) rather than *PEP* 8.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Name Conventions

    ### Definition of Name Styles

    The naming conventions use the following styles (source: [python.org](https://www.python.org/dev/peps/pep-0008/#naming-conventions)):

    * Classes normally use CapWords, for example `MyClass`.
    * User-defined exception classes follow the class-naming convention and normally use the suffix `Error` when they represent an error, for example `ConfigurationError`.
    * Functions, methods, and variables use lowercase words separated by underscores as needed for readability.
    * Constants normally use uppercase words separated by underscores, for example `WATER_DENSITY = 1000`.

    Some variable name formats trigger a particular behavior of Python:

    * `_single_leading_underscore` variables indicate weak internal use and will not be imported with `from module import *`
    * `__double_leading_underscore` variables invoke name mangling in classes (e.g., a method called `__dlu` of the class `MyClass` will be mangled into `_MyClass__dlu`)
    * `__double_leading_and_trailing_underscore__` variables are *magic* objects or attributes in user-controlled namespaces (e.g., `__init__` or `__call__` in classes) <br>Only use documented magic attributes and never invent them. Read more about magic methods in the chapter on [Python classes](https://hydro-informatics.com/jupyter/classes.html#magic).
    * `single_trailing_underscore_` variables are used to avoid conflicts with Python keywords (e.g., `MyClass(class_='AnotherClass')`)

    ### Object Names

    Use the above-defined styles for naming Python items as follows:

    * Classes: `CamelCase` (`CapWords`) letters only such as `MyClass`
    * Constants: `UPPERCASE` letters only, where underscores may improve readability (e.g., use at a module level for example to assign water density `RHO = 1000`)
    * Exceptions: `CamelCase` (`CapWords`) letters only (exceptions should be predefined *Error* classes; typically use the suffix `Error` (e.g., `TypeError`)
    * Functions: `lowercase` letters only, where underscores may improve readability; sometimes `mixedCase` applies to ensure backward compatibility of prevailing styles
    * Methods (class function, non-public): `_lowercase` letters only with a leading underscore, where underscores may improve readability
    * Methods (class function, public): `lowercase` letters only, where underscores may improve readability
    * Modules: `lowercase` letters only, where underscores may improve readability
    * Packages: `lowercase` letters only, where underscores are discouraged
    * Variables: `lowercase` letters only, where underscores may improve readability
    * Variables (global): `lowercase` letters only, where underscores may improve readability; note that "global" should limit to variable usage within one module only.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Important**: Never start a variable name with a number. Do **use `array_2d`**, but do **not use `2d_array`**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## More Code Style Recommendations

    To ensure code compatibility and program efficiency, the *PEP 8* style guide provides other general recommendations (read more in the [Python docs](https://www.python.org/dev/peps/pep-0008/#programming-recommendations)):

    * Prefer a `def` statement when creating a named function; do not assign a lambda expression directly to a name. A short lambda can be appropriate when passed directly as an argument, for example `items.sort(key=lambda item: item.name)`.
    * When exceptions are expected, use `try` - `except` clauses (see the [errors and exceptions](https://hydro-informatics.com/pyerror#try-except) section).
    * Ensure that methods and functions return objects consistently, for example:
    """)
    return


@app.cell
def _(np):
    def a_function_with_return(x):
        if x > 0:
            return np.sqrt(x)
        return np.nan

    return


if __name__ == "__main__":
    app.run()
