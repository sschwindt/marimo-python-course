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
    # Hello Data Types

    About Python, variable types and script execution.

    > **Requirements:** For running code locally, [install Python](https://hydro-informatics.com/python-basics/pyinstall.html) along with an [IDE](https://hydro-informatics.com/get-started/ide.html) that fits your needs and preferences.

    ## Load Python Environment

    These pages are written with [JupyterLab](https://jupyter.org/). For the best learning experience make sure to read about [IDEs](https://hydro-informatics.com/get-started/ide.html) before starting this tutorial.

    ## The First Lines of Code

    The examples in the first steps revolve around ice cream to illustrate the utility of simple code snippets. If you do not like ice cream, replace it with your favorite category of things.

    The very first thing you need to run Python code is, obviously, Python itself. Python can be started in a standard (system) terminal or a terminal of an IDE. Make sure to use a standard terminal for your platform according to the [Python installation](https://hydro-informatics.com/python-basics/pyinstall.html) descriptions. For instance:

    * On Windows, click on the start menu, tap `Anaconda Prompt`, and hit `Enter`
    * On Linux, open the system Terminal (e.g., Gnome Terminal by pressing `Ctrl` +  `Alt` + `T` - if nothing happens, have a look at the [Linux Terminal introduction](https://hydro-informatics.com/get-started/vm.html#linux-terminal))
    * On macOS, find the Terminal (or *Command Line Tools*), tap `Python`, and hit `Enter`

    **Alternatively**, **use your favorite IDE** to run Python code in a terminal environment:

    * With **PyCharm** (Windows):
        * Create a new empty project and use the *wrr-proj* environment (read [how to get it](https://hydro-informatics.com/python-basics/pyinstall.html#conda-env-windows-preference) and [how to create a PyCharm project](https://hydro-informatics.com/python-basics/pyinstall.html#pycharm-python-projects))
        * Find and click on the **Python Console** tab at the bottom of the PyCharm window
        * The Python console is now ready to use.
    * With **Jupyter** (cross-platform):
        * Open a Terminal following the above descriptions
        * Enter `jupyter-lab` (or `jupyter lab`, or `jupyterlab`, or `jupyter notebook` depending on your installation) > Jupyter opens in your web browser
        * Navigate to a local copy of this Jupyter notebook and run any code block (click on a code block and hit the run triangle button in the top menu).
    * With Atom (Windows / Linux / macOS - sunset software!):
        * Make sure the *flusstools* environment is installed for your platform (read [how to get it](https://hydro-informatics.com/python-basics/pyinstall.html))
        * In Atom, install and enable the `platformio-ide-terminal` ([read more](https://hydro-informatics.com/get-started/ide.html#enable-python-console))
        * In Atom, go to **Packages** (top menu) > **platformio-ide-terminal** > **New Terminal**
        * Windows + Anaconda users: enter `conda activate flussenv`
        * Linux + pip/venv users: make sure where your `vflussenv` lives and tap `source vflussenv/bin/activate` ([read more](https://hydro-informatics.com/python-basics/pyinstall.html#quick-guide))
        * All platforms: tap `python` - the console is now ready to use.

    Ultimately, **you are ready to** get the very first response (output) from the **Python** console. Start with a simple call of the `print` function by entering:
    """)
    return


@app.cell
def _():
    print("This is output from the digital ice cream printer.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Recall that the `print` command, like all other Python commands that will follow, can be either run in a *Python* console (e.g., *Conda Prompt* on Windows or *Terminal* on Linux) or in your favorite IDE. In addition, we can write down the `print` command in a **Python file ending on `.py`** (e.g., `icecream_tutorial.py`) and run the file. For instance, in **PyCharm**:

    * Expand the project branch (if not yet done: on the left side of the window)
    * Right-click in the project folder, select `New` > `Python File` and name the new *Python* (`.py`) file (e.g., `icecream_tutorial.py`).
    * Copy the above `print("...")` code into the new Python file and save it.
    * Right-click in the Python file, then `Run icecream_tutorial.py` (alternatively: press the `Ctrl` + `Shift` + `F10` keys).
    * Now, the *Python Console* should pop up at the bottom of the window and it will print the text in the above `print` command.

    In any **other (IDE) Terminal**, `cd` to the directory where the Python file (`icecream_tutorial.py`) lives, then enter `python icecream_tutorial.py` and hit `Enter`.

    > In the following, there will not be anymore the differentiation between using PyCharm or any other IDE and Jupyter. Thus, **Run the script/code block** means: run the script in your favorite IDE in the following.

    With the `"` apostrophes in the `print` command, we pass a ***string*** variable to the `print` command. Instead of using `"`, one can also use `'` but it is important to use the same type of apostrophe at the beginning and the end of the string (text) variable.

    > Be reasonable with the usage of `print`. Especially in loops, `print` leads to unnecessary system load and slows down the script.

    A marginal note: In Python3 `print` is a function, not a keyword as in Python2. `print` is useful, for example, to make a script show where it is currently running. It is also possible to print other types of variables than strings, but the combination of numerical and text variables requires more encoding (see next sections).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Python Variables and Data Types

    The above-shown `print` function already involved *string* variables. In addition, there are a couple of other variable (data) types in Python:

     - text
     - boolean
     - number (numeric)
     - tuple
     - list
     - dictionary

    > Data and variable types are difficult to understand if you simply try to learn them by heart. Remember that different data types can be useful when writing code for a particular solution.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Text

    Text variables in *Python* are *strings* (`str`) that consist of multiple *characters* (`chr`):

    | Type | Example     | Description                        |
    |------|:-----------:|------------------------------------|
    | str  | `"apple"`   | String embraced with double quotes |
    |      | `'apple'`   | String embraced with single quotes |
    |      | `\"\"\"apple\"\"\"` | Literal string (multi-line text) |
    | chr  | `"a"`       | Character (unit of a string)       |

    In addition, string variables have some built-in functions that facilitate coding. To create (instantiate) a string variable, use the `=` sign as follows:
    """)
    return


@app.cell
def _():
    flavor1 = "vanilla" # str
    first_letter = "v" # str / char
    print(flavor1.upper())
    print(flavor1[0])
    print(flavor1.split("ll")[0])
    return (flavor1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Characters can be converted to numbers and the other way round. The built-in `ord()` function returns the Unicode code point of a character, and `chr()` does the reverse. This is useful, for example, to iterate over alphabetically ordered lists.
    """)
    return


@app.cell
def _():
    print(ord("c"))  # character -> integer (Unicode code point)
    print(chr(99))   # integer -> character
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Boolean

    Boolean variables are either `True` (1) or `False` (0) with many useful code implementations. We will come back to booleans (**bool**) later in the section on conditional (`if ...`) statements.
    """)
    return


@app.cell
def _():
    bowl = False
    print("The bowl exists: " + str(bowl))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Numbers (Numeric)

    Python knows a couple of different numeric data types:

    | Type    | Example | Description                                              |
    |---------|:-------:|----------------------------------------------------------|
    | `int`   | `10`    | Signed Integer                                           |
    | `float` | `5.382` | Floating point real number                               |
    | `complex` | `1.43j` | Complex number; `j` (or `J`) denotes the imaginary unit |

    To create a numeric variable, use the `=` sign as follows:
    """)
    return


@app.cell
def _():
    scoops = 2 # int
    weight = 0.453 # float
    return scoops, weight


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Python** does not require a type assignment for a variable because it **is a high-level, interpreted programming language** (other than, for example, *C++*). However, once a variable was assigned a data type, do not change it in the code (it is just good practice - so that scoops remain integers).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    If a print statement combines numeric and text variables, the numeric variables first have to be converted to text, and then **concatenated** to a string. There are several ways to combine multiple variables in a text string:
    """)
    return


@app.cell
def _(scoops, weight):
    print("My ice cream consists of %d scoops." % scoops) # use %d for integers, %f for floats and %s for strings
    print("My ice cream weighs %1.3f kg." % weight)
    print("My ice cream weighs " + str(weight) + " kg.")
    print("My ice cream weighs {0} kg and has {1} scoops".format(weight * scoops, scoops)) # multiple variable conversion

    # f-strings (Python 3.6+) are the modern, preferred way to format text:
    print(f"My ice cream weighs {weight:.3f} kg and has {scoops} scoops.")
    return


@app.cell
def _(weight):
    print("My ice cream weighs " + weight + " kg.") # this cannot work because weight is a float
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### List

    A list is a series of values, which is embraced with brackets `[]`. The values can be any other data type (i.e., numeric, text, dictionary, or tuple), or even another list (so-called *nested lists*).
    """)
    return


@app.cell
def _(flavor1):
    flavors = ["chocolate", "bread", flavor1] # a list of strings
    nested_list = [[1, 2, 3], ["a", "b", "c"]]
    print(nested_list)
    print("A list of strings: " + str(list("ABC")))
    return (flavors,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The items of a list are called **entries** and *entries* can be appended, inserted, or deleted from a list.

    > Python always starts counting from zero. Thus, the first entry of a list is entry number 0.

    Also lists have many useful built-in functions:
    """)
    return


@app.cell
def _(flavors):
    flavors.append("cherry") # append an entry at the end
    print(flavors)
    flavors.insert(0, "lemon") # insert an entry at position 0
    print(flavors)
    print(f"There are {len(flavors)} flavors in my list.")
    print(*flavors) # print all elements of the list (note: cannot be concatenated to a str)
    print("This is all I have: " + str(flavors[:]).strip("[]"))
    del flavors[2] # bread is not a flavor, so let's remove it
    print("This is all I have: " + ", ".join(flavors))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Tuple

    A tuple represents a collection of Python objects, similar to a list, and the sequence of values (data types) in a tuple can take any type. Elements of a tuple are also indexed with integers. In contrast to lists, a tuple is embraced with round parentheses `()` and a **tuple is immutable** while **lists are mutable**. This means that a tuple object can no longer be modified after it has been created. So why would you like to use tuples then? The answer is that a tuple is more memory efficient than a mutable object because the immutable tuple can create references to existing objects. In addition, a tuple can serve as a `key` of a dictionary (see below), which is not possible with a list.
    """)
    return


@app.cell
def _():
    a_tuple = ("a text element", 1, 3.03) # example tuple
    print(a_tuple[0])
    print(a_tuple[-1]) # last element of a tuple (this also works with lists ..)

    # comparison of lists and tuples
    import time # we need this package (module here) and we will learn more about modules later
    print("patience ...")

    # iterate over a list with 100000 elements
    start_time = time.perf_counter()
    a_list = [] # empty list
    x = range(100000)
    for item in x: a_list.append(item)
    print("Run time with list: " + str(time.perf_counter() - start_time) + " seconds.")

    # iterate over a tuple with 100000 elements with modifying the tuple
    start_time = time.perf_counter()
    new_tuple = () # empty tuple
    x = range(100000)
    for item in x: new_tuple = new_tuple + (item,)
    print("Run time with tuple modification: " + str(time.perf_counter() - start_time) + " seconds.")

    # iterate over a tuple with 100000 elements if no modification of the tuple is needed
    start_time = time.perf_counter()
    new_tuple = tuple(range(100000)) 
    for item in new_tuple: pass
    print("Run time without tuple modification: " + str(time.perf_counter() - start_time) + " seconds.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Dictionary

    Dictionaries are a powerful data type in Python and have the basic structure `my_dict = {key: value}`. In contrast to lists, an element of a dictionary is called by invoking a `key` rather than an entry number. A dictionary is not enumerated and `key`s just point to their `value`s (whatever data type the `value` is).
    """)
    return


@app.cell
def _():
    my_dict =  {1: "Value 1", "a": "Value 2"}
    another_dict = {"list1": [1, 2, 3], "number2": 1}
    my_dict [1]
    return (my_dict,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Also dictionaries have many useful built-in functions:
    """)
    return


@app.cell
def _(my_dict):
    my_dict.update({3: "Value 3"})  # add a dictionary element 
    my_dict
    del my_dict[1] # delete a dictionary element 
    len(my_dict) # get the length (number of dictionary elements)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In addition, two lists of the same length can be *zipped* into a dictionary:
    """)
    return


@app.cell
def _():
    weight_1 = [0.5, 1.0, 1.5, 2.0]
    price = [1, 1.5, 1.8, 2.0]
    apple_weight_price = dict(zip(weight_1, price))
    print('{0} kg apples cost EUR {1}.'.format(weight_1[2], apple_weight_price[weight_1[2]]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Sets

    A Python set is a mutable object that is instantiated with curly brackets. Sets are unordered (in contrast to lists and tuples), and therefore, useful for mathematical operations, such as the union, intersection, difference, or symmetric difference of sets of elements. The below code block features the instantiation of two sets and the application of mathematical operators.
    """)
    return


@app.cell
def _():
    ice_shop_a = {"vanilla", "chocolate", "green"}
    ice_shop_b = {"blue", "chocolate", "vanilla"}

    print("Ice shops united: " + str(ice_shop_a | ice_shop_b))
    print("Both shops offer in common: " + str(ice_shop_a & ice_shop_b))
    print("This is what shop a has, but not shop b: " + str(ice_shop_a - ice_shop_b))
    print("This is what shop b has, but not shop a: " + str(ice_shop_b.difference(ice_shop_a)))
    print("This is what is unique to both shops (symmetric difference): " + str(ice_shop_a ^ ice_shop_b))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **How to initialize an empty set?** Writing `new_variable = {}` instantiates an empty **dictionary**, not a set. Thus, to initialize an empty set, write `new_set = set()`.

    > **What is a frozenset?** A frozenset can be created with `frozenset(set)` and has the characteristics of a set, but its elements cannot be modified once assigned. Similar to tuples that are immutable lists, frozensets are immutable sets. Why can it make sense to use a frozenset? Because a set is mutable and unhashable, which is why it cannot be used as dictionary keys as opposed to frozensets that are hashable and can be used as keys to a dictionary.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Operators

    The following operators compare data types and output boolean values (`True`or `False`):

    * `a == b` *a* equals *b* (same value)
    * `a is b` *a* is *b* (same object in memory — a stricter test than `==`)
    * `a and b` *a* and *b*
    * `a or b` *a* or *b*
    * `a <= b` *a* smaller than or equal to *b* (similar without equal sign)
    * `a >= b` *a* larger than or equal to *b* (similar without equal sign)
    * `a in b` *a* in *b* (e.g., membership test in a string or list — see example below)
    """)
    return


@app.cell
def _():
    print(not False)
    print(1 == 1)  # value equality
    print(1 == 2)
    print("ice" in "ice cream")
    return


if __name__ == "__main__":
    app.run()
