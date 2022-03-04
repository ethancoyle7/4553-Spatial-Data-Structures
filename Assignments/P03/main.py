# pandas data frame from cites in a csv\n",

# link to replit running plot of diagram
# https://replit.com/@ethancoyle71/anotherone#main.py


import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib
matplotlib.use('TkAgg')# for replit to recognize the plot
import matplotlib.pyplot as plt

from shapely.ops import unary_union
from geovoronoi import voronoi_regions_from_coords, points_to_coords
from geovoronoi.plotting import subplot_for_map, plot_voronoi_polys_with_points_in_area
df1 = pd.read_csv("cities.csv")

# geopandas data frame from a geojson file\n",
gdf2 = gpd.read_file('cities.geojson')

gdf1 = gpd.GeoDataFrame(df1, geometry=gpd.points_from_xy(df1.lon, df1.lat))
# viewing the head of the geo dataframe
gdf1.head()
"#boundary = gpd.read_file(\"data/us_nation_border.geojson\")\n",
boundary = gpd.read_file("us_border.shp")
fig, ax = plt.subplots(figsize=(12, 10))
boundary.plot(ax=ax, color= "gray")
gdf2.plot(ax=ax, markersize=2.5, color="blue")
ax.axis("off")
plt.axis('equal')

minx, miny, maxx, maxy = gdf2.total_bounds
print(minx,miny,maxx,maxy)
ax.set_xlim(minx-5, maxx+5)
ax.set_ylim(miny, maxy)
plt.show()
boundary = boundary.to_crs(epsg=3395)
gdf_proj = gdf2.to_crs(boundary.crs)
boundary_shape = unary_union(boundary.geometry)
coords = points_to_coords(gdf_proj.geometry)
region_polys, region_pts = voronoi_regions_from_coords(coords, boundary_shape)
fig, ax = subplot_for_map(figsize=(12, 10))
gdf1.plot(ax=ax, markersize=2.5, color="blue")
plot_voronoi_polys_with_points_in_area(ax, boundary_shape, region_polys, coords, region_pts)
plt.show()

for i,poly in region_polys.items():
    print(poly)
plt.show() 