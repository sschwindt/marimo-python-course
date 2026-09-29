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
    # Vectorize and Rasterize

    This section introduces geospatial dataset conversion with Python. In particular, the goal of this section is to guide to an understanding of conversions from raster to vector data formats and vice versa.

    > **Requirements:**
    > * Make sure to understand [handling of gridded raster data](https://hydro-informatics.com/jupyter/geo-raster.html) and [shapefile handling](https://hydro-informatics.com/jupyter/geo-shp.html)
    > * Understand the creation of the [least cost path](https://hydro-informatics.com/jupyter/geo-raster.html#leastcost) raster dataset.

    > **Tips:**
    > * The functions featured in this section are partially also implemented in [flusstools](https://flusstools.readthedocs.io/).
    > * To use those functions, make sure flusstools is installed and import it as follows: `from flusstools import geotools`. Some of the functions shown in this tutorial can then be used with `geotools.function_name()`.

    ## Import relevant Libraries

    Make sure to import the relevant packages for handling rasters, shapefiles, and geospatial references:
    """)
    return


@app.cell
def _():
    from osgeo import gdal
    from osgeo import osr
    from osgeo import ogr

    return gdal, ogr


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Vectorize

    ### Raster to Line

    In this section, we convert the [least cost path](https://hydro-informatics.com/jupyter/geo-raster.html#leastcost) raster dataset ([least_cost.tif](https://github.com/hydro-informatics/jupyter-python-course/raw/main/geodata/rasters/least-cost.tif)) into a (poly) line shapefile. For this purpose, we first write a function called `offset2coords()`, which represents the inverse of the [`coords2offset()`](https://hydro-informatics.com/jupyter/geo-raster.html#lc-fun) function, and converts x/y offset (in *integer* pixel numbers) to coordinates of a geospatial dataset's geo-transformation:
    """)
    return


@app.function
def offset2coords(geo_transform, offset_x, offset_y):
    # get origin and pixel dimensions from geo_transform (osgeo.gdal.Dataset.GetGeoTransform() object)
    origin_x = geo_transform[0]
    origin_y = geo_transform[3]
    pixel_width = geo_transform[1]
    pixel_height = geo_transform[5]
    
    # calculate x and y coordinates
    coord_x = origin_x + pixel_width * (offset_x + 0.5)
    coord_y = origin_y + pixel_height * (offset_y + 0.5)

    # return x and y coordinates
    return coord_x, coord_y


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Note:** The offset is added 0.5 pixels in both x and y directions to meet the center of the pixel rather than the top-left pixel corner.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, we can write a core function to convert a raster dataset to a line shapefile. We name this function `raster2line()` and it builds on the following workflow:

    * Open a `raster`, its band as `array`, and `geo_transform` (geo-transformation) defined with the `raster_file_name` argument in the [`open_raster`](https://hydro-informatics.com/geo-raster#open-raster) function from the raster section.
    * Calculate the maximum center-to-center distance (`max_distance`) between diagonally adjacent pixels from the actual pixel width *&Delta;x* and height *&Delta;y*
    * Get the `trajectory` of pixels that have a user-defined `pixel_value` (e.g., `1` to trace 1-pixels in the binary *least_cost.tif*) and report an error if the index arrays are empty (`trajectory[0].size == 0`).
    * Use the above-defined `offset2coords` function to append point coordinates to a `points` list.
    * Create a `multi_line` object (instance of `ogr.Geometry(ogr.wkbMultiLineString)`), which represents the (void) final least cost path.
    * Iterate through all possible combinations of points (excluding combinations of points with themselves) with [`itertools.combinations(iterable, r=number-of-combinations=2`](https://docs.python.org/3/library/itertools.html)).
        - Points are stored in the `points` list.
        - `point1` and `point2` are required to get the distance between pairs of points.
        - If the `distance` between the points is smaller than `max_distance`, the function creates a line object from the two points and appends it to the `multi_line` object.

    * Create a new shapefile (named `out_shp_fn`) using the [`create_shp()`](https://hydro-informatics.com/geo-shp#create-shp) function (with integrated shapefile name length verification from flusstools `geotools.create_shp()`).
    * Add the `multi_line` object as a new feature to the shapefile (according to the descriptions in the [shapefile section](https://hydro-informatics.com/geo-shp#line-create)).
    * Create a `.prj` projection file (recall descriptions in the [shapefile section](https://hydro-informatics.com/geo-shp#prj-shp)) using the spatial reference system of the input `raster` with the [`get_srs()`](https://hydro-informatics.com/geo-raster#lc-fun) function.

    The `raster2line` function is also implemented in the [`flusstools.geotools.geotools`](https://raw.githubusercontent.com/Ecohydraulics/flusstools-pckg/refs/heads/main/src/flusstools/geotools/geotools.py) script.
    """)
    return


@app.cell
def _():
    import itertools
    import numpy as np
    from flusstools.geotools import raster2array
    from flusstools.geotools import create_shp
    from flusstools.geotools import get_srs
    from flusstools.geotools import make_prj

    return create_shp, get_srs, itertools, make_prj, np, raster2array


@app.cell
def _(create_shp, get_srs, itertools, make_prj, np, ogr, raster2array):
    def raster2line(raster_file_name, out_shp_fn, pixel_value):
        """
        Convert a raster to a line shapefile, where pixel_value determines line start and end points
        :param raster_file_name: STR of input raster file name, including directory; must end on ".tif"
        :param out_shp_fn: STR of target shapefile name, including directory; must end on ".shp"
        :param pixel_value: INT/FLOAT of a pixel value
        :return: None (writes new shapefile).
        """

        # calculate max. distance between points
        # ensures correct neighbourhoods for start and end pts of lines
        raster, array, geo_transform = raster2array(raster_file_name)
        pixel_width = abs(geo_transform[1])
        pixel_height = abs(geo_transform[5])
        max_distance = np.hypot(pixel_width, pixel_height) * 1.001

        # extract pixels with the user-defined pixel value from the raster array
        trajectory = np.where(array == pixel_value)
        if trajectory[0].size == 0:
            print("ERROR: The defined pixel_value (%s) does not occur in the raster band." % str(pixel_value))
            return None

        # convert pixel offset to coordinates and append to nested list of points
        points = []
        count = 0
        for offset_y in trajectory[0]:
            offset_x = trajectory[1][count]
            points.append(offset2coords(geo_transform, offset_x, offset_y))
            count += 1

        # create multiline (write points dictionary to line geometry (wkbMultiLineString)
        multi_line = ogr.Geometry(ogr.wkbMultiLineString)
        for i in itertools.combinations(points, 2):
            point1 = ogr.Geometry(ogr.wkbPoint)
            point1.AddPoint(i[0][0], i[0][1])
            point2 = ogr.Geometry(ogr.wkbPoint)
            point2.AddPoint(i[1][0], i[1][1])

            distance = point1.Distance(point2)
            if distance < max_distance:
                line = ogr.Geometry(ogr.wkbLineString)
                line.AddPoint(i[0][0], i[0][1])
                line.AddPoint(i[1][0], i[1][1])
                multi_line.AddGeometry(line)

        # write multiline (wkbMultiLineString2shp) to shapefile
        new_shp = create_shp(out_shp_fn, layer_name="raster_pts", layer_type="line")
        lyr = new_shp.GetLayer()
        feature_def = lyr.GetLayerDefn()
        new_line_feat = ogr.Feature(feature_def)
        new_line_feat.SetGeometry(multi_line)
        lyr.CreateFeature(new_line_feat)

        # create projection file
        srs = get_srs(raster)
        make_prj(out_shp_fn, int(srs.GetAuthorityCode(None)))

        # close the output shapefile and release the input raster
        new_line_feat = None
        lyr = None
        new_shp = None
        raster = None
        print("Success: Wrote %s" % str(out_shp_fn))

    return (raster2line,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The `raster2line()` function can be called as follows to convert the least cost path from pixel (raster) to line (vector) format:
    """)
    return


@app.cell
def _(raster2line):
    import os
    source_raster_fn = '' + os.path.abspath('') + '/geodata/rasters/least-cost.tif'
    target_shp_fn = '' + os.path.abspath('') + '/geodata/shapefiles/least-cost.shp'
    pixel_value = 1
    raster2line(source_raster_fn, target_shp_fn, pixel_value)
    return (os,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![img](https://hydro-informatics.com/_images/qgis-least-cost-line.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Challenge:** There is a small error in the `least_cost` line. Can you find the error? What can be done to fix the error?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Note:** Network routing is the functional core of the [`NetworkX` library (see *Open source libraries*)](https://hydro-informatics.com/geopy/geo-pckg.html#other-geo-pckgs). Read more about network analyses on [Michael Diener's GitHub pages](https://github.com/mdiener21/python-geospatial-analysis-cookbook/tree/master/ch08).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Raster to Polygon

    `gdal.Polygonize` converts connected raster regions to polygons. It reads source values through an integer buffer, so floating-point values are truncated unless they are scaled and converted first; `gdal.FPolygonize` is the floating-point alternative. The `float2int()` helper below applies an optional scale factor before rounding so decimal precision can be retained in the stored integer classes. It uses the [`raster2array()`](https://hydro-informatics.com/geo-raster#createarray) and [`create_raster()`](https://hydro-informatics.com/geo-raster#create-raster) functions from the raster section.
    """)
    return


@app.cell
def _():
    from flusstools.geotools import create_raster, open_raster

    return create_raster, open_raster


@app.cell
def _(create_raster, gdal, get_srs, np, raster2array):
    def float2int(raster_file_name, band_number=1, scale_factor=1):
        """
        :param raster_file_name: STR of target file name, including directory; must end on ".tif"
        :param band_number: INT of the raster band number to open (default: 1)
        :param scale_factor: positive numeric factor applied before rounding (default: 1)
        :output: new_raster_file_name (STR)
        """
        # use raster2array function to get raster, np.array and the geo transformation
        raster, array, geo_transform = raster2array(raster_file_name, band_number=band_number)
    
        # scale, round, and convert valid pixels to integers
        try:
            if scale_factor <= 0:
                raise ValueError("scale_factor must be positive")
            array = np.where(np.isnan(array), -9999, np.rint(array * scale_factor)).astype(np.int32)
        except (TypeError, ValueError):
            print("ERROR: Invalid raster pixel values.")
            return raster_file_name
    
        # get spatial reference system
        src_srs = get_srs(raster)
    
        # create integer raster    
        new_name = raster_file_name.split(".tif")[0] + "_int.tif"
        create_raster(new_name, array, epsg=int(src_srs.GetAuthorityCode(None)),
                      rdtype=gdal.GDT_Int32, geo_info=geo_transform)
        # return name of integer raster
        return new_name

    return (float2int,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Next, we will create the `raster2polygon()` function that implements the following workflow:

    1. Use the `float2int()` function to convert raster values to integers. Choose a scale factor greater than one when decimal precision must be retained; divide the resulting class values by the same factor when interpreting them.
    1. Create a new shapefile (named `out_shp_fn`) using the [`create_shp()`](https://hydro-informatics.com/jupyter/geo-shp.html#create-shp) function (also available from flusstools: `geotools.create_shp()`).
    1. Add a new `ogr.OFTInteger` field (recall [how field creation works](https://hydro-informatics.com/jupyter/geo-shp.html#add-field)) in the shapefile section) named by the optional `field_name` input argument.
    1. Run [`gdal.Polygonize`](https://gdal.org/api/gdal_alg.html#_CPPv414GDALPolygonize15GDALRasterBandH15GDALRasterBandH9OGRLayerHiPPc16GDALProgressFuncPv) with:

        * `hSrcBand=raster_band`
        * `hMaskBand=None` (optional raster band to define polygons)
        * `hOutLayer=dst_layer`
        * `iPixValField=0` (if no field was added, set to `-1` in order to create an `FID` field; if more fields were added, set to `1`, `2`, ... )
        * `papszOptions=[]` (no effect for `ESRI Shapefile` driver type)
        * `callback=None` for not using the reporting algorithm (`GDALProgressFunc()`)

    1. Create a `.prj` projection file (recall descriptions in the [shapefile section](https://hydro-informatics.com/jupyter/geo-shp.html#prj-shp)) using the spatial reference system of the input `raster` with the [`get_srs()`](https://hydro-informatics.com/jupyter/geo-raster.html#lc-fun) function.
    """)
    return


@app.cell
def _(create_shp, float2int, gdal, get_srs, make_prj, ogr, open_raster):
    def raster2polygon(file_name, out_shp_fn, band_number=1, field_name="values", scale_factor=1):
        """
        Convert a raster to polygon
        :param file_name: STR of target file name, including directory; must end on ".tif"
        :param out_shp_fn: STR of a shapefile name (with directory e.g., "C:/temp/poly.shp")
        :param band_number: INT of the raster band number to open (default: 1)
        :param field_name: STR of the field where scaled raster values will be stored (default: "values")
        :param scale_factor: positive numeric factor applied before integer conversion (default: 1)
        :return: None
        """
        # ensure that the input raster contains integer values only and open the input raster
        file_name = float2int(file_name, band_number=band_number, scale_factor=scale_factor)
        raster, raster_band = open_raster(file_name, band_number=1)

        # create new shapefile with the create_shp function
        new_shp = create_shp(out_shp_fn, layer_name="raster_data", layer_type="polygon")
        dst_layer = new_shp.GetLayer()

        # create new field to define values
        new_field = ogr.FieldDefn(field_name, ogr.OFTInteger)
        dst_layer.CreateField(new_field)

        # Polygonize(band, hMaskBand[optional]=None, destination lyr, field ID, papszOptions=[], callback=None)
        gdal.Polygonize(raster_band, None, dst_layer, 0, [], callback=None)

        # create projection file
        srs = get_srs(raster)
        make_prj(out_shp_fn, int(srs.GetAuthorityCode(None)))

        # close datasets so pending writes are flushed
        raster_band = None
        raster = None
        dst_layer = None
        new_shp = None
        print("Success: Wrote %s" % str(out_shp_fn))

    return (raster2polygon,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Note:**
    > * `Polygonize` can also be run from [terminal/Anaconda prompt](https://hydro-informatics.com/jupyter/geo-raster.html#terminal) by typing [`gdal_polygonize`](https://gdal.org/programs/gdal_polygonize.html).
    > * Both the `float2int()` and the `raster2polygon()` functions are also available in flusstools with `flusstools.geotools.float2int()` and `flusstools.geotools.raster2polygon()` respectively ([have a look at the geotools.py script](https://raw.githubusercontent.com/Ecohydraulics/flusstools-pckg/main/flusstools/geotools/geotools.py)).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The `raster2polygon()` function can be implemented, for example, to convert the water depth raster for 1000 CFS (*h001000.tif* from the [*River Architect* sample datasets](https://github.com/RiverArchitect/SampleData/tree/master/01_Conditions/2100_sample)) to a polygon shapefile:
    """)
    return


@app.cell
def _(os, raster2polygon):
    src_raster = '' + os.path.abspath('') + '/geodata/rasters/h001000.tif'
    tar_shp = '' + os.path.abspath('') + '/geodata/shapefiles/h_poly_cls.shp'
    raster2polygon(src_raster, tar_shp)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Rasterize (Vector Shapefile to Raster)

    Similar to `gdal.Polygonize`, [`gdal.RasterizeLayer`](https://gdal.org/python/osgeo.gdal-module.html#RasterizeLayer) represents a handy option to convert a shapefile into a raster. However, to be precise, a shapefile is not really converted into a raster but burned onto a raster. Thus, values stored in a field of a shapefile feature are used (burned) as pixel values for creating a new raster. Attention is required to ensure that the correct values and data types are used. To this end, the below shown `rasterize()` function implements the following workflow that avoids potential conversion headaches:

    1. Open the user-provided input shapefile name and layer.
    1. Read the spatial extent of the layer.
    1. Derive the x-y resolution as a function of the spatial extent and a user-defined `pixel_size` (optional keyword argument with default value).
    1. Create a new GeoTIFF raster using the
        * user-defined `output_raster_file_name`,
        * calculated x and y resolution, and
        * `eType` (default is `gdal.GDT_Float32` - recall all data type options listed in the [raster section](https://hydro-informatics.com/jupyter/geo-raster.html#etypes).
    1. Apply the geotransformation defined by the source layer extents and the `pixel_size`.
    1. Create one raster `band`, fill the `band` with the user-defined `no_data_value` (default is `-9999`), and set the `no_data_value`.
    1. Set the spatial reference system of the raster to the same as the source shapefile.
    1. Apply `gdal.RasterizeLayer` with
        * `dataset=target_ds` (target raster dataset),
        * `bands=[1]` (*list(integer)* - increase to defined more raster bands and assign other values, for example, from other fields of the source shapefile),
        * `layer=source_lyr` (layer with features to burn to the raster),
        * `pfnTransformer=None` ([read more in the gdal docs](https://gdal.org/api/python/osgeo.gdal.html?highlight=rasterize#osgeo.gdal.Rasterize)),
        * `pTransformArg=None` ([read more in the gdal docs](https://gdal.org/api/python/osgeo.gdal.html?highlight=rasterize#osgeo.gdal.Rasterize)),
        * `burn_values=[0]` (a default value that is burned to the raster),
        * `options=["ALL_TOUCHED=TRUE"]` assigns the polygon's field value to every pixel touched by the polygon; without it, polygon rasterization normally selects pixels whose centers lie within the polygon,
        * `options=["ATTRIBUTE=" + str(kwargs.get("field_name"))]` defines the field name with values to burn.
    """)
    return


@app.cell
def _(gdal, np, ogr):
    def rasterize(in_shp_file_name, out_raster_file_name, pixel_size=10, no_data_value=-9999,
                  rdtype=gdal.GDT_Float32, **kwargs):
        """
        Converts any shapefile to a raster
        :param in_shp_file_name: STR of a shapefile name (with directory e.g., "C:/temp/poly.shp")
        :param out_raster_file_name: STR of target file name, including directory; must end on ".tif"
        :param pixel_size: INT of pixel size (default: 10)
        :param no_data_value: Numeric (INT/FLOAT) for no-data pixels (default: -9999)
        :param rdtype: gdal.GDALDataType raster data type - default=gdal.GDT_Float32 (32 bit floating point)
        :kwarg field_name: name of the shapefile's field with values to burn to the raster
        :return: None (writes the raster defined by out_raster_file_name)
        """

        # open data source
        source_ds = ogr.Open(in_shp_file_name)
        if source_ds is None:
            print("Error: Could not open %s." % str(in_shp_file_name))
            return None
        source_lyr = source_ds.GetLayer()

        # read extent
        x_min, x_max, y_min, y_max = source_lyr.GetExtent()

        # get x and y resolution
        x_res = int(np.ceil((x_max - x_min) / pixel_size))
        y_res = int(np.ceil((y_max - y_min) / pixel_size))

        # create destination data source (GeoTIff raster)
        target_ds = gdal.GetDriverByName('GTiff').Create(out_raster_file_name, x_res, y_res, 1, eType=rdtype)
        target_ds.SetGeoTransform((x_min, pixel_size, 0, y_max, 0, -pixel_size))
        band = target_ds.GetRasterBand(1)
        band.Fill(no_data_value)
        band.SetNoDataValue(no_data_value)

        # get spatial reference system and assign to raster
        srs = source_lyr.GetSpatialRef()
        if srs is None:
            raise ValueError("The input layer has no spatial reference.")
        target_ds.SetProjection(srs.ExportToWkt())

        field_name = kwargs.get("field_name")
        if not field_name:
            raise ValueError("field_name is required when burning attribute values.")

        gdal.RasterizeLayer(
            target_ds, [1], source_lyr,
            options=["ALL_TOUCHED=TRUE", "ATTRIBUTE=" + str(field_name)],
        )

        # flush and close datasets
        band.FlushCache()
        band = None
        target_ds = None
        source_lyr = None
        source_ds = None

    return (rasterize,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Tip:** `Rasterize` can also be run from [terminal/Anaconda prompt](https://hydro-informatics.com/jupyter/geo-raster.html#terminal) with [`gdal_rasterize`](https://gdal.org/programs/gdal_rasterize.html).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Finally, the `rasterize()` function can be called to convert the polygonized water depth polygon shapefile */geodata/shapefiles/h_poly_cls.shp* ([download it as a zip file](https://github.com/hydro-informatics/jupyter-python-course/raw/main/geodata/shapefiles/h_poly_cls.zip)) back to a raster (this is practically useless but an illustrative exercise). Pay attention to the data type, which is `gdal.GDT_Int32` in combination with the correctly defined `field_name` argument.
    """)
    return


@app.cell
def _(gdal, os, rasterize):
    src_shp = r"" + os.path.abspath("") + "/geodata/shapefiles/h_poly_cls.shp"
    tar_ras = r"" +  os.path.abspath("") + "/geodata/rasters/h_re_rastered.tif"
    rasterize(src_shp, tar_ras, pixel_size=5, rdtype=gdal.GDT_Int32, field_name="values")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ![img](https://hydro-informatics.com/_images/qgis-h-rasterized.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Exercise:** Familiarize yourself with the conversion of rasters and shapefiles in the [geospatial ecohydraulics](https://hydro-informatics.com/exercises/ex-geco) exercise.
    """)
    return


if __name__ == "__main__":
    app.run()
