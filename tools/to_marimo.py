"""Convert jupyter-python-course notebooks into marimo notebooks.

Markdown is adapted to what marimo renders: MyST admonitions become
marimo `/// admonition` blocks, and links that only resolve inside the
Jupyter Book point to hydro-informatics.com.
"""
import glob
import json
import os
import re
import subprocess
import sys
import tempfile

SRC, DST, MARIMO = sys.argv[1], sys.argv[2], sys.argv[3]
SITE = "https://hydro-informatics.com"

LINKS = {
    "](#licenses)": f"]({SITE}/geo-arcpy#licenses)",
    "](arcpy-errors)": f"]({SITE}/geo-arcpy#arcpy-errors)",
    "](geo-raster.html#zonal)": f"]({SITE}/geo-raster#zonal)",
    "hhttps://": "https://",
}

# Code patches for constructs marimo rejects (star imports, shell lines,
# imports placed after their first use): notebook -> [(old, new), ...]
CODE_PATCHES = {
    "b05-pypckg": [("from icecreamery_all import *", "from icecreamery_all import icecreamdialogue")],
    "b07-pyplot": [
        ("pip install cmocean", "# run in a terminal (not in the notebook): pip install cmocean"),
        # pyo.init_notebook_mode() and pyo.iplot() only work in IPython;
        # marimo displays the last expression of a cell
        ("pyo.init_notebook_mode() \n", ""),
        ("pyo.init_notebook_mode()  # activate to create local function script\n", ""),
        ("pyo.init_notebook_mode()  # only necessary in jupyter\n", ""),
        ("fig.show()\npyo.iplot(fig, filename='population')", "fig  # marimo displays the last expression"),
        ("fig.show()\n\n\n# In local IDE use fig.show() - use iplot(fig) to procude local script for running figure functions\n"
         "#fig.show(filename='basic-line2', include_plotlyjs=False, output_type='div')\n"
         "pyo.iplot(fig, filename='temperature-evolution')", "fig  # marimo displays the last expression"),
        ('fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})\nfig.show()',
         'fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})\nfig'),
    ],
    "geo-arcpy": [("from arcpy.sa import *",
                   "from arcpy.sa import CellStatistics, Con, Float, Int, IsNull, SquareRoot")],
    "geo03-convert": [("from flusstools.geotools import *",
                       "from flusstools.geotools import create_raster, offset2coords, open_raster")],
    "geo02-raster": [("from osgeo import osr\n", "import numpy as np\nfrom osgeo import osr\n"),
                     ("import numpy as np\n# set the name of the output GeoTIFF raster",
                      "# set the name of the output GeoTIFF raster")],
    # WebAssembly export: fun/ is bundled as a wheel without the csv
    "bedload-exercise": [(
        "ch.lire_hecras()",
        "if sys.platform == \"emscripten\" and not ch.HECRAS.exists():  "
        "# version WebAssembly (navigateur) : télécharge les données\n"
        "    from pyodide.http import pyfetch as _pyfetch\n"
        "    _response = await _pyfetch(\n"
        "        \"https://raw.githubusercontent.com/sschwindt/marimo-python-course/main/data/hecras-arbogne.csv\")\n"
        "    ch.HECRAS.write_bytes(await _response.bytes())\n"
        "ch.lire_hecras()")],
}

# WebAssembly export: data files that a notebook reads, downloaded from
# GitHub into the browser's virtual file system by a cell after the imports
REPO_RAW = "https://raw.githubusercontent.com/sschwindt/marimo-python-course/main/"
WASM_DATA = {
    "b06-pynum": ["data/pure-numbers.txt"],
    "b07-pyplot": ["data/example_flow_gauge.xlsx", "data/FlowDepth009.csv", "data/temperature_change.csv"],
    "b10-xml": ["data/river_struct.json"],
}
WASM_CELL = """# WebAssembly (browser) version only: download the course data files
import sys as _sys

if _sys.platform == "emscripten":
    import os as _os
    from pyodide.http import pyfetch as _pyfetch

    for _file in ({files}
    ):
        _os.makedirs(_os.path.dirname(_file), exist_ok=True)
        _response = await _pyfetch(
            "{repo}" + _file
        )
        with open(_file, "wb") as _local_file:
            _local_file.write(await _response.bytes())"""

# PEP 723 dependencies for the WebAssembly export: packages that only local
# modules import, and pure-Python packages that Pyodide does not ship
SCRIPT_DEPS = {
    "b06-pynum": ["marimo", "numpy", "openpyxl", "pandas"],
    "b07-pyplot": ["cmocean", "marimo", "matplotlib", "numpy", "openpyxl", "pandas", "plotly"],
    "b10-xml": ["marimo", "numpy", "openpyxl", "pandas"],
    "bedload-exercise": ["marimo", "matplotlib", "numpy", "pandas"],
}
MD_PATCHES = {
    "b07-pyplot": [("The following example uses `plotly.offline` to plot data in notebook mode "
                    "(`pyo.init_notebook_mode()`) and `pyo.iplot()` can be used to write plot functions "
                    "to a locally-living script for interactive plotting.",
                    "In marimo, a plotly figure is displayed when it is the last expression of a cell "
                    "(the Jupyter version of this notebook uses `pyo.init_notebook_mode()` and `pyo.iplot()` "
                    "instead, which only work in IPython).")],
    "geo-arcpy": [("where *Spatial Analyst* objects are imported using `*` to enable",
                   "where *Spatial Analyst* objects are imported by name (marimo does not allow `*` imports) to enable")],
}

ADMONITION = re.compile(r"^(`{3,})\s*\{admonition\}\s*(.*?)\n(.*?)^\1\s*$", re.S | re.M)


def myst_admonition(m):
    title, body = m.group(2).strip(), m.group(3)
    kind = "note"
    opt = re.match(r"\s*:class:\s*([^\n]*)\n", body)
    if opt:
        kind = opt.group(1).split(",")[0].strip() or kind
        body = body[opt.end():]
    return f"/// admonition | {title}\n    type: {kind}\n\n{body.strip()}\n///"


def fix_markdown(text):
    text = ADMONITION.sub(myst_admonition, text)
    for old, new in LINKS.items():
        text = text.replace(old, new)
    return text


for path in sorted(glob.glob(os.path.join(SRC, "*.ipynb"))):
    nb = json.load(open(path, encoding="utf-8"))
    name = os.path.splitext(os.path.basename(path))[0]
    applied = set()
    for cell in nb["cells"]:
        src = "".join(cell["source"])
        if cell["cell_type"] == "markdown":
            src = fix_markdown(src)
            patches = MD_PATCHES.get(name, [])
        else:
            cell["outputs"], cell["execution_count"] = [], None
            patches = CODE_PATCHES.get(name, [])
        for old, new in patches:
            if old in src:
                src = src.replace(old, new)
                applied.add(old)
        cell["source"] = src
    missing = [o for o, _ in CODE_PATCHES.get(name, []) + MD_PATCHES.get(name, []) if o not in applied]
    if missing:
        print(f"{name}: patch not applied: {missing}")
    if name in WASM_DATA:
        files = "".join(f'\n        "{f}",' for f in WASM_DATA[name])
        nb["cells"].insert(0, {"cell_type": "code", "metadata": {}, "outputs": [], "execution_count": None,
                               "source": WASM_CELL.format(files=files, repo=REPO_RAW)})
    with tempfile.TemporaryDirectory() as tmp:
        tmp_nb = os.path.join(tmp, name + ".ipynb")
        json.dump(nb, open(tmp_nb, "w", encoding="utf-8"), ensure_ascii=False)
        out = os.path.join(DST, name + ".py")
        subprocess.run([MARIMO, "convert", tmp_nb, "-o", out], check=True,
                       stdout=subprocess.DEVNULL)
    with open(out, encoding="utf-8") as f:
        code = f.read()
    code = code.replace("@app.cell\nasync def _():\n    # WebAssembly (browser) version only",
                        "@app.cell(hide_code=True)\nasync def _():\n    # WebAssembly (browser) version only")
    if name in SCRIPT_DEPS:
        deps = "".join(f'#     "{d}",\n' for d in SCRIPT_DEPS[name])
        code = f"# /// script\n# dependencies = [\n{deps}# ]\n# ///\n" + code
    with open(out, "w", encoding="utf-8") as f:
        f.write(code)
    check = subprocess.run([MARIMO, "check", out], capture_output=True, text=True)
    status = "ok" if check.returncode == 0 else "CHECK FAILED\n" + check.stdout + check.stderr
    print(f"{name:45s} {status}")
