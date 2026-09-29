"""Export the marimo notebooks as WebAssembly (browser) pages for GitHub Pages.

marimo bundles local packages (e.g., fun/) as wheels in public/wheels/, but
every export empties that folder. This script exports each notebook into its
own temporary directory and merges the pages, assets, and wheels into the
repository root.

    python tools/export_wasm.py marimo
"""
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

MARIMO = sys.argv[1] if len(sys.argv) > 1 else "marimo"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WHEELS = os.path.join(ROOT, "public", "wheels")
# notebooks that cannot run in Pyodide (tkinter, arcpy, GDAL)
SKIP = {"b11-gui", "geo-arcpy", "geo01-shp", "geo02-raster", "geo03-convert"}
WHEEL_REF = re.compile(r"wheels/([^\"'\\]+?\.whl)")


def is_notebook(path):
    with open(path, encoding="utf-8") as f:
        return "app = marimo.App(" in f.read()


notebooks = sorted(
    os.path.splitext(os.path.basename(p))[0]
    for p in glob.glob(os.path.join(ROOT, "*.py"))
    if is_notebook(p) and os.path.splitext(os.path.basename(p))[0] not in SKIP
)
os.makedirs(WHEELS, exist_ok=True)
used_wheels = set()
with tempfile.TemporaryDirectory() as tmp:
    for i, name in enumerate(notebooks):
        out_dir = os.path.join(tmp, name)
        subprocess.run([MARIMO, "export", "html-wasm", os.path.join(ROOT, name + ".py"),
                        "-o", os.path.join(out_dir, name + ".wasm.html"), "--mode", "edit", "-f"],
                       check=True, stdout=subprocess.DEVNULL)
        shutil.copy(os.path.join(out_dir, name + ".wasm.html"), ROOT)
        if i == 0:  # assets/ is identical for all exports of one marimo version
            shutil.rmtree(os.path.join(ROOT, "assets"), ignore_errors=True)
            shutil.copytree(os.path.join(out_dir, "assets"), os.path.join(ROOT, "assets"))
        for wheel in glob.glob(os.path.join(out_dir, "public", "wheels", "*.whl")):
            shutil.copy(wheel, WHEELS)
        with open(os.path.join(ROOT, name + ".wasm.html"), encoding="utf-8") as f:
            refs = {r.replace("%2B", "+") for r in WHEEL_REF.findall(f.read())}
        used_wheels |= refs
        print(f"{name:45s} exported" + (f" (wheels: {', '.join(sorted(refs))})" if refs else ""))

for wheel in glob.glob(os.path.join(WHEELS, "*.whl")):
    if os.path.basename(wheel) not in used_wheels:
        os.remove(wheel)
        print(f"removed stale wheel {os.path.basename(wheel)}")
missing = [w for w in used_wheels if not os.path.isfile(os.path.join(WHEELS, w))]
if missing:
    sys.exit(f"ERROR: wheels referenced but missing in public/wheels/: {missing}")
print(f"{len(notebooks)} notebooks exported; commit public/wheels/ along with the pages")
