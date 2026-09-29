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
    # Errors, Logging, and Debugging

    Handle error types and troubleshoot (debug).

    > **Requirements:** Make sure to complete the Python introduction on data types before diving into this tutorial.

    ## Errors & Exceptions

    ### Error Types

    To err is human and Python helps us to find our mistakes by providing [error](https://docs.python.org/3/tutorial/errors.html) type descriptions. Here is a list of common errors that may occur when writing/running Python code:

    | Error Type          | Description                                                 | Example                                                   |
    |---------------------|-------------------------------------------------------------|-----------------------------------------------------------|
    | `KeyError`          | A mapping key is not found.                                 | May occur when referencing a non-existing dictionary key. |
    | `ImportError`       | Importing a module that does not exist                      | `import the-almighty-module`                              |
    | `IndentationError`  | The code block indentation is not correct.                  | See [code style descriptions](https://hydro-informatics.com/python-basics/pystyle.html#indentation)      |
    | `IndexError`        | An index outside the range of a variable is used.           | `nums = [1, 2]; print(nums[2])`                           |
    | `NameError`         | An undefined variable is referenced.                        | `print(a)`                                                |
    | `TypeError`         | Incompatible data types and/or operators are used together. | `"my_string" / 10`                               |
    | `ValueError`        | Right data type, but an inappropriate value.                                   | `int(input("Number:"))` answered with `t`                 |
    | `ZeroDivisionError` | Division by zero.                                           | `3 / 0`                                                   |

    Still, there are many more error types that can occur, and Python developers maintain comprehensive descriptions of built-in exceptions on the [Python documentation web site](https://docs.python.org/3/library/exceptions.html).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exception Handling with `try` - `except`

    `try` and `except` keywords test a code block and if it crashes, an `exception` is raised, but the script itself will not crash (unless otherwise defined in the `except` statement). The basic structure is:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```python
    try:
        # code block
    except ErrorType:
        print("Error / warning message.")
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The `ErrorType` is technically not necessary (i.e., `except:` does the job, too), but adding an `ErrorType` is good practice to enable efficient debugging or making other users understand the origin of an error or warning. The following example illustrates the implementation of a `ValueError` in an interactive console script that requires users to type an integer value.
    """)
    return


@app.cell
def _():
    try:
        x = int(input("How many scoops of ice cream do you want? "))
    except ValueError:
        print("What's that? sorry, please try again.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The `try` statement can also have an `else` clause, which runs only if the `try` block raised no exception (here using helper functions such as `key_not_found` or `handle_value`):
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```python
    try:
        value = a_dictionary[key]
    except KeyError:
        return key_not_found(key)
    else:
        return handle_value(value)
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The `pass` Statement
    When we start writing code, we are often facing a complex challenge that cannot be coded all at a time. For these challenges, Python helps us with the `pass` statement that enables the implementation of empty (void) code blocks and running code incrementally (i.e., to debug the code). In addition, the above error type definitions aid to understand errors that we made in already written code. For instance, to define later what happens when Python runs into a `NameError`, a `pass` statement can be implemented as follows:
    """)
    return


@app.cell
def _(b):
    try:
        _a = 5
        c = _a + b  # we want to define b later on with a complex formula
    except NameError:
        pass  # we know that we did not define b yet
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > The `pass` statement should only be temporary and it has a much broader application range, for example, in [functions](https://hydro-informatics.com/jupyter/pyfun.html) and [classes](https://hydro-informatics.com/jupyter/classes.html).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Logging

    The `print()` function is useful to print variables or computation progress to the console (not too often though; printing takes time and slows down calculations). For robust reporting of errors or other important messages, however, a log file represents a better choice. So what is a log file or the act of logging? We know logbooks from discoverers or adventurers, who write down their experiences ordered by dates. Similarly, a code can write down (*log*) its "experiences", but in a file instead of a book. For this purpose, Python has the standard [*logging* library](https://docs.python.org/3/howto/logging.html). For the moment, it is sufficient to know that the *logging* library can be imported in any Python script with `import logging` (more information about packages, modules, and libraries is provided in the [Package, Modules and Libraries](https://hydro-informatics.com/jupyter/pypckg.html) section).

    The below code block imports the *logging* module, and uses the following keyword arguments to set the `logging.basicConfig`:

    * `filename="my-logfile.log"` makes the logging module write messages to a file named `"my-logfile.log"` in the same directory where the Python script is running.
    * `format="%(asctime)s - %(message)s` sets the logging format to `YYYY-MM-DD HH:MM:SS.sss - `*Message text* (more format options are listed in the [Python docs](https://docs.python.org/3/howto/logging.html#displaying-the-date-time-in-messages)).
    * `filemode="w"` overwrites previous messages in the log file (remove this argument to append messages instead of overwriting).
    * `level=logging.DEBUG` defines the severity of messages written to the log file, where `DEBUG` is adequate for problem diagnoses in codes; other levels of event severity are:
        - `logging.INFO` to write all confirmation messages of events that worked as expected.
        - `logging.WARNING` (**default**) to indicate when an unexpected event happened or when an event may cause an error in the future (e.g., because of insufficient disk space).
        - `logging.ERROR` to report serious problems that make the code crashing or not produce the desired result.
        - `logging.CRITICAL` is a broader serious problem indicator, where the program itself may not be able to continue running (e.g., not only the code but also Python crashes).

    Until here, messages are only written to the log file, but we cannot see any message in the console. To enable simultaneous logging to a log file and the console (Python terminal), use `logging.getLogger().addHandler(logging.StreamHandler())` that appends an *io* stream handler.

    To write a message to the log file (and Python terminal), use
    * `logging.debug("message")` for code diagnoses,
    * `logging.info("message")` for progress information (just like we used `print("message")` before),
    * `logging.warning("warning-message")` for unexpected event documentation (without the program being interrupted),
    * `logging.error("error-message")` for errors that entail malfunction of the code, and
    * `logging.critical("message")` for critical errors that may lead to program (Python) crashes.

    *Warning*, *error*, and *critical* messages should be implemented in exception raises (see above `try` - `except` statements).

    At the end of a script, logging should be stopped with `logging.shutdown()` because otherwise the log file is locked by Python and the Python Kernel needs to be stopped to make modifications (e.g., removing) to the log file.
    """)
    return


@app.cell
def _():
    import logging
    logging.basicConfig(filename='my-logfile.log', format='%(asctime)s - %(message)s', filemode='w', level=logging.DEBUG)
    logging.getLogger().addHandler(logging.StreamHandler())
    logging.debug('This message is logged to the file.')
    logging.info('Less severe information is also logged to the file.')
    logging.warning('Warning messages are logged, too.')
    _a = 'text'
    try:
        logging.info(str(_a ** 2))
    except TypeError:
        logging.error('The variable is not numeric.')
    # stop logging
    logging.shutdown()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    And this is how `my-logfile.log` looks like:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```
    2025-05-25 18:51:46,657 - This message is logged to the file.
    2025-05-25 18:51:46,666 - Less severe information is also logged to the file.
    2025-05-25 18:51:46,667 - Warning messages are logged, too.
    2025-05-25 18:51:46,669 - The variable is not numeric.
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Events can also be documented by instantiating a logger object with `logger = logging.getLogger(__name__)`. This favorable solution is recommended for advanced coding such as writing a new [(custom) Python library](https://hydro-informatics.com/jupyter/pypckg.html)) (read more in the [Python docs on advanced logging](https://docs.python.org/3/howto/logging.html#advanced-logging-tutorial)). An example script with a more sophisticated logger is provided with the [Logger script at the course repository](https://github.com/hydro-informatics/material-py-codes/raw/master/logging/Logger.py).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Debugging

    Once you wrote more or less complex code, the ultimate question is: *Will it run?* The disappointing answer is no (in most cases), but there is a remedy called *debugging*, which is the act of removing bugs (errors) from code. Still, large code blocks can be a nightmare for debugging and this section provides some principles to reduce the factor of scariness that debugging may involve.

    ### Use Exceptions Precisely
    Embrace critical code blocks precisely with `try` - `except` keywords and possible errors. This will help later to identify possible error origins.

    > Document self-written error messages in `except` statements from the beginning on (e.g., in a markdown document) and establish a developer [wiki](https://hydro-informatics.com/documentation/documentation.html#wikis) including possible error sources and remedy descriptions.

    ### Use Descriptive Variable Names
    Give variables, functions, and other objects descriptive and meaningful names. Abbreviations will always be necessary, but those should be descriptive (e.g., use acronyms). For variables and functions, use small letters only. For classes use CamelCase.

    ### Deal with Errors
    If an error message is raised, **read the error message thoroughly** and several times to **understand the origin** of the error. Error messages often indicate the particular script and the line number where the error was raised. In the case that the error is not an apparent result of misused data types or any of the above error messages (e.g., an error raised within an external module/package), use your favorite search engine to troubleshoot the error.

    ### Verify Output
    The fact that code runs does not inherently imply that the result (output) is the desired output. Therefore, run the code with input parameters that yield existing output from another source (e.g. manual calculation) and verify that the code-produced output corresponds to the existing (desired) output.

    ### Code with a Structured Approach
    Think about the code structure before starting with punching in a bunch of code blocks and storing them in some Python files. Structural and/or behavior diagrams aid in developing a sophisticated code framework. The developers of the Unified Modeling Language (UML) provide solid guidelines for developing structure and behavior [UML diagrams](https://en.wikipedia.org/wiki/Unified_Modeling_Language#Diagrams) in software engineering.

    > Take a sheet of paper and a pencil before you start to engineer code and sketch how the code will produce the desired output.

    ### Soft Alternatives

    Explain your problem to a friend or just speak it out loud: Rephrasing and trying to explain a problem to another person (even if it is just an imaginary person or group of people) often represents a troubleshot itself.

    Take a walk, sleep on the problem, or do other things with low brain occupation. While you are dealing with other things, your brain continues to think about the problem (Wikipedia even devoted a page to this so-called process of [*incubation*](https://en.wikipedia.org/wiki/Incubation_(psychology))).
    """)
    return


if __name__ == "__main__":
    app.run()
