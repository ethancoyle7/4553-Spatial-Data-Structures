#################################################################
## Name - Ethan Coyle                                           #
## Inst.- Dr. Griffin                                           #
## P03  - Graphic vornoi                                        #
##                                                              #
## The purpose of this assignment is to read in the data from   #
## the cities.csv file and the data for the gities.geojson and  #
## create a voronoi of the ufo data and the city boundaries     #
##                                                              #
## Important user note : I could not get geovornoi to properly  #
## work in my geo environment so i had to run this through repli#
## I will attach my replit link to this as well because it does #
## work inside of replit                                        #
## if imports for the geovornoi are imported properly might not #
## have to use replit link but that is the only way i got it to #
## work                                                         #
##                                                              #
## Replit Link : https://replit.com/@ethancoyle71/stuff#main.py #
##                                                              #
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
  USBorderShape=gdp.read_file("Assignments/P03/us_border_shp/us_border.shp") # us border shape file
except IOError:
  print("the data file wasnt read in please try another data file name")
try:
  GeoJsonCities = gdp.read_file("Assignments/P03/cities.geojson") # read in the city data from the geojson file
except IOError:
  print("the data file was not read in properly might wanna check the name")
try:
  UFOData = pd.read_csv("Assignments/P03/UFOSightings.csv")
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
plt.savefig("Assignments/P03/graph.png")

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
    if shapely.geometry.polygon.Polygon ==type(rtree[PolyGonData]): # if the polygon is a polygon
        PolygonType = 'SinglePolyGon' # if the polygon is a single polygon
        PointsInPolyGon = np.asarray(rtree[PolyGonData].exterior.coords)
        PointsInPolyGon = PointsInPolyGon.tolist() # append coords to polygon point list
    else:
        PolygonType = 'MultiPolyGon' # if the polygon is a multi polygon
        PointsInPolyGon = [] # empty list for out points in our polygon
        for data in rtree[PolyGonData]: # for the data inside of our rtree polygon
            Coordinates = np.asarray(data.exterior.coords) # convert the coordinates to numpy array of coords
            Coordinates = Coordinates.tolist() # convert the numpy array to a list
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
        'Polygon Type ': PolygonType, # append the polygon type
        'Polygon Points': PointsInPolyGon, # append the polygon points
        'Point List': PointList # append the point list
    })
    # add the outfile list of polygons to the graph plt
    plt.plot(PointList[0], PointList[1], 'ro')



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
  with open('Assignments/P03/PointsInPolys.json', 'w') as outfile:
      outfile.write(json.dumps(OutFileList,indent=4))
except IOError:
  print("hmm did ufos take your dat file because there is an error")
finally:
  print("we are all done now good bye chap")

  # read in the pointsinpolys json and plot it on a voronoi diagram

