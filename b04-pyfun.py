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
    # Functions

    Leverage the power of code recycling with functions.

    > **Requirements:** Make sure to understand data types and loops introduced in the section on [Loops and Conditional Statements](https://hydro-informatics.com/jupyter/pyloop.html).

    ## What are functions?

    Functions are a convenient way to divide code into handy, reusable, and better readable blocks, which help to structure code. Function blocks can accept parametric arguments and are reusable. Thus, functions are a key element for sharing code and working in teams. The basic structure of a Python function involves:

    * A `def` keyword followed by a function name with *arguments* in parentheses and a code block.
    * The type of *arguments* that a function can receive are:
        - Required arguments: `arg`
        - Default keyword arguments (with default values): `arg=value`
        - Arbitrary positional (optional) arguments: `*args`
        - Arbitrary (optional) keyword arguments: `**kwargs`

    Using optional (keyword) arguments makes functions more robust and flexible. The code block of a function is indented, similar to loops:
    """)
    return


@app.cell
def _(arguments, f):
    def my_function(argument1, *args, **kwargs):
        something = f(arguments)
        return something

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A Basic Example

    Only a handful of countries (notably the United States) still use imperial units in everyday life, while most countries use the *Système international d'unités* (SI units). Let's write a simple function to help imperial unit users convert *feet* (imperial) to *meters* (SI).

    In the following example, the function name is `feet_to_meter` and the function accepts one argument, which is `feet`. The function returns the `feet` argument multiplied with a `conversion_factor` of 0.3048, which corresponds to the conversion factor from feet to meters. In this simple example, the `conversion_factor` variable cannot be modified externally and only exists in the *namespace* of the function.

    > In general, internal variables (i.e., variables defined within a function), such as `conversion_factor`, are not accessible outside (the namespace) of the function.
    """)
    return


@app.function
def feet_to_meter(feet):
    conversion_factor = 0.3048
    return conversion_factor * feet


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Function Calls

    To call a function, it must be defined before the call. The function may be defined in the same script or in another script, which can then be imported as a module ([read more about modules and packages in the next section](https://hydro-informatics.com/python-basics/pypckg)). Then we can call, for example, the above-defined `feet_to_meter` function as follows:
    """)
    return


@app.cell
def _():
    feet_value = 10
    meter_value = feet_to_meter(feet_value)
    print("{0} feet are {1} meters.".format(feet_value, feet_to_meter(feet_value)))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Optional Arguments *args

    Replacing the non-optional `feet` argument in the above function with an optional argument `*args` enables the conversion of as many length values as the function receives. The following lines explain step-by-step how that works.

    1.  Make sure that anyone understands the input and output parameters of the function by adding inline *docstrings* with a pair of triple double-apostrophes (`\"\"\"`) that embraces input parameters (`:params parameter_name: definition`) and the function return (`:output: definition`).
    1. By default, we will assume that multiple values are provided. Therefore, a list called `value_list` is instantiated at the beginning of the function, while `conversion_factor` remains the same as before.
    1. A for-loop over `*args` identifies and processes the arguments provided. Why a for-loop? <br>Python automatically collects `*args` into a tuple, and therefore, we can iterate over `*args`, even though the provided values were not passed as a list or tuple.
    1. The for-loop in the `try` code block includes a `try` - `except` statement to verify if the provided values (arguments) are numeric and can be converted to meters. If the `try` block runs successfully, the expression `arg * conversion_factor` appends the converted argument `arg` to `value_list`.
    1. Eventually, the `return` keyword returns the value list.
    """)
    return


@app.function
def feet_to_meter_1(*args):
    """ 
    :param name: numeric values in feet
    :output: returns list of values in meter
    """
    value_list = []
    conversion_factor = 0.3048
    for arg in args:
        try:
            value_list.append(arg * conversion_factor)
        except TypeError:
            print(str(arg) + ' is not a number.')
    return value_list


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With the newly defined and more flexible function, we can now call `feet_to_meter` with as many arguments as needed:
    """)
    return


@app.cell
def _():
    print('Function call with 3 values: ')
    print(feet_to_meter_1(3, 1, 10))
    print('Function call with no value: ')
    print(feet_to_meter_1())
    print('Function call with non-numeric values:')
    print(feet_to_meter_1('just', 'words'))
    print('Function call with mixed numeric and non-numeric values:')
    print(feet_to_meter_1('just', 'words', 2))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Optional Keyword Arguments **kwargs

    In the last paragraphs, we made the `feet_to_meter` function more flexible so that it can now receive as many arguments as needed. Until now, the internal `conversion_factor` variable cannot be modified from outside the function, which limits flexibility. For instance, imagine we are writing this function for a historian. In the past, imperial units were widespread in many cultures (e.g., Greek, Roman, or Chinese) with varying length definitions between 0.250 m and 0.335 m. That means the historian will need flexibility regarding the conversion factor, while we still want to use 0.3048 m as the default value. This requirement can be implemented with optional keyword arguments `**kwargs` and this is how it works in the code block below:

    1. Add `**kwargs` after `*args` in the function `def` parentheses (the order of `*args, **kwargs` is important).
    1. Keep `conversion_factor = 0.3048` as the default value (we want the function to be functional also without any keyword argument provided).
    1. Similar to the `*args` statement, Python automatically identifies variables beginning with `**` as optional keyword arguments (actually, the name *args* and *kwargs* does not matter - the `*` signs are important). The difference to `*args` is that Python identifies `**kwargs` as a dictionary.
    1. A for-loop iterates over the *kwargs*-dictionary and the `if` statement identifies any optional keyword argument that contains the string `"conv"` as conversion_factor.
    1. A `try`- `except` statement tests if the provided value for the keyword argument is numeric by attempting a conversion to `float()`.

    The rest of the function remains unchanged.
    """)
    return


@app.function
def feet_to_meter_2(*args, **kwargs):
    """ 
    :param *args: numeric values in feet
    :output: returns list of values in meter
    """
    value_list = []
    conversion_factor = 0.3048
    for key, value in kwargs.items():
        if 'conv' in key:
            try:
                conversion_factor = float(value)
                print('Using conversion factor = ' + str(value))
            except (ValueError, TypeError):
                print(str(value) + ' is not a number (using default value 0.3048).')
    for arg in args:
        try:
            value_list.append(arg * conversion_factor)
        except TypeError:
            print(str(arg) + ' is not a number.')
    return value_list


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Test different conversion factors with the newly defined flexibility of the `feet_to_meter` function:
    """)
    return


@app.cell
def _():
    print('Function call with 3 values and a conversion factor of 0.32: ')
    print(feet_to_meter_2(3, 1, 10, conv_factor=0.32))
    print('Function call with 3 values and a conversion factor of 1/7 with slightly different name: ')
    print(feet_to_meter_2(3, 1, 10, conversion_factor=1 / 7))
    print('Function call with 2 values with default conversion factor: ')
    print(feet_to_meter_2(25, 10))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Default Keyword Arguments

    Keyword arguments can also be defined by default. The below example shows how the `conversion_factor` can be default-defined in the `def` function parentheses. Note that `conversion_factor` must be defined after any optional arguments `*args`.
    """)
    return


@app.function
def feet_to_meter_3(*args, conversion_factor=0.3048):
    """ 
    :param *args: numeric values in feet
    :output: returns list of values in meter
    """
    value_list = []
    for arg in args:
        try:
            value_list.append(arg * conversion_factor)
        except TypeError:
            print(str(arg) + ' is not a number.')
    return value_list


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can use `feet_to_meter` with or without or with a conversion factor and after a list of values:
    """)
    return


@app.cell
def _():
    print('Function call with a conversion factor of 0.313 and two values: ')
    print(feet_to_meter_3(1, 10, conversion_factor=0.313))
    print('Function call with 3 values without any conversion factor: ')
    print(feet_to_meter_3(3, 1, 10))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Function Wrappers and Decorators

    If multiple functions contain similar lines, chances are that those functions can be further factorized by using function wrappers and decorators. A typical example is a license checkout (e.g. to use a commercial Python module/package, such as Esri's `arcpy`) or if we want to use a recurring error statement with `try` - `except` statements.

    For instance, consider two or more functions that should receive, process, and produce numerical output from user input. These functions may look like this:
    """)
    return


@app.cell
def _():
    def multiply_arguments(*args):
        result = 1.0
        try:
            for arg in args:
                result = result * arg
            print('The result is: ' + str(result))
        except TypeError:
            print('ERROR: The calculation could not be performed (input arguments: %s)' % str(args))
        except ValueError:
            print('ERROR: The calculation could not be performed (input arguments: %s)' % str(args))
        return result

    def sum_up_arguments(*args):
        result = 0.0
        try:
            for arg in args:
                result = result + arg
        except TypeError:
            print('ERROR: The calculation could not be performed (input arguments: %s)' % str(args))
        except ValueError:
            print('ERROR: The calculation could not be performed (input arguments: %s)' % str(args))
        return result

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Both functions involve the statement `print("The result is: " + str(result))` to print the results to the Python console (e.g., to get some intermediate information) and to run only on valid (i.e., numeric) input with the help of exception (`try` - `except`) statements. However, we want our functions to focus on the calculation only and this is where a wrapper function helps.

    A wrapper function can be defined by first defining a standard function (e.g., `def verify_result`) and then passing another function (`func`) as an argument. In this function (`verify_result`), we can then place a nested `def wrapper()` function that will embrace `func`. It is important to use both optional `*args` and optional keyword `**kwargs` in the wrapper function and the call to `func` to make the wrapper as flexible as possible.
    """)
    return


@app.function
def verify_result(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            print("Success. The result is %1.3f." % float(result))
            return result
        except TypeError:
            print("ERROR: The calculation could not be performed because of at least one non-numeric input (input arguments: %s)" % str(args))
            return 0.0
        except ValueError:
            print("ERROR: The calculation could not be performed because of non-numeric input (input arguments: %s)" % str(args))
            return 0.0
    return wrapper


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, we can use an `@`-decorator to wrap the above math functions in the `verify_result(fun)` function. When Python reads the beautiful, code-decorating `@` sign, it automatically looks for the wrapper function defined after the `@` sign to wrap the following function.
    """)
    return


@app.cell
def _():
    @verify_result
    def multiply_arguments_1(*args):
        result = 1.0
        for arg in args:
            result = result * arg
        return result

    @verify_result
    def sum_up_arguments_1(*args):
        result = 0.0
        for arg in args:
            result = result + arg
        return result

    return multiply_arguments_1, sum_up_arguments_1


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The two functions (`multiply_arguments` and `sum_up_arguments`) can be called as usual, for example:
    """)
    return


@app.cell
def _(multiply_arguments_1, sum_up_arguments_1):
    multiply_arguments_1(3, 4)
    multiply_arguments_1(3, 4, 'not a number')
    sum_up_arguments_1(3, 4)
    sum_up_arguments_1('absolutely', 'no', 'valid', 'input')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The above wrapper function returns the wrapped function results, too. However, in order to use built-in function attributes (e.g., the function's name with `__name__`, the function's docstring with `__doc__`, or the module in which the function is defined with `__module__`) outside of the wrapper, we need the wrapper function to return the wrapped (decorated) function itself. This can be done as follows:
    """)
    return


@app.cell
def _():
    def error_func(*args, **kwargs):
        return 0.0

    def verify_result_1(func):

        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except TypeError:
                print('ERROR: The calculation could not be performed because of at least one non-numeric input (input arguments: %s)' % str(args))
                return error_func(*args, **kwargs)
            except ValueError:
                print('ERROR: The calculation could not be performed because of non-numeric input (input arguments: %s)' % str(args))
                return error_func(*args, **kwargs)
        return wrapper

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Note the difference: the `wrapper` function now returns `func(*args, **kwargs)` instead of the numeric variables as result. If the function cannot be executed because of invalid input, the wrapper will return an error function (`error_func`), which ensures the consistency of the wrapper function. One may think that the error function returning 0.0 is obsolete because the exception statements could directly return 0.0. However, 0.0 is a *float* variable, while `error_func` is a function and the function wrapper should always return the same data type, regardless of an exception raise (error) or a successful execution. This is what makes code consistent.

    This paragraph showed examples of using the decorators in the shape of an `@` sign to wrap (embrace) a function. Decorators are also a useful feature in Python classes, for example, when a class function returns static values. Read more about decorators in classes later in the chapter on [object orientation and classes](https://hydro-informatics.com/jupyter/classes.html#decorators).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Iterators and Generators

    A characteristic of *list*, *tuple*, and *dictionary* data types is their iterability, which is provided by their `__iter__` built-in method. Thus, iterability is the reason why we can write:
    """)
    return


@app.cell
def _():
    for e in [1, 2, 3]: print(e)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Besides iterations, Python also enables the creation of generators (i.e., generator functions). Instead of using a `return` statement, a generator function ends with one (or more) `yield` statement(s), returning data as long as a `next()` function (inherent step in iterations) is called. An application of a generator is, for example, the flattening of nested lists (i.e., remove sub-lists and write all variables directly into a non-nested list):
    """)
    return


@app.cell
def _():
    from collections.abc import Iterable

    def flatten(nested_list):
        for e in nested_list:
            if isinstance(e, Iterable) and not isinstance(e, str):
                for x in flatten(e):
                    yield x
            else:
                yield e
            
    a_nested_list = [[1, 2, 3], ["a", "b", "c"]]
    flattened_list = list(flatten(a_nested_list))
    print(flattened_list)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > The above example uses `Iterable` from the standard module `collections.abc`. More about importing packages and modules is discussed in the [Modules & Packages](https://hydro-informatics.com/python-basics/pypckg) section.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Lambda Functions

    [Lambda (*&lambda;*) calculus](https://en.wikipedia.org/wiki/Lambda_calculus) is a formal language for expressing computation-based function abstraction and was introduced in the 1930s by the mathematician Alonzo Church. Lambda functions originate from functional programming and represent short, anonymous (i.e, without a name) functions. Although Python is not inherently a functional programming language, functional concepts were implemented early in Python, for example with the `map()`, `filter()`, and `reduce()` functions and also the `lambda` operator.

    In Python, an anonymous (nameless) lambda function can take any number of arguments, but can only have one expression. The arguments consist of a comma-separated list of variables and the expression uses these arguments. The **syntax** of `lambda` functions is:

    `lambda arguments : expression`

    The following example illustrates a `lambda` function with one argument and adds 1 to the argument:
    """)
    return


@app.cell
def _():
    add_one = lambda number : number + 1
    print(add_one(1))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That was nice but quite useless. Here is an example of a slightly more useful lambda function that sums up two input arguments:
    """)
    return


@app.cell
def _():
    sum_up = lambda x, y : x + y
    print(sum_up(1, 5))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The above-shown function for converting feet to meters can also be written as a lambda function:
    """)
    return


@app.cell
def _():
    feet_to_meter_4 = lambda ft_value: ft_value * 0.3048
    print(feet_to_meter_4(10))
    return (feet_to_meter_4,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Using a `lambda` function made the code shorter. In addition, to evaluate the `feet_to_meter` `lambda` function for multiple values, we can use the `map()` function. The syntax of a `map()` function is:

    `result = map(function, sequence)`

    where `sequence` can be a *list* or a *tuple*. Thus, to evaluate a *tuple* of four values, we can write:
    """)
    return


@app.cell
def _(feet_to_meter_4):
    four_ft_values = (4, 9.7, 7, 2)
    print(list(map(feet_to_meter_4, four_ft_values)))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The `list()` function converts the `map()` output into a *list* to evaluate the `map()` function (otherwise, the result would be something like `<map object at ...>`).

    If the `feet_to_meter` function is not needed at another place in the code, one can also write:
    """)
    return


@app.cell
def _():
    print(list(map(lambda x : x * 0.3048, (4, 9.7, 7, 2))))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Another feature of Python is the `filter(function, list)` function that represents an elegant solution to filter out those elements from a list for which the function returns `True`. The following code block illustrates a `filter` that eliminates all numbers from a `some_numbers` list, which can be divided by three.
    """)
    return


@app.cell
def _():
    some_numbers = list(range(1, 10))
    print(list(filter(lambda x: x % 3, some_numbers)))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Formerly, the `reduce()` function for merging down list input into one value was implemented in Python. However, Python's original author *Guido van Rossum* removed it from the built-in namespace in *Python 3* — it now lives in `functools.reduce` ([read his post](https://www.artima.com/weblogs/viewpost.jsp?thread=98196)), which is why it is not featured here as a built-in.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Exercise:** Get familiar with functions in the [Hydraulics (1d)](https://hydro-informatics.com/exercises/ex-ms) exercise.
    """)
    return


if __name__ == "__main__":
    app.run()
