# Import Geopandas modules
import geopandas
import geoplot
# Import shapely to convert string lat-longs to Point objects
from shapely.geometry import Point
import pandas as pd

df = pd.read_csv('Assignments/P02/UFOSightings.csv')
print(df.head(20))
# initialize the bounding box for the united states
top = 49.3457868 # north lat
leftborder = -124.7844079 # west long
rightborder = -66.9513812 # east long
bottom =  24.7433195 # south lat

# drop uneccesary of the left bounding box border of us both past or before 
# based on the top and bottom vals
df = df.drop(df[(df['lon'] <= leftborder) & (df['lat'] <= bottom)].index)
df = df.drop(df[(df['lon'] <= leftborder) & (df['lat'] >= top)].index)
df = df.drop(df[(df['lon'] >= leftborder) & (df['lat'] <= bottom)].index)
df = df.drop(df[(df['lon'] >= leftborder) & (df['lat'] >= top)].index)

# drop uneccesary of the right bounding box border of us both past or before 
# based on the top and bottom vals
df = df.drop(df[(df['lon'] >= rightborder) & (df['lat'] <= bottom)].index)
df = df.drop(df[(df['lon'] >= rightborder) & (df['lat'] >= top)].index)
df = df.drop(df[(df['lon'] <= rightborder) & (df['lat'] <= bottom)].index)
df = df.drop(df[(df['lon'] <= rightborder) & (df['lat'] >= top)].index)

# there is one outlier that didnt get removed so look at the outlier
# lat and long and hard code in to remove it(over in europe)
df = df.drop(df[(df['lon'] == -8.5962) & (df['lat'] == 42.3358)].index)
# Setup Geopandas Dataframe
# Assumes data stored in pandas DataFrame df
geometry = [Point(xy) for xy in zip(df.lon, df.lat)]

gdf = geopandas.GeoDataFrame(df, geometry=geometry)
print(gdf)
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