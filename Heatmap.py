##Import modules## 
import processing
import numpy as np 
from osgeo import gdal, gdal_array
from qgis.PyQt.QtCore import QSettings
import os

##Define home directory##
##Please note that the folder should only contain the input csv file(s)##
folder = "C:/Documents/csv_folder/"

##Define desired color for the heatmap##
##Please note that the color list should be as long as the number of csv files in the input folder if you want to have different colors for the different heatmaps##
##It is also possible to only enter one color when all heatmaps should be the same color##
##The colors can be red, blue, green and purple and should be written in lower case##
color_lis = ["blue"]


def make_heatmap(folder, color_lis):
    """
    This  function loops simultaneously over the csv file(s) and the color list. 
    First, the csv file is converted to a point layer.
    On this point layer, Voronoi Masking is applied to obfuscate the original data for safety reasons.
    With the new point layer, a Kernel Density Estimation (KDE) is performed.
    The KDE result is then classified based on user defined boundaries.
    The function returns heatmaps of the input file(s). 
    
    Before execution, several parameters need to be defined or changed based on user needs. 
    The exact steps can be found in the README documentation on GitHub: BramR123/Heatmaps-in-QGIS/README.md.
    """

    if len(color_lis) == 1:
        color_lis = color_lis * len(os.listdir(folder))


    for filename, color in zip(os.listdir(folder), color_lis):

        ##CSV layer features##
        delimiter = ";"
        Xcoor = "X"
        Ycoor = "Y"

        ##Output layer paths & names## 
        Output_layer = folder + filename.split(".")[0] + ".tif"
        Desired_layer_name = filename.split(".")[0]

        ##Define percentile classes (DEFAULT EQUAL INTERVAL: 80, 60, 40, 20, 0)##
        CLASSES = [80, 60, 40, 20, 0]

        ##Define heatmap characteristics##
        ##This section defines the heatmap weight column name, radius & resolution.##
        ##Depending on the crs of the data there are a few options:##
        ##WGS 84:     Municipality default radius & resolution: 0.01 & 0.0005##
        ##WGS 84:     Province default radius & resolution:     0.1 & 0.001##
        ##Amersfoort: Municipality default radius & resolution: 500 & 20##
        ##Amersfoort: Province default radius & resolution:     5000 & 100##

        HMweight = 'Aantal'
        HMradius = 500
        HMres = 20

        #############################################
        #                                           #
        #  NO NEED TO MODIFY CODE BELOW THIS POINT  #
        #                                           #
        #############################################

        ##Prepare settings##
        QSettings().setValue("/app/projections/unknownCrsBehavior", 'UseProjectCrs')

        ##Adding vector point layer from csv##
        uri = "file://" + folder + filename + "?delimiter={}&xField={}&yField={}".format(delimiter, Xcoor, Ycoor)
        vlayer = QgsVectorLayer(uri, folder + filename.split(".")[0] + "Point_layer.shp", "delimitedtext")
        QgsProject.instance().addMapLayer(vlayer)

        ##Create voronoi polygons##
        processing.run(
        "qgis:voronoipolygons",
            {
                'BUFFER' : 0, 
                'INPUT' : folder + filename.split(".")[0] + "Point_layer.shp", 
                'OUTPUT' : folder + filename.split(".")[0] +"VM_polygons.shp"
            }
        )

        ##Convert voronoi polygons to lines##
        processing.run(
            "qgis:polygonstolines",
            {
                'INPUT' : folder + filename.split(".")[0] + "VM_polygons.shp",
                'OUTPUT' : folder + filename.split(".")[0] + "VM_lines.shp"
            }
        )

        ##Snap original points to voronoi knots##
        processing.run(
            "qgis:snapgeometries",
            {
                'BEHAVIOR' : 4,
                'INPUT' : folder + filename.split(".")[0] + "Point_layer.shp",
                'OUTPUT' : folder + filename.split(".")[0] + "Point_layer_VM.shp",
                'REFERENCE_LAYER' : folder + filename.split(".")[0] + "VM_lines.shp",
                'TOLERANCE' : 2000 
            }
        )

        ##Perform KDE with snapped points##
        processing.run(
            "qgis:heatmapkerneldensityestimation",
            {
                'DECAY': 0,
                'INPUT': folder + filename.split(".")[0] + "Point_layer_VM.shp",
                'KERNEL': 0,
                'OUTPUT': folder + filename.split(".")[0] + "KDE_VM.sdat", 
                'OUTPUT_VALUE': 0,
                'PIXEL_SIZE': HMres,
                'RADIUS': HMradius,
                'RADIUS_FIELD': None,
                'WEIGHT_FIELD': HMweight
            }
        )

        ##Perform reclassify with predefined CLASSES##
        dataset = gdal.Open(folder + filename.split(".")[0] + "KDE_VM.sdat")
        a = dataset.ReadAsArray()
        output = np.zeros_like(a).astype(np.uint8)

        na = a[a != -9999]

        P = {}
        for perc in CLASSES:
            percentile_array = np.percentile(na, perc)
            P[perc] = percentile_array

        F = {}
        for i, perc in enumerate(reversed(CLASSES)):
            output = np.where(a > P[perc], i+1, output)
            F[perc] = output

        gdal_array.SaveArray(output, Output_layer, "gtiff", prototype=dataset)

        ##Set symbology and load result to map##
        Final_result = iface.addRasterLayer(Output_layer, Desired_layer_name, "gdal")

        stats = Final_result.dataProvider().bandStatistics(1, QgsRasterBandStats.All)
        value0 = 0
        value1 = 1
        value2 = 2
        value3 = 3
        value4 = 4
        value5 = 5

        fnc = QgsColorRampShader()
        fnc.setColorRampType(QgsColorRampShader.Exact)

        red = [
        QgsColorRampShader.ColorRampItem(value0, QColor(255, 255, 255)),
        QgsColorRampShader.ColorRampItem(value1, QColor(255, 197, 151)),
        QgsColorRampShader.ColorRampItem(value2, QColor(248, 159, 107)),
        QgsColorRampShader.ColorRampItem(value3, QColor(231, 77, 21)),
        QgsColorRampShader.ColorRampItem(value4, QColor(192, 31, 38)),
        QgsColorRampShader.ColorRampItem(value5, QColor(130, 0, 30))]

        blue = [
        QgsColorRampShader.ColorRampItem(value0, QColor(255, 255, 255)),
        QgsColorRampShader.ColorRampItem(value1, QColor(192, 231, 255)),
        QgsColorRampShader.ColorRampItem(value2, QColor(119, 203, 229)),
        QgsColorRampShader.ColorRampItem(value3, QColor(61, 149, 212)),
        QgsColorRampShader.ColorRampItem(value4, QColor(34, 86, 160)),
        QgsColorRampShader.ColorRampItem(value5, QColor(20, 53, 100))]

        green = [
        QgsColorRampShader.ColorRampItem(value0, QColor(255, 255, 255)),
        QgsColorRampShader.ColorRampItem(value1, QColor(237, 240, 199)),
        QgsColorRampShader.ColorRampItem(value2, QColor(201, 222, 133)),
        QgsColorRampShader.ColorRampItem(value3, QColor(133, 188, 34)),
        QgsColorRampShader.ColorRampItem(value4, QColor(52, 138, 58)),
        QgsColorRampShader.ColorRampItem(value5, QColor(15, 95, 52))]

        purple = [
        QgsColorRampShader.ColorRampItem(value0, QColor(255, 255, 255)),
        QgsColorRampShader.ColorRampItem(value1, QColor(248, 193, 217)),
        QgsColorRampShader.ColorRampItem(value2, QColor(227, 140, 191)),
        QgsColorRampShader.ColorRampItem(value3, QColor(190, 62, 142)),
        QgsColorRampShader.ColorRampItem(value4, QColor(140, 23, 112)),
        QgsColorRampShader.ColorRampItem(value5, QColor(73, 0, 69))]

        if color == "red":
            fnc.setColorRampItemList(red)
        elif color == "blue":
            fnc.setColorRampItemList(blue)
        elif color == "green":
            fnc.setColorRampItemList(green)
        elif color  == "purple":
            fnc.setColorRampItemList(purple)

        shader = QgsRasterShader()
        shader.setRasterShaderFunction(fnc)

        renderer = QgsSingleBandPseudoColorRenderer(Final_result.dataProvider(), 1, shader)
        Final_result.setRenderer(renderer)

##Call function to create heatmap##        
make_heatmap(folder, color_lis)
