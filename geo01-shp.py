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
    # Shapefile (Vector) Handling

    This section introduces geospatial analysis of shapefiles with gdal, ogr, and osr.

    > **Requirements:**
    > * Make sure to understand [shapefiles](https://hydro-informatics.com/geospatial-data#shp) and [vector data](https://hydro-informatics.com/geospatial-data#vector).
    > * Accomplish the [QGIS tutorial](https://hydro-informatics.com/use-qgis)

    The core functions featured in this section are also implemented in [flusstools](https://flusstools.readthedocs.io). To use those functions, make sure flusstools is installed and import it as follows: `from flusstools import geotools`. Some of the functions shown in this tutorial can then be used with `geotools.function_name()`.

    ## Load an Existing Shapefile

    OSGeo's `ogr` module handles shapefiles. After importing the library, obtain the `"ESRI Shapefile"` driver with `ogr.GetDriverByName("ESRI Shapefile")`. The driver can open a shapefile dataset with `shp_driver.Open("path/to/file.shp")`; obtain its layer with `shp_dataset.GetLayer()`.
    """)
    return


@app.cell
def _():
    from osgeo import ogr
    _shp_driver = ogr.GetDriverByName('ESRI Shapefile')
    shp_dataset = _shp_driver.Open('geodata/shapefiles/iws_va.shp')
    shp_layer = shp_dataset.GetLayer()
    return ogr, shp_layer


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Tip:** To get a full list of supported `ogr` drivers (e.g., for `DXF`, `ESRIJSON`, `GPS`, `PDF`, `SQLite`, `XLSX`, and many more), [download the script `get_ogr_drivers.py`](https://raw.githubusercontent.com/hydro-informatics/material-py-codes/main/geo/get_ogr_drivers.py) from hydro-informatics on Github.

    > **Warning:** Importing `ogr` with `from gdal import ogr` is deprecated since GDAL v3. Therefore, `ogr` must be imported from `osgeo`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Create a New Shapefile

    `ogr` also enables creating a new point, line, or polygon shapefile. The following code block defines a function for creating a shapefile, where the optional keyword argument `overwrite` is used to control whether an existing shapefile with the same name should be overwritten (default: `True`).
    The command `shp_driver.CreateDataSource(SHP-FILE-DIR)` creates a new shapefile and the rest of the function adds a layer to the shapefile if the optional keyword arguments `layer_name` and `layer_type` are provided. Both optional keywords must be *string*s, where `layer_name` can be any name for the new layer. `layer_type` must be either `"point"`, `"line"`, or `"polygon"` to create a point, (poly)line, or polygon shapefile, respectively. The function uses the `geometry_dict` *dictionary* to assign the correct `ogr.SHP-TYPE` to the layer. There are more options for extending the `create_shp(...)` function listed on [*pcjericks*' Github pages](https://pcjericks.github.io/py-gdalogr-cookbook/geometry.html).
    """)
    return


@app.cell
def _(ogr):
    import os

    def create_shp(shp_file_dir, overwrite=True, *args, **kwargs):
        """
        :param shp_file_dir: STR of the shapefile path (ends in ".shp")
        :param overwrite: [optional] BOOL - if True, existing files are overwritten
        :kwarg layer_name: [optional] STR of the layer name - if None: no layer will be created
        :kwarg layer_type: [optional] STR ("point", "line", or "polygon") - if None: no layer will be created
        :output: returns an ogr.DataSource
        """
        shp_driver = ogr.GetDriverByName('ESRI Shapefile')
        if os.path.exists(shp_file_dir) and overwrite:
            shp_driver.DeleteDataSource(shp_file_dir)
        new_shp = shp_driver.CreateDataSource(shp_file_dir)
        if kwargs.get('layer_name') and kwargs.get('layer_type'):  # check if output file exists if yes delete it
            geometry_dict = {'point': ogr.wkbPoint, 'line': ogr.wkbMultiLineString, 'polygon': ogr.wkbMultiPolygon}
            try:
                new_shp.CreateLayer(str(kwargs.get('layer_name')), geom_type=geometry_dict[str(kwargs.get('layer_type').lower())])
            except KeyError:  # create and return new shapefile object
                print("Error: Invalid layer_type provided (must be 'point', 'line', or 'polygon').")
            except TypeError:
                print('Error: layer_name and layer_type must be string.')  # create layer if layer_name and layer_type are provided
            except AttributeError:
                print('Error: Cannot access layer - opened in other program?')  # create dictionary of ogr.SHP-TYPES
        return new_shp  # create layer

    return create_shp, os


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The `create_shp` function is also provided with  [flusstools](https://flusstools.readthedocs.io) ([`flusstools.geotools.create_shp()`](https://flusstools.readthedocs.io/en/latest/geotools.html#module-flusstools.geotools.shp_mgmt)) and aids to create a new shapefile (make sure to get the directory right):
    """)
    return


@app.cell
def _(create_shp, os):
    a_new_shp_file = create_shp(r"" + os.getcwd() + "/geodata/shapefiles/new_polygons.shp", layer_name="basemap", layer_type="polygon")

    # release data source
    a_new_shp_file = None
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Important:** A shapefile **field name** may not have more than **10 characters** because attributes are stored in a dBASE table (read more in [Esri's shapefile docs](https://desktop.arcgis.com/en/arcmap/latest/manage-data/shapefiles/geoprocessing-considerations-for-shapefile-output.htm)).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Shapefiles can also be created and drawn in QGIS and the following figures guide through the procedure of creating a polygon shapefile. We will not need the resulting shapefile in this section anymore, but later for making it interact with raster datasets.

    The first step to making a shapefile with QGIS is obviously to run QGIS and create a new project. The following example uses water depth and flow velocity raster data as background information to delineate the so-called [*morphological unit* of *slackwater*](https://www.sciencedirect.com/science/article/pii/S0169555X14000099). Both the water depth and flow velocity rasters are part of the [*River Architect* sample datasets](https://github.com/RiverArchitect/riverarchitect/tree/main/sample-data) (precisely located at [`RiverArchitect/SampleData/01_Conditions/2100_sample/`](https://github.com/RiverArchitect/riverarchitect/tree/main/sample-data/01_Conditions/2100_sample)). After downloading the sample data, they can be imported in QGIS by dragging the files from the **Browser** panel into the *Layers* panel.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Get and Set Shapefile Projections

    The terminology used in the `.prj` files of a shapefile corresponds to the definitions in the [geospatial data](https://hydro-informatics.com/geopy/geospatial-data.html#prj) section. In Python, information about the coordinate system is available through `shp_layer.GetSpatialRef()` of the `ogr` library:
    """)
    return


@app.cell
def _(shp_layer):
    shp_srs = shp_layer.GetSpatialRef()
    print(shp_srs)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This `GEOGCS` definition of the above shapefile corresponds to Esri's *well-known* text (WKT). Since the shapefile format was developed by Esri, Esri's WKT (**esriwkt**) format must be used in `.prj` files. The *Open Geospatial Consortium* (*OGC*) uses a different well-known text in their `EPSG:XXXX` definitions (e.g., available at [spatialreference.org](http://www.spatialreference.org)).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```java
    GEOGCS["WGS 84",
           DATUM["WGS_1984", SPHEROID["WGS84", 6378137, 298.257223563, AUTHORITY["EPSG", "7030"]], AUTHORITY["EPSG","6326"]],
           PRIMEM["Greenwich", 0, AUTHORITY["EPSG", "8901"]],
           UNIT["degree",0.01745329251994328, AUTHORITY["EPSG","9122"]],AUTHORITY["EPSG","4326"]]
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    To redefine or newly define the coordinate system of a shapefile, we can use [spatialreference.org](http://www.spatialreference.org) through Python's default `urllib` library.

    > **Note:** Running the following code block requires an internet connection.
    """)
    return


@app.cell
def _():
    import urllib.request


    # function to get spatialreferences with epsg code
    def get_esriwkt(epsg):    
        # usage get_epsg_code(4326)
        try:
            with urllib.request.urlopen("https://spatialreference.org/ref/epsg/{0}/esriwkt/".format(epsg)) as response:
                return response.read().decode("utf-8").strip()
        except Exception:
            pass
        try:
            with urllib.request.urlopen("https://spatialreference.org/ref/sr-org/epsg{0}-wgs84-web-mercator-auxiliary-sphere/esriwkt/".format(epsg)) as response:
                return response.read().decode("utf-8").strip()
            # sr-org codes are available at "https://spatialreference.org/ref/sr-org/{0}/esriwkt/".format(epsg)
            # for example EPSG:3857 = SR-ORG:6864 -> https://spatialreference.org/ref/sr-org/6864/esriwkt/ = EPSG:3857
        except Exception:
            print("ERROR: Could not find epsg code on spatialreference.org. Returning default WKT(epsg=4326).")
            return 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295],UNIT["Meter",1]]'

    return (get_esriwkt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This function can be used to create a new projection file:
    """)
    return


@app.cell
def _(get_esriwkt):
    # open the hypy-area shapefile
    shp_file = 'hypy-area'
    with open('geodata/shapefiles/{0}.prj'.format(shp_file), 'w') as _prj:
    # create new .prj file for the shapefile (.shp and .prj must have the same name)
        epsg_code = get_esriwkt(4326)
        _prj.write(epsg_code)
        print('Wrote projection file : ' + epsg_code)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    An offline alternative for generating a `.prj` file is the `osr` library that comes along with `gdal`:
    """)
    return


@app.cell
def _():
    from osgeo import osr

    def get_wkt(epsg, wkt_format="esriwkt"):
        default = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295],UNIT["Meter",1]]'
        spatial_ref = osr.SpatialReference()
        try:
            spatial_ref.ImportFromEPSG(epsg)
        except TypeError:
            print("ERROR: epsg must be integer. Returning default WKT(epsg=4326).")
            return default
        except Exception:
            print("ERROR: epsg number does not exist. Returning default WKT(epsg=4326).")
            return default
        if wkt_format=="esriwkt":
            spatial_ref.MorphToESRI()
        # return a nicely formatted WKT string (alternatives: ExportToPCI(), ExportToUSGS(), or ExportToXML())
        return spatial_ref.ExportToPrettyWkt()

    return get_wkt, osr


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Transform (Re-project) a Shapefile

    A re-projection may be needed, for instance, to use a shapefile in `EPSG:4326` (e.g., created with QGIS) in a web-GIS application (e.g., open street maps) that typically uses `EPSG:3857`. To apply a different projection to geometric objects of a shapefile, it is not enough to simply rewrite the `.prj` file. Therefore, the following example shows the re-projection of the `countries.shp` shapefile from the [Natural Earth quick start kit](http://naciscdn.org/naturalearth/packages/Natural_Earth_quick_start.zip). The following workflow performs the reprojection:

    * The shapefile to transform is located in the subdirectory `geodata/shapefiles/countries.shp` and open it in the Python script as described above.
    * Read and identify the spatial reference system used in the input shapefile:
        - Create a spatial reference object with `in_sr = osr.SpatialReference(str(shapefile.GetSpatialRef()))`.
        - Detect the spatial reference system in EPSG format with `AutoIdentifyEPSG()`.
        - Assign the EPSG-formatted spatial reference system to the spatial reference object of the input shapefile (`ImportFromEPSG(int(in_sr.GetAuthorityCode(None)))`).
    * Create the output spatial reference with `out_sr = osr.SpatialReference()` and apply the target EPSG code (`out_sr.ImportFromEPSG(3857)`).
    * Create a coordinate transformation object (`coord_trans = osr.CoordinateTransformation(in_sr, out_sr)`) that enables re-projecting geometry objects later.
    * Create the output polygon shapefile with the above-defined `create_shp` function using `layer_name="basemap"` and `layer_type="polygon"`.
    * Copy the field names and types of the input shapefile:
        - Read the attribute layer from the input file's layer definitions with `in_lyr_def = in_shp_lyr.GetLayerDefn()`
        - Iterate through the field definitions and append them to the output shapefile layer (`out_shp_lyr`)
    * Iterate through the geometry features in the input shapefile:
        - Use the new (output) shapefile's layer definitions (`out_shp_lyr_def = out_shp_lyr.GetLayerDefn()`) to append transformed geometry objects later.
        - Define an iteration variable `in_feature` as an instance of `in_shp_lyr.GetNextFeature`.
        - In a `while` loop, instantiate every geometry (`geometry = in_feature.GetGeometryRef()`) in the input shapefile, transform the `geometry` (`geometry.Transform(coord_trans)`), convert it to an `ogr.Feature()` with the `SetGeometry(geometry)` method, copy field values (nested `for`-loop), and append the new feature to the output shapefile layer (`out_shp_lyr.CreateFeature(out_feature)`).
        - At the end of the `while`-loop, look for the next feature in the input shapefile's attributes with `in_feature = in_shp_lyr.GetNextFeature()`
    * Release all layer and dataset references by assigning `None` so the dataset closes and pending writes are flushed.
    * Assign the new projection EPSG:3857 using the above-defined `get_wkt` function.
    """)
    return


@app.cell
def _(create_shp, get_wkt, ogr, os, osr):
    _shp_driver = ogr.GetDriverByName('ESRI Shapefile')
    in_shp = _shp_driver.Open('' + os.path.abspath('') + '/geodata/shapefiles/countries.shp')
    in_shp_lyr = in_shp.GetLayer()
    in_sr = osr.SpatialReference(str(in_shp_lyr.GetSpatialRef()))
    in_sr.AutoIdentifyEPSG()
    in_sr.ImportFromEPSG(int(in_sr.GetAuthorityCode(None)))
    out_sr = osr.SpatialReference()
    out_sr.ImportFromEPSG(3857)
    coord_trans = osr.CoordinateTransformation(in_sr, out_sr)
    out_shp = create_shp('' + os.path.abspath('') + '/geodata/shapefiles/countries-web.shp', layer_name='basemap', layer_type='polygon')
    out_shp_lyr = out_shp.GetLayer()
    in_lyr_def = in_shp_lyr.GetLayerDefn()
    for i in range(0, in_lyr_def.GetFieldCount()):
        out_shp_lyr.CreateField(in_lyr_def.GetFieldDefn(i))
    out_shp_lyr_def = out_shp_lyr.GetLayerDefn()
    in_feature = in_shp_lyr.GetNextFeature()
    while in_feature:
        geometry = in_feature.GetGeometryRef()
        geometry.Transform(coord_trans)
        out_feature = ogr.Feature(out_shp_lyr_def)
        out_feature.SetGeometry(geometry)
        for i in range(0, out_shp_lyr_def.GetFieldCount()):
            out_feature.SetField(out_shp_lyr_def.GetFieldDefn(i).GetNameRef(), in_feature.GetField(i))
        out_shp_lyr.CreateFeature(out_feature)
        in_feature = in_shp_lyr.GetNextFeature()
    in_shp = None
    in_shp_lyr = None
    out_shp = None
    out_shp_lyr = None
    with open('' + os.path.abspath('') + '/geodata/shapefiles/countries-web.prj', 'w+') as _prj:
        _prj.write(get_wkt(3857))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Challenge:** Re-write the above code block in a `re_project(shp_file, target_epsg)` function.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    In the case of success, the code sequence `in_sr.AutoIdentifyEPSG()` returns `0` (i.e., it successfully recognized the `EPSG` number), but unfortunately, many EPSG numbers are not known to `AutoIdentifyEPSG()`. In the case that `AutoIdentifyEPSG()` did not function properly, the method does not return `0`, but `7`, for example. A workaround for the limited functionality of `srs.AutoIdentifyEPSG()` is `srs.FindMatches`. `srs.FindMatches` returns a *matching* `srs_match` from a larger database, which is somewhat nested; for instance, use:<br>

    ```python
    matches = srs.FindMatches()
    ```

    Then, `matches` looks like this: `[(osgeo.osr.SpatialReference, INT)]`. Therefore, a complete workaround for `srs.AutoIdentifyEPSG()` (or `in_sr.AutoIdentifyEPSG()` in the code block above) looks like this:
    """)
    return


@app.cell
def _(osr):
    # set epsg and create spatial reference object
    epsg = 3857
    srs = osr.SpatialReference()
    srs.ImportFromEPSG(epsg)

    # identify spatial reference
    auto_detect = srs.AutoIdentifyEPSG()
    if auto_detect != 0:
        srs = srs.FindMatches()[0][0]  # Find matches returns list of tuple of SpatialReferences
        srs.AutoIdentifyEPSG()  # Re-perform auto-identification
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Add Fields and Point Features to a Shapefile

    A shapefile feature can be a point, a line, or a polygon, which has field attributes (e.g., `"id"=1` to describe that this is polygon number 1 or associated to an `id` block 1). Field attributes can be more than just an *ID*entifier and include, for example, the polygon area or city labels as in the above-shown example illustrating *iws_va.shp* (`shp_driver.Open("geodata/shapefiles/iws_va.shp")`).

    To **create a point shapefile**, we can use the above-introduced `create_shp` function (or `flusstools.geotools.create_shp(shp_file_dir="\")`) and set the projection with the `get_wkt()` function (also above introduced). The following code block shows the usage of both functions to create a *river.shp* point shapefile that contains three points located at three rivers in central Europe. The code block also illustrates the creation of a field in the attribute table and the creation of three point features. Here is how the code works:

    * The shapefile is located in the `rivers_pts` variable. Note that the `layer_type` already determines the type of geometries that can be used in the shapefile. For instance, adding a line or polygon feature to an `ogr.wkbPoint` layer will result in an `ERROR 1` message.
    * The `basemap` (layer) is attributed to the variable `lyr = river_pts.GetLayer()`.
    * A *string*-type field is added and appended to the attribute table:
        - instantiate a new field with `field_gname = ogr.FieldDefn("FIELD-NAME", ogr.OFTString)` (recall: the field name may not have more than 10 characters!)
        - append the new field to the shapefile with `lyr.CreateField(field_gname)`
        - other field types than `OFTString` can be: `OFTInteger`, `OFTReal`, `OFTDate`, `OFTTime`, `OFTDateTime`, `OFTBinary`, `OFTIntegerList`, `OFTRealList`, or `OFTStringList`.
    * Add three points stored in `pt_names = {RIVER-NAME: (x-coordinate, y-coordinate)}` in a loop over the dictionary keys:
        - for every new point, create a feature as a child of the layer definitions with `feature = ogr.Feature(lyr.GetLayerDefn())`
        - set the value of the field name for every point with `feature.SetField(FIELD-NAME, FIELD-VALUE)`
        - create a string of the new point in WKT format with `wkt = "POINT(X-COORDINATE Y-COORDINATE)"`
        - convert the WKT-formatted point into a point-type geometry with `point = ogr.CreateGeometryFromWkt(wkt)`
        - set the new point as the new feature's geometry with `feature.SetGeometry(point)`
        - append the new feature to the layer with `lyr.CreateFeature(feature)`
    * Unlock (release) the shapefile by overwriting the `lyr` and `river_pts` variable with `None`.

    > **Important:** Release the `lyr` and `river_pts` references (here by assigning `None`) so the dataset closes and pending writes are flushed.
    """)
    return


@app.cell
def _(create_shp, get_wkt, ogr, os):
    _shp_dir = '' + os.path.abspath('') + '/geodata/shapefiles/rivers.shp'
    river_pts = create_shp(_shp_dir, layer_name='basemap', layer_type='point')
    with open(_shp_dir.split('.shp')[0] + '.prj', 'w+') as _prj:
    # create .prj file for the shapefile for web application references
        _prj.write(get_wkt(3857))
    _lyr = river_pts.GetLayer()
    field_gname = ogr.FieldDefn('rivername', ogr.OFTString)
    # get basemap layer
    _lyr.CreateField(field_gname)
    pt_names = {'Aare': (916136.03, 6038687.72), 'Ain': (623554.12, 5829154.69), 'Inn': (1494878.95, 6183793.83)}
    # add string field "rivername"
    for n in pt_names.keys():
        pt_feature = ogr.Feature(_lyr.GetLayerDefn())
        pt_feature.SetField('rivername', n)
    # names and coordinates of central EU rivers in EPSG:3857 WG84 / Pseudo-Mercator
        _wkt = 'POINT(%f %f)' % (float(pt_names[n][0]), float(pt_names[n][1]))
        _point = ogr.CreateGeometryFromWkt(_wkt)
        pt_feature.SetGeometry(_point)
        _lyr.CreateFeature(pt_feature)
    # add the three rivers as points to the basemap layer
    _lyr = None
    # release files
    river_pts = None  # create Feature as child of the layer  # define value n (river) in the rivername field  # use WKT format to add a point geometry to the Feature  # append the new feature to the basemap layer
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The resulting `rivers.shp` shapefile can be imported in QGIS along with a DEM from the [Natural Earth quick start kit](http://naciscdn.org/naturalearth/packages/Natural_Earth_quick_start.zip).

    ![img](https://hydro-informatics.com/_images/qgis-rivers.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Multiline (Polyline) Shapefile

    Similar to the procedure for creating and adding points to a new point shapefile, a (multi) line (or polyline) can be added to a shapefile. The `create_shp` function creates a multi-line shapefile when the layer type is defined as `"line"` (`flusstools.geotools.create_shp(shp_file_dir="\", layer_type="line")`). The coordinate system is created with the above-defined `get_wkt()` function.

    > **Tip:** The term *multi-line* is used in *OGC* and `ogr`, while *polyline* is used in Esri GIS environments.

    The following code block uses the coordinates of cities along the Rhine River, stored in a *dictionary* named `station_names`. The city names are not used and only the coordinates are appended with `line.AddPoint(X, Y)`. As before, a field is created to give the river a name. The actual line feature is again created as a child of the layer with `line_feature = ogr.Feature(lyr.GetLayerDefn())`. Running this code block produces a line that approximately follows the Rhine River between France and Germany.
    """)
    return


@app.cell
def _(create_shp, get_wkt, ogr, os):
    _shp_dir = '' + os.path.abspath('') + '/geodata/shapefiles/rhine_proxy.shp'
    rhine_line = create_shp(_shp_dir, layer_name='basemap', layer_type='line')
    with open(_shp_dir.split('.shp')[0] + '.prj', 'w+') as _prj:
    # create .prj file for the shapefile for web application references
        _prj.write(get_wkt(3857))
    _lyr = rhine_line.GetLayer()
    station_names = {'Basel': (844361.68, 6035047.42), 'Kembs': (835724.27, 6056449.76), 'Breisach': (842565.32, 6111140.43), 'Rhinau': (857547.04, 6158569.58), 'Strasbourg': (868439.31, 6203189.68)}
    # get basemap layer
    line = ogr.Geometry(ogr.wkbLineString)
    for stn in station_names.values():
    # coordinates for EPSG:3857 WG84 / Pseudo-Mercator
        line.AddPoint(stn[0], stn[1])
    field_name = ogr.FieldDefn('river', ogr.OFTString)
    _lyr.CreateField(field_name)
    line_feature = ogr.Feature(_lyr.GetLayerDefn())
    line_feature.SetGeometry(line)
    line_feature.SetField('river', 'Rhine')
    # create line object and add points from station names
    _lyr.CreateFeature(line_feature)
    _lyr = None
    # create field named "river"
    # create feature, geometry, and field entry
    # add feature to layer
    rhine_line = None
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The resulting `rhine_proxy.shp` shapefile can be imported in QGIS along with a DEM and the cities point shapefile from the [Natural Earth quick start kit](http://naciscdn.org/naturalearth/packages/Natural_Earth_quick_start.zip).

    ![img](https://hydro-informatics.com/_images/qgis-rhine.png)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Polygon Shapefile

    Polygons are surface patches that can be created point-by-point, line-by-line, or from a `"Multipolygon"` WKB definition. When creating polygons from points or lines, we want to create a surface and this is why the corresponding geometry type is called `wkbLinearRing` for building polygons from both points or lines (rather than `wkbPoint` or `wkbLine`, respectively). The following code block features an example for building a polygon shapefile delineating the hydraulic laboratory of the University of Stuttgart. The difference between the above example for creating a line shapefile are:

    * The projection is `EPSG:4326`.
    * The point coordinates are generated within an `ogr.wkbLinearRing` object step-by-step rather than in a loop over *dictionary* entries.
    * File, variable, and field names.
    """)
    return


@app.cell
def _(create_shp, get_wkt, ogr, os):
    _shp_dir = '' + os.path.abspath('') + '/geodata/shapefiles/va4wasserbau.shp'
    va_geo = create_shp(_shp_dir, layer_name='basemap', layer_type='polygon')
    with open(_shp_dir.split('.shp')[0] + '.prj', 'w+') as _prj:
    # create .prj file for the shapefile for GIS map applications
        _prj.write(get_wkt(4326))
    _lyr = va_geo.GetLayer()
    pts = ogr.Geometry(ogr.wkbLinearRing)
    # get basemap layer
    pts.AddPoint(9.103686, 48.744251)
    pts.AddPoint(9.104689, 48.744198)
    # create polygon points
    pts.AddPoint(9.104667, 48.74396)
    pts.AddPoint(9.103557, 48.744009)
    pts.AddPoint(9.103686, 48.744251)
    poly = ogr.Geometry(ogr.wkbPolygon)
    poly.AddGeometry(pts)
    field = ogr.FieldDefn('building', ogr.OFTString)  # close the ring
    _lyr.CreateField(field)
    # create polygon geometry
    poly_feature_defn = _lyr.GetLayerDefn()
    # build polygon geometry from points
    poly_feature = ogr.Feature(poly_feature_defn)
    poly_feature.SetGeometry(poly)
    # add field to classify building type
    poly_feature.SetField('building', 'Versuchsanstalt')
    _lyr.CreateFeature(poly_feature)
    _lyr = None
    va_geo = None
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Build Shapefile from JSON

    Loading geometry data from in-line defined variables is cumbersome in practice, where geospatial data are often provided on public platforms (e.g., land use or cover).  The following example uses a JSON file generated with map service data from the [Baden-Württemberg State Institute for the Environment, Survey and Nature Conservation (LUBW)](https://udo.lubw.baden-wuerttemberg.de/), where polygon nodes are stored in WKT polygon geometry format  (`"MultiPolygon (((node1_x node1_y, nodej_x, nodej_y, ... ...)))"`):

    * The JSON file ([download hq100-dreisam.json](https://raw.githubusercontent.com/hydro-informatics/jupyter-python-course/main/geodata/json/hq100-dreisam.json) and save it to a subdirectory called `/geodata/json/`) is read with [pandas](https://hydro-informatics.com/python-basics/pynum.html#pandas) and the shapefile is created, as before, with the `create_shp` function.
    * The projection is `EPSG:25832`.
    * Two fields are added in the form of
        - `"tbg_name"` (the original string name of the polygons in the LUBW data), and
        - `"area"` (a real number field, in which the polygon area is calculated in m<sup>2</sup> using `polygon.GetArea()`).
    * The polygon geometries are derived from the WKT-formatted definitions in the `"wkt_geom"` field of the pandas dataframe object `dreisam_inundation`.
    """)
    return


@app.cell
def _(create_shp, get_wkt, ogr, os):
    # get data from json file
    import pandas as pd
    dreisam_inundation = pd.read_json('' + os.path.abspath('') + '/geodata/json/hq100-dreisam.json')
    _shp_dir = '' + os.path.abspath('') + '/geodata/shapefiles/dreisam_hq100.shp'
    # create shapefile
    dreisam_hq100 = create_shp(_shp_dir, layer_name='basemap', layer_type='polygon')
    with open(_shp_dir.split('.shp')[0] + '.prj', 'w+') as _prj:
        _prj.write(get_wkt(25832))
    # create .prj file for the shapefile for GIS map applications
    _lyr = dreisam_hq100.GetLayer()
    _lyr.CreateField(ogr.FieldDefn('tbg_name', ogr.OFTString))
    _lyr.CreateField(ogr.FieldDefn('area', ogr.OFTReal))
    # get basemap layer
    for _wkt, tbg in zip(dreisam_inundation['wkt_geom'], dreisam_inundation['TBG_NAME']):
        feature = ogr.Feature(_lyr.GetLayerDefn())
    # add string field "tbg_name"
        feature.SetField('tbg_name', tbg)
        polygon = ogr.CreateGeometryFromWkt(_wkt)
    # add string field "area"
        feature.SetField('area', polygon.GetArea())
        feature.SetGeometry(polygon)
        _lyr.CreateFeature(feature)
    _lyr = None  # create Feature as child of the layer
    dreisam_hq100 = None  # assign tbg_name  # use WKT format to add a polygon geometry to the Feature  # define default value of 0 to the area field  # append the new feature to the basemap layer
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Tip:** Open the new `dreisam_hq100.shp` in QGIS and explore the attribute table.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    GeoJSON text can also be used to create an `ogr.Geometry` with `ogr.CreateGeometryFromJson(GEOJSON_TEXT)`:
    """)
    return


@app.cell
def _(ogr):
    geojson_data = '{"type":"Point","coordinates":[1013452.282805,6231540.674235]}'
    _point = ogr.CreateGeometryFromJson(geojson_data)
    print('X=%d, Y=%d (EPSG:3857)' % (_point.GetX(), _point.GetY()))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Calculate Geometric Attributes

    The above code block illustrates the usage of `polygon.GetArea()` to calculate the polygon area in m<sup>2</sup>. The `ogr` library provides many more functions to calculate geometric attributes of features and here is a summary:

    * Unify multiple polygons <br>
        `wkt_... = ...`<br>
        `polygon_a = ogr.CreateGeometryFromWkt(wkt_1)`<br>
        `polygon_b = ogr.CreateGeometryFromWkt(wkt_2)`<br>
        `polygon_union = polygon_a.Union(polygon_b)`
    * Intersect two polygons <br>
        `polygon_intersection = polygon_a.Intersection(polygon_b)`
    * Envelope (minimum and maximum extents) of a polygon <br>
        `env = polygon.GetEnvelope()` <br>
        `print("minX: %d, minY: %d, maxX: %d, maxY: %d" % (env[0], env[2], env[1], env[3]))`
    * Convex hull (envelope surface) of multiple geometries (points, lines, polygons) <br>
        `all_polygons = ogr.Geometry(ogr.wkbGeometryCollection)`<br>
        `for feature in POLYGON-SOURCE-LAYER: all_polygons.AddGeometry(feature.GetGeometryRef())`<br>
        `convexhull = all_polygons.ConvexHull()`<br>
        Save `convexhull` to shapefile (use the `create_shp` function as shown in the above examples or read more at [pcjericks' Github pages](https://pcjericks.github.io/py-gdalogr-cookbook/vector_layers.html#save-the-convex-hull-of-all-geometry-from-an-input-layer-to-an-output-layer))<br>
        Tip: To create a tight hull (e.g., of a point cloud), look for `concavehull` functions.
    * Length (of a line) <br>
        `wkt = "LINESTRING (415128.5 5320979.5, 415128.6 5320974.5, 415129.75 5320974.7)"`<br>
        `line = ogr.CreateGeometryFromWkt(wkt)`<br>
        `print("Length = %d" % line.Length())`
    * Area (of a polygon):  `polygon.GetArea()` (see above example)
    * Example to calculate [centroid coordinates of polygons](https://pcjericks.github.io/py-gdalogr-cookbook/geometry.html#quarter-polygon-and-create-centroids).

    > **Tip:** Geometric methods use the geometry's coordinate values directly. Thus, `GetArea()` returns square coordinate units (for example, m<sup>2</sup> only when the coordinates use meters). A `.prj` file documents the CRS but does not make `GetArea()` reproject the geometry.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Export to Other Formats

    The above examples deal with `.shp` files only, but other formats can be useful (e.g., to create web applications or export to *Google Earth*). To this end, the following paragraphs illustrate the creation of GeoJSON and KML files. Several other conversions can be performed, not only between file formats but also between feature types. For instance, polygons can be created from point clouds (among others with the `ConvexHull` method mentioned above). Interested students can learn more about conversions in [Michael Diener's *Python Geospatial Analysis Cookbook*](https://github.com/mdiener21/python-geospatial-analysis-cookbook).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
 
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### GeoJSON
    GeoJSON files can be easily created as before, even without activating a driver:
    """)
    return


@app.cell
def _(ogr, os):
    _triangle = ogr.Geometry(ogr.wkbLinearRing)
    _triangle.AddPoint(-11717151.498691, 2356192.894805)
    _triangle.AddPoint(-11717120.446149, 2355586.175893)
    _triangle.AddPoint(-11719392.059083, 2354012.050842)
    polygon_1 = ogr.Geometry(ogr.wkbPolygon)
    polygon_1.AddGeometry(_triangle)
    with open('' + os.path.abspath('') + '/geodata/geojson/pitillal-triangle.geojson', 'w+') as _gjson:
        _gjson.write(polygon_1.ExportToJson())
    return (polygon_1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    For more robust file handling and defining a projection, activate the driver `ogr.GetDriverByName("GeoJSON")`. Thus, the creation and manipulation of GeoJSON files work similarly to the shapefile handlers shown above.
    """)
    return


@app.cell
def _(ogr, osr, polygon_1):
    gjson_driver = ogr.GetDriverByName('GeoJSON')
    sr = osr.SpatialReference()
    sr.ImportFromEPSG(3857)
    _gjson = gjson_driver.CreateDataSource('pitillal-full.geojson')
    gjson_lyr = _gjson.CreateLayer('pitillal-full.geojson', geom_type=ogr.wkbPolygon, srs=sr)
    feature_def = gjson_lyr.GetLayerDefn()
    new_feature = ogr.Feature(feature_def)
    new_feature.SetGeometry(polygon_1)
    gjson_lyr.CreateFeature(new_feature)
    _gjson = None
    gjson_lyr = None
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### KML (Google Earth)
    To display point, line, or polygon features in Google Earth, features can be plugged into Google's [KML](https://developers.google.com/kml/documentation/kml_tut) (Keyhole Markup Language), similar to the creation of a GeoJSON file, and with the function `geometry.ExportToKML`:
    """)
    return


@app.cell
def _(ogr, os):
    _triangle = ogr.Geometry(ogr.wkbLinearRing)
    _triangle.AddPoint(-11717151.498691, 2356192.894805)
    _triangle.AddPoint(-11717120.446149, 2355586.175893)
    _triangle.AddPoint(-11719392.059083, 2354012.050842)
    polygon_2 = ogr.Geometry(ogr.wkbPolygon)
    polygon_2.AddGeometry(_triangle)
    with open('' + os.path.abspath('') + '/geodata/pitillal-triangle.kml', 'w+') as _gjson:
        _gjson.write(polygon_2.ExportToKML())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Moreover, similar to GeoJSON files and shapefiles, KML files can be generated more robustly (with a defined projection, for example). All you need to do is initiating the KML driver (`kml_driver = ogr.GetDriverByName("KML")`) and define a KML data source (`kml_file = kml_driver.CreateDataSource(FILENAME.KML)`).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Exercise:** Familiarize with shapefile handling in the [geospatial ecohydraulics](https://hydro-informatics.com/exercises/ex-geco) exercise.
    """)
    return


if __name__ == "__main__":
    app.run()
