# marimo-python-course

The Python course notebooks from [hydro-informatics.com](https://hydro-informatics.com) as [marimo](https://marimo.io) notebooks. marimo notebooks are plain Python files (`.py`) that run reactively: when you change a cell, every cell that depends on it re-runs automatically.

The notebooks are converted from the Jupyter versions in [jupyter-python-course](https://github.com/hydro-informatics/jupyter-python-course). The explanations and the full course live on [hydro-informatics.com](https://hydro-informatics.com).

## Run the notebooks

1. Clone this repository and change into it:

   ```
   git clone https://github.com/sschwindt/marimo-python-course.git
   cd marimo-python-course
   ```

2. Create and activate the conda environment (includes marimo and all course packages):

   ```
   conda env create -f environment.yml
   conda activate hy-marimo
   ```

   For the basic chapters (`b01` to `b05`, `b08`, `b09`), `pip install marimo` is enough.

3. Open a notebook **from the repository root**, so that relative paths such as `data/` and `geodata/` resolve:

   ```
   marimo edit b01-pybase.py
   ```

   `marimo edit` without a file name opens a browser page listing all notebooks.

## Notebooks

| Notebook | Chapter on hydro-informatics.com |
|----------|----------------------------------|
| `b01-pybase.py` | [Hello Data Types](https://hydro-informatics.com/pybase) |
| `b02-pyerror.py` | [Errors, Logging, and Debugging](https://hydro-informatics.com/pyerror) |
| `b03-pyloop.py` | [Loops and Conditional Statements](https://hydro-informatics.com/pyloop) |
| `b04-pyfun.py` | [Functions](https://hydro-informatics.com/pyfun) |
| `b05-pypckg.py` | [Packages, Modules and Libraries](https://hydro-informatics.com/pypckg) |
| `b06-pynum.py` | [Data Files, NumPy & Pandas](https://hydro-informatics.com/pynum) |
| `b07-pyplot.py` | [Plotting](https://hydro-informatics.com/pyplot) |
| `b08-pystyle.py` | [Code Style and Conventions](https://hydro-informatics.com/pystyle) |
| `b09-classes.py` | [Object Orientation and Classes](https://hydro-informatics.com/classes) |
| `b10-xml.py` | [Structured Data (XML, xlsx & JSON)](https://hydro-informatics.com/xml) |
| `b11-gui.py` | [Graphical User Interfaces](https://hydro-informatics.com/gui) |
| `geo01-shp.py` | [Shapefile (Vector) Handling](https://hydro-informatics.com/geo-shp) |
| `geo02-raster.py` | [Raster (Grid) Handling](https://hydro-informatics.com/geo-raster) |
| `geo03-convert.py` | [Vectorize and Rasterize](https://hydro-informatics.com/geo-convert) |
| `geo-arcpy.py` | [The Commercial arcpy Library](https://hydro-informatics.com/geo-arcpy) |
| `hydraulic-jump.py` | [Hydraulic Jump Design](https://hydro-informatics.com/hydraulic-jump) |
| `bedload-exercise.py` | [Bedload Exercise](https://hydro-informatics.com/bedload-exercise) |
| `schwimmstabilitaet.py` | [Stability of Floating Bodies](https://hydro-informatics.com/schwimmstabilitaet) |
| `rechenbeispiel-staustufendurchbildung.py` | [Hydraulic Design of a Barrage](https://hydro-informatics.com/rechenbeispiel-staustufendurchbildung) |
| `extra-svc.py` | Support vector classification (extra) |
| `show-case.py` | Minimal example |

## Differences from the Jupyter version

- marimo does not allow a variable to be defined in more than one cell. Variables that the Jupyter notebooks redefined in several cells carry a leading underscore (e.g., `_top`), which makes them local to their cell.
- marimo does not allow `from module import *`; those imports list the used names explicitly.
- Shell commands such as `pip install cmocean` belong in a terminal, not in a notebook cell.
- `b11-gui.py` opens desktop (tkinter) windows, and `geo-arcpy.py` needs the Python environment of ESRI's ArcGIS Pro with marimo installed into it.

## Updating from the Jupyter notebooks

`tools/to_marimo.py` regenerates all notebooks from a local clone of jupyter-python-course, including the fixes listed above (`CODE_PATCHES` and `MD_PATCHES`), and runs `marimo check` on each result:

```
python tools/to_marimo.py ../jupyter-python-course . marimo
```

Supporting folders (`data/`, `fun/`, `geodata/`, `gui/`) are copied separately.
