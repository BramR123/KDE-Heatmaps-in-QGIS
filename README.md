# Heatmaps-in-QGIS
A PyQGIS script for creating aesthetic heatmaps in a safe way.

This PyQGIS script creates heatmaps from .csv point data in a safe way through the use of voronoi masking. The script can be executed in the Python extension in QGIS. 
The novelty of this methodology can be found in its adaptive data obfuscation techniques, ensuring the geo-privacy of single data points.

Please check the workflow below, together with the [tutorial](https://github.com/BramR123/Heatmaps-in-QGIS/blob/main/Tutorial/README.md) to fully understand the functionality of the provided code.

## Workflow
![alt text](https://github.com/BramR123/Heatmaps-in-QGIS/blob/main/Workflow.jpg?raw=true)

## Script usage
Several things need to be adjusted to your personal preferences before running the script. Be sure to follow the following steps BEFORE running the code:
1. Double check your csv file(s): Make sure that there are no empty records and you use the correct decimals
2. Define home directory: This is the place where you put your .csv file(s) (and nothing else)
3. Define colors: This could either be one color for all maps, or you could specify a list of colors
4. Define .csv layer features, such as: delimiter of the .csv file(s), the Latitude (Y) and Longitude (X) column headers
5. Define classes: This is based on your preferences on classifying the data.
6. Define heatmap characteristics: Based on the type of CRS you are using, you should modify the heatmap radius and resolution according to the set example in the script itself.

## Good to know
- If you do NOT want to include voronoi masking in your heatmap, you can exclude the voronoi part of the script. In that case, make sure that you directly use the point layer for the Kernel Density Estimation.
- If you want to modify pieces of the code, feel free to branch from this repository.
- Any questions? Feel free to adress an issue.
