from shapely.geometry import Point, Polygon,shape
import geopandas as gpd
import requests

# reading in the country datafile
countries = gpd.read_file('Assignments\P04\countries.geojson')
print(countries.head())



collection = requests.get('http://cdn.buenosaires.gob.ar/datosabiertos/datasets/barrios/barrios.geojson').json()
features = collection["features"]
for feature in features:
    s = shape(feature["geometry"])
    print(s.centroid)