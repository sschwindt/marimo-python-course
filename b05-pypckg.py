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
    # Packages, Modules and Libraries

    Import external libraries and organize your code into functional chunks.

    > **Requirements:** Make sure to understand [Python functions](https://hydro-informatics.com/jupyter/pyfun.html).

    ## Import Packages or Modules

    Importing a module or package in Python makes the names defined or exposed by that module or package accessible in a script. These may include functions, classes, variables, and other objects. Importable code can come from different locations and formats: it may be part of Python itself, belong to the standard library, be located in a local project, or be provided by an installed third-party package. Third-party packages are commonly installed into the interpreter environment using package-management tools such as *conda* ([read more about conda-installing](https://hydro-informatics.com/pyinstall#install-pckg)) or *pip* ([read more about pip-installing](https://hydro-informatics.com/pyinstall#pip-install-pckg))

    Modules from Python's standard library (e.g., `os`) and built-in modules (e.g., `sys`) are normally available without installing additional packages. Other modules and packages may need to be installed first.

    /// admonition | The Difference between a Module and a Package
        type: note

    A **module** is a single importable unit, commonly represented by a Python file such as `a_module.py` (e.g., `import a_module`). Modules can also be implemented in other ways, for example as built-in or compiled extension modules.

    A **package** organizes modules and potentially subpackages in a directory hierarchy, allowing imports such as `from a_package.module import a_function`. A package is itself importable and has a `__path__` attribute. Regular packages usually contain an `__init__.py` file, whereas *namespace packages* can exist without one.

    Sounds fuzzy? Read this section down to the bottom and come back here to re-read this note.
    ///
    The `os` module provides functions for interacting with the operating system, for example, for working with files, directories, paths, and environment variables. So let's import this essential module:
    """)
    return


@app.cell
def _():
    import os
    print(os.getcwd()) # print current working directory
    print(os.path.abspath('')) # print directory of script running
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Overview of Import Options

    Here is an overview of options to import packages or modules (hierarchical parts of packages):

    | Command | Description | Usage of attributes |
    |---------|-------------|---------------------|
    | `import package_name` | Import an original module | `package.item()` |
    | `import package_name as nickname` | Import module and rename (alias) it in the script |  `nickname.item()` |
    | `from package-name import item` | Import only a function, class or other items |  `item()` |
    | `from package-name import *` | Import all items |  `item()` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Example
    """)
    return


@app.cell
def _():
    import matplotlib.pyplot as plt # import the pyplot module of the matplotlib package and alias it with plt

    x = []
    y = []

    for e in range(1, 10):
        x.append(e)
        y.append(e**2)

    plt.plot(x, y)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### What is the best way to import a package or module?
    There is no global answer to this question. However, be aware that `from package-name import *` shadows any existing variable or other items in the script. Thus, only use `*` when you are aware of all contents of a module or package. This is also why [PEP 8](https://peps.python.org/pep-0008/) discourages wildcard imports and recommends placing all imports at the top of a script. The import statement in the middle of the following example is for demonstration purposes only:
    """)
    return


@app.cell
def _():
    pi = 9.112  # define a float called pi
    print(f'Pi is not {pi:.3f}.')
    from math import pi
    print(f'Pi is {pi:.3f}.')  # this overwrites the previously defined variable pi
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Tip:** Define default import packages for *JupyterLab*'s *IPython* kernel (read more on the [*Python* installation page](https://hydro-informatics.com/python-basics/pyinstall.html#ipython-config)).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### What items (attributes, classes, functions) are in a module?
    Sometimes we want to explore modules or to check variable attributes. This is achieved with the `dir()` command:
    """)
    return


@app.cell
def _():
    import sys
    print(sys.path)
    print(dir(sys))

    a_string = "zabaglione"
    print(", ".join(dir(a_string.split("gl"))))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Create a new Module

    In object-oriented programming and code factorization, writing custom, new modules is an essential task. To write a new module, first, create a new script. Then, open the new script and add some parameters and functions.
    """)
    return


@app.cell
def _():
    # icecreamdialogue.py
    _flavors = ['vanilla', 'chocolate', 'bread']
    _price_scoops = {1: 'two euros', 2: 'three euros', 3: 'your health'}
    _welcome_msg = f'Hi, I only have {_flavors[0]}. How many scoops do you want?'
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    [`icecreamdialogue.py`](https://github.com/hydro-informatics/icecream/raw/master/single-scripts/icecreamdialogue.py) can now either be executed as a script (nothing will happen visibly) or imported as a module to access its variables (e.g., `icecreamdialogue.flavors`):
    """)
    return


@app.cell
def _():
    import icecreamdialogue as icd
    print(icd.welcome_msg)
    _scoops_wanted = 2
    print(f'That makes {icd.price_scoops[_scoops_wanted]} please')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Make Script Stand-alone

    As an alternative, we can append the call to items in [`icecreamdialogue.py`](https://github.com/hydro-informatics/icecream/raw/master/single-scripts/icecreamdialogue.py) in the script and run it as a stand-alone script by adding an `if __name__ == "__main__":` block:
    """)
    return


@app.cell
def _():
    # icecreamdialogue_standalone.py
    _flavors = ['vanilla', 'chocolate', 'bread']
    _price_scoops = {1: 'two euros', 2: 'three euros', 3: 'your health'}
    _welcome_msg = f'Hi, I only have {_flavors[0]}. How many scoops do you want?'
    if __name__ == '__main__':
        print(_welcome_msg)
        _scoops_wanted = 2
        print(f'That makes {_price_scoops[_scoops_wanted]} please')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now we can run [`icecreamdialogue_standalone.py`](https://github.com/hydro-informatics/icecream/raw/master/single-scripts/icecreamdialogue_standalone.py) in a terminal (e.g., Linux Terminal, *PyCharm*'s *Terminal* tab at the bottom of the window, or VS Code's integrated terminal).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ***
    ```
    C:\temp\ python icecreamdialogue_standalone.py
    ```
    ***
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Note:** Depending on the definition of system variables used in the *Terminal* environment, Python must be called with a different variable name than `python` (e.g., `python3` on some Linux platforms).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Standalone Scripts with Input Parameters

    To make the script more flexible, we can define, for instance, `scoops_wanted` as an input variable of a function.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```python
    # icecreamdialogue_standalone_withinput.py
    import sys # sys provides access to command line arguments

    flavors = ["vanilla", "chocolate", "bread"]
    price_scoops = {1: "two euros", 2: "three euros", 3: "your health"}
    welcome_msg = f"Hi, I only have {flavors[0]}. How many scoops do you want?"

    def dialogue(scoops_wanted): # formerly in the __main__ statement
        print(welcome_msg)
        print(f"That makes {price_scoops[scoops_wanted]} please")

    if __name__ == "__main__":
        if len(sys.argv) > 1: # make sure input is provided
            # if true: call the dialogue function with the input argument
            dialogue(int(sys.argv[1]))
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now, we can run `icecreamdialogue_standalone_withinput.py` in a terminal:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ***
    ```
    C:\temp\ python icecreamdialogue_standalone_withinput.py 2
    ```
    ***
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Initialization of a Package (Hierarchically Organized Module)

    Good practice involves module cohesion and maintainability. Consequently, a package will most likely consist of multiple scripts that are stored in one folder and one core script serves for the initiation of the scripts. This core script is called `__init__.py` and Python will look for this script name in a package folder. Namespace packages may omit `__init__.py`. Example structure of a package called `icecreamery`:

    * `icecreamery` (folder name)
      - `__init__.py`   - optional package initiation *Python* script
      - `icecreamdialogue.py`  - dialogue producing *Python* script
      - `icecream_maker.py`   - virtual ice cream producing *Python* script

    To automatically invoke the two relevant scripts (sub-modules) of the `icecreamery` package, the `__init__.py` needs to include the following:
    """)
    return


@app.cell
def _():
    # __init__.py
    print(f'Invoking __init__.py for {__name__}')  # only for demonstration - keep __init__.py silent in production packages
    import icecreamery.icecreamdialogue, icecreamery.icecream_maker

    return (icecreamery,)


@app.cell
def _(icecreamery):
    # example usage of the icecreamery package
    print(icecreamery.icecreamdialogue.welcome_msg)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Do you remember the `dir()` function? Applied to a package (e.g., `dir(icecreamery)`), it lists the items that are currently defined in the package namespace. However, to control which sub-modules a wildcard import (`from icecreamery import *`) loads, define an `__all__` list in the `__init__.py`:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```python
    # __init__.py with __all__ list
    __all__ = ['icecreamdialogue', 'icecream_maker']
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The full example of the `icecreamery_all` package is also available in an [icecream](https://github.com/hydro-informatics/icecream) repository.
    """)
    return


@app.cell
def _():
    # example usage of the icecreamery package
    from icecreamery_all import icecreamdialogue
    print(icecreamdialogue.welcome_msg)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Package Creation Summary

    The structure of a module can be more complex than the above example list (e.g., with sub-folders). When you write a package, consider using [meaningful script and variable names](https://hydro-informatics.com/python-basics/pystyle.html#libs), along with appropriate documentation.

    > **Try logging:** implement a custom [logger](https://hydro-informatics.com/python-basics/pyerror.html#logging) in your module with `logger = logging.getLogger(__name__)` (replace `__name__` with for example `my-module-log`).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Reload (Re-import) a Package or Module

    Since Python 3, reloading a module requires importing the `importlib` module first. Reloading only makes sense if you are actively writing a new module. To reload a module, type:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```python
    import importlib
    importlib.reload(my_module)
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Tip:** In JupyterLab (IPython), the two magic commands `%load_ext autoreload` and `%autoreload 2` automatically reload all modified modules before every cell execution, which makes manual `importlib.reload()` calls unnecessary during active module development.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Package Development & PyPI (pip) Deployment

    The `icecreamery` example shows how a package works internally. To make a package installable for anyone through `pip install icecreamery`, it needs to be deployed to [PyPI](https://pypi.org/), the Python Package Index that *pip* queries in the background ([read more about pip-installing](https://hydro-informatics.com/python-basics/pyinstall.html#pip-install-pckg)). This section first summarizes the deployment workflow, including automation with GitHub workflows and documentation on Read the Docs, and then explains good practice for developing a package collaboratively.

    ### From Local Code to a pip-installable Package

    Modern Python packaging is driven by a single `pyproject.toml` file, which replaces the formerly used `setup.py` (see [PEP 621](https://peps.python.org/pep-0621/)). A deployment-ready repository resembles the following structure, which is known as the *src layout*:

    ```
    icecreamery/                  (repository root)
        src/
            icecreamery/          (the package itself)
                __init__.py
                icecreamdialogue.py
                icecream_maker.py
        tests/                    (automated tests, e.g., for pytest)
        docs/                     (documentation source, e.g., for Sphinx)
        examples/                 (functional usage examples)
        pyproject.toml            (package metadata and build configuration)
        README.md
        LICENSE
    ```

    The `pyproject.toml` file defines how *pip* (or any other installer) builds and installs the package:

    ```toml
    [build-system]
    requires = ["setuptools>=77"]
    build-backend = "setuptools.build_meta"

    [project]
    name = "icecreamery"
    version = "0.1.0"
    description = "Virtual ice cream sales dialogues"
    readme = "README.md"
    license = "BSD-3-Clause"
    requires-python = ">=3.10"
    dependencies = [
        "matplotlib",
        "numpy",
    ]
    ```

    While developing, install the package in **editable mode** into the active environment:

    ```
    pip install -e .
    ```

    The `-e` (editable) flag makes Python import the package directly from the local development clone instead of a static copy in the *site-packages* folder, so code modifications take effect immediately without re-installing.

    To deploy a release on PyPI manually:

    1. Register (for free) at [pypi.org](https://pypi.org/) and, for rehearsing uploads, at [test.pypi.org](https://test.pypi.org/).
    1. Build the distribution archives (a source archive and a wheel) with `python -m build` (install the builder once with `pip install build`). The archives land in a new `dist/` folder.
    1. Upload the archives with [twine](https://twine.readthedocs.io/): `python -m twine upload dist/*`. Best practice: rehearse the upload with `python -m twine upload --repository testpypi dist/*` first.

    Done. From now on, everyone can `pip install icecreamery`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Automate Testing and Deployment with GitHub Workflows

    Manually building and uploading every release is error-prone. [GitHub Actions](https://docs.github.com/en/actions) automate such recurring jobs with so-called workflows, which are YAML files stored in the `.github/workflows/` folder of a repository. Two workflows are particularly useful for package development:

    * A **test (continuous integration) workflow** that runs the test suite (e.g., with [pytest](https://docs.pytest.org/)) for every push and pull request, ideally on multiple Python versions and operating systems. Thus, broken code is flagged before it is merged into `main` (recall the [Collaboration & Branches](https://hydro-informatics.com/get-started/git.html#collaboration) section).
    * A **publish workflow** that builds and uploads the package to PyPI whenever a new release (version tag) is published on GitHub.

    Best practice for the publish workflow is PyPI's [Trusted Publishing](https://docs.pypi.org/trusted-publishers/), which links the GitHub repository directly to the PyPI project (a one-time setup in the PyPI account settings), so that no API tokens need to be stored in the repository secrets:

    ```yaml
    # .github/workflows/publish.yml
    name: Publish to PyPI

    on:
      release:
        types: [published]

    jobs:
      publish:
        runs-on: ubuntu-latest
        environment: pypi
        permissions:
          id-token: write   # required for PyPI Trusted Publishing
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with:
              python-version: "3.12"
          - name: Build distribution archives
            run: |
              python -m pip install build
              python -m build
          - name: Upload to PyPI
            uses: pypa/gh-action-pypi-publish@release/v1
    ```

    With this workflow in place, publishing a new version reduces to increasing the version number in `pyproject.toml` and clicking on **Draft a new release** (with a tag such as `v0.1.1`) on GitHub.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Documentation on Read the Docs (Free Plan)

    A pip-installable package without documentation will hardly be used by anyone. The de-facto standard for hosting Python package documentation is [Read the Docs](https://about.readthedocs.com/), which builds and hosts documentation of public (open-source) repositories for free at `PACKAGE-NAME.readthedocs.io` (the free plan shows small ads). The workflow:

    1. Write consistent docstrings (e.g., in [numpy](https://numpydoc.readthedocs.io/en/latest/format.html) or [Google](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) style) for all modules, classes, and functions, so that documentation generators can render the API reference automatically.
    1. Create a `docs/` folder with a [Sphinx](https://www.sphinx-doc.org/) project (`sphinx-quickstart`) and enable the `sphinx.ext.autodoc` and `sphinx.ext.napoleon` extensions in `docs/conf.py` to pull the docstrings into the documentation. [MkDocs](https://www.mkdocs.org/) with the *mkdocstrings* plugin is a popular alternative.
    1. Add a `.readthedocs.yaml` configuration file (required by Read the Docs) to the repository root:

    ```yaml
    # .readthedocs.yaml
    version: 2

    build:
      os: ubuntu-24.04
      tools:
        python: "3.12"

    sphinx:
      configuration: docs/conf.py

    python:
      install:
        - method: pip
          path: .
        - requirements: docs/requirements.txt
    ```

    4. Sign in at [readthedocs.org](https://readthedocs.org/) with a GitHub account and import the repository. Read the Docs installs a webhook, so every push to `main` triggers an automatic rebuild of the documentation, and every release tag can be published as a version-specific documentation build.

    Done. The documentation now updates itself with every push.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Collaborative Package Development

    As soon as several developers (e.g., a research group) push code to the same package repository, working on [dedicated branches with pull requests](https://hydro-informatics.com/get-started/git.html#collaboration) is only half of the story. The following good practice rules keep a growing package maintainable (this list stems from painful experience with real-world research code):

    **Strictly follow [PEP 8](https://peps.python.org/pep-0008/):**

    * *Naming conventions*: make sure that all script (module) filenames and variable names follow good practice, that is, short, `lowercase_with_underscores` names for modules, functions, and variables, `CamelCase` for classes, and `UPPERCASE` for constants (recall [meaningful script and variable names](https://hydro-informatics.com/python-basics/pystyle.html#libs)).
    * *Module shadowing*: never name an internal script or folder after an installed library or module (e.g., `math.py`, `numpy.py`, or a folder called `matplotlib/`). Because Python searches the script's own directory before the *site-packages* folder, the local file gets imported instead of the intended library, which leads to seemingly inexplicable import failures. Overly generic names, such as `plots.py` or `plots/`, are risky for the same reason: they easily collide with third-party modules and get confused with plotting libraries like `matplotlib.pyplot`.
    * *Docstrings*: equip every module and every function with a docstring, so that collaborators (and documentation generators, see above) understand what the code does without reverse-engineering it.
    * *File length and code redundancy*: a modular package structure means that scripts should remain concise. For context, we once had to refactor a plotting script that had grown to more than 3500 lines, partly because of copy-pasted (redundant) code blocks. Break large files down into logical sub-modules and strictly follow the DRY (Don't Repeat Yourself) principle.

    **Use dedicated folders for examples and templates** to keep the core package (i.e., the `src/` directory) clean:

    * `dev-examples/`: ongoing research or development cases (e.g., `dev-examples/cylinder-flume-telemac/`). Configure the repository to block large files (e.g., anything above 20 MB), because large simulation outputs do not belong in a *git* repository and should be backed up separately.
    * `examples/`: finalized, cleaned-up, and functional examples, along with README information on how to run them.
    * `templates/`: generalized versions of the example scripts that use keyword arguments instead of hardcoded paths.

    **Maintain strict top-level cleanliness**: do not add or move files directly into the repository root or the package source directory. For instance, keep environment activation scripts in a dedicated folder (e.g., `env-scripts/`) and invoke them from your local environment or example directories as needed.

    **Stay synchronized with `main`**: pull the latest `main` branch regularly and always before creating a new branch. In addition, install the package from the local development clone in editable mode (`pip install -e .`) instead of manipulating relative imports or `sys.path` so that example scripts import your latest local code rather than a globally installed *site-packages* copy. AI assistants (e.g., *Claude Code* or *Codex*) can help to robustly refactor legacy scripts with broken imports, but review their modifications as critically as any other pull request.
    """)
    return


if __name__ == "__main__":
    app.run()
