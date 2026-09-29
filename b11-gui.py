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
    # Graphical User Interfaces (GUIs)

    Make code user-friendly.

    ![img](https://hydro-informatics.com/_images/hello-gui.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A Graphical User Interface (GUI) facilitates setting input variables of scripts. This is particularly useful for reusing a script that you have written a long time ago, without having to study the whole script again in detail. Although it is arguable whether GUIs are still appropriate in times of web applications, large and in particular copyrighted data must be processed locally. Ultimately, for local data processing, a GUI can be very convenient to run self-written, custom programs.

    Several GUI libraries (packages) are available for Python and this chapter builds on the [tkinter](https://docs.python.org/3/library/tkinter.html) library. Alternatives are, for instance, [*wxPython*](https://www.wxpython.org/) or [*Jython*](https://www.jython.org/) (a *Java* implementation of *Python 2*). `tkinter` is a standard library, which does not need to be installed additionally. For a quick example, type in the terminal (e.g., *Anaconda Prompt*, *PyCharm* or *Linux* terminal - not in Python itself):
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```
    python -m tkinter
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **If you encounter troubles with `tkinter` on *Linux***, make sure that `tkinter` for Python is installed, either with <br>`sudo apt install python3-tk`  or <br>`sudo apt install python3.X-tk` (replace `X` with your Python version) or<br> `sudo apt install tk8.6-dev` to install the library only (this should be sufficient). <br>If the above comments do not work, make sure that the `tkinter` repository is available to your system, for example on Debian: `sudo add-apt-repository ppa:deadsnakes/ppa` (the repository address may change and depends on your Linux and Python versions).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `tkinter` works on most popular platforms (*Linux*, *macOS*, *Windows*) and is not only available to Python, but also [Ruby](https://www.ruby-lang.org), [Perl](https://www.perl.org/), [Tcl](https://www.tcl-lang.org/) (the origin of `tkinter`), and many more languages. Because it supports languages like *Ruby* or *Perl*, `tkinter` can be used for local GUIs as well as for web applications.

    > **Tips:**
    > * All GUI codes featured in this chapter can be downloaded from the [course repository](https://github.com/hydro-informatics/jupyter-python-course/tree/main/gui).
    > * Consider using another IDE than Jupyter (e.g., PyCharm, VS Code, or Spyder) for running the code blocks provided in this notebook.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## The First GUI
    The very first step is to `import tkinter`, usually using the alias `as tk`. With `tk.Tk()`, a so-called parent window (e.g., `top`) can be created, in which further elements will be accommodated. All further elements are created as `tk` child-objects of the parent window and placed (arranged) in the parent window using the `pack()` or `grid()` method. Here, we will use `pack` most of the time and `grid` will be useful to place elements at an exact position on the window (e.g., `tk.ELEMENT.grid(row=INT, column=INT)`). To display the GUI, the parent window `top` must be launched with `top.mainloop()` after arranging all elements. The following code block shows how to create a parent window with a label element (`tk.Label`).
    """)
    return


@app.cell
def _():
    import tkinter as tk
    _top = tk.Tk()
    _a_label = tk.Label(_top, text='A label just shows some text.')
    _a_label.pack()
    _top.mainloop()
    return (tk,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![img](https://hydro-informatics.com/_images/py-tk-first.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    After calling the `mainloop()` method, the window is in a *wait* state. That means the window is waiting for `events` being triggered through user action (e.g., a click on a button). This is called *event-driven programming*, where *event handlers* are called rather than a single linear flow in the form of a sequence of (Python) commands.

    For now, our window uses default values, for instance, for the window title, size, and background color. These window properties can be modified with the `title`, `minsize` or `maxsize`, and `configure` attributes of the `top` parent window:
    """)
    return


@app.cell
def _(tk):
    _top = tk.Tk()
    _a_label = tk.Label(_top, text='A label just shows some text.')
    _a_label.pack()
    _top.title('My first GUI App')
    _top.minsize(628, 382)
    _top.configure(bg='sky blue')
    _top.mainloop()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![img](https://hydro-informatics.com/_images/py-tk-first-config.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Add a Button to Call a Function

    Currently, the window only shows a (boring) label and waits for events that do not exist. With a `tk.Button` we can add an event trigger, which still needs something to trigger. To this end, define a `call_back` function that creates an infobox, which is an object of `showinfo` from `tkinter.messagebox` (i.e., it needs to be imported).
    """)
    return


@app.cell
def _(tk):
    from tkinter.messagebox import showinfo
    # more message boxes: askokcancel, askyesno

    def call_back(message):
        showinfo('This is an Infobox', message)
    _top = tk.Tk()
    _a_label = tk.Label(_top, text='Here is the button.')
    _a_label.pack()
    a_button = tk.Button(_top, text='>> Click <<', command=lambda: call_back('Greetings from the Button.'))
    a_button.pack()
    # add a button
    _top.mainloop()
    return (showinfo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![img](https://hydro-informatics.com/_images/py-tk-button.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Note:** The `command` keyword receives a [lambda](https://hydro-informatics.com/python-basics/pyfun.html#lambda) function that links to the `call_back` function. Why do we need this complication? The answer is that the `call_back` function would be automatically triggered with the `mainloop()` method if we were not using a `lambda` function.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## A Vanilla `tkinter` Program

    The above code blocks instantiate `tkinter` objects (*widgets*) in non-object-oriented script style. However, when we write a GUI, we most likely want to start an application (*App*) by running the script. This is why `tkinter` widgets are usually created as objects of custom classes that typically inherit from `tk.Frame`. Therefore, the following code block recasts the previous example into an object-oriented code with the template from the [section on Python classes](https://hydro-informatics.com/jupyter/classes.html#template).

    The below example creates a `VanillaApp`, which is a child of `tk.Frame` (`tkinters` *master* frame). The initialization method `__init__` needs to invoke `tk.Frame` and `pack()` it to initialize the window. After that, we can place other `widget`s such as labels and buttons as before. In the `VanillaApp`, we can also directly implement the above `call_back` function as a method. In addition, make the script run stand-alone (not supported by a beautiful Jupyter notebook) by adding an `if __name__ == "__main__": VanillaApp().mainloop()` statement at the bottom of the script (read more about the `__main__` statement in the [section on packages](https://hydro-informatics.com/jupyter/pypckg.html#standalone)).
    """)
    return


@app.cell
def _(showinfo, tk):
    # define the VanillaApp class
    class VanillaApp(tk.Frame):
        def __init__(self, master=None):
            tk.Frame.__init__(self, master)
            self.pack()
        
            table_label = tk.Label(master, text="Do you want vanilla ice?")
            table_label.pack()
            vanilla_button = tk.Button(master, text="I want Vanilla", command=lambda: self.call_back("Here is Vanilla!"))
            vanilla_button.pack()
            no_vanilla_button = tk.Button(master, text="I want something else", command=lambda: self.call_back("Here is bread!"))
            no_vanilla_button.pack()
        
        def call_back(self, message):
            showinfo("This is an Infobox", message)


    # instantiate a VanillaApp object
    if __name__ == "__main__":
        VanillaApp().mainloop()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![img](https://hydro-informatics.com/_images/py-tk-vanilla.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Make Script a Stand-alone App

    The above code block providing the `VanillaApp` class can be copied to any external Python file and saved as, for example, `vanilla_app.py`. Next, in *Anaconda Prompt* (Windows) or *Linux Terminal* start the GUI as follows (depending on the [Python installation](https://hydro-informatics.com/python-basics/pyinstall.html) used):

    1. Activate the required environment, for example:
        * Windows/Anaconda: `conda activate flussenv`
        * Linux/Virtualenv: `source vflussenv/bin/activate`
    2. Navigate to the directory where the script is located (use `cd` in [Windows](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/cd) or [Linux/macOS](http://www.linfo.org/cd.html)).
    3. Type `python vanilla_app.py` (or `python -m vanilla_app.py`) to launch the GUI.

    This sequence of commands can also be written to a batch or bash file ([`.bat` on Windows](https://www.wikihow.com/Write-a-Batch-File)) or shell script ([.sh on Linux/macOS](https://www.linux.com/training-tutorials/writing-simple-bash-script/) - [alternative documentation](http://linuxcommand.org/lc3_writing_shell_scripts.php)). After writing and saving a batch or bash file, double-click on the file to start the Python-based GUI.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## More Widgets

    There are many more widgets than labels and buttons and the below figure features some of them including:

    * A definition of the GUI window name with `master.title("Window name")`
    * A definition of the GUI window icon (ICO) with `master.iconbitmap("directory/icon-file.ico")`

    > **Attention:** Some recent versions of `tkinter` cannot open icons because of an unknown error that might stem from relative path definitions in the library. Therefore, if you get an error message such as `TclError: bitmap "gui/sample-icon.ico" not defined`, the only solution might be to comment out the line `self.master.iconbitmap("gui/sample-icon.ico")`.

    * `tk.Menu` with drop-down cascade
    * `tk.Label` (see above)
    * `tk.Button` (see above)
    * `tk.Entry` that is a blank field where users can enter values or words
    * `ttk.Combobox` that is a drop-down menu in the master frame ([tk-themed](https://docs.python.org/3/library/tkinter.ttk.html) `ttk` widget)
    * `tk.Listbox` with a `tk.Scrollbar`, where the scrollbar is required to navigate to listbox entries that are not in the visible range of the listbox size
    * `tk.Checkbutton` that can be checked (ticked) to set a `tk.BooleanVar()` object to `True` (default: not checked -> `False`)<br>Alternatively, have a look at [`tk.Radiobutton`](https://tkdocs.com/tutorial/widgets.html#radiobutton) to enable selections from a multiple-choice frame (rather than the `False`-`True`-only frame of a checkbutton)
    * `tk.PhotoImage` to display a sub-sampled image in the GUI

    ![img](https://raw.githubusercontent.com/sschwindt/hydroinformatics/main/docs/img/py-tk-elements.png)

    The next block features the code that creates the `tkinter` widgets in the figure (the [script](https://raw.githubusercontent.com/hydro-informatics/jupyter-python-course/main/gui/start_gui.py), [image](https://raw.githubusercontent.com/hydro-informatics/jupyter-python-course/main/gui/sunny-image.gif) and [icon](https://raw.githubusercontent.com/hydro-informatics/jupyter-python-course/main/gui/gui-icon.ico) are available at the course repository):
    """)
    return


@app.cell
def _(showinfo, tk):
    from tkinter import ttk

    class _MyApp(tk.Frame):

        def __init__(self, master=None):
            tk.Frame.__init__(self, master)
            self.master.title('Master Title')
            self.master.iconbitmap('gui/sample-icon.ico')
            ww = 628
            wh = 382
            wx = (self.master.winfo_screenwidth() - ww) / 2
            wy = (self.master.winfo_screenheight() - wh) / 2
            self.master.geometry('%dx%d+%d+%d' % (ww, wh, wx, wy))
            self.dx = 5
            self.dy = 5
            self.mbar = tk.Menu(self)
            self.master.config(menu=self.mbar)
            self.ddmenu = tk.Menu(self, tearoff=0)
            self.mbar.add_cascade(label='A Drop Down Menu', menu=self.ddmenu)
            self.ddmenu.add_command(label='Drop Down Entry 1', command=lambda: self.hello('Drop Down Menu!'))
            self.a_label = tk.Label(master, text='A Label')
            self.a_label.grid(column=0, row=0, padx=self.dx, pady=self.dy)
            self.a_button = tk.Button(master, text='A Button', command=lambda: self.hello('The Button!'))
            self.a_button.grid(column=0, row=1, padx=self.dx, pady=self.dy)
            self.an_entry = tk.Entry(master, width=20)
            self.an_entry.grid(column=0, row=2, padx=self.dx, pady=self.dy)
            self.cbox = ttk.Combobox(master, width=20)
            self.cbox.grid(column=0, row=3, padx=self.dx, pady=self.dy)
            self.cbox['state'] = 'readonly'
            self.cbox['values'] = ['Combobox Entry 1', 'Combobox Entry 2', 'Combobox Entry ...']
            self.cbox.set('Combobox Entry 1')
            self.cbox_selection = self.cbox.get()
            self.scrlbar = tk.Scrollbar(master, orient=tk.VERTICAL)
            self.scrlbar.grid(sticky=tk.W, column=1, row=4, padx=self.dx, pady=self.dy)
            self.lbox = tk.Listbox(master, height=3, width=20, yscrollcommand=self.scrlbar.set)
            for e in ['Listbox Entry 1', 'Listbox Entry 2', 'With Scrollbar ->', 'lb entry n']:
                self.lbox.insert(tk.END, e)
            self.lbox.grid(sticky=tk.E, column=0, row=4, padx=self.dx, pady=self.dy)
            self.scrlbar.config(command=self.lbox.yview)
            self.lbox_selection = self.lbox.get(0)
            self.check_variable = tk.BooleanVar()
            self.cbutton = tk.Checkbutton(master, text='Tick this Checkbutton', variable=self.check_variable)
            self.cbutton.grid(sticky=tk.E, column=2, row=0, padx=self.dx, pady=self.dy)
            logo = tk.PhotoImage(file='gui/sunny-image.gif')
            logo = logo.subsample(2, 2)
            self.l_img = tk.Label(master, image=logo)
            self.l_img.image = logo
            self.l_img.grid(row=1, column=2, rowspan=4)
            tk.Label(text='                                                    ').grid(row=0, column=1)

        @staticmethod
        def hello(message):
            showinfo('Got Message from ...', message)
    if __name__ == '__main__':
        _MyApp().mainloop()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    As usual in *Python*, there are many more options (widgets) available and the [TkDocs](https://tkdocs.com/) offers a detailed, modern overview of available `tkinter` objects.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## `tkinter` Variables

    In the above example, the checkbox receives a `tk.BooleanVar()`, which takes a `True` value when a user checks the checkbox. There are more variables that can be associated with `tkinter` widgets (e.g., `tk.Entry`, `tk.Listbox`, or `ttk.Combobox`). `tkinter` variables correspond basically to [Python data types](https://hydro-informatics.com/jupyter/pybase.html#var) with special methods that are required to set or retrieve (get) user-defined values of these data types. Here is an overview of `tkinter` variables:

    * `tk.BooleanVar()` is a *boolean* that can be `True` or `False`
    * `tk.DoubleVar()` is a numeric floating point (*float*) variable
    * `tk.IntVar()` is a numeric *integer* variable
    * `tk.StringVar()` is a *string* (i.e., typically some text)

    How does Python know when to retrieve a user-defined value? Typically, we want to evaluate user-defined values when we call a function that receives user-defined values as input arguments. Default, predefined default values in a script can be set with `VARIABLE.set()` and the user settings can be retrieved with `VARIABLE.get()`. The following [script](https://raw.githubusercontent.com/hydro-informatics/jupyter-python-course/main/gui/variable_gui.py) and the [icon](https://raw.githubusercontent.com/hydro-informatics/jupyter-python-course/main/gui/sample-icon.ico) are available at the course repository.
    """)
    return


@app.cell
def _(showinfo, tk):
    import random

    class _MyApp(tk.Frame):

        def __init__(self, master=None):
            tk.Frame.__init__(self, master)
            self.master.title('GUI with variables')
            self.master.iconbitmap('gui/sample-icon.ico')
            ww = 628
            wh = 100
            wx = (self.master.winfo_screenwidth() - ww) / 2
            wy = (self.master.winfo_screenheight() - wh) / 2
            self.master.geometry('%dx%d+%d+%d' % (ww, wh, wx, wy))
            self.a_label = tk.Label(master, text='Enter a value to call:')
            self.a_label.grid(column=0, row=0, padx=5, pady=5)
            self.user_entry = tk.StringVar()
            self.an_entry = tk.Entry(master, width=20, textvariable=self.user_entry)
            self.an_entry.grid(column=1, row=0, padx=5, pady=5)
            self.a_button = tk.Button(master, text='Call Message!', command=lambda: self.message_distributor())
            self.a_button.grid(column=2, row=0, padx=5, pady=5)
            self.check_variable = tk.BooleanVar()
            self.cbutton = tk.Checkbutton(master, text='Check this box to use a random message instead of the entry', variable=self.check_variable)
            self.cbutton.grid(sticky=tk.E, column=0, columnspan=3, row=1, padx=5, pady=5)
            self.check_variable.set(False)

        def message_distributor(self):
            if not self.check_variable.get():
                showinfo('User message', self.user_entry.get())
            else:
                showinfo('Random message', self.random_message())

        def random_message(self):
            random_words = ['summer', 'winter', 'is', 'cold', 'hot', 'will be']
            return ' '.join(random.sample(random_words, 3))
    if __name__ == '__main__':
        _MyApp().mainloop()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![img](https://hydro-informatics.com/_images/py-tk-variables.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Design, Place and Modify Widgets

    The above code examples use both the `OBJECT.grid()` and the `OBJECT.pack()` methods (geometry managers) to place widgets in the GUI. There is an additional geometry manager in the form of the `place` method. The choice of a convenient geometry manager depends on your preferences and there are pros and cons for the three geometry managers:

    * `pack`
        - automatically places widgets within a box
        - works best for simple GUIs, where all widgets are in one column or row
        - complex layouts can only be handled with complicated workarounds (tip: do not try)
    * `place`
        - places widgets at absolute or relative *x*-*y* positions
        - works well for graphical arrangements of widgets
    * `grid`
        - places widgets in columns and rows of a grid
        - works well with table-like apps and structured layouts

    To enable more graphical flexibility, widgets accept many optional keywords to change their foreground (`fg`) or background (`bg`) color. In addition, widgets can be modified with the `tk.OBJECT.config(PARAMETER_TO_CONFIGURE=NEW_CONFIG)` method.

    The following sections provide more details on the `place` and `grid` geometry managers (the relevant functions of `pack` are already above shown: `pack()` -  that is all) and illustrate keyword arguments along with widget methods to modify widgets.

    ### Place with `place` and Use Object Colors

    The simplest geometry manager is the `pack` method, which works even without any keyword provided (see the very first examples in this section). With the `pack` method, widgets can be placed relatively in the window (`relx` and `rely`, where both must be < 1) or with absolute positions (`x` and `y`, where both should fit into the window dimensions defined through `self.config(width=INT, height=INT)`). The axis origin (zero positions of *x* and *y*) is determined with the `anchor` keyword.
    """)
    return


@app.cell
def _(tk):
    class PlacedApp(tk.Frame):
        def __init__(self, master=None, **options):
            tk.Frame.__init__(self, master, **options)
            self.pack(expand=True, fill=tk.BOTH)
            self.config(width=628, height=100)
            self.master.title("A placed GUI")
            tk.Label(self, text="Vanilla", bg="goldenrod", fg="dark slate gray").place(anchor=tk.NW, relx=0.2, y=10)
            tk.Label(self, text="Green green tree", bg="OliveDrab1").place(anchor=tk.E, relx=0.8, rely=0.5)
            tk.Label(self, text="Blue sky", bg="DeepSkyBlue4", fg="floral white").place(anchor=tk.CENTER, x=300, rely=0.8)


    if __name__ == '__main__':
        PlacedApp().mainloop()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![img](https://hydro-informatics.com/_images/py-tk-placed.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Note:** The above example does not create class objects of `tk.Labels`, which makes the labels non-modifiable. This definition of widgets is acceptable to shorten the often long GUI scripts, but only if the widgets should not be modified later.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Place Objects with `grid`
    In `grid`-ed GUIs, the widget alignment can be controlled with the `sticky` argument that uses cardinal directions (e.g., `sticky=tk.W` aligns or "sticks" a widget at the west, meaning, left side, of a GUI). The `padx` and `pady` keywords arguments enable the implementation of pixel space around widgets.
    """)
    return


@app.cell
def _(showinfo, tk):
    class GriddedApp(tk.Frame):

        def __init__(self, master=None, **options):
            tk.Frame.__init__(self, master, **options)
            self.pack(expand=True, fill=tk.BOTH)
            self.config(width=628, height=100)
            self.master.title('A grid GUI')
            tk.Label(self, text='Enter name: ', bg='bisque2', fg='gray21').grid(sticky=tk.W, row=0, column=0, padx=10)
            tk.Entry(self, bg='gray76', width=20).grid(sticky=tk.EW, row=0, column=1, padx=5)
            tk.Button(self, text='Show message', bg='pale turquoise', fg='red4', command=lambda: showinfo('Info', 'Random message')).grid(row=0, column=2, padx=5)
            tk.Checkbutton(self, text='A Checkbutton over multiple columns').grid(sticky=tk.E, row=1, column=0, columnspan=3, pady=15)
    if __name__ == '__main__':
        GriddedApp().mainloop()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![img](https://hydro-informatics.com/_images/py-tk-grid.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Configure Widgets
    Upon user action (an event), we may want to modify previously defined widgets. For instance, we may want to change the text of a label or the layout of a button to indicate successful or failed operations. For this purpose, `tkinter` objects can be modified with `tk.OBJECT.config(PARAMETER_TO_CONFIGURE=NEW_CONFIG)`. Moreover, objects can be deleted (destroyed) with `tk.OBJECT.destroy()`, even though this is not an elegant method for any other widgets than pop-up windows (child frames of the master frame).
    """)
    return


@app.cell
def _(showinfo, tk):
    from tkinter.messagebox import showerror

    class ReConfigApp(tk.Frame):

        def __init__(self, master=None, **options):
            tk.Frame.__init__(self, master, **options)
            self.config(width=628, height=100)
            self.pack()
            self.user_depth = tk.DoubleVar()
            self.kst = 40.0
            self.w = 5.0
            self.slope = 0.002
            self.master.title('A GUI that reconfigures its widgets')
            tk.Label(self, text='Enter water depth (numeric, in meters): ', bg='powder blue', fg='medium blue').grid(sticky=tk.W, row=0, column=0, padx=10)
            tk.Entry(self, bg='alice blue', width=20, textvariable=self.user_depth).grid(sticky=tk.EW, row=0, column=1, padx=5)
            self.eval_button = tk.Button(self, text='Estimate flow velocity', bg='snow2', fg='dark violet', command=lambda: self.call_estimator())
            self.eval_button.grid(row=0, column=2, padx=5)

        def call_estimator(self):
            try:
                flow_depth = float(self.user_depth.get())
            except tk.TclError:
                return showerror('ERROR', 'Non-numeric value entered.')
            self.eval_button.config(fg='green4', bg='DarkSeaGreen1')
            showinfo('Result', 'The estimated flow velocity is: ' + str(self.estimate_u(flow_depth)))

        def estimate_u(self, h):
            try:
                return self.kst * h ** (2 / 3) * self.slope ** 0.5
            except ValueError:
                showerror('ERROR: Bad values defined.')
                return None
            except TypeError:
                showerror('ERROR: Bad data types defined.')
                return None
    if __name__ == '__main__':
        ReConfigApp().mainloop()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![img](https://hydro-informatics.com/_images/py-tk-config.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ***

    > **Challenges:**
    > 1. The roughness value varies as a function of surface characteristics. Can you implement a `ttk.Combobox` to let a user choose a Strickler *k<sub>st</sub>* roughness value between 10 and 85 (integers) and define the channel slope in a `tk.Entry` or a custom pop-up window (see below)?
    > 2. The cross-section averaged flow velocity also depends on the cross-section geometry. Can you implement `tkinter` widgets to enable the definition of a bank slope `m` and channel base width `w` for calculating the hydraulic radius?

    ![img](https://hydro-informatics.com/_images/lowVariables_xs.png)

    ***
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Pop-up Windows

    ### Default Messages from `tkinter.messagebox`

    The `tkinter.messagebox` library provides standard pop-up windows, such as:

    * `showinfo(title=STR, message=STR)` that prints an information message (see above examples).
    * `showwarning(title=STR, message=STR)` that prints a warning message.
    * `showerror(title=STR, message=STR)` that prints an error message (see above example).
    * `askyesno(title=STR, message=STR)` that returns `False` or `True` depending on a user's answers to a *Yes-or-No* question.
    * `askretrycancel(title=STR, message=STR)` that returns `False` or `True`, or re-attempts to run an event (function) depending on a user's answers to a *Yes-or-No-or-Cancel* question.
    * `askokcancel(title=STR, message=STR)` that returns `False` or `True` depending on a user's answers to an *OK* question.

    Read more about default pop-up windows in the [Python docs](https://docs.python.org/3/library/tkinter.messagebox.html).

    ### Top-level Custom Pop-ups
    The default windows may not meet the needs for every application, for instance, to invite users to enter a custom value. In this case, a `tk.Toplevel` object aids in producing a customized pop-up window, and the below example shows how a customized top-level pop-up window can be called within a method. With the `tk.Toplevel` widget and the `tk.Frame` (master) widgets, the code block produces two frames, in which buttons, labels, or any other `tkinter` object can be placed. The very first argument of any `tkinter` widget-object created determines whether the object is placed in the master or the top-level frame. For example, `tk.Entry(self).pack()` creates an entry in the master `tk.Frame`, and `tk.Entry(pop_up).pack()` creates an entry in the child `tk.Toplevel`.
    """)
    return


@app.cell
def _(tk):
    from tkinter.messagebox import showwarning

    class PopApp(tk.Frame):
        def __init__(self, master=None, **options):
            tk.Frame.__init__(self, master, **options)
            self.config(width=628, height=50)
            self.pack()
        
            self.master.title("Custom pop-up GUI")
            self.pop_button = tk.Button(self, text="Open pop-up window", bg="cadet blue", fg="white smoke", command=lambda: self.new_window())
            self.pop_button.pack()
        
        def destroy_buttons(self):
            self.pop_button.destroy()
            self.p_button1.destroy()
            self.p_button2.destroy()        
            showwarning("Congratulations", "This app is useless now. Don't press red-ish buttons ...")
        
        def new_window(self):
            pop_up = tk.Toplevel(master=self)
            # add two buttons to the new pop_up Toplevel object (window)
            self.p_button1 = tk.Button(pop_up, text="Destroy buttons (do not click here)", fg="DarkOrchid4",
                                       bg="HotPink1", command=lambda: self.destroy_buttons())
            self.p_button2 = tk.Button(pop_up, text="Close window", command=lambda: pop_up.quit())  
            self.p_button1.pack()
            self.p_button2.pack()


    if __name__ == '__main__':
        PopApp().mainloop()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![img](https://hydro-informatics.com/_images/py-tk-popup-custom.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### File Dialog (Open ...)
    When a custom function's argument is a file or file name, we most likely want the user to be able to select the file type needed. The [tkinter.filedialog](https://docs.python.org/3/library/dialog.html#module-tkinter.filedialog) library provides methods to let users choose general or specific file types. Specific file types can be defined with the `filetypes=("Name", "*.ending")` (or `filetypes=("Name", "*.ending1;*.ending2;...")` for multiple file types) keyword argument. The following example illustrates the usage of `tkinter.filedialog`'s `askopenfilename`.
    """)
    return


@app.cell
def _(showinfo, tk):
    from tkinter.filedialog import askopenfilename

    class OpenFileApp(tk.Frame):

        def __init__(self, master=None, **options):
            tk.Frame.__init__(self, master, **options)
            self.config(width=628, height=50)
            self.pack()
            self.master.title('GUI to open a file')
            self.pop_button = tk.Button(self, text='Open a text file', bg='light steel blue', fg='dark slate gray', command=lambda: self.open_file())
            self.pop_button.pack()

        def open_file(self):
            file_types = (('Text', '*.txt;*.csv;*.asc'),)
            file_name = askopenfilename(initialdir='.', title='Select a text file', filetypes=file_types, parent=self)
            showinfo('File info', 'You selected ' + str(file_name))  # equivalent to [("Text", "*.txt;*.csv;*.asc")]
    if __name__ == '__main__':
        OpenFileApp().mainloop()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![img](https://hydro-informatics.com/_images/py-tk-filedialog.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Quit
    To cleanly quit a GUI, use `tk.Frame.quit()` (i.e., in a custom class, write `self.quit()` or `master.quit()`). The above example of the `PopApp` class also features the `destroy()` method, which helps to remove particular widgets.

    `tkinter` provides many more options such as the implementation of tabs with `ttk.Notebook()` (requires [binding](https://docs.python.org/3/library/tkinter.html#bindings-and-events) of tab objects), tables (`from tkintertable import TableCanvas, TableModel`), or interactive graphic objects with [matplotib](https://hydro-informatics.com/jupyter/pyplot.html#matplotlib).

    ```python
    import matplotlib
    matplotlib.use('TkAgg')
    import numpy as np
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    ```

    Enjoy creating your custom apps!
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Exercise:** Get familiar with creating GUIs and object orientation in the [GUI exercise](https://hydro-informatics.com/jupyter/gui.html).
    """)
    return


if __name__ == "__main__":
    app.run()
