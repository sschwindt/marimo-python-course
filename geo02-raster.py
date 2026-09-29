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
    # Raster (Grid) Handling

    This section introduces geospatial analysis of raster (gridded) data with `gdal` and `rasterstats`. Download sample raster datasets from [River Architect](https://github.com/RiverArchitect/riverarchitect/tree/main/sample-data). In particular, this section uses GeoTIFF rasters located in [`RiverArchitect/SampleData/01_Conditions/2100_sample/`](https://github.com/RiverArchitect/riverarchitect/tree/main/sample-data/01_Conditions/2100_sample).

    > **Requirements:**
    > * Make sure to understand [gridded raster data](https://hydro-informatics.com/geospatial-data#raster), in particular, the `.tif` ([`GeoTIFF`](https://hydro-informatics.com/glossary#term-GeoTIFF)) format
    > * Accomplish the [QGIS tutorial](https://hydro-informatics.com/use-qgis)

    > **Tips:**
    > * While OSGeo's `ogr` module is useful for shapefile handling, raster data are best handled by `gdal`.
    > * The functions featured in this section are partially also implemented in [flusstools](https://flusstools.readthedocs.io/).
    > * To use those functions, make sure flusstools is installed and import it as follows: `from flusstools import geotools`. Some of the functions shown in this tutorial can then be used with `geotools.function_name()`.

    ## Load raster

    ### Open Existing Raster Data

    Raster data can be opened in Python code as an instance of `gdal.Open("FILENAME")`. The following code block provides a function to open any raster specified with the `file_name` input argument. One of the most important elements when dealing with raster data is the raster band, which takes on a similar data carrier role as `GetLayer` in shapefile handling. To access the raster band, the below-shown `open_raster` function:

    1. Enables error and warning feedback with `gdal.UseExceptions()` (this step is vital when using gdal).
    1. Opens the provided raster `file_name` embraced by `try` - `except` statements to inform if and why a potential error occurred while opening the raster.
    1. Opens the raster band number stated in the optional `band_number` keyword argument with `raster_band = raster.GetRasterBand(band_number)` (the default value is `1`).
    1. Returns the raster and raster band objects.
    """)
    return


@app.cell
def _():
    from osgeo import gdal


    def open_raster(file_name, band_number=1):
        """
        Open a raster file and access its bands
        :param file_name: STR of a raster file directory and name
        :param band_number: INT of the raster band number to open (default: 1)
        :output: osgeo.gdal.Dataset, osgeo.gdal.Band objects
        """
        gdal.UseExceptions()
        # open raster file or return None if not accessible
        try:
            raster = gdal.Open(file_name)
        except RuntimeError as e:
            print("ERROR: Cannot open raster.")
            print(e)
            return None
        # open raster band or return None if corrupted
        try:
            raster_band = raster.GetRasterBand(band_number)
        except RuntimeError as e:
            print("ERROR: Cannot access raster band.")
            print(e)
            return None
        return raster, raster_band

    return gdal, open_raster


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Tip:** This function is available in flusstools. For instance, use it with `from flusstools import geotools` and `geotools.open_raster("path/to/raster.tif")`.

    To use the `open_raster` function, call it with a file name as shown in the following code block with the `h001000.tif` raster from the [*River Architect* sample data](https://github.com/RiverArchitect/SampleData/archive/master.zip). The script then releases both the band and dataset references to close the GeoTIFF.
    """)
    return


@app.cell
def _(open_raster):
    import os
    file_name = r"" + os.getcwd() + "/geodata/rasters/h001000.tif"
    src, depth = open_raster(file_name)
    print(src)
    print(depth)
    depth = None
    src = None
    return (os,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Raster Band Statistics and Toolbox Scripts

    Once the raster and its band are loaded with the above `open_raster` function, we can access statistical information (e.g., the minimum or the maximum), identify the *no-data* value (i.e., a pre-defined value that is assigned to pixels without value), or the type of units used.

    Python scripts for processing geospatial data can also be embedded as plugins in GIS desktop applications (e.g., as plugins in QGIS or Toolbox in ArcGIS Pro). To run a Python script in a GIS desktop application, it should be written as a standalone script that can receive input arguments. The interested reader can learn more about implementing plugins in QGIS in the [QGIS docs](https://docs.qgis.org/3.22/en/docs/pyqgis_developer_cookbook/plugins/index.html).

    > **Note:** QGIS wraps many external algorithm types, which are available through the **QGIS Processing Toolbox**. These algorithms belong, for example, to *SAGA* or *GRASS GIS*.

    Here we will only write the next code block so that it can be run in a console/terminal application as a standalone script (recall the [instructions for writing standalone script](https://hydro-informatics.com/jupyter/pypckg.html#standalone)).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```python
    import sys
    from osgeo import gdal

    # make sure to use exceptions
    gdal.UseExceptions()

    def how2use():
        # provide usage instructions for the script
        print(\"\"\"
        $ raster_band_info.py [ band number ] input-raster
        \"\"\")
        # exit program if wrong input arguments provided
        sys.exit(1)


    def get_color_bands(raster_band):
        \"\"\"
        :param raster_band: osgeo.gdal.Band object
        :output: list of color bands used in raster_band
        \"\"\"

        # get ColorTable and return False if None
        color_table = raster_band.GetColorTable()
        if color_table is None:
            print("Band has no ColorTable.")
            return None
        else:
            print("Found %i color definitions." % int(color_table.GetCount()))

        # iterate through color_table and append objects found to color_bands list
        color_bands = []
        for c in range(0, color_table.GetCount() ):
            entry = color_table.GetColorEntry(c)
            if not entry:
                continue
            color_bands.append(str(color_table.GetColorEntryAsRGB(c, entry)))
        return color_bands

    def main(band_number, input_file):
        src, band = open_raster(input_file, band_number=band_number)
        print("Band minimum: ", band.GetMinimum())
        print("Band maximum: ", band.GetMaximum())
        print("No-data value: ", band.GetNoDataValue())
        print("Band unit type: ", band.GetUnitType())

        try:
            print(", ".join(get_color_bands(band)))
        except TypeError:
            print("ColorTable: None")

    if __name__ == '__main__':
        # make standalone
        if len( sys.argv ) < 3:
            print(\"\"\"
            ERROR: Provide two arguments:
            1) the band number (int) and 2) input raster directory (str)
            \"\"\")
            how2use()

        main(int(sys.argv[1]), str(sys.argv[2]))
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To run this script, save it as [raster_band_info.py](https://raw.githubusercontent.com/hydro-informatics/jupyter-python-course/main/geodata/raster_band_info.py) (e.g., in `C:\temp` in Windows or `~/temp/` in Linux) and navigate to the script directory in a terminal interface (e.g., in PyCharm's Terminal, Anaconda Prompt, or the Linux Terminal) using the `cd` command. Then run the script to get statistics of the water depth raster `h001000.tif` with (in Windows):
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```
    C:\temp\ python raster_band_info.py 1 "C:\temp\geodata\rasters\h001000.tif"
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    On Linux and with the [flussenv activated](https://hydro-informatics.com/python-basics/pyinstall.html#pip-quick) tap, for example:

    ```
    python raster_band_info.py 1 "$HOME/temp/geodata/rasters/h001000.tif"
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```
    Band minimum:  0.0
    Band maximum:  7.0613012313843
    No-data value:  -3.4028234663852886e+38
    Band unit type:
    Band has no ColorTable.
    ColorTable: None
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Create and Save a Raster (from Array)

    ### Raster Drivers

    Just like for shapefile files, the appropriate `gdal` driver (analogous to `ogr` drivers) must be loaded to save a raster. To get a full list of `gdal` raster drivers run:
    """)
    return


@app.cell
def _(gdal):
    driver_list = [str(gdal.GetDriver(i).GetDescription()) for i in range(gdal.GetDriverCount())]
    driver_list.sort()
    print(", ".join(driver_list[:]))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Raster Data Types

    The output raster pixels can be one of the following data types (source: [gdal.org/doxygen/](https://gdal.org/doxygen/classGDALDataset.html)):

    * `GDT_Unknown` Unknown or unspecified type
    * `GDT_Byte` 8 bit unsigned integer
    * `GDT_UInt16` 16 bit unsigned integer
    * `GDT_Int16` 16 bit signed integer
    * `GDT_UInt32` 32 bit unsigned integer
    * `GDT_Int32` 32 bit signed integer
    * `GDT_Float32` 32 bit floating point
    * `GDT_Float64` 64 bit floating point
    * `GDT_CInt16` Complex Int16
    * `GDT_CInt32` Complex Int32
    * `GDT_CFloat32` Complex Float32
    * `GDT_CFloat64` Complex Float64
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Create a Raster (Array to Raster)

    Knowing the basics of raster handling, data types, and Python, we can create a raster from a numeric array. Since a raster is basically a georeferenced array, it is convenient to convert a [numpy array](https://hydro-informatics.com/python-basics/pynum.html#array-matrix-operations) into a raster (band). The function blocks feature the conversion of a *numpy* array into a GeoTIFF raster according to the following workflow:

    1. Check out the GeoTIFF driver (`driver = gdal.GetDriverByName('GTiff')`).
    1. Retrieve the array size and (number of rows `rows` and columns `cols`).
    1. Create a new GeoTIFF raster (`new_raster = driver.Create(file_name, cols, rows, 1, eType=rdtype)`), where
        - `file_name` is the directory and name of the new raster file ending on `.tif` (e.g., `"C:\\temp\\rasters\\new.tif"`).
        - `cols`, `rows` represent the array shape, and `eType` is the geospatial data type (see above list)
    1. Set the geographic origin, which is stored in the `origin` (*tuple*) parameter and defines the `pixel_width` and `pixel_height` (pixel units defined with `srs` - see below).
    1. Replace `np.nan` values in the numpy array with `nan_value`.
    1. Instantiate a `band` object, set the `NoDataValue` to `nan_value`, and write the array to the `band`.
    1. Create a spatial reference system object  (`srs`) as a function of the `epsg` input parameter and export it to WKT format.
    1. Release the raster (flush from cache).

    > **Note:** The CRS identified by `epsg` determines the coordinate units used by `pixel_width` and `pixel_height`. With `epsg=3857`, widths and heights are expressed in meters. With `epsg=4326`, they are expressed in degrees, so the ground dimensions of a one-degree pixel vary with latitude.
    """)
    return


@app.cell
def _(gdal):
    import numpy as np
    from osgeo import osr


    def create_raster(file_name, raster_array, origin=None, epsg=4326, pixel_width=10, pixel_height=10,
                      nan_value=-9999.0, rdtype=gdal.GDT_Float32, geo_info=False):
        """
        Convert a numpy.array to a GeoTIFF raster with the following parameters
        :param file_name: STR of target file name, including directory; must end on ".tif"
        :param raster_array: np.array of values to rasterize
        :param origin: TUPLE of (x, y) origin coordinates
        :param epsg: INT of EPSG:XXXX projection to use - default=4326
        :param pixel_height: INT of pixel height in CRS coordinate units - default=10
        :param pixel_width: INT of pixel width in CRS coordinate units - default=10
        :param nan_value: INT/FLOAT no-data value to be used in the raster (replaces non-numeric and np.nan in array)
                            default=-9999.0
        :param rdtype: gdal.GDALDataType raster data type - default=gdal.GDT_Float32 (32 bit floating point)
        :param geo_info: TUPLE defining a gdal.DataSet.GetGeoTransform object (supersedes origin, pixel_width, pixel_height)
                            default=False
        """
        # check out driver
        driver = gdal.GetDriverByName('GTiff')

        # create raster dataset with number of cols and rows of the input array
        cols = raster_array.shape[1]
        rows = raster_array.shape[0]
        new_raster = driver.Create(file_name, cols, rows, 1, eType=rdtype)    

        # apply geo-origin and pixel dimensions
        if not geo_info:
            origin_x = origin[0]
            origin_y = origin[1]
            new_raster.SetGeoTransform((origin_x, pixel_width, 0, origin_y, 0, pixel_height))
        else:
            new_raster.SetGeoTransform(geo_info)
    
        # replace np.nan values
        raster_array[np.isnan(raster_array)] = nan_value

        # retrieve band number 1
        band = new_raster.GetRasterBand(1)
        band.SetNoDataValue(nan_value)
        band.WriteArray(raster_array)
        band.SetScale(1.0)

        # create projection and assign to raster
        srs = osr.SpatialReference()
        srs.ImportFromEPSG(epsg)
        new_raster.SetProjection(srs.ExportToWkt())

        # release raster band
        band.FlushCache()

    return create_raster, np, osr


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To call the function for writing a random numpy array, we can now use the `create_raster()` function (also available from `geotools.create_raster()`):
    """)
    return


@app.cell
def _(create_raster, np, os):
    # set the name of the output GeoTIFF raster
    raster_name = r"" + os.getcwd() + "/geodata/rasters/random_unis_dem.tif"
    # create a random numpy array (DEM-like values) - can be replaced with any other numpy.array
    unis_dem = np.random.rand(300, 300) + 455.0
    # overwrite one pixel with np.nan
    unis_dem[5, 7] = np.nan
    # define a raster origin in EPSG:3857
    raster_origin = (1013428.396233, 6231555.006177)
    # call create_raster to create a 1-m-resolution raster in EPSG:4326 projection
    create_raster(raster_name, unis_dem, raster_origin,  pixel_width=1,  pixel_height=1, epsg=3857)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![img](https://hydro-informatics.com/_images/qgis-ras-unis.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Raster Calculus (Raster / Band to Array)

    The procedure described with the `create_raster()` function can be used vice-versa, to create [numpy array](https://hydro-informatics.com/python-basics/pynum.html#array-matrix-operations) from raster bands. The raster converted to a numpy array enables algebraic or other logical operations to be applied to existing raster data.

    Need an example? In the *RiverArchitect SampleData*, the units of the water depth raster `h001000.tif` are in U.S. customary feet and the units of the flow velocity raster `u001000.tif` are in feet per second. However, to calculate the [Froude number](https://hydro-informatics.com/documentation/glossary.html#term-Froude-number) (involves the gravity constant) for every pixel based on the two rasters (water depth and flow velocity), it is convenient to convert both rasters into m and m/s, respectively. For this purpose, the following code block features another re-usable, custom function that loads a raster as an array and overwrites `NoDataValues` with `np.nan` (`raster` and `band` can be instantiated with the above `open_raster` function):
    """)
    return


@app.cell
def _(np, open_raster):
    def raster2array(file_name, band_number=1):
        """
        :param file_name: STR of target file name, including directory; must end on ".tif"
        :param band_number: INT of the raster band number to open (default: 1)
        :output: (1) ndarray() of the indicated raster band, where no-data values are replaced with np.nan
                 (2) the GeoTransformation used in the original raster
        """
        # open the raster and band (see above)
        raster, band = open_raster(file_name, band_number=band_number)
        # read array data from band
        band_array = band.ReadAsArray()
        # overwrite NoDataValues with np.nan
        band_array = np.where(band_array == band.GetNoDataValue(), np.nan, band_array)
        # return the array and GeoTransformation used in the original raster
        return raster, band_array, raster.GetGeoTransform()

    return (raster2array,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The `raster2array()` function is also included in flusstools: `geotools.raster2array()`

    > **Challenge:** The `raster2array` function returns a tuple: `output[0]` is the dataset, `output[1]` is the array, and `output[2]` is the geotransform. Can you make this return structure clearer?

    Finally, to create a Froude number GeoTIFF raster, the following code block makes use of the `raster2array` function for converting the water depth and flow velocity GeoTIFF rasters into a numpy array, performing simple algebraic calculations to convert the rasters to m and m/s, respectively, and save the resulting GeoTIFF file. In detail, the workflow involves to:

    * Define the input raster file names with directories (`h_file` and `u_file`),
    * Load original rasters as `ndarray` with the `raster2array()` function and get the original `GeoTransform` description,
    * Convert all values from U.S. customary feet to S.I. metric units (recall the [`feet_to_meter()`](https://hydro-informatics.com/jupyter/pyfun.html#kwargs) function from the Python basics), and
    * Save a new copy of the raster.
    """)
    return


@app.cell
def _(create_raster, np, os, raster2array):
    _h_file = '' + os.getcwd() + '/geodata/rasters/h001000.tif'
    u_file = '' + os.getcwd() + '/geodata/rasters/u001000.tif'
    h_ras, h, h_geo_info = raster2array(_h_file)
    u_ras, u, u_geo_info = raster2array(u_file)
    h = h * 0.3048
    u = u * 0.3048
    with np.errstate(divide='ignore', invalid='ignore'):
        Froude = u / np.sqrt(h * 9.81)
    create_raster(file_name='' + os.path.abspath('') + '/geodata/rasters/Fr1000cfs.tif', raster_array=Froude, epsg=6418, geo_info=h_geo_info)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Reproject a Raster

    The transformation (and reprojection) of a raster into another coordinate system involves rotating, shifting, and shearing pixels. If one of these operations is skipped, the reprojected raster may be squeezed, twisted, or placed anywhere in the world but not where it should be placed. Therefore, the approach for the reprojection of a raster into another coordinate reference system implies the following steps:

    1. Retrieve the source and target spatial reference systems (e.g., derive from a `gdal.Dataset` or an `EPSG` authority code).
    1. Read the geo transformation of the source dataset ( `gdal.Dataset.GetGeoTransform()`).
    1. Derive the number of pixels and the spacing between pixels in the new (reprojected) dataset.
    1. Instantiate the new (reprojected) dataset.
    1. Project an image of the source dataset onto the new (reprojected) dataset (`gdal.ReprojectImage()`).

    The spatial reference system can be derived from a dataset with the explanations in the [shapefile](https://hydro-informatics.com/jupyter/geo-shp.html#reproject-shp) section by writing a `get_srs()` function. The following code block shows the `get_srs()` function (uses the `osr` library from `osgeo` / `gdal` ), which is also integrated in [flusstools](https://flusstools.readthedocs.io/en/latest/geotools.html#module-flusstools.geotools.srs_mgmt) (`geotools.get_srs()`).
    """)
    return


@app.cell
def _(osr):
    def get_srs(dataset):
        """
        Get the spatial reference of any gdal.Dataset
        :param dataset: osgeo.gdal.Dataset (raster)
        :output: osr.SpatialReference
        """
        sr = osr.SpatialReference()
        sr.ImportFromWkt(dataset.GetProjection())
        # auto-detect epsg
        auto_detect = sr.AutoIdentifyEPSG()
        if auto_detect != 0:
            sr = sr.FindMatches()[0][0]  # Find matches returns list of tuple of SpatialReferences
            sr.AutoIdentifyEPSG()
        # assign input SpatialReference
        sr.ImportFromEPSG(int(sr.GetAuthorityCode(None)))
        return sr

    return (get_srs,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With the `open_raster()` and `get_srs()` functions, we have the necessary ingredients for a raster reprojection function called `reproject_raster()`. The function below lets GDAL calculate a suitable output extent and resolution for the target CRS.
    """)
    return


@app.cell
def _(gdal, osr):
    def reproject_raster(source_dataset, source_srs, target_srs):
        """
        Reproject a raster dataset to an in-memory warped VRT.
        :param source_dataset: osgeo.gdal.Dataset (instantiate with gdal.Open(RASTER-FILE))
        :param source_srs: osgeo.osr.SpatialReference (instantiate with get_srs(source_dataset))
        :param target_srs: osgeo.osr.SpatialReference for the target CRS
        """
        # use traditional GIS axis order for GDAL 3 and later
        source_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
        target_srs.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)


        return gdal.AutoCreateWarpedVRT(
            source_dataset,
            source_srs.ExportToWkt(),
            target_srs.ExportToWkt(),
            gdal.GRA_Bilinear,
        )

    return (reproject_raster,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Using `reproject_raster` requires a source dataset and a target spatial reference. The target reference can be created from an EPSG code or, as below, read from an orientation dataset. This example reprojects the Froude-number raster to the CRS of [web_frame.tif](https://raw.githubusercontent.com/hydro-informatics/jupyter-python-course/main/geodata/rasters/web_frame.tif), which is `EPSG:3857`.

    The warped in-memory dataset is then saved as a GeoTIFF with `create_raster()`.
    """)
    return


@app.cell
def _(create_raster, get_srs, open_raster, os, reproject_raster):
    # load original and orientation rasters
    source_file_name = '' + os.path.abspath('') + '/geodata/rasters/Fr1000cfs.tif'
    orientation_file_name = '' + os.path.abspath('') + '/geodata/rasters/web_frame.tif'
    src_dataset, src_band = open_raster(source_file_name)
    ort_dataset, ort_band = open_raster(orientation_file_name)
    _src_srs = get_srs(src_dataset)
    new_srs = get_srs(ort_dataset)
    print('Source EPSG: ' + str(_src_srs.GetAuthorityCode(None)))
    print('Target EPSG: ' + str(new_srs.GetAuthorityCode(None)))
    ort_dataset, ort_band = (None, None)
    reproj_dataset = reproject_raster(src_dataset, _src_srs, new_srs)
    reproj_file_name = '' + os.path.abspath('') + '/geodata/rasters/Fr1000cfs_reproj.tif'
    array_data = reproj_dataset.ReadAsArray()
    # flush orientation dataset
    new_epsg = int(new_srs.GetAuthorityCode(None))
    geo_transformation = reproj_dataset.GetGeoTransform()
    # create re-projected raster and save as GeoTIFF
    create_raster(reproj_file_name, raster_array=array_data, epsg=new_epsg, geo_info=geo_transformation)
    reproj_dataset = None
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Plotted in QGIS, the reprojected Froude-number raster looks like this:

    ![img](https://hydro-informatics.com/_images/qgis-reproj-Froude.png)

    The `reproject_raster` function is also available (slightly modified) in [flusstools](https://flusstools.readthedocs.io/en/latest/geotools.html#module-flusstools.geotools.srs_mgmt) (`geotools.reproject_raster()`), where saving the new reprojected raster is embedded in the function (automatically appends the syllable `"_epsg[NO]"` to the original file name).

    > **Note:** To display multiple rasters with different coordinate systems on the same map in QGIS, the coordinate systems must be harmonized in most cases. While QGIS will automatically propose to convert a raster with a non-project-compliant CRS to the project CRS, it also has a dedicated function for adjusting raster coordinate systems: In QGIS, click on the **Raster** menu > **Projections** > **Warp (Reproject)...**. Select the raster(s) to reproject (i.e., the raster(s) to harmonize with the project coordinate system). However, *Warp* may not perform all reprojection steps as desired and lead to wrong placements of the new raster. The *Warp* method is also available in Python through `gdal.Warp` ([read the docs](https://gdal.org/tutorials/warp_tut.html)): <br><br>`kwargs={'format': 'GTiff', 'geoloc': True}`<br>`gdal.Warp(TARGET_GEO_TIFF_FILE_NAME, SOURCE_GEO_TIFF_FILE_NAME, **kwargs)`

    > **The coordinate transformation fails** when no transformation between the indicated source and target spatial reference system can be established (i.e., `gdal` does not know the transformation). This problem occurs often when old, regional coordinate systems are transformed into coordinate systems for web applications (e.g., `EPSG=3857`). Read more in the [gdal docs](https://gdal.org/tutorials/osr_api_tut.html#coordinate-transformation).`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Zonal Statistics for Morphological Units

    In hydraulic and geospatial analyses, the question of statistical values of certain areas of one or more rasters often arises. For instance, we may be interested in mean values and standard deviations in specific zones of a water body. For this purpose, *Zonal statistics* enable the delineation of an area of a raster by using a polygon shapefile.

    The *River Architect* dataset includes a slackwater zone and zonal statistics help to identify the mean water depth and flow velocity of slackwaters, which are a so-called morphological unit ([recall the create-shapefile section](https://hydro-informatics.com/jupyter/geo-shp.html#create-shp)).

    > **Background:** Instream morphological units aid in describing the geospatial organization of fluvial landforms, which play an important role in ecohydraulic analyses and river restoration. For instance, *pool* units describe deep water zones with low flow velocity, *riffle* units are typically characterized by shallow water depths and high velocity, and *slackwater* units are shallow flow zones with low flow velocity (many juvenile fish love slackwaters). [Wyrick and Pasternack (2014)](https://www.sciencedirect.com/science/article/pii/S0169555X14000099) introduce the delineation of morphological units and an open-access summary can be found in the [Appendix Sect. 5 in Schwindt et al. (2020)](https://ars.els-cdn.com/content/image/1-s2.0-S235271101930281X-mmc1.pdf).

    To analyze a visually apparent slackwater unit, we can draw a polygon in a new shapefile that delineates morphological units. The following figures guide through the creation of a polygon shapefile and the delineation of the slackwater with QGIS. Start by opening QGIS and creating a new project. Import the water depth and flow velocity rasters showing the slow and shallow water zone. Then follow the workflow in the illustrations below.

    ![img](https://hydro-informatics.com/_images/qgis-create-shp.png)
    ![img](https://hydro-informatics.com/_images/qgis-new-shp.png)
    ![img](https://hydro-informatics.com/_images/qgis-toggle-editing.png)
    ![img](https://hydro-informatics.com/_images/qgis-draw-polygon.png)

    Finalize the drawing by clicking on the **Save Edits** disk button (between **Toggle Editing** and **Add Polygon**). Just in case, the slackwater delineation polygon shapefile is also available at [the jupyter-python repository](https://raw.githubusercontent.com/hydro-informatics/jupyter-python-course/main/geodata/shapefiles/slackwater-poly.zip) of this eBook.

    > **Recall:** The new polygon is not saved as long as the edits are not saved. That means: Regularly saving edits when drawing features in QGIS.

    Zonal statistics can be calculated directly with `gdal` and `ogr`, but the separate [rasterstats](https://pythonhosted.org/rasterstats/) package provides the convenient `rasterstats.zonal_stats(SHP-FILE, RASTER, STATISTICS-TYPES)` function. With `zonal_stats`, we can obtain statistics of the water depth and flow velocity rasters within the new slackwater polygon. The vector and raster inputs must already use the same CRS because rasterstats does not reproject them.
    """)
    return


@app.cell
def _(os):
    import rasterstats as rs
    _h_file = '' + os.getcwd() + '/geodata/rasters/h001000.tif'
    u_file_1 = '' + os.getcwd() + '/geodata/rasters/u001000.tif'
    zone = '' + os.getcwd() + '/geodata/shapefiles/slackw-poly.shp'
    _h_stats = rs.zonal_stats(zone, _h_file, stats=['min', 'max', 'median', 'majority', 'sum'])
    _u_stats = rs.zonal_stats(zone, u_file_1, stats='min max median majority sum')
    print(_h_stats)
    print(_u_stats)
    return rs, u_file_1, zone


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Recall that both rasters are in the U.S. customary unit system (i.e., feet and feet per second). More statistics can be calculated with `zonal_stats`: <br>
    `min`, `max`, `mean`, `count`, `sum`, `std`, `median`, `majority`, `minority`, `unique`, `range`, `nodata`, `percentile_<q>` (where `<q>` can be any float number between 0 and 100).

    In addition, user-defined statistics can be added, where the [numpy.ma](https://numpy.org/doc/stable/reference/routines.ma.html#masked-arrays-arithmetics) module is particularly useful with its array handling capacities, such as for transposing or specifying statistics along an axis. For instance, we can define a specific function to calculate the standard deviation as follows:
    """)
    return


@app.cell
def _(np):
    def raster_std(raster_array):
        return np.ma.std(raster_array)

    return (raster_std,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To use the `raster_std` function in `zonal_stats`, write something similar to this:
    """)
    return


@app.cell
def _(raster_std, rs, u_file_1, zone):
    _u_stats = rs.zonal_stats(zone, u_file_1, stats='min max', add_stats={'stdev': raster_std})
    print(_u_stats)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Clip a Raster
    The above-introduced `rasterstats.zonal_stats` method works with *"Mini-Rasters"*, which represent clips of the input raster to the user-defined polygon shapefile. Moreover, a mini-raster itself can be obtained by defining the optional keyword argument `raster_out=True`. In the case that we want to get the original raster clipped without and statistical operation, we can use a little trick by defining an additional statistics function that returns the original array:
    """)
    return


@app.function
def original(raster_array):
    return raster_array


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    With `raster_out=True` and the `original()` function, we can retrieve the clipped raster in the following array types:

    * `mini_raster_array` - a clipped and masked numpy array,
    * `mini_raster_affine` - a transformation as an `Affine` object (i.e., with [affine 6-parameter transformation](https://gdal.org/user/raster_data_model.html#affine-geotransform)), and
    * `mini_raster_nodata` - `NoData` values.

    The following code block illustrates the usage for retrieving a numpy array:
    """)
    return


@app.cell
def _(os, rs, zone):
    _h_file = '' + os.getcwd() + '/geodata/rasters/h001000.tif'
    _h_stats = rs.zonal_stats(zone, _h_file, stats='count', add_stats={'original': original}, raster_out=True)
    print(_h_stats[0].keys())
    print(_h_stats[0]['mini_raster_array'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Tip:** Use the above methods to assign a projection and save the clipped array as a GeoTIFF raster. The `create_raster` helper is also implemented in [flusstools](https://flusstools.readthedocs.io/en/latest/geotools.html#module-flusstools.geotools.raster_mgmt) and can be called as `geotools.create_raster(...)`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Slope / Aspect Maps and Built-in Command Line Scripts

    Hillslope maps are an important parameter in hydraulics, hydrology, and ecology. For instance, the slope determines the flow direction of water and it is also a criterion for delineating the habitat of many species. To calculate hill slope gradients and directions, `gdal` has a command-line tool called `gdaldem` , which requires a DEM (Digital Elevation Model) raster. The general use of `gdaldem` in the command line is (arguments in brackets are optional):
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```
    gdaldem slope input_dem output_slope_map  [-p use percent slope (default=degrees)] [-s scale* (default=1)] [-alg ZevenbergenThorne] [-compute_edges] [-b Band (default=1)] [-of format] [-co "NAME=VALUE"]* [-q]
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To call the command-line tool, we can either use a terminal/command prompt or Python's standard library `subprocess`. The following code block illustrates the usage of the `gdaldem` command line tool through [`subprocess.call()`](https://docs.python.org/3/library/subprocess.html) to create a slope raster (in percent) from the *River Architect* sample data's [`dem.tif`](https://raw.githubusercontent.com/hydro-informatics/jupyter-python-course/main/geodata/rasters/dem.tif). Note that `subprocess.call()` returns `0` if the command execution was successful and any other return value indicates an error.
    """)
    return


@app.cell
def _(os):
    import subprocess
    cmd_create_slope = 'gdaldem slope {0}/geodata/rasters/dem.tif {0}/geodata/rasters/slope-percent.tif -p'.format(os.path.abspath(''))
    subprocess.call(cmd_create_slope, shell=True)
    return (subprocess,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![img](https://hydro-informatics.com/_images/qgis-slope.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In addition to the absolute slope (inclination in degrees), it can be important to know the slope direction. A raster indicating this direction is called an **aspect raster**. By default, `gdaldem aspect` uses azimuths: north is 0° (and 360°), east is 90°, south is 180°, and west is 270°. The `-trigonometric` option instead uses east=0°, north=90°, west=180°, and south=270°.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```
    gdaldem aspect input_dem output_aspect_map [-trigonometric] [-zero_for_flat] [-alg ZevenbergenThorne] [-compute_edges] [-b Band (default=1)] [-of format] [-co "NAME=VALUE"]* [-q]
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To create an aspect raster of the *River Architect* sample data DEM run:
    """)
    return


@app.cell
def _(os, subprocess):
    cmd_create_aspect = "gdaldem aspect {0}/geodata/rasters/dem.tif {0}/geodata/rasters/slope-aspect.tif".format(os.path.abspath(""))
    subprocess.call(cmd_create_aspect, shell=True)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![img](https://hydro-informatics.com/_images/qgis-aspect.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Least Cost Path between Pixels (and another Way of Reprojection)

    ### Ecohydraulic Background
    Least cost paths are important to plan efficient routes for navigation (e.g., in a car) and they can also be helpful in ecohydraulics. Let's take for a moment the position of a fish that, after a flood with decreasing discharge, wants to swim as fast as possible from the floodplain back into the main channel where there is enough water. In the figure below, point 1 shows the starting point on the floodplain and point 2 the destination in the main channel. The reddish background represents the above-produced slope raster (*slope-percent.tif*) and the water depth at average annual discharge is colored in blue.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![img](https://hydro-informatics.com/_images/qgis-slope-pts.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    A least-cost path depends entirely on the cost surface. Using positive slope magnitude directly favors routes with smaller accumulated slope; it does not by itself enforce a steep or monotonically downhill route. A biologically meaningful cost surface must therefore encode the movement assumptions explicitly.

    > **A note on hydro-peaking:** In many rivers, fish face the daily challenge of escaping from the deadly trap of lateral depressions. The reason for this is that many hydroelectric power plants cause abrupt fluctuations in discharge due to fluctuations in energy demand and production (so-called **hydro-peaking**). As a result, there is a high stranding risk for fish in many regulated rivers that are subjected to hydro-peaking. The following figure illustrates stranding risk zones as a function of discharge (in cubic feet per second) at the lower Yuba River (California, USA).

    ![img](https://hydro-informatics.com/_images/ra-stranding.png)

    *Image source: [The River Architect Wiki / Kenneth Larrieu](https://riverarchitect.github.io/RA_wiki/StrandingRisk)*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Functions and Libraries Involved

    The `skimage` (`scikit-image`) library (see [Other packages in the Open source libraries section](https://hydro-informatics.com/geopy/geo-pckg.html#other-geo-pckgs)) provides with [`skimage.graph.route_through_array`](https://scikit-image.org/docs/0.19.x/api/skimage.graph.html) a smart method to calculate the least cost path by summing up pixel-wise connections from point 1 to point 2.

    Here is how it works: Assume a numpy array (e.g., with random slope values) that looks like this:
    """)
    return


@app.cell
def _(np):
    slope_image = np.random.randint(100, size=(3, 5))
    slope_image
    return (slope_image,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To find the fastest way from array index `[0][0]` (top left  `point_1 = (0, 0)`) to array index `[2][4]` (bottom right point `point_2 = (2, 4)`), we can use `route_through_array()` to get a *list* (`least_cost_path_indices`) with the array coordinates of the path to go, and the costs (`weight`) involved (sum of all pixels of the least cost path):
    """)
    return


@app.cell
def _(slope_image):
    from skimage.graph import route_through_array

    point_1 = (0, 0)
    point_2 = (2, 4)
    least_cost_path_indices, weight = route_through_array(slope_image, point_1, point_2)
    least_cost_path_indices, weight
    return least_cost_path_indices, route_through_array


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To integrate the least cost path list into an array that we can *rasterize* (`geotools.create_raster()`), we can paste `least_cost_path_indices` into a numpy-zeros array of the original slope raster (image) as a transposed list.
    """)
    return


@app.cell
def _(least_cost_path_indices, np, slope_image):
    least_cost_path_indices_1 = np.array(least_cost_path_indices).T
    least_cost_path_array = np.zeros_like(slope_image)
    least_cost_path_array[least_cost_path_indices_1[0], least_cost_path_indices_1[1]] = 1
    least_cost_path_array
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In practice, the slope raster is georeferenced, and therefore, we have to use pixel coordinates relative to the coordinate system origin. For this purpose, we need two more functions:

    * One function to calculate the pixel-index related offset that we will name `coords2offset`: The `coords2offset()` function will return the x-y shift in the form of "number of pixels" (two *integer*s, one for *x* and one for *y* shift).
    * The [above-defined `get_srs()`](https://hydro-informatics.com/jupyter/geo-raster.html#reproject-raster) function (i.e., `geotools.get_srs()`).

    The `coords2offset()` function looks like this:
    """)
    return


@app.function
def coords2offset(geo_transform, x_coord, y_coord):
    """
    Returns x-y pixel offset
    :param geo_transform: osgeo.gdal.Dataset.GetGeoTransform() object
    :param x_coord: FLOAT of x-coordinate
    :param y_coord: FLOAT of y-coordinate
    :return: offset_x, offset_y (both integer of pixel numbers)
    """
    origin_x = geo_transform[0]
    origin_y = geo_transform[3]
    pixel_width = geo_transform[1]
    pixel_height = geo_transform[5]
    offset_x = int((x_coord - origin_x) / pixel_width)
    offset_y = int((y_coord - origin_y) / pixel_height)
    return offset_x, offset_y


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Tip:** The `coords2offset()` function is also available in flusstools with more robust raise-exception notation: use with `geotools.coords2offset()` and have a look into the script located in [`flusstools.geotools.dataset_mgmt`](https://raw.githubusercontent.com/Ecohydraulics/flusstools-pckg/main/flusstools/geotools/dataset_mgmt.py).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The `coords2offset()` function converts a raster array (e.g., produced with the above-defined `geotools.raster2array()` function) into an array that can be used with `route_through_array()` with the following workflow:

    1. Use the raster's `geo_transform` (`gdal.Dataset.GetGeoTransform = (origin_x, pixel_width, 0, origin_y, 0, pixel_height)`) and the start and end point coordinates (i.e, `start_coord` of point 1 and `stop_coord` of point 2) in `coords2offset()` to get their pixel indices (`start_index_x`, `start_index_y`, `stop_index_x`, and `stop_index_y`) in the raster array.
    1. Replace `np.nan` values in the raster array with values that are higher than the maximum value of the array. Do not use zeros, because we want to exclude the `np.nan` pixels from the least cost path later by overwriting `np.nan` with very high pixel costs.
    1. Use `route_through_array()` as above explained with the optional arguments `geometric=True` (use the [*MCP_Geometric* class](https://scikit-image.org/docs/0.19.x/api/skimage.graph.html#skimage.graph.MCP_Geometric) rather than [*MCP_base*](https://scikit-image.org/docs/0.19.x/api/skimage.graph.html#skimage.graph.MCP) to calculate costs) and `fully_connected=True` (enables using diagonal pixels as direct neighbors).
    1. Integrate the least cost path list (`index_path`) into a numpy-zeros array (child of `raster_array`, as explained above) and return the `path_array`.
    """)
    return


@app.cell
def _(np, route_through_array):
    def create_path_array(raster_array, geo_transform, start_coord, stop_coord):
        # transform coordinates to array index
        start_index_x, start_index_y = coords2offset(geo_transform, start_coord[0], start_coord[1])
        stop_index_x, stop_index_y = coords2offset(geo_transform, stop_coord[0], stop_coord[1])

        # replace np.nan with max raised by an order of magnitude to exclude pixels from least cost
        raster_array[np.isnan(raster_array)] = np.nanmax(raster_array) * 10

        # create path and costs
        index_path, cost = route_through_array(raster_array, (start_index_y, start_index_x),
                                                   (stop_index_y, stop_index_x),
                                                   geometric=True, fully_connected=True)


        index_path = np.array(index_path).T
        path_array = np.zeros_like(raster_array)
        path_array[index_path[0], index_path[1]] = 1
        return path_array

    return (create_path_array,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Application

    Recall, we defined the following functions (all are available in [flusstools](https://flusstools.readthedocs.io) through `from flusstools import geotools`) that we can use for the calculation of the least cost path to get from point 1 to point 2 in the *slope-percent.tif* raster:

    * `geotools.raster2array()`
    * `geotools.create_path_array()`
    * `geotools.get_srs()`
    * `geotools.create_raster()`

    The below code block uses these functions as follows:

    1. Define input (*slope-percent.tif*) and output (*least_cost.tif*) raster names (with directories).
    1. Define the coordinates of points 1 and 2 as *tuple*s (x, y) in the *EPSG:6418* projection.
    1. Load the input raster(`src_raster`), its band as array (`raster_array`), and geotransformation (`geo_transform`) with the `raster2array()` function.
    1. Get the least cost path indicated with ones in an array of zeros ( i.e., an on-off `path_array`) with the `create_path_array()` function.
    1. Get the `osgeo.osr.SpatialReference` of the input raster (`src_raster = osgeo.gdal.Dataset("slope-percent.tif")`).
    1. Create the least cost path GeoTIFF raster with the `create_raster()` function as a `gdal.GDT_Byte` band.
    """)
    return


@app.cell
def _(create_path_array, create_raster, gdal, get_srs, os, raster2array):
    in_raster_name = '' + os.path.abspath('') + '/geodata/rasters/slope-percent.tif'
    out_raster_name = '' + os.path.abspath('') + '/geodata/rasters/least-cost.tif'
    point_1_coord = (6749261.940928269, 2206970.3517958256)
    point_2_coord = (6749016.82820663, 2207050.614910375)
    src_raster, raster_array, geo_transform = raster2array(in_raster_name)
    path_array = create_path_array(raster_array, geo_transform, point_1_coord, point_2_coord)
    _src_srs = get_srs(src_raster)
    create_raster(out_raster_name, path_array, epsg=int(_src_srs.GetAuthorityCode(None)), rdtype=gdal.GDT_Byte, geo_info=geo_transform)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![img](https://hydro-informatics.com/_images/qgis-least-cost.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Legitimately, you may wonder whether it was better to represent the least cost path as a line. Of course, that is correct. However, this operation is a conversion of a raster into a line shapefile, which is explained in the next section on [geodata conversion](https://hydro-informatics.com/jupyter/geo-convert.html#raster2line). Curious readers can also directly use the `raster2line()` function of flusstools (or have a look at it in the  [flusstools.geotools/dataset_mgmt.py](https://raw.githubusercontent.com/Ecohydraulics/flusstools-pckg/main/flusstools/geotools/dataset_mgmt.py) script).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Exercise:** Familiarize with raster handling in the [geospatial ecohydraulics](https://hydro-informatics.com/exercises/ex-geco) exercise.
    """)
    return


if __name__ == "__main__":
    app.run()
