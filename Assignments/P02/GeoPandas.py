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
# VERY IMPORTANT Note -                                           #
#                      I only got thegeopandas for the distance   #
#                      to work in replit and it is taking and     #
#                      very long time to iterate through however  #
#                      the distances are correct                  #
#                      I have tried to implement geopandas in     #
#                      vscode but it does not like the output     #
# Replit Instructions                                             #
#                     Here is the link to my replit account       #
#                     where all the data is stored can be run and #
#                     once it is done, the correct output will be #
#                     displayed                                   #
#Replit Link: https://replit.com/@ethancoyle71/geopandas#main.py  #
#                                                                 #
# The other main.py iterated through the file and produces the    #
# correct result but is missing the distances                     #
##                                                                #
## Instructions:                                                  #
##       click run on the program(no special tasks needed)        #
##       try excepts added for input and output checking for      #
##       valid files output file will display geojson file        #
##       associated with mapping Github automatically creates map #
###################################################################
# creating our inports
import pandas as pd # for the dataframe
import json # reading the json data for output
import random as rand # for color generation of points
from shapely.geometry import Point # for the geopandas distance
import geopandas as gpd # import our geopandas library



# first read in the dataframe with the ufo sightings and print out 
# the head to make sure that it is reading properly
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
print("The length of the dataframe is :",len(df3))
# converting from df3 to list to be able to calculate the distance
# will be read in meters
LongitudeList1 = df3.Longitude.tolist()
# print(LongitudeList1)
LonList=df3.lon.tolist()
LatitudeList1=df3.Latitude.tolist()
LatList=df3.lat.tolist()
# all the lengths of the list are equal 17064 values
print(" The number of items in LtList are :\n", len(LatList))
print(" The number of items in Longitude List 1 are :\n", len(LongitudeList1))
print(" The number of items in LatitudeList 1 :\n", len(LatitudeList1))
print(" The number of items in LonList are :\n", len(LonList))

# create an empty list called sitances
distances=[]
# since all the ranges are within the same length can iterate through all four data files looking at the length
for i in range(len(df3)):
  
  # first point
  pnt1 = Point(LonList[i], LatList[i])
  # second point
  pnt2 = Point(LongitudeList1[i], LatitudeList1[i])
  # call the geopandas to figure out the distance from the capital and the 
  # state
  points_df = gpd.GeoDataFrame({'geometry': [pnt1, pnt2]}, crs='EPSG:4326')
  # using an online gps coordinate system will map out the plot and figure out
  # the distances between the two
  points_df = points_df.to_crs('EPSG:5234')
  points_df2 = points_df.shift() 
  #We shift the dataframe by 1 to align pnt1 with pnt2
  distance= points_df.distance(points_df2)/1627.344
   # divide by 1627.344 because the answer is in meters and the conversion will be in miles
  # the list makes a nan row so op the index 0 which is the nan values for everything
  distance.pop(0)
  
  # append each distance to the list 
  distances.append(distance)
  #print(distances)
# once the list is all appended, add to the collum in our dataframe
df3['Distance From Capital'] = distances
#print("the new dataframe is :", df3) # to view dataframs
# convert our dataframe to a gejson
def df_to_geojson(df3, properties, lat='lat', lon='lon'):
    # create a new python dict to contain our geojson data, using geojson format
    geojson = {'type':'FeatureCollection', 'features':[]}
    
    # loop through each row in the dataframe and convert each row to geojson format
    for _, row in df3.iterrows():
        
        # setting the colors to random for rgb color schematic
        # each color is chosing a random integer between 0 and 255
        Red = lambda: rand.randint(0,255)
        Green = lambda: rand.randint(0,255)
        Blue = lambda: rand.randint(0,255)
        # return the formatted colors in formatted string
        ColorGeneration= f'#%02X%02X%02X' % (Red(),Blue(),Green())
        # create a feature template to fill in
        featured = {'type':'Feature',
                   "properties":
                   {
                    # what will show in the information icon when clicked
                    "marker-color": ColorGeneration,
                    "city": row['city'],
                    "state" : row['state'],
                    "longitude": row['lon'],
                    "latitude": row['lat'],
                    "distance": row['Distance From Capital']
                    },   # for each row add the calculated distance from geopandas  
                    # whats the geometry look like? These are points   
                   'geometry':{'type':'Point',
                               'coordinates':[row['lon'],row['lat']]
                              }
                    }
        # for each column, get the value and add it as a new feature property
        
        # add to dict list
        geojson['features'].append(featured)
    
    return geojson # return the converted geojson

cols = ['state', 'city', 'lat', 'lon']
# call to create the geojson stuff
geojson = df_to_geojson(df3, cols)
# for visualization print out the geojson to terminal
print(geojson)

#open up and try to execute the importing of the output file
try:
    with open('output.geojson', 'w') as file:
        file.write(json.dumps(geojson, indent=4))
# if unsuccessful, throw error message
except IOError:
    print("unsuccessful at pushing to the ouput.\
            SOMETHING WENT WRONG BONEHEAD\n")