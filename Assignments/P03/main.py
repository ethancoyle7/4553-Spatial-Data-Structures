# Import Geopandas modules

import pandas as pd
# Import shapely to convert string lat-longs to Point objects
from shapely.geometry import Point
# Import Geopandas modules
import geopandas
import geoplot
# Import shapely to convert string lat-longs to Point objects

df1 = pd.read_csv('UFOSightings.csv')
print(df1.head(20))

# read in the data associated with the bounding boxes of the united states
# states
df2= pd.read_csv('StateCapitals.csv')
print(df2.head(10))
print(df2['state']) # this will be the value of comparison to the data
                     # inside of the csv file of cities

# given the merge, we merge the two together to merge the data frames together 
# on the state name and create a new data frame that holds the values
# including the max  and mins of the x and y
df3 = pd.merge(df1, df2,
                   on='state',
                   how='right')
df3.dropna(subset = ["city"], inplace=True)
print('output now is :\n', df3)
# to make easier to look at this lets drop uneccesary collums
# make the implace to be true so we dont have to worrry
# if not then we have to assign the changes to new dataframe
df3.drop(['shape','duration','date_time'], axis=1,inplace=True)
print("Our new dataframe is :n\n", df3)

# initialize the bounding box for the united states
top = 49.3457868 # north lat
leftborder = -124.7844079 # west long
rightborder = -66.9513812 # east long
bottom =  24.7433195 # south lat

# drop uneccesary of the left bounding box border of us both past or before 
# based on the top and bottom vals
df3 = df3.drop(df3[(df3['lon'] <= leftborder) & (df3['lat'] <= bottom)].index)
df3 = df3.drop(df3[(df3['lon'] <= leftborder) & (df3['lat'] >= top)].index)
df3 = df3.drop(df3[(df3['lon'] >= leftborder) & (df3['lat'] <= bottom)].index)
df3 = df3.drop(df3[(df3['lon'] >= leftborder) & (df3['lat'] >= top)].index)

# drop uneccesary of the right bounding box border of us both past or before 
# based on the top and bottom vals
df3 = df3.drop(df3[(df3['lon'] >= rightborder) & (df3['lat'] <= bottom)].index)
df3 = df3.drop(df3[(df3['lon'] >= rightborder) & (df3['lat'] >= top)].index)
df3 = df3.drop(df3[(df3['lon'] <= rightborder) & (df3['lat'] <= bottom)].index)
df3 = df3.drop(df3[(df3['lon'] <= rightborder) & (df3['lat'] >= top)].index)

# there is one outlier that didnt get removed so look at the outlier
# lat and long and hard code in to remove it(over in europe)
df3 = df3.drop(df3[(df3['lon'] == -8.5962) & (df3['lat'] == 42.3358)].index)
# Setup Geopandas Dataframe
# Assumes data stored in pandas DataFrame df
geometry = [Point(xy) for xy in zip(df3.lon, df3.lat)]
gdf = geopandas.GeoDataFrame(df3, geometry=geometry)

# Import USA data for region clipping
USA = geopandas.read_file(geoplot.datasets.get_path('contiguous_usa'))

# Set the map projection
proj = geoplot.crs.AlbersEqualArea(central_longitude=-98, central_latitude=39.5)

# Setup the Voronoi axes; this creates the Voronoi regions
ax = geoplot.voronoi(gdf,  # Define the GeoPandas DataFrame
                     hue='values',  # df column used to color regions
                     clip=USA,  # Define the voronoi clipping (map edge)
                     projection=proj,  # Define the Projection
                     cmap='Reds',  # color set
                     k=None,  # No. of discretized buckets to create
                     legend=True, # Create a legend
                     edgecolor='white',  # Color of the voronoi boundaries
                     linewidth=0.01  # width of the voronoi boundary lines
                    )
# Render the plot with a base map
geoplot.polyplot(USA,  # Base Map
                 ax=ax,  # Axis attribute we created above
                 extent=USA.total_bounds,  # Set plotting boundaries to base map boundaries
                 edgecolor='black',  # Color of base map's edges
                 linewidth=1,  # Width of base map's edge lines
                 zorder=1  # Plot base map edges above the voronoi regions
                 )