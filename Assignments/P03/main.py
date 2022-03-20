#################################################################
## Name - Ethan Coyle                                           #
## Inst.- Dr. Griffin                                           #
## P03  - Graphic vornoi                                        #
##                                                              #
## The purpose of this assignment is to read in the data from   #
## the cities.csv file and the data for the gities.geojson and  #
## create a voronoi of the ufo data and the city boundaries     #
#################################################################

########################################################
# ██╗███╗   ███╗██████╗  ██████╗ ██████╗ ████████╗███████╗ #
# ██║████╗ ████║██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝  #
# ██║██╔████╔██║██████╔╝██║   ██║██████╔╝   ██║   ███████╗ #
# ██║██║╚██╔╝██║██╔═══╝ ██║   ██║██╔══██╗   ██║   ╚════██║ #
# ██║██║ ╚═╝ ██║██║     ╚██████╔╝██║  ██║   ██║   ███████║ #
# ╚═╝╚═╝     ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝ #
#########################################################
import numpy as np # our numpy array read in as np
import pandas as pd # our pandas read in as pd
import geopandas as gdp # geopandas dataframs as gdp
import json # for the json output
import shapely # for the shapeley diagram stuff
import matplotlib.pyplot as plt # plotting out the data

# other imports for our data sing geovornoi for the voronoi diagram
from shapely.ops import unary_union
from geovoronoi import voronoi_regions_from_coords, points_to_coords
from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area

##########################################################
# ███████╗██╗██╗     ███████╗███████╗    ██╗    ██╗ ██████╗  #
# ██╔════╝██║██║     ██╔════╝██╔════╝    ██║   ██╔╝██╔═══██╗ #
# █████╗  ██║██║     █████╗  ███████╗    ██║  ██╔╝ ██║   ██║ #
# ██╔══╝  ██║██║     ██╔══╝  ╚════██║    ██║ ██╔╝  ██║   ██║ #
# ██║     ██║███████╗███████╗███████║    ██║██╔╝   ╚██████╔╝ #
# ╚═╝     ╚═╝╚══════╝╚══════╝╚══════╝    ╚═╝╚═╝     ╚═════╝  #
###########################################################
                                                          
#We need to open up our file to be read in and used inside of main
try:
  USBorderShape=gdp.read_file("us_border.shp") # us border shape file
except IOError:
  print("the data file wasnt read in please try another data file name")
try:
  GeoJsonCities = gdp.read_file("cities.geojson") # read in the city data from the geojson file
except IOError:
  print("the data file was not read in properly might wanna check the name")
try:
  UFOData = pd.read_csv("UFOData.csv")
  # reda in the ufo sightings to geopandas df and read in that gdp lon and lat
  UFOData = gdp.GeoDataFrame(UFOData, geometry=gdp.points_from_xy(UFOData.lon, UFOData.lat))
except IOError:
  print("hmm that data for the ufo has mysteriously gone missing ")

#################################################################
# ██████╗ ██╗      ██████╗ ████████╗████████╗██╗███╗   ██╗ ██████╗  #
# ██╔══██╗██║     ██╔═══██╗╚══██╔══╝╚══██╔══╝██║████╗  ██║██╔════╝   #
# ██████╔╝██║     ██║   ██║   ██║      ██║   ██║██╔██╗ ██║██║  ███╗ #
# ██╔═══╝ ██║     ██║   ██║   ██║      ██║   ██║██║╚██╗██║██║   ██║ #
# ██║     ███████╗╚██████╔╝   ██║      ██║   ██║██║ ╚████║╚██████╔╝  #
# ╚═╝     ╚══════╝ ╚═════╝    ╚═╝      ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝  #
  ################################################################
                                                                 
#create the size of the plot for our voronoi diagram
fig, ax = subplot_for_map(figsize=(15, 15))
# shape of the border and the coordinates and the geometry for vornoi diagram
border_proj = GeoJsonCities.to_crs(USBorderShape.crs)
ShapeOfBorder = unary_union(USBorderShape.geometry)
Coordinates = points_to_coords(border_proj.geometry)
PolyRegions,RegionPoints = voronoi_regions_from_coords(Coordinates, ShapeOfBorder)

RegionLength = len(PolyRegions)
Length=RegionLength
#We need to  create a geopandas series for the regins in our polygon to use with the rtree
rtree = gdp.GeoSeries(PolyRegions)

# plot the vornoi with the axis, the border shape, the polygon regions, regionpts and the coordinates
plot_voronoi_polys_with_points_in_area(ax, ShapeOfBorder, PolyRegions, Coordinates, RegionPoints)
# save the figure as graph.png
plt.savefig("graph.png")

# create some empty list for our output and the list of points to be used inside of main
OutFileList = []
PointList = []
##################################
# ███╗   ███╗ █████╗ ██╗███╗   ██╗ #
# ████╗ ████║██╔══██╗██║████╗  ██║ #
# ██╔████╔██║███████║██║██╔██╗ ██║  #
# ██║╚██╔╝██║██╔══██║██║██║╚██╗██║  #
# ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║  #
# ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝  #
###################################                                

# for  the polygon data in the range of the lenngth of the polygon region
for PolyGonData in range(0, Length):
    #makes sure the right PolyGonData is used so output is accurate
    if shapely.geometry.polygon.Polygon ==type(rtree[PolyGonData]):
        PolygonType = 'SinglePolyGon'
        PointsInPolyGon = np.asarray(rtree[PolyGonData].exterior.coords)
        PointsInPolyGon = PointsInPolyGon.tolist() # append coords to polygon point list
    else:
        PolygonType = 'MultiPolyGon'
        PointsInPolyGon = [] # empty list for out points in our polygon
        for data in rtree[PolyGonData]: # for the data inside of our rtree polygon
            Coordinates = np.asarray(data.exterior.coords) # convert the coordinates to numpy array of coords
            Coordinates = Coordinates.tolist()
            PointsInPolyGon.append(Coordinates) # append the points to the polygon point list

    #we need to get all the ufo data through a query base 
    #DataQuery spatial index of all geometries in the tree with extents that intersect the rtree data polgyondata
    DataQuery = rtree.sindex.query(rtree[PolyGonData])

    # ensure that we pass back tohe polygon points and not the border
    for CoordinatePoints in DataQuery:
        if type(rtree[CoordinatePoints]) == shapely.geometry.point.Point:
            # append the x and y coordinate points to the point list for each polygon
            PointList.append([rtree[CoordinatePoints].x, rtree[CoordinatePoints].y])
    # output list to hold the key value pairs in json for the type, points in the polygon and the list of points
    OutFileList.append({
        'Polygon Type ': PolygonType,
        'Polygon Points': PointsInPolyGon,
        'Point List': PointList
    })
#####################################################
#  ██████╗ ██╗   ██╗████████╗██████╗ ██╗   ██╗████████╗ #
# ██╔═══██╗██║   ██║╚══██╔══╝██╔══██╗██║   ██║╚══██╔══╝ #
# ██║   ██║██║   ██║   ██║   ██████╔╝██║   ██║   ██║   #
# ██║   ██║██║   ██║   ██║   ██╔═══╝ ██║   ██║   ██║   #
# ╚██████╔╝╚██████╔╝   ██║   ██║     ╚██████╔╝   ██║   #
#  ╚═════╝  ╚═════╝    ╚═╝   ╚═╝      ╚═════╝    ╚═╝   #
  ###################################################
                                                     
# try opening the output file
try:
  # try opening file to filename as writeable to the outfile
  with open('PointsInPolys.json', 'w') as outfile:
      outfile.write(json.dumps(OutFileList,indent=4))
except IOError:
  print("hmm did ufos take your dat file because there is an error")
finally:
  print("we are all done now good bye chap")