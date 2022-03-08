# pandas data frame from cites in a csv\n",

#################################################################
## Name - Ethan Coyle                                           #
## Inst.- Dr. Griffin                                           #
## P03  - Graphic vornoi                                        #
##                                                              #
## The purpose of this assignment is to read in the data from   #
## the cities.csv file and the data for the gities.geojson and  #
## create a voronoi of the ufo data and the city boundaries     #
#################################################################
## vscode does not like geovoroni in the terminal even in 
## geo environment so I had to run this in the replit  
# link to replit running plot of diagram
# https://replit.com/@ethancoyle71/anotherone#main.py
import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use('TkAgg') ## required for replit to properly run the GUI because of prerequisites from matplot lib
import matplotlib.pyplot as plt


# user notes  if geovornoi is working on IDE, then the relative path
from shapely.ops import unary_union
from geovoronoi import voronoi_regions_from_coords, points_to_coords
from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area
df1 = pd.read_csv("Assignments\P03\cities.csv")

# geopandas data frame from a geojson file\n",
gdf2 = gpd.read_file('Assignments\P03\cities.geojson')

gdf1 = gpd.GeoDataFrame(df1, geometry=gpd.points_from_xy(df1.lon, df1.lat))
# viewing the head of the geo dataframe
gdf1.head()

# read in the border shape file for the united states 
boundary = gpd.read_file("us_border.shp")
fig, ax = plt.subplots(figsize=(12, 10))
boundary.plot(ax=ax, color= "gray")
gdf2.plot(ax=ax, markersize=2.5, color="blue")
ax.axis("off")
plt.axis('equal')

# creating the boundary for the united states reading the boundary crs file
boundary = boundary.to_crs(epsg=3395)
gdf_proj = gdf2.to_crs(boundary.crs)
boundary_shape = unary_union(boundary.geometry)
coords = points_to_coords(gdf_proj.geometry)
region_polys, region_pts = voronoi_regions_from_coords(coords, boundary_shape)
fig, ax = subplot_for_map(figsize=(12, 10))
#gdf1.plot(ax=ax, markersize=2.5, color="blue")
plot_voronoi_polys_with_points_in_area(ax, boundary_shape, region_polys, coords, region_pts)
plt.show()

# lets see the polygon  vals
for i,poly in region_polys.items():
    print(poly)
# save the plot figure to a file
plt.savefig("Assignments\P03\graph.png")