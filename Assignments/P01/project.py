#############################################
## Author - Ethan Coyle                     #
## Instr  - Dr. Griffin                     #
## Class  - CMPS 4553 Spatial DS            #
## Assign - Convert JSON to GEOJSON         #
## Due    - 2/1/2022                        #
## About  - the purpose of this program is  #
##          to read in a json file and      #
##          convert it to a proper geojson  #
##          format to be viewed by the      #
##          user to better visualize        #
##          the grographical data in the    #
##          file.                           #
##                                          #
## Instructions:                            #
##       click run on the program           #
##       no special tasks needed            #
##       try excepts added for input and    #
##       output checking for valid files    #
##       output file will display geojson   #
##       file associated with mapping       #
##       Github automatically creates map   #
#############################################

## start our inport for using in the program
import json
import random as rand
from rich import print # nice easy printing visually appealing

# create a class to read the input data and do some conversions with it
class OrderedCities:
    ## contructor for the class orderedcities will be ranked eventually
    # from the east coast to the west coast according to the population
    def __init__(self):
        self.StateName = {}
        self.MaxPopulationCities = {}
        self.CityRank = []
        self.JsonListToGeoList = []

    # function definintion to read the input file 
    # we also need to check for invalid file types so we read the 
    # input in a try except to throw errors if we have issues reading inpuet
    def ReadInput(self):
        # try reading the input file from the given file
        try:
            with open('Assignments/P01/testdata.json', 'r') as data:
                # assign the json loaded data into a file called InputData for use
                InputData = json.load(data)
        # if cant then toss an error
        except FileNotFoundError:
            print("Error! Error! Error! File not found \n")
            
        # for each city in data
        # if the city is not in then append it to the list of city names
        for city in InputData:
            if not city['state'] in self.StateName:
                state = city['state']
                self.StateName[state] = []
            # append the city and state names
            self.StateName[city['state']].append(city)

    # function definition to filter through the cities and the items
    # will determine the cities by their population
    def FilterCity(self):

        # loop through the data
        for state, InputData in self.StateName.items():
            max = -1 # default max value
            for data in InputData:
                # if the pop is greater than previous max
                if data['population'] > max:
                    # if the longitude is less than 110
                    if data['longitude'] < 110:
                        # if the longitude less than 50
                        if data['latitude'] < 50:
                            #if the lat is greater than 25
                            if data['latitude'] > 25:
                                # assign the integer population to max
                                max = int(data['population'])
                                # assign the data to population state
                                self.MaxPopulationCities[state] = data
            
    def rank_cities(self):
        
        # append the population of the cities to list in order to rank
        # according to the population
        for key, value in self.MaxPopulationCities.items():
            self.CityRank.append(value)

        # Sort ranked cities by population, this will allow us to use the
        # ranking as the marker for GeoJson
        # cities ranked by the population
        # allows for easy utilization in the transferral to proper geojson 
        # format

        self.CityRank = sorted(self.CityRank,key=lambda data: data['population'])

        # Set the ranking of the Cities, will begin at 1 being the smallest
        RankingOrder = 1
        # for each item inside of this ranked cities assign a RankingOrderber
        for item in self.CityRank:
            item['rank'] = RankingOrder
            RankingOrder += 1 
            # ranking them by RankingOrderber 
        # to print out the sorted ranked list print(self.CityRank)

    # function definition for the color generation
    # here we have red green and blue colors
    # we are integrating a random selection for each one of the colors t
    # then we are returning that random color back
    def ColorGeneration(self):
        # setting the colors to random for rgb color schematic
        # each color is chosing a random integer between 0 and 255
        Red = lambda: rand.randint(0,255)
        Green = lambda: rand.randint(0,255)
        Blue = lambda: rand.randint(0,255)
        # return the formatted colors in formatted string
        return f'#%02X%02X%02X' % (Red(),Blue(),Green())

    # to convert to a geo json style format
    # function definition will convert to a suitable
    # file formatting which can be used in geojson.io
    # in the case of Github display will be displayed in output
    #box
    def FileConversion(self):

        self.JsonListToGeoList = {
            "type": "FeatureCollection",
            "features": []
            # have type feature collection and then added features
            # including long and lats etc.
        }
        for InputData in self.CityRank:
            # get the color of the marker, the size and the symbol
            InputData['marker-color'] = self.ColorGeneration()
            InputData['marker-size'] = "small"
            InputData['marker-symbol'] = InputData['rank']

            # append the features of each city for nice usng
            # geojson list will be of type feature and have properties
            # from the input data which include the markers and sizes
            # then will have a type point to poistion on the latitude and
            # longitude
            self.JsonListToGeoList['features'].append(
                {
                "type": "Feature",
                "properties": InputData,
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
        # Sorting by longitudes 
        # Property is argument and looking at property longitude
        self.CityRank = sorted(self.CityRank,key=lambda CityRank: CityRank['longitude'])
        # to view the sorted ranks by population use print(self.CityRank)
        # for i in the range of the length of the specified CityRank
        for i in range(len(self.CityRank)):
            # assigning the rank if it is not in the length-1 or else
            # we need to remove hawaii and alaska
            if_i = i+1 if i is not (len(self.CityRank) - 1) else i
            # append the features to each and call the generated random
            # colors for red,green and blue and create the line string 
            # for connectivity
            self.JsonListToGeoList['features'].append(
                {
                    "type": "Feature",
                    "properties":{
                        "stroke": self.ColorGeneration(),
                        "stroke-width": 2,
                    },
                    "geometry":{
                        "type": "LineString",
                        "coordinates":[
                            [self.CityRank[i]['longitude'],
                            self.CityRank[i]['latitude']],
                            [self.CityRank[if_i]['longitude'],
                             self.CityRank[if_i]['latitude']],
                        ]
                    }
                }
            )
        # open up the output file and then dump the conversion inside of the 
            # converted json to geojson list to the output using keyword dumps
        try:
            with open('Assignments/P01/output.geojson', 'w') as file:
                file.write(json.dumps(self.JsonListToGeoList, indent=4))
        except IOError:
            print("unsuccessful at pushing to the ouput.\
                   SOMETHING WENT WRONG BONEHEAD\n")
        print("Congratulations, Check the output now\n\n")
        
# now inside the main derivation of the object created main driver
# object called cities of the OrderedCities class
# perform the tasks in order to convert to geojson
# each call goes to the function definition to do the 
# implementation task by calling the object.(calling function)()
Cities = OrderedCities()
Cities.ReadInput()
Cities.FilterCity()
Cities.rank_cities()
Cities.FileConversion()
# end of the main driver and the program exitting now