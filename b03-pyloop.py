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
    # Loops and Conditional Statements

    Iterate and apply conditional criteria.

    > **Requirements:** Make sure to understand statements as defined in the section on [Errors, Logging, and Debugging](https://hydro-informatics.com/jupyter/pyerror.html).

    *Python* provides two basic types of loops to iterate through objects or functions: the `for` and the `while` loop statements. Both loop types have additional options and can be combined with conditional statements. Conditional statements evaluate *boolean* arguments (`True`/`False`) using the keywords `if: ... else: ...`. This section introduces the two loop types and conditional statements as integral parts of loops.

    ## Conditional Statements (`if` - `else`)
    Conditional statements open with an `if` keyword, followed by a test condition (e.g., `variable >= 2`) and action to accomplish when the test condition is `True` ([*boolean*](https://hydro-informatics.com/python-basics/pybase.html#boolean) test result). The conditional statement can be followed by the `elif` (*else if*) and/or `else` keywords, which represent alternative tests in the case that the `if` test condition was `False`. However, when the `if` statement was `True`, none of the following statements will be evaluated.
    """)
    return


@app.cell
def _():
    variable_2_test = "ice cream"
    if "cream" in variable_2_test:
        print("It's creamy, for sure.")
    elif "ice" in variable_2_test:
        print("It's cold, ice-cold cream.")
    else:
        print("Anything but ice cream.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Any operator can be used in the test condition (see [operators](https://hydro-informatics.com/python-basics/pybase.html#operators)) and conditions can be nested, too.

    > The code blocks in the `if` - `else` statements are indented and Python uses the indentation to group statements. The same applies to loops, functions, and classes. An IDE automatically indents code, but basic text editors may not do the job. Keep in mind that wrong indentation can be an error source.
    """)
    return


@app.cell
def _():
    number_of_scoops = 3
    if number_of_scoops <= 0:
        print("Why? How can you?")
    elif number_of_scoops < 4:
        if number_of_scoops == 1: # this is a nested if-statement
            print("One is better than nothing.")
        else:
            print("That is reasonable.")
    else:
        print("A lot. Still reasonable. Maybe.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `for`-loop

    `for` loops serve for the sequential iteration through objects such as lists or arrays. `for` loops can also be complemented with `else` statements at the end (whyever you would want to do this...).
    """)
    return


@app.cell
def _():
    for e in range(0, 8, 2):
        print("e is %d now." % e)

    flavors = ["chocolate", "bread", "cherry"] 
    for index in range(len(flavors)): 
        print(flavors[index])
    else:
        print(" --- end of second loop.")
    
    # produces the same
    for e in flavors:
        print(e)
    return (flavors,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In many cases, it is useful to iterate not only either on the iteration number (an incrementing *integer* value) or the elements of a list (e.g., a *string* value), but both simultaneously. Both the iteration step number and the list elements can be accessed with the `enumeration` built-in function:
    """)
    return


@app.cell
def _(flavors):
    for iteration_step, list_element in enumerate(flavors):
        print("The list element {0} is at position number {1}.".format(list_element, str(iteration_step)))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `while`-loop

    `while` loops run until a test condition (expression) is `True`. Similar to the `if` statement, the test condition can be composed of just one variable or an expression including [operators](https://hydro-informatics.com/python-basics/pybase.html#operators) (e.g., `while a > b`). To modify a variable within a `while` loop, use `+=` (add amount), `-=` (subtract amount), `*=` (multiply with), or `/=` (divide by). Also `while` loops can be complemented with `else` statements.

    > Make sure that every `while` loop can terminate — either its test condition eventually becomes `False`, or the loop contains a `break` statement. Otherwise, the script may be caught in an endless loop.
    """)
    return


@app.cell
def _():
    count = 10
    while (count > 7):
        count -= 1
        print("Count down %d " % count)
    else:
        print("Mission aborted.")

    count = 0
    while True:
        print("Count up: %d " % count)
        count += 1 # Replaces count = count + 1 - also works with -=, *= and /=
        if count > 3:
            break
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Example

    Use this code block to practice with data types, `for` loops and conditional `if` statements by modifying the variables `scoops` and `favorite_flavor`. Note the implementation of `try` and `except` statements ensures that whatever element number of `scoops` or `favorite_flavor` you define will not crash the script.
    """)
    return


@app.cell
def _(flavors):
    scoops = 2 # re-define the number of scoops
    favorite_flavor = "vanilla" # choose your favorite flavor

    size_scoops = {1: "small", 2: "medium", 3: "this is too much ice cream"}
    price_scoops = {1: "3 dollars", 2: "5 dollars", 3: "your health"}
    print("Hi,\nI want %d scoop-s in a waffle, please." % scoops)

    try:
        size = " " + str(size_scoops[scoops])
        price = str(price_scoops[scoops])
    except KeyError:
        size = "n unavailable number of scoops"
        price = "not defined"


    print("My pleasure to serve you. You have chosen a" + size + " ice cream. The price is " + price + ".")
    print("Let me guess your favorite flavor. Say stop when I'm correct.")
    for f in flavors:
        print("I guess your favorite flavor is %s." % f)
        if f == favorite_flavor:
            print("Stop, that\'s it!")
            if f == "bread":
                print("Sorry, this is not a bakery.")
            break
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Exercise:** Practice the application of loops with the [Hydraulics (1d)](https://hydro-informatics.com/exercises/ex-ms) exercise.
    """)
    return


if __name__ == "__main__":
    app.run()
