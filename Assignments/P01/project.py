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
        self.GeoJsonList = []

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
        except EnvironmentError as e:
            print(f'Error, unable to open the specified folder: Error Type = {e}')
        # for each city in data
        for city in InputData:
            if not city['state'] in self.StateName:
                state = city['state']
                self.StateName[state] = []
            self.StateName[city['state']].append(city)

    # function definition to filter through the cities and the items
    # will determine the cities by their population
    def FilterCity(self):
        for state, InputData in self.StateName.items():
            max = -1 # default max value
            for data in InputData:
                # where the data falls withing the long and lat lines
                if data['population'] > max and data['longitude'] < 110 \
                        and data['latitude'] < 50 and data['latitude'] > 25:
                    max = int(data['population'])
                    self.MaxPopulationCities[state] = data
            # for data, value in self.MaxPopulationCities.items():
            #     print(data, value)

    # function definition to parse through the cities by population a
    # will rank them according to the values low to high
    def rank_cities(self):
        
        for key, value in self.MaxPopulationCities.items():
            self.CityRank.append(value)

        # Sort ranked cities by population, this will allow us to use the
        # ranking as the marker for GeoJson
        # cities ranked by the population
        # allows for easy utilization in the transferral to proper geojson 
        # format

        self.CityRank = sorted(self.CityRank,key=lambda data: data['population'])

        # Set the ranking of the Cities, will begin at 1 being the smallest
        num = 1
        # for each item inside of this ranked cities assign a number
        for item in self.CityRank:
            item['rank'] = num
            num += 1 
            # ranking them by number 
        # print out the sorted ranked list
        print(self.CityRank)

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
    
    def FileConversion(self):
        self.GeoJsonList = {
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
            self.GeoJsonList['features'].append({
                "type": "Feature",
                "properties": InputData,
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        InputData['longitude'],
                        InputData['latitude'],
                    ]}})
        # Sorting by longitudes 
        # Property is argument and looking at property longitude
        self.CityRank = sorted(self.CityRank,key=lambda Property: Property['longitude'])
        print(self.CityRank)
       
        for i in range(len(self.CityRank)):
            # assigning the rank if it is not in the length-1 or else
            
            if_i = i+1 if i is not (len(self.CityRank) - 1) else i
            self.GeoJsonList['features'].append(
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
        
        with open('Assignments/P01/output.geojson', 'w') as file:
            # open up the output file and then dump the conversion inside
            file.write(json.dumps(self.GeoJsonList, indent=4))
        
if __name__ == '__main__':
    # object called cities of the OrderedCities class
    Cities = OrderedCities()

    # perform the tasks in order to convert to geojson
    # each call goes to the function definition to do the 
    # implementation task by calling the object.(calling function)()
    Cities.ReadInput()
    Cities.FilterCity()
    Cities.rank_cities()
    Cities.FileConversion()