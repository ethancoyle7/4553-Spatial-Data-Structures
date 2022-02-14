import pandas as pd
import json

#import geopandas as gpd
# first read in the dataframe with the ufo sightings and print out 
# the head to make sure that it is reading properly
df = pd.read_csv('Assignments/P02/UFOSightings.csv')
print(df.head(20))
# to make easier to look at this lets drop uneccesary collums
# make the implace to be true so we dont have to worrry
# if not then we have to assign the changes to new dataframe
df.drop(['shape','duration','date_time'], axis=1,inplace=True)
print("Our new dataframe is :n\n", df)
# df.drop(df[ df['lat'] < 50].index, inplace=True)
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


# want to test the number of occurances in each state
print("The number of occurances in each state are :\n")
print(df['state']. value_counts())
print("The number of occurances in each city  are :\n")
print(df['city']. value_counts())  

df['lat'] = df['lat'].astype(float)
df['lon'] = df['lon'].astype(float)
df['state'] = df['state'].str.title()
df['city'] = df['city'].str.title()

# convert our dataframe to a gejson
def df_to_geojson(df, properties, lat='lat', lon='lon'):
    # create a new python dict to contain our geojson data, using geojson format
    geojson = {'type':'FeatureCollection', 'features':[]}

    # loop through each row in the dataframe and convert each row to geojson format
    for _, row in df.iterrows():
        
        # create a feature template to fill in
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}

        # fill in the coordinates
        feature['geometry']['coordinates'] = [row[lon],row[lat]]

        # for each column, get the value and add it as a new feature property
        for prop in properties:
            feature['properties'][prop] = row[prop]
        
        # add this feature (aka, converted dataframe row) to the list of features inside our dict
        geojson['features'].append(feature)
    
    return geojson

cols = ['state', 'city', 'lat', 'lon']
geojson = df_to_geojson(df, cols)
print(geojson)

# 
try:
    with open('Assignments/P02/output.geojson', 'w') as file:
        file.write(json.dumps(geojson, indent=4))
except IOError:
    print("unsuccessful at pushing to the ouput.\
            SOMETHING WENT WRONG BONEHEAD\n")

