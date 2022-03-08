import geopandas as gpd
import matplotlib.pyplot as plt 
from mpl_toolkits.axes_grid1 import make_axes_locatable 
  
# Reading the world shapefile 
world_data = gpd.read_file(r'Assignments\P06\WorldShape\Visualizing Geodata\world.shp')
world_data = world_data[['NAME', 'geometry']]
  
# Calculating the area of each country 
world_data['area'] = world_data.area
  
# Removing Antarctica from GeoPandas GeoDataframe
world_data = world_data[world_data['NAME'] != 'Antarctica']
world_data[world_data.NAME=="India"].plot()