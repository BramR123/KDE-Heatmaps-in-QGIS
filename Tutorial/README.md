# Tutorial

In this folder, a short tutorial including test datasets can be found and a working example will be given.

The folder comprises of two datasets; one with the locations of earthquakes from the years 1950 to 2000, and another dataset with locations of earthquakes from the year 2000 up until 2021.
Besides the location and the year of the earthquake, the magnitude column is also taken into account, resulting in a bigger kernel weight when the magnitude is higher.
The dataset is obtained and configured from the [Significant Earthquake Database](http://www.qgistutorials.com/en/).
For the sake of testing with the script, the dataset has been split in two, so that two heatmaps can be created simultaneously.

***Disclaimer: The main goal of the script is to create heatmaps safely on a smaller scale (e.g., municipality/province). For a broader understanding of the data obfuscation part, a global scale is used for the example dataset.***

## Getting started
You can load the script directly into the Python extension in QGIS. However, several things need to be adjusted to your personal preferences before running the script. Be sure to follow the following steps BEFORE running the code:

1. Double check your csv file(s): Make sure that there are no empty records and you use the correct decimals
2. Define home directory: This is the place where you put your .csv file(s) (and nothing else)
3. Define colors: This could either be one color for all maps, or you could specify a list of colors
4. Define .csv layer features, such as: delimiter of the .csv file(s), the Latitude (Y) and Longitude (X) column headers
5. Define classes: This is based on your preferences on classifying the data.
6. Define heatmap characteristics: Based on the type of CRS you are using, you should modify the heatmap radius and resolution according to the set example in the script itself.

## Heatmap output
The code produces numerous files while creating the heatmap. These are, for your convenience, not directly loaded into your map. In this section, a brief explanation will be given on [voronoi masking](https://www.sciencedirect.com/science/article/pii/S0143622815001666).

After creating a heatmap with the test data (using a heatmap radius of 10 and a heatmap resolution of 0.1) the following heatmap is created:

![Heatmap](https://github.com/BramR123/Heatmaps-in-QGIS/blob/main/Tutorial/EQ_heatmap.PNG?raw=true)

The original dataset however had other 'starting points' than that the heatmap is displaying. The voronoi polygons (orange) have been plotted together with the original earthquake locations (red) and the shifted earthquake locations (green) in the map below:
![Heatmap_voronoi](https://github.com/BramR123/Heatmaps-in-QGIS/blob/main/Tutorial/EQ_heatmap_voronoi.PNG?raw=true)

## To conclude...
As can be seen, the points in the high density earthquake cluster around Greece, Turkey, and Iran have been shifting a little due to the voronoi masking. It is not really necessary to 'obfuscate' the data too much, as noise is already created by the numerous points around this location. On the other hand, there is also a red original data point around The Maldives, that shifted to just in front of the coast of Sri Lanka. This is due to the lower point density in that specific area. Now, in this case, it is indeed weird to be moving an earthquake several hundreds of kilometers, as the scale is quite small and the original data is not very vulnerable. However, with more vulnerable/local datasets, the main goal of voronoi masking is to provide an adaptive data obfuscation, making it more difficult to trace back to a single household or company. It is not only the voronoi masking that obfuscates the data. Also the kernel density estimation, together with the reclassification of the data, cater for even more geo-privacy. Still, caution should be taken when publishing maps with sensitive information.
