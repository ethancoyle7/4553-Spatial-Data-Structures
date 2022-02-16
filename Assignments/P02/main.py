###################################################################
##                  Author - Ethan Coyle                          #
##                  Instr  - Dr. Griffin                          #
##                  Class  - CMPS 4553 Spatial DS                 #
##                  Assign - Convert JSON to GEOJSON              #
##                  Due    - 2/15/2022                            #
##                                                                #
###################################################################
## About  - the purpose of this program is to read in a csv file  #
#           and filter through all the reported ufo sightings and #
#           convert it to a geo json format with bounding box     #
#           inside of the us to map out all the sightings within  #
#           the united states to see visually which states have   #
#           reported citings                                      #
##                                                                #
## Instructions:                                                  #
##       click run on the program(no special tasks needed)        #
##       try excepts added for input and output checking for      #
##       valid files output file will display geojson file        #
##       associated with mapping Github automatically creates map #
###################################################################
# creating our inports
import pandas as pd
import json
## geopandas isnt wanting to download so in order to complete run the
## program in a way such that will compare the citites.geojson to 
## and it longitudes and latitudes and compare values


#import geopandas as gpd
# first read in the dataframe with the ufo sightings and print out 
# the head to make sure that it is reading properly
df1 = pd.read_csv('Assignments/P02/UFOSightings.csv')
print(df1.head(20))

# read in the data associated with the bounding boxes of the united states
# states
df2= pd.read_csv('Assignments/P02/unitedstatesboundingboxes.csv')
print(df2.head(10))
print(df2['state']) # this will be the value of comparison to the data
                     # inside of the csv file of cities

# given the merge, we merge the two together to merge the data frames together 
# on the state name and create a new data frame that holds the values
# including the max  and mins of the x and y
df3 = pd.merge(df1, df2,
                   on='state',
                   how='right')
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


# want to test the number of occurances in each state
print("The number of occurances in each state are :\n")
print(df3['state']. value_counts())
# number of occurances in city data
print("The number of occurances in each city  are :\n")
print(df3['city']. value_counts()) 

df3['lat'] = df3['lat'].astype(float)
df3['lon'] = df3['lon'].astype(float)
df3['state'] = df3['state'].str.title()
df3['city'] = df3['city'].str.title()

# convert our dataframe to a gejson
def df_to_geojson(df3, properties, lat='lat', lon='lon'):
    # create a new python dict to contain our geojson data, using geojson format
    geojson = {'type':'FeatureCollection', 'features':[]}

    # loop through each row in the dataframe and convert each row to geojson format
    for _, row in df3.iterrows():
        
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
        # add to dict list
        geojson['features'].append(feature)
    
    return geojson # return the converted geojson

cols = ['state', 'city', 'lat', 'lon']
# call to create the geojson stuff
geojson = df_to_geojson(df3, cols)
# for visualization print out the geojson to terminal
print(geojson)

#open up and try to execute the importing of the output file
try:
    with open('Assignments/P02/output.geojson', 'w') as file:
        file.write(json.dumps(geojson, indent=4))
# if unsuccessful, throw error message
except IOError:
    print("unsuccessful at pushing to the ouput.\
            SOMETHING WENT WRONG BONEHEAD\n")

