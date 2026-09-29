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
    ## Show case

    This is a markdown block.
    """)
    return


@app.cell
def _():
    # Python block

    a = 7.0
    b = 4.0

    print("Welcome to the Python lecture starting in November (month %i)." % int(a + b))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Next ...

    This is another markdown block.
    """)
    return


if __name__ == "__main__":
    app.run()
