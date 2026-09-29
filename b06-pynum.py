# /// script
# dependencies = [
#     "marimo",
#     "numpy",
#     "openpyxl",
#     "pandas",
# ]
# ///
import marimo

__generated_with = "0.25.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
async def _():
    # WebAssembly (browser) version only: download the course data files
    import sys as _sys

    if _sys.platform == "emscripten":
        import os as _os
        from pyodide.http import pyfetch as _pyfetch

        for _file in (
            "data/pure-numbers.txt",
        ):
            _os.makedirs(_os.path.dirname(_file), exist_ok=True)
            _response = await _pyfetch(
                "https://raw.githubusercontent.com/sschwindt/marimo-python-course/main/" + _file
            )
            with open(_file, "wb") as _local_file:
                _local_file.write(await _response.bytes())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Data Files, NumPy & Pandas

    Basic (text) file handling, *NumPy*, *pandas*, and *DateTime*. This notebook is also available at [hydro-informatics.com](https://hydro-informatics.com/jupyter/pynum.html).

    # Load and Write Basic Data Files

    Data can be stored in many different (text) file formats such as *txt* or *csv* files. Python provides the `open(file)` and `write(...)` functions to read and write data from nearly every text file format. In addition, there are packages such as `csv` (for *csv* files), which simplify handling specific file types. The following sections illustrate the use of the `open(file)` and `write(...)` functions. The later shown *pandas* module provides more functions to import and export numeric data along with row and column headers.

    ## Load (Open) Text File Data

    The `open` command loads text files as file object in Python. The syntax of the `open` command is:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```python
    open("file-name", "mode")
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    where:

    * `file-name` is the file to open (e.g., `"data.txt"`); if the file is not in the script directory, the *filename* needs to be extended by the full directory (path) to the data file (e.g., `"C:/experiment1/data.txt"`).
    * `mode` defines the access type and it can take the following values:
        - `"r"` - read-only (default value if no `"mode"` value is provided); the file cannot be modified nor overwritten.
        - `"rb"` - read-only in binary format; the binary format is advantageous if the file is not a text file but media such as pictures or videos.
        - `"r+"` - read and write (no new file will be created).
        - `"w"` - write-only; a new file is created if a file with the provided `file-name` does not yet exist.
        - `"wb"` - write-only in binary mode.
        - `"w+"` - create, write and read.
        - `"wb+"` - write and read in binary mode.
        - `"a"` - append new data to a file; the write-pointer is placed at the end of the file and a new file is created if a file with the provided `file name` does not yet exist.
        - `"ab"` - append new data in binary mode (write-only).
        - `"a+"` - both append (write at the end) and read.
        - `"ab+"` - append and read data in binary mode.

    When `"r"` or `"w"` modes are used, the file pointer (i.e, the blinking cursor that you can see, for example, in Word documents) is placed at the beginning of the file. For `"a"` modes, the file pointer is placed at the end of the file.

    It is good practice to read and write data from and to a file within a `with` statement to avoid file lock issues. For example, the following code block creates a new text file within a `with` statement:
    """)
    return


@app.cell
def _():
    with open("data/new.csv", mode="w+") as file:
        file.write("And yet it moves.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Read-only

    Once the file object is created, we can parse the file and copy the file data content to a desired Python [data type](https://hydro-informatics.com/python-basics/pybase.html#var) (e.g., a list, tuple or dictionary). Parsing the data works with [*for-loops*](https://hydro-informatics.com/python-basics/pyloop.html#for) (other loop types will also work) to iterate on lines and line entries. The lines represent *strings* and data columns can be separated by using the built-in *string* function `line_as_list = str().split("SEPARATOR")`, where `"SEPARATOR"` can be `","` (comma), `";"` (semicolon), `"\t"` (tab), or any other sign. After reading all data from a file, use `file_object.close()` to avoid that the file is locked by Python and cannot be opened by another program.

    The following example opens a text file called *pure-numbers.txt* ([download pure-numbers.txt](https://raw.githubusercontent.com/hydro-informatics/jupyter-python-course/main/data/pure-numbers.txt) into a local sub-folder called *data*) that contains *float* numbers between 0.0 and 10.0. The file has 17 data rows (e.g., for 17 experimental runs) and 4 data columns (e.g., for 4 measurements per experimental run), which are separated by a *TAB* (`"\t"` separator). The below code block uses the built-in function `readlines()` to parse the file lines, splits the lines using the `"\t"` separator, and loops over the line entries to append them to the list variable `data_list` only if `entry` is numeric (verified with the `try` - `except` statement). `data_list` is a nested list that is initiated at the beginning of the script and a sub-list (nested list) is appended for every file line (row).
    """)
    return


@app.cell
def _():
    _file_object = open('data/pure-numbers.txt')  # read file with default "mode"="r"
    data_list = []
    for _line in _file_object.readlines():  # this will be a nested list with 17 sub-lists (rows) containing 4 entries (columns)=
        _line_as_list = _line.split('\t')
        data_list.append([])
        for _entry in _line_as_list:  # converts the line into a list using a tab (\t) separator
            try:  # append an empty sub-list for every file line (17 rows)
                data_list[-1].append(float(_entry))
            except ValueError:
                print('Warning: %s is not a number. Replacing value with 0.0.' % str(_entry))  # try to append the entry as floating point number to the last sub-list, which is pointed at using [-1]
    print('Number of rows: %d' % len(data_list))
    print('Number of columns: %d' % len(data_list[0]))
    _file_object.close()  # if entry is not numeric, append 0.0 to the sub-list and print a warning message
    # verify that data_list contains the 17 rows (sub-lists) with the built-in list function __len__()
    # verify that the first sub-list has four entries (number of columns)
    print(data_list)  # close file (otherwise it will be locked as long as Python is still running!) alternative: use with-statement  # print the data
    return (data_list,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Recall:** The `with` statement from the above example avoids that we need to write `file.close()`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Create and Write Files

    A file is created with the `"w"` or `"a"` modes (e.g., `open(file_name, mode="a")`).

    > **Tip:** When `mode="w"`, the provided file is opened with the pointer at position zero. Writing data will make the pointer overwrite any existing data at the position. That means any existing data in the opened file will be overwritten. To avoid overwriting data in an existing file use `mode="a"`.

    Imagine that the loaded `data_list` contains measurements in mm. For each value in each sub-list, append the string `"nan"` to `new_data_list` if the value is less than or equal to 1.0; otherwise, preserve the original numeric value. If indices are used explicitly, access a nested-list value as `data_list[i][j]`.
    Use a `with` statement and context manager to ensure that the file is closed automatically after the block finishes.
    """)
    return


@app.cell
def _(data_list):
    # create a new list and overwrite all values <= 1.0 with nan
    new_data_list = []  
    for i in data_list:
        new_data_list.append([])
        for j in i:
            if j <= 1.0:
                new_data_list[-1].append("nan")
            else:
                new_data_list[-1].append(j)

    print(new_data_list)
    # write the modified new_data_list to a new text file
    new_file = open("data/modified-data.csv", mode="w+")  # lets just use csv: Python does not care about the file ending (could also be file.wayne)
    for row in new_data_list:
        new_line = ", ".join([str(e) for e in row]) + "\n"
        new_file.write(new_line)
    new_file.close()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Modify Existing Files

    Existing text files can be opened and modified in either `mode="r+"` (pretending that information needs to be read before it is modified) or `mode="a+"`. Recall that `"r+"` will place the pointer at the beginning of the file and `"a"` will place the pointer at the end of the file. Thus, if we want to modify lines or entries of an existing file, `"r+"` is the good choice and if we want to append data at the end of the file, `"a"` is the good choice (`+` is not strictly needed in the case of `"a"`). This section shows two examples: (1) modification of existing data in a file using `"r+"`, and (2) appending data to an existing file using `"a"`.

    **Example 1 - Replace data in an existing file with `"r+"`:** In the previous code block, we eliminated all measurements that were smaller than 1 *mm* because of the precision of the measurement device. However, we have retained all other values with two-digit accuracy - an accuracy that is not given. Consequently, all decimal places in the measurements must also be eliminated. To achieve this, we have to round all measured values with Python's built-in round function (`round(number, n-digits)`) to zero decimal places (i.e., `n-digits = 0`).
    In this example (featured in the below code block), an exception `IOError` is raised when the file `"data/modified-data.csv"` does not exist (or if it is locked by another software). An `if` statement ensures that rounding the data is only attempted if the file exists.
    The overwriting procedure first reads all lines of the file into the `lines` variable. After reading all lines, the pointer is at the end of the file, and `file.seek(0)` puts the pointer back to position 0 (i.e., at the beginning of the file). `file.truncate()` purges the file. Thus, the original file is blank for a moment and all file contents are stored in the `lines` variable. Rounding the data happens within a *for-loop* that:

    * Splits the comma-separated line *string* (produces `lines_as_list`).
    * Creates the temporary list `_numeric_line_`, where rounded, numeric values are stored (the variable is overwritten in every iteration).
    * Loops over the line entries (`line_as_list`), where an exception statement appends rounded (to zero digits), numeric values and appends `"nan"` when an entry is not numeric.
    * Writes the modified line to the `"data/modified-data.csv"` *csv* file.

    Finally, the *csv* is closed with `modified_file.close()`.
    """)
    return


@app.cell
def _():
    try:
        with open('data/modified-data.csv', mode='r+') as modified_file:
            lines = modified_file.readlines()
            modified_file.seek(0)
            modified_file.truncate()
            for _line in lines:
                _line_as_list = _line.split(', ')
                numeric_line = []
                for _entry in _line_as_list:
                    try:
                        numeric_line.append(round(float(_entry), 0))
                    except ValueError:
                        numeric_line.append(_entry.strip())
                modified_file.write(', '.join((str(entry) for entry in numeric_line)) + '\n')
        print('Processed file.')
    except OSError as error:
        print(f'Could not process the file: {error}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In theory, the above code block can be re-written as a function to modify any data in a file. In addition, other threshold values or particular data ranges can be filtered using `if` - `else` statements.

    **Example 2 - Append data to an existing file with `"a"`:** By coincidence, you find a hand-written measurement protocol that has data of an 18th experimental run, which is not in the electronic measurement data file due to a data transmission error. Now, you want to add the data to the above-produced *csv* file. Entering the data does not take much work, because only 4 measurements were performed per experimental run and the below code block contains the hand-written data in a list variable called `forgotten_data`.
    This example uses the `os` module (recall [Package, Modules and Libraries](https://hydro-informatics.com/jupyter/pypckg.html)) to verify if the data file exists with `os.path.isfile()` (the `os.getcwd()` statement is a gadget here). The code block features the usage of a `with` statement (i.e., a `with` - context manager or name space).

      The essential part of the code that writes the line to the data file is `file.write(line)`, where `line` corresponds to the above-introduced `", ".join(list-of-strings) + "\n"` *string*.
    """)
    return


@app.cell
def _():
    import os
    print(os.getcwd())
    forgotten_data = [4.0, 3.0, 'nan', 8.0]
    if os.path.isfile('data/modified-data.csv'):
        with open('data/modified-data.csv', mode='a') as _file_object:
            _file_object.write(', '.join([str(e) for e in forgotten_data]) + '\n')
        print('Data appended.')
    else:
        print('The file does not exist.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Challenge:** The expression `", ".join([str(e) for e in a_list]) + '\n'` is a recurring expression in many of the above-shown code blocks. How does a function look like that automatically generates this expression for lists of different data types?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # NumPy

    *NumPy* provides high-level mathematical functions for linear algebra including operations on multi-dimensional arrays and matrices. The open-source *NumPy* (for *Numerical Python*) library is written in Python and [C](https://en.wikipedia.org/wiki/C_(programming_language)), and comes with comprehensive documentation ([download the latest version on the developer's web site](https://numpy.org/doc/) or [read the developer's online tutorial](https://numpy.org/devdocs/user/quickstart.html)).

    ## Installation

    *NumPy* can be installed through *Anaconda* ([recall instructions](https://hydro-informatics.com/python-basics/pyinstall.html#install-additional-python-packages)) and the developers recommend using a scientific Python distribution (*Anaconda*) with [*SciPy Stack*](https://scipy.org/install/).

    The provided *Anaconda* [environment.yml (`flussenv`)](https://raw.githubusercontent.com/Ecohydraulics/flusstools-pckg/main/environment.yml) already includes *NumPy* (more information in the [conda installation section](https://hydro-informatics.com/python-basics/pyinstall.html#conda-env)). Similarly, Linux users will have *NumPy* installed in a virtual environment (e.g., `vflussenv`) with *pip* (recall [pip-installing flusstools](https://hydro-informatics.com/python-basics/pyinstall.html#quick-guide)). Otherwise, to install *NumPy* in any other *conda* environment, open *Anaconda Prompt* (*Start* > type *Anaconda Prompt*) and type:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```python
    conda activate ENVIRONMENT-NAME
    conda install numpy
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To pip-install *NumPy* in any other virtual environment tap:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```python
    pip install numpy
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Usage

    The NumPy library is typically imported with `import numpy as np`. Create a NumPy array with `np.array(values)`, where `values` is array-like input such as a list or tuple. Nested sequences can be used to create multidimensional arrays; for example, `np.array([[1, 2, 3], [4, 5, 6]])` creates an array with two rows and three columns.

    > **Note:** This section provides insights into basic *NumPy* functions and it does not (rather: cannot) cover all *NumPy* functions and data types. Generally speaking, be sure that whatever mathematical operation you want to perform, *NumPy* offers a solution. Check out the [*NumPy* documentation](https://numpy.org/devdocs/user/quickstart.html), [have a look at *NumPy*'s built-in functions and methods overview](https://numpy.org/devdocs/user/quickstart.html#functions-and-methods-overview), or use your favorite search engine with the search words **numpy** ***FUNCTION***.

    The following code block shows very basic usage of *NumPy* (or: numpy) imported as `np` and the creation of a *2x3* numpy array. The rounded parentheses indicated that the value sequence of the `np.array` represents a tuple for creating a multi-dimensional array.
    """)
    return


@app.cell
def _():
    import numpy as np
    an_array = np.array(([2, 3, 1], [4, 5, 6]))
    print(an_array)
    return an_array, np


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *NumPy* arrays (data type: *ndarray*) have many built-in features, for example to output the array size:
    """)
    return


@app.cell
def _(an_array):
    print(type(an_array))
    print("Array dimensions: " + str(an_array.shape))
    print("Total number of array elements: " + str(an_array.size))
    print("Number of array axes: " + str(an_array.ndim))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    There are many types of `np.array`s and many ways to create them:
    """)
    return


@app.cell
def _(np):
    print(np.array([(2, 3, 1), (4, 5, 6)]))  # the same as an_array
    print(np.array([[2, 3, 1], [4, 5, 6]], dtype=complex))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Arrays of zeros or ones or empty arrays can be created with *integer* or *float* data types. When creating such arrays, be aware of using tuples (i.e., sequences embraced with rounded parentheses) to define array dimensions:
    """)
    return


@app.cell
def _(np):
    print(np.zeros((2,6)))
    print(np.ones((2,6), dtype=np.float64))  # other dtypes: int16, np.int16, float, np.float32, np.complex64
    print(np.empty((2,6)))
    print(np.empty((2,6), dtype=np.int16))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `np.empty(shape)` allocates an array without initializing its entries. Any displayed values are arbitrary remnants of memory and may differ between runs. Fill every entry before reading or using the array; use `np.zeros(shape)` or `np.ones(shape)` when initialized values are required.

    > **Data type sizes:** *NumPy* data types have different sizes (in [bytes](https://en.wikipedia.org/wiki/Byte)) and the more digits, the larger the variable size. For example, `np.float64` has an item size of 8 bytes (64/8), while `np.float32` has an item size of 4 bytes (32/8) only. Use `ndarray.itemsize` (e.g., `an_array.itemsize`) to find out the size of an array in bytes. For analyses of large datasets, the data type gets very important regarding computation speed and storage.

    *NumPy* provides the `arange(start, end, step-size)` function to create numeric sequences. Such sequences represent arrays (`ndarray`) that can later be reshaped (i.e., re-organized in columns and rows).
    """)
    return


@app.cell
def _(np):
    print("1D array:")
    print(np.arange(0, 10, 2))  # 1D array
    print("\n2D array:")
    print(np.arange(0, 12, 2).reshape(2, 3))  # 2D array
    print("\n3D array:")
    print(np.arange(1, 13, 1).reshape(2, 2, 3))  # 3D array
    print("\n1D Linspace (start, end, number-of-elements):")
    print(np.linspace(0, np.pi, 3))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Random numbers can be generated with *NumPy*'s random number generator `np.random` and its `.random(range_tuple)` function.
    """)
    return


@app.cell
def _(np):
    rand_array = np.random.random((2,4))
    print(rand_array)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Built-in array functions enable finding minimum or maximum values, or sums of arrays:
    """)
    return


@app.cell
def _(an_array, np):
    print("Sum of 12-elements ones-array: " + str(np.ones((2,6)).sum()))
    print("Minimum: " + str(an_array.min()))
    print("Maximum: " + str(an_array.max()))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Color Arrays

    Arrays may also contain color information, where colors represent a mix of the three base colors red, green, and blue (**RGB**). Thus, one color can be defined as `[red-value, green-value, blue-value]`, and a value of `0` means that a color tone is not present, while `255` is its **maximum** value. There is no color when all color tone values are zero, which corresponds to *black*; when all color tones are maximum (255), the color mix corresponds to *white*. This way, array elements can be lists of color tones, and plotting such arrays produces images. The following example produces an array with 5 color-list elements, which could be plotted as a very basic image with 5 pixels (one black, red, green, blue, and white, respectively):
    """)
    return


@app.cell
def _(np):
    color_set = np.array([[0, 0, 0],         # black
                          [255, 0, 0],       # red
                          [0, 255, 0],       # green
                          [0, 0, 255],       # blue
                          [255, 255, 255]])  # white
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Array (Matrix) Operations

    Array calculations (matrix operations) follow the rules of linear algebra:
    """)
    return


@app.cell
def _(np):
    A = np.random.random((2,4))
    B = np.random.random((4,2))
    print("Subtraction: " + str(A.transpose() - B))
    print("Element-wise product: " + str(A.transpose() * B))
    print("Matrix product (option 1): " + str(A @ B))
    print("Matrix product (option 2): " + str(A.dot(B)))
    return A, B


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Further element-wise calculations include exponential (`**`), geometric (`np.sin`, `np.cos`, `np.tan`, etc.), and boolean operators:
    """)
    return


@app.cell
def _(A, np):
    print("A to the power of 3: " + str(A**3))
    print("Exponential: " + str(np.exp(A)))
    print("Square root: " + str(np.sqrt(A)))
    print("Sine of A times 3: " + str(np.sin(A) * 3))
    print("Boolean where A is smaller than 0.3: " + str(A < 0.3))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Array Shape Manipulation

    Sometimes it is necessary to stack a multi-dimensional array into a vector or recast the shape of an array. Beyond the `reshape()` function, there are a couple of other options to manipulate the shape of an array:
    """)
    return


@app.cell
def _(A, B, np):
    print("Flattened matrix A (into a vector):\n" + str(A.ravel()))
    print("\nTranspose matrix A and append B:\n" + str(np.array([A.transpose(), B])))
    print("\nTranspose matrix A and append B and cast into a (4x4) array:\n" + str(np.array([A.transpose(), B]).reshape(4,4)))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## *NumPy* File Handling and `np.nan`

    In the above examples on file handling, measurement data were loaded from text files, manipulated (modified), and (re-)written. The data manipulation involved the introduction of `"nan"` (*not-a-number*) values, which were excluded because measurements <1 mm were considered errors. Why didn't we use zeros here? Zeros are numbers, too, and have a significant effect on data statistics (e.g., for calculating mean values). However, the `"nan"` *string* value may cause difficulties in data handling, in particular regarding the consistency of function output. *NumPy* provides with the `np.nan` data type a powerful alternative to the tedious `"nan"` *string*.

    *NumPy* also has a text file load function called `np.loadtxt(file-name, *args, **kwargs)`, which imports text files as `np.array`s of *float* values. The default *float* value type can be adapted with the optional keyword `dtype`. Other optional keyword arguments are:

    * `delimiter=STR` (e.g., `delimiter=';'`), where the default is `"None"`
    * `usecols=TUPLE` (e.g., `usecols=(1, 3)` extracts the 2<sup>nd</sup> and 4<sup>th</sup> column), where also one *integer* value is possible to read just on single column
    * `skiprows=INT` (e.g., `skiprows=2` skips the first two lines), where the default is `0`
    * more arguments are available and listed in the [*NumPy* documentation](https://numpy.org/doc/stable/reference/generated/numpy.loadtxt.html).

    The following example loads the above-created *csv* file *data/modified-data.csv* containing *integer* and `"nan"` *string* values, which are automatically converted to `np.nan`.
    """)
    return


@app.cell
def _(np):
    experiment_data = np.loadtxt("data/modified-data.csv", delimiter=",")
    print("This is the data 4th line (row): " + str(experiment_data[3, :]))
    print("The data type of the 3rd (%s) entry is: " % str(experiment_data[3, 2]) + str(type(experiment_data[3, 2])))
    return (experiment_data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In addition, or as an alternative, the function `np.load()` picks up data from file-like `.npz`, `.npy`, or pickled (saved Python objects) data sources (more information is available in the [*NumPy* docs](https://numpy.org/doc/stable/reference/generated/numpy.load.html#numpy.load)).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Statistics
    The above examples featured array functions to assess basic array statistics such as the minimum and maximum. *NumPy* provides many more functions for array statistics such as the mean, median, or standard deviation, including functions that account for `np.nan` values. The following example illustrates some of the statistical functions with the experimental data from the above examples. Note the usage of `nanmean` instead of `mean` and statistics along array axis, where the optional keyword argument `axis=0` corresponds to columns and `axis=1` to statistics along rows in 2-dimensional arrays (maximum axis number corresponds to the array dimensions *n* minus 1, i.e., maximum `axis=n-1`).
    """)
    return


@app.cell
def _(experiment_data, np):
    print("Mean value (without nan): " + str(np.mean(experiment_data)))  # no applicable result
    print("Mean value with np.nan: " + str(np.nanmean(experiment_data))) 
    print("Mean value along axis 0 (columns): " + str(np.nanmean(experiment_data, axis=0))) 
    print("Mean value along axis 1 (rows): " + str(np.nanmean(experiment_data, axis=1)))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following paragraphs represent a tabular overview of statistical functions in *NumPy* (source: *NumPy* docs). The listed functions only represent the baseline and *NumPy* provides many more options, which can be leveraged using any search engine with *NumPy* and the desired function as a search keyword.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ***

    Basic statistic functions

    | Function                              | Description                                                                                 |
    |---------------------------------------|---------------------------------------------------------------------------------------------|
    | [`nanmin(a[, axis, out, keepdims])`](https://numpy.org/doc/stable/reference/generated/numpy.nanmin.html#numpy.nanmin)      | Minimum of an array or along an axis, ignoring `np.nan`.                     |
    | [`nanmax(a[, axis, out, keepdims])`](https://numpy.org/doc/stable/reference/generated/numpy.nanmax.html#numpy.nanmax)      | Maximum of an array or along an axis, ignoring `np.nan`.                 |
    | [`ptp(a[, axis, out])`](https://numpy.org/doc/stable/reference/generated/numpy.ptp.html#numpy.ptp)                   | Range of values (max - min) along an axis.                                          |
    | [`percentile(a, q[, axis, out, ...])`](https://numpy.org/doc/stable/reference/generated/numpy.percentile.html#numpy.percentile)    | q-th percentile of data along a specified axis.                            |
    | [`nanpercentile(a, q[, axis, out, ...])`](https://numpy.org/doc/stable/reference/generated/numpy.nanpercentile.html#numpy.nanpercentile) | q-th percentile of data along a specified axis, ignoring `np.nan`. |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ***

    Mean (average), standard deviation, and variances

    | Function                                          | Description                                                                   |
    |---------------------------------------------------|-------------------------------------------------------------------------------|
    | [`median(a[, axis, out, overwrite_input, keepdims])`](https://numpy.org/doc/stable/reference/generated/numpy.median.html#numpy.median) | Median along an (optional) axis.                                  |
    | [`average(a[, axis, weights, returned])`](https://numpy.org/doc/stable/reference/generated/numpy.average.html#numpy.average)             | Weighted average along an (optional) axis.                        |
    | [`mean(a[, axis, dtype, out, keepdims])`](https://numpy.org/doc/stable/reference/generated/numpy.mean.html#numpy.mean)             | Arithmetic mean along an (optional) axis.                         |
    | [`std(a[, axis, dtype, out, ddof, keepdims])`](https://numpy.org/doc/stable/reference/generated/numpy.std.html#numpy.std)        | Standard deviation along an (optional) axis.                      |
    | [`var(a[, axis, dtype, out, ddof, keepdims])`](https://numpy.org/doc/stable/reference/generated/numpy.var.html#numpy.var)        | Variance along an (optional) axis.                                |
    | [`nanmedian(a[, axis, out, overwrite_input, ...])`](https://numpy.org/doc/stable/reference/generated/numpy.nanmedian.html#numpy.nanmedian)   | Median along an (optional) axis, ignoring `np.nan`.             |
    | [`nanmean(a[, axis, dtype, out, keepdims])`](https://numpy.org/doc/stable/reference/generated/numpy.nanmean.html#numpy.nanmean)          | Arithmetic mean along an (optional) axis, ignoring `np.nan`.          |
    | [`nanstd(a[, axis, dtype, out, ddof, keepdims])`](https://numpy.org/doc/stable/reference/generated/numpy.nanstd.html#numpy.nanstd)     | Standard deviation along an (optional) axis, while ignoring `np.nan`. |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ***

    Correlating data (arrays)

    | Function                                       | Description                                             |
    |------------------------------------------------|---------------------------------------------------------|
    | [`corrcoef(x[, y, rowvar, bias, ddof])`](https://numpy.org/doc/stable/reference/generated/numpy.corrcoef.html#numpy.corrcoef)           | Pearson (product-moment) correlation coefficients. |
    | [`correlate(a, v[, mode])`](https://numpy.org/doc/stable/reference/generated/numpy.correlate.html#numpy.correlate)                        | Cross-correlation of two 1-dimensional sequences.       |
    | [`cov(m[, y, rowvar, bias, ddof, fweights, ...])`](https://numpy.org/doc/stable/reference/generated/numpy.cov.html#numpy.cov) | Estimate covariance matrix, based on data and weights.   |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ***

    Generate and plot histograms

    | Function                                          | Description                                                                |
    |---------------------------------------------------|----------------------------------------------------------------------------|
    | [`histogram(a[, bins, range, normed, weights, ...])`](https://numpy.org/doc/stable/reference/generated/numpy.histogram.html#numpy.histogram) | Histogram of a set of data.                                    |
    | [`histogram2d(x, y[, bins, range, normed, weights])`](https://numpy.org/doc/stable/reference/generated/numpy.histogram2d.html#numpy.histogram2d) | Bi-dimensional histogram of two data samples.                  |
    | [`histogramdd(sample[, bins, range, normed, ...])`](https://numpy.org/doc/stable/reference/generated/numpy.histogramdd.html#numpy.histogramdd)   | Multidimensional histogram of some data.                       |
    | [`bincount(x[, weights, minlength])`](https://numpy.org/doc/stable/reference/generated/numpy.bincount.html#numpy.bincount)                 | Count number of occurrences of each value in array of non-negative ints.   |
    | [`digitize(x, bins[, right])`](https://numpy.org/doc/stable/reference/generated/numpy.digitize.html#numpy.digitize)                        | Indices of the bins to which each value in input array belongs. |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Can *NumPy* do *MATLAB*&reg;?

    Are you considering switching to Python after starting softly into programming with *MATLAB&reg;*-like software? There are many reasons for enhancing data analyses with Python and here are some facilitators for previous *MATLAB&reg;* users:

    * *MATLAB&reg;* matrices can be loaded and saved with [`scipy.io.loadmat(matrix-file-name)`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.io.loadmat.html#scipy.io.loadmat) (use `import scipy`).
    * *NumPy*'s `np.array` replaces *MATLAB&reg;*'s matrix notation (even though there is the historic, deprecated *NumPy* data type `np.matrix`).
    * Import many *MATLAB&reg;* features from `np.matlib` (e.g., `from numpy.matlib import rand, zeros, ones, empty, eye)` or more generally `import numpy.matlib as M`).
    * Find the *NumPy* equivalent of many *MATLAB&reg;* function in the [*NumPy* documentation](https://numpy.org/doc/stable/user/numpy-for-matlab-users.html#table-of-rough-matlab-numpy-equivalents).
    * To emulate *MATLAB&reg;*'s plot functions use the `pylab` package and import it as `from pylab import *`. <br>&#9888; This overwrites all other (standard) definitions of the `plot()` function and `array()` objects. So this usage is deprecated. [Read the plotting section](https://hydro-informatics.com/python-basics/pyplot) for comprehensive plotting instructions with Python.

    *MATLAB&reg; is a registered trademark of The MathWorks.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Exercise:** Practice *numpy* and *csv* file handling in the [Reservoir design](https://hydro-informatics.com/exercises/ex-sp) exercise.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Pandas

    *pandas* is a powerful library for data analyses and manipulation with Python. It can handle *NumPy* arrays, and both packages jointly represent a powerful data processing engine. The power of *pandas* lies in processing data frames, data labeling (e.g., workbook-like column names), and flexible file handling functions (e.g., the built-in `read_csv(csv-file)` function). While *NumPy* arrays enable calculations with multidimensional arrays (beyond 2-dimensional tables) and low memory consumption, *pandas* `DataFrame`s efficiently process and label tabular data with more than ~100,000 rows. Because of its labelling capacity, *pandas* also finds broad application in machine learning. In summary, *pandas*' functionality builds on top of *NumPy* and both libraries are maintained by the [*SciPy*](https://www.scipy.org/) (*Scientific computing tools for Python*) community that also produces `matplotlib` (see [the plotting section](https://hydro-informatics.com/python-basics/pyplot) and *IPython* (*Jupyter*'s *Python* kernel).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Installation

    *pandas* can be installed through *Anaconda* ([recall instructions](https://hydro-informatics.com/python-basics/pyinstall.html#install-additional-python-packages)) and the developers recommend using a scientific Python distribution (*Anaconda*) with [*SciPy Stack*](https://scipy.org/install/).

    The provided *Anaconda* [environment.yml (`flussenv`)](https://raw.githubusercontent.com/Ecohydraulics/flusstools-pckg/main/environment.yml) already includes *pandas* (more information in the [conda installation section](https://hydro-informatics.com/python-basics/pyinstall.html#conda-env)). Similarly, Linux users will have *pandas* installed in a virtual environment (e.g., `vflussenv`) with *pip* (recall [pip-installing flusstools](https://hydro-informatics.com/python-basics/pyinstall.html#quick-guide)). Otherwise, to install *pandas* in any other *conda* environment, open *Anaconda Prompt* (*Start* > type *Anaconda Prompt*) and type:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```python
    conda activate ENVIRONMENT-NAME
    conda install pandas
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To pip-install *pandas* in any other virtual environment tap:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```python
    pip install pandas
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Usage

    *pandas* standard import alias is `pd`: `import pandas as pd`. The following sections provide an overview of basic *pandas* functions and many more features are documented in the [developer's docs](https://pandas.pydata.org/pandas-docs/stable/user_guide/index.html).

    ## Data frames & Series
    The below code block illustrates one way to create a *pandas* data frame (`pd.DataFrame`), one of *pandas* core objects. Note the difference between a 1-dimensional series `pd.Series` (corresponds to a one-column data frame), and an n-dimensional data frame with **row (=index)** and column names. The default row names number rows starting from 0 (unlike Office software that starts at row no. 1), without column names. Column names can be initially defined as a [list](https://hydro-informatics.com/python-basics/pybase.html#list) and replaced with a [dictionary](https://hydro-informatics.com/python-basics/pybase.html#dict) that maps the initial list entries to new names.
    """)
    return


@app.cell
def _(np):
    import pandas as pd

    print("A 1-column pd.DataFrame:\n"+ str(pd.Series([3, 4, np.nan])))  # a simple pandas data frame with one column

    row_names = np.arange(1, 4, 1)
    wb_like_df = pd.DataFrame(np.random.randn(len(row_names), 3), 
                              index=row_names, columns=['A', 'B', 'C'])
    print("\nThis is a workbook-like (row and column names) data frame:\n" + str(wb_like_df))
    print("\nRename column names with dictionary:\n" + str(wb_like_df.rename(
            columns={'A': 'Series 1', 'B': 'Series 2', 'C': 'Series 3'})))
    print("\nTranspose the data frame:\n" + str(wb_like_df.T))
    return (pd,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A *pandas* `DataFrame` object can also be created from a [dictionary](https://hydro-informatics.com/python-basics/pybase.html#dict), where the dictionary keys define column names and the dictionary values constitute the data of every column:
    """)
    return


@app.cell
def _(np, pd):
    df = pd.DataFrame({'Flow depth': pd.Series(np.random.uniform(low=0.1, high=0.3, size=(4,)), dtype='float32'),
                       'Sediment': ["yes", "no", "yes", "no"],
                       'Flow regime': pd.Categorical(["fluvial", "fluvial", "supercritical", "critical"]),
                       'Water': "Always there"})
    print("A dictionary-built data frame:\n" + str(df))
    print("\nFrame data types:\n" + str(df.dtypes))
    return (df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Built-in attributes and methods of a *pandas* `DataFrame` enable easy access to the top (head) and the bottom of a data frame and many more object characteristics (recall: use `dir(dict_df)` or [read the developer's docs](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html)):
    """)
    return


@app.cell
def _(df):
    print("Head of the dictionary-based dataframe (first two rows):\n" + str(df.head(2)))
    print("\nEnd (tail) of the dictionary-based dataframe (last row):\n" + str(df.tail(1)))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Example: Create a `pandas.DataFrame` of Froude Numbers

    In hydraulics, the [*Froude* number ***Fr***](https://hydro-informatics.com/documentation/glossary.html#term-Froude-number) characterizes the flow regime as "fluvial" (Fr<1), "critical" (Fr=1), or "super-critical" (Fr>1). The precision of measurement devices in physical flume experiments makes the exact determination of the *critical* moment a challenge and forces researchers to apply an interval around 1, rather than the exact value of `1.0`:

    | ***Fr*** | (0.00, 0.95( | (0.95, 1.00(           | (1.00)   | )1.00, 1.05)           | )1.05, inf(    |
    |----------|--------------|------------------------|----------|------------------------|----------------|
    | *Flow*   | fluvial      | near-critical (slow) | critical | near-critical (fast) | super-critical |

    `pd.DataFrame( ... )` objects are a convenient way to classify and store flume experiment data:
    """)
    return


@app.cell
def _(np, pd):
    def classify_froude(fr):
      if fr < 0.95:
    	  return "fluvial"
      if fr < 1.0:
    	  return "near-critical (slow)"
      if fr == 1.0:
    	  return "critical"
      if fr <= 1.05:
    	  return "near-critical (fast)"
      return "super-critical"

    Fr_measured = np.random.uniform(low=0.01, high=2.00, size=10)
    Fr_classified = [classify_froude(fr) for fr in Fr_measured]
    obs_df = pd.DataFrame({"measured": Fr_measured, "flow regime": Fr_classified})
    print(obs_df)
    return (obs_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Append Data to a `pandas.DataFrame`

    Avoid repeatedly inserting rows into a DataFrame. Collect new records first and construct a DataFrame once, or concatenate batches with `pd.concat()`. Assigning a complete column is direct and efficient.

    The following code block illustrates both adding a row and a column to an existing *pandas* data frame.
    """)
    return


@app.cell
def _(obs_df, pd):
    import random
    new_rows = pd.DataFrame({'measured': [0.996], 'flow regime': ['near-critical (slow)']})
    obs_df_1 = pd.concat([obs_df, new_rows], ignore_index=True)
    obs_df_1['with sediment'] = [bool(random.getrandbits(1)) for _ in range(len(obs_df_1))]
    print(obs_df_1.tail(3))
    return (obs_df_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## NumPy Arrays and pandas Data Frames

    A NumPy array has one data type (`dtype`), while a pandas DataFrame can use a different dtype for each column. `DataFrame.to_numpy()` selects a common dtype for the resulting array and may require type coercion or a copy, depending on the DataFrame's column dtypes. DataFrame index and column labels are not included in the resulting array. If one column of the *pandas* `DataFrame` is non-numeric, the conversion involves copying the object, which then causes high computational costs. Note that the *index* and *column* labels of a *pandas* `DataFrame` are lost in the conversion from `pd.DataFrame` to `np.ndarray`.
    """)
    return


@app.cell
def _(obs_df_1):
    print(obs_df_1.to_numpy())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Access Data Frames Entries

    Elements of data frames are accessible by the column and row label (`df.loc[index=row, column-label]`) or number (`df.iloc`):
    """)
    return


@app.cell
def _(df):
    print("Label localization results in: " + str(df.loc[2, "Flow depth"]))
    print("Same result with integer grid location: " + str(df.iloc[2, 0]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reshape Data Frames

    Single or multiple rows (indices) and columns can be extracted from and combined into new or existing `DataFrame` objects:
    """)
    return


@app.cell
def _(df, pd):
    print(pd.DataFrame([df["Flow depth"], df["Sediment"]]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The `df.stack()` method pivots the columns of a data frame, which is a powerful tool to classify data that can take different dimensions (e.g., the volume and weight of 1 m<sup>3</sup> water - read more about the [stack method](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.stack.html#pandas.DataFrame.stack)).
    """)
    return


@app.cell
def _(df):
    print(df.stack()[0])
    df.unstack()  # unstack data frame
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Big datasets often contain large amounts of data with many labels, but we are often only interested in a small subset of the data. To this end, data frame subsets can be created with `df.pivot(index, columns, **values)` ([Pivot method](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.pivot.html#pandas.DataFrame.pivot)):
    """)
    return


@app.cell
def _(df):
    print("Pivot table for \'Flow regime\':\n" + str(df.pivot(index="Sediment", columns="Flow depth")["Flow regime"]))
    print("\nPivot table for \'Water\':\n" + str(df.pivot(index="Sediment", columns="Flow depth")["Water"]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In addition, `df.pivot_table(index, columns, values, aggfunc)` ([Pivot table function](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.pivot_table.html#pandas.DataFrame.pivot_table)) enables inline Office-like function application to one or more rows and/or columns.
    """)
    return


@app.cell
def _(df, np):
    print("\'mean\' for \'Flow depth\':\n" + str(df.pivot_table(index="Sediment", columns="Flow regime", values="Flow depth", aggfunc=np.mean)))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Read more about reshaping and pivoting data frames in the [developer's docs](https://pandas.pydata.org/pandas-docs/stable/user_guide/reshaping.html).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## File Handling (*csv*, Workbooks, and More)

    *pandas* can read from and write to many data file types, which makes it extremely powerful for analyzing any data. The following table summarizes the most important file types for numerical hydraulic, morphodynamic, and fluvial landscape analyses, and more file type handlers can be found at the [developer's docs](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html).

    |  File type                                                                  |  *pandas* read                                                                                         |  *pandas* write                                                                                       | Usage example                                                                                           |
    |-----------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------|
    |  CSV |  [`read_csv`](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-read-csv-table)       |  [`to_csv`](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-store-in-csv)          | Reading from data loggers (e.g., discharge, flow depth)    |
    |  Google BigQuery  |  [`read_gbq`](https://en.wikipedia.org/wiki/BigQuery)|  [`to_gbq`](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-bigquery)              | Analyze social media   |
    |  JSON |  [`read_json`](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-json-reader)         |  [`to_json`](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-json-writer)          | Manipulate [BASEMENT](https://hydro-informatics.com/numerics/basement.html) model files    |
    |  HTML |  [`read_html`](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-read-html)           |  [`to_html`](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-html)                 | Process  web site data        |
    |  [HDF5 Format](https://support.hdfgroup.org/HDF5/doc1.6/UG/08_TheFile.html) |  [`read_hdf`](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-hdf5)                 |  [`to_hdf`](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-hdf5)                  | Analyze [BASEMENT](https://hydro-informatics.com/basement) or [HEC-RAS](https://www.mdpi.com/2073-4441/10/10/1382) output files |
    |  Python Pickle Format |  [`read_pickle`](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-pickle)            |  [`to_pickle`](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-pickle)     | Cache memory dump       |
    |  SQL  |  [`read_sql`](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-sql)     |  [`to_sql`](https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html#io-sql)  | Retrieve and write data to SQL data bases    |
    | Workbooks (Excel / OpenDocument) | `read_excel` | `to_excel` | Exchange tabular data with spreadsheet software; supported formats and required engines depend on the file extension. |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The following code block illustrates how the above produced *data/modified-data.csv* file can be loaded and saved to a workbook with *pandas*. *pandas* uses [openpyxl](https://openpyxl.readthedocs.io) by default, but this usage varies depending on the workbook file type (e.g., `.ods`, `.xls`, and `xlsb` build on other packages - [read more about the `engine` keyword](https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html)).
    """)
    return


@app.cell
def _(pd):
    measurement_data = pd.read_csv("data/modified-data.csv", sep=",", header=None, names=["Test 1", "Test 2", "Test 3", "Test 4"])
    print("Header of data/modified-data.csv:\n" + str(measurement_data.head(3)))
    measurement_data.to_excel("data/modified-data-wb.xlsx", sheet_name="2025-01-01 Tests")
    return (measurement_data,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > pandas infers each column's dtype from its values. A column containing both numbers and text commonly has an `object` or string-related dtype, but an Excel writer can still store numeric and text cells in the same worksheet column. Use `np.nan` or another supported missing-value marker instead of the literal string `"nan"` when missing numeric data should remain distinguishable from text.

    A *pandas* `ExcelWriter` object can be created to write multiple `pd.DataFrame` objects to a workbook, on one or more sheets. Here is an example, where the non-numeric `"nan"` strings are replaced in `measurement_data` with `np.nan` to yield a purely numeric data frame in two steps (`# (1)` and `# (2)`):
    """)
    return


@app.cell
def _(df, measurement_data, np, pd):
    measurement_data_1 = measurement_data.replace('nan', np.nan, regex=True)  # (1) replace "nan" with np.nan
    measurement_data_1 = measurement_data_1.apply(pd.to_numeric)  # (2) convert all data to numeric
    with pd.ExcelWriter('data/modified-data-wb-EW.xlsx') as writer:
    # write workbook with pd ExcelWriter object
        measurement_data_1.to_excel(writer, sheet_name='2025-01-01 Tests')
        df.to_excel(writer, sheet_name='pandas example')
    return (measurement_data_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Categorical Data

    *string* variables that represent statistically relevant categories are the baseline for data classification and statistics. *pandas* provides the special data type of `dtype="category"` to facilitate statistical analyses.

    In the above Froude-number example, we used five categories to classify the flow regime as a function of the *Froude number*, which can serve as categories. This is useful, for instance, when no water was flowing or when a sensor broke in an experiment and we want to categorize our measurements to filter valid tests only:
    """)
    return


@app.cell
def _(pd):
    flow_regimes = ["fluvial", "near-critical (slow)", "critical", "near-critical (fast)", "super-critical"]
    observation_examples = ["fluvial", "dry", "critical", "near-critical (slow)", "measurement error"]
    Fr_cat = pd.Categorical(observation_examples, categories=flow_regimes, ordered=False)
    print(pd.Series(Fr_cat))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Data Frame Statistics

    *pandas* has efficient routines to perform workbook-like row or column sorting (e.g., [`df.sort_index()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_index.html) or [`df.sort_values()`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sort_values.html)), and enables the fast calculation of data frame statistics with `df.describe()`, where 25%, 50%, and 75% represent the *i-th* percentiles:
    """)
    return


@app.cell
def _(measurement_data_1):
    measurement_data_1.describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Statistical *pandas* data frame methods overlap with *NumPy* methods and include:

    * `df.abs()` calculates absolute values
    * `df.cumprod()` calculates the cumulative product
    * `df.cumsum()` calculates the cumulative sum
    * `df.count()` counts the number of non-null observations
    * `df.max()` calculates the maximum value
    * `df.mean()` calculates the mean (average)
    * `df.min()` calculates the minimum value
    * `df.mode()` calculates the mode
    * `df.prod()` calculates the product
    * `df.std()` calculates the standard deviation
    * `df.sum()` calculates the sum
    """)
    return


@app.cell
def _(measurement_data_1):
    print('Mean:\n' + str(measurement_data_1.mean()))
    print('Median:\n' + str(measurement_data_1.median()))
    print('Standard deviation:\n' + str(measurement_data_1.std()))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Note:** *pandas* has many more built-in functionalities, for example, to plot histograms or any data using the `matplotlib` library, and machine learning.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Apply Custom (Own) Functions to Data Frames

    *pandas* data frames have a built-in `apply(fun, args=(...))` method that enables applying a custom function to (parts of) a `pd.DataFrame` object. The following code block borrows from the `feet_to_meter` function from the [functions](https://hydro-informatics.com/jupyter/pyfun.html#kwargs) chapter ([download converter.py](https://raw.githubusercontent.com/hydro-informatics/jupyter-python-course/main/fun/converter.py)). The *pandas* docs provide more information about the [pandas.apply](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.apply.html) method.
    """)
    return


@app.cell
def _(np, pd):
    from fun.converter import feet_to_meter
    df_1 = pd.DataFrame({'Feet': np.random.randint(0, 100, size=6), 'Meters': np.ones(6) * np.nan})
    # create data frame with random integers
    df_1['Meters'] = df_1['Feet'].apply(feet_to_meter)
    # apply feet_to_meter to the Meters columns of the data frame
    print(df_1)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Dates and Time

    *pandas* involves methods for calculations and labeling with date and time values through [`pd.Timestamp`](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html), which converts date-time-like strings into timestamps or creates timestamps from keyword arguments:
    """)
    return


@app.cell
def _(pd):
    print(pd.Timestamp('2025-01-01T12'))
    print(pd.Timestamp(year=2025, month=1, day=1, hour=12))
    print(pd.Timestamp(2025, 1, 1, 12))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The expression `pd.Timestamp(2025, 1, 1, 12)` mimics the powerful `datetime.datetime` *API* (Application Programming Interface) of the `datetime` Python library, which provides sophisticated methods for handling time-dependent values. While *pandas*' built-in timestamps are convenient for creating time series within `pd.DataFrame` objects and workbook-like tables, `datetime` is one of the best solutions for time-dependent calculations in Python. `datetime` is available by default (i.e., it must not be *conda* or *pip*-installed) and is efficiently applicable, for example, to data that were collected over several years including leap years. The `datetime` package comes with many attributes and methods, which are documented in detail in the [Python docs](https://docs.python.org/3/library/datetime.html).

    The standard usage is:
    """)
    return


@app.cell
def _():
    import datetime as dt
    start_date = dt.datetime(2024, 2, 25, 22, 30, 0)
    end_date = dt.datetime(year=2024, month=3, day=2, hour=2, minute=15, second=30)
    print("Datetime variables can be subtracted:\n" + str(end_date - start_date))
    print("The result is a %s object." % type(end_date - start_date))
    return dt, end_date, start_date


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `dt.timedelta` objects can also be separately defined:
    """)
    return


@app.cell
def _(dt, end_date, start_date):
    time_diff = dt.timedelta(days=0, seconds=0, microseconds=0, milliseconds=0, minutes=0, hours=23, weeks=0)
    act_time = start_date
    print('Iterate from start to end date with stepsize=time_diff:')
    while act_time <= end_date:
        print(act_time.strftime('%Y-%m(%h)-%d, %H:%M:%S'))
        act_time = act_time + time_diff
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That is all for the introduction to data and file handling. Though there is much more to data processing than shown in this chapter and the next other chapters of this eBook will occasionally feature more tools.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Exercise:** Practice *pandas* and its *csv* file handling routines, as well as basic date-time handling in the [flood return period calculation](https://hydro-informatics.com/exercises/ex-floods) exercise.
    """)
    return


if __name__ == "__main__":
    app.run()
