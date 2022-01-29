###################################################################
##                  Author - Ethan Coyle                          #
##                  Instr  - Dr. Griffin                          #
##                  Class  - CMPS 4553 Spatial DS                 #
##                  Assign - Convert JSON to GEOJSON              #
##                  Due    - 2/1/2022                             #
##                                                                #
###################################################################
## About  - the purpose of this program is to read in a json file #
##          and convert it to a proper geojson format to be viewed#
##          by the user to better visualize the grographical data #
##          in the file.                                          #
##                                                                #
## Instructions:                                                  #
##       click run on the program(no special tasks needed)        #
##       try excepts added for input and output checking for      #
##       valid files output file will display geojson file        #
##       associated with mapping Github automatically creates map #
###################################################################
import json
import random as rand
from rich import print # nice easy printing visually appealing

# initilize variables 
StateName = {} # list of state names
MaxPopulationCities = {}# cities and their population
CityRank = [] # the ranking of our cities
JsonListToGeoList = [] # converting from json to geojson

print("First, Lets read the infile to see if working\n")
# try reading the input file from the given file
try:
    with open('Assignments/P01/testdata.json', 'r') as data:
        # assign the json loaded data into a file called InputData for use
        InputData = json.load(data)
# if cant then toss an error
except FileNotFoundError:
    print("Error! Error! Error! File not found \n")
# if no errors present, proceed to the next step
print("Now lets add the cities according to their state to the list of Statenames\n")

for city in InputData:
    if not city['state'] in StateName: # if the city not there add it
        state = city['state']
        StateName[state] = []
    # append the city and state names
    StateName[city['state']].append(city)

# next we need to get rid of Alaska and Hawaii by looking at the longs and lats
print("Now get rid of Hawaii and Alaska\n")
# loop through the data
for state, InputData in StateName.items():
    max = -1 # default max value
    for data in InputData:
        # if the pop is greater than previous max
        if data['population'] > max:
            # if the longitude is less than 110
            if data['longitude'] < 110:
                # if the longitude less than 50
                if data['latitude'] < 50 and data['latitude'] > 25:
                        # assign the integer population to max
                    max = int(data['population'])
                        # assign the data to population state
                    MaxPopulationCities[state] = data
        # append the population of the cities to list in order to rank
print("Now lets rank our cities based on their population\n")
for key, value in MaxPopulationCities.items():
    CityRank.append(value)
# the city rank will now be sorted usin lamba key data and population is the data key
CityRank = sorted(CityRank,key=lambda data: data['population'])

        # Set the ranking of the Cities, will begin at 1 being the smallest
RankingOrder = 1
        # for each item inside of this ranked cities assign a RankingOrderber
for item in CityRank:
    item['rank'] = RankingOrder
    RankingOrder += 1 
# now we have our random colors for the markers so we proceed to the 
print("Finally, we will convert to the GeoJson\n")

JsonListToGeoList = {
    "type": "FeatureCollection",# have type feature collection and then added features
    "features": []              # including long and lats etc. 
}
for InputData in CityRank:
    # setting the colors to random for rgb color schematic
    # each color is chosing a random integer between 0 and 255
    Red = lambda: rand.randint(0,255)
    Green = lambda: rand.randint(0,255)
    Blue = lambda: rand.randint(0,255)
        # return the formatted colors in formatted string
    ColorGeneration= f'#%02X%02X%02X' % (Red(),Blue(),Green())
    # get the color of the marker, the size and the symbol
    #list of features,property from the input and data figures 
    JsonListToGeoList['features'].append(
        {
        "type": "Feature",
        "properties":{
                "marker-color": ColorGeneration,
                "marker-size": "medium",
                "marker-symbol": InputData['rank']+ 1,
                "city": InputData['city'],
                "growth": InputData['growth'],
                "latitude": InputData['latitude'],
                "longitude": InputData['longitude'],
                "population": InputData['population'],
                "state" : InputData['state']
            },        
        "geometry": 
        {
            "type": "Point",
            "coordinates": 
            [
                InputData['longitude'],
                InputData['latitude'],
            ]
        }
        })
CityRank = sorted(CityRank,key=lambda CityRank: CityRank['longitude'])
# longitude is the value we looking to sort by from the city rank
for i in range(len(CityRank)):
    if i != len(CityRank) - 1:
        # each color is chosing a random integer between 0 and 255
        Red = lambda: rand.randint(0,255)
        Green = lambda: rand.randint(0,255)
        Blue = lambda: rand.randint(0,255)
        # return the formatted colors in formatted string
        ColorGeneration= f'#%02X%02X%02X' % (Red(),Blue(),Green())
        
        JsonListToGeoList['features'].append(
        {
            "type": "Feature",
            "properties": {
                "stroke": ColorGeneration,
                "stroke-width": 2,
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [CityRank[i]['longitude'],
                    CityRank[i]['latitude']],
                    [CityRank[i + 1]['longitude'], 
                    CityRank[i + 1]['latitude']]
                ]
            }
        }
        )
# open up the output file and then dump the conversion inside of the 
    # converted json to geojson list to the output using keyword dumps
try:
    with open('Assignments/P01/output.geojson', 'w') as file:
        file.write(json.dumps(JsonListToGeoList, indent=4))
except IOError:
    print("unsuccessful at pushing to the ouput.\
            SOMETHING WENT WRONG BONEHEAD\n")
print("Congratulations, Check the output now\n\n")
# end of the driver and end of the program
