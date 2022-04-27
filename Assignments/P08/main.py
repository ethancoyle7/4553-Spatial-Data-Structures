####################################################################################
##                                                                                ##
##  Author- Ethan Coyle                                                           ##                                                
##  Date-   4/27/2022                                                             ##
##  Class-  CMPS 4551                                                             ##
##          Dr. Griffin                                                           ##
##  Assignment- P08                                                               ##    
##                                                                                ##
####################################################################################
##                                                                                ##
##  This is the main file for the program.                                        ##
##                                                                                ##
##  Description:                                                                  ##
##                                                                                ##
##  This program is designed to take in a file and output the following:          ##
##  We will read in our data files for the united states citys and states and then##
##  we are doing a query of each state in the united states and querying the      ##
##  population of the states themselves and depending on the population of the    ##
##  the color coded map display will vary. I decided to start with normal roygbiv ##
##  but I ran out of those so i kept doing light roygbiv colors until ran out     ##
##  again then light brown is the least populated country and the highest populate##
##  country is a black/grey while falls down from 20 million and down  California ##
##  seems to have the highest population while areas like maine have very low pop ##
##  But the purpose of this project is to read the spatial data and do a query ove##
##  the population of the states and cities and then display the map with the     ##
##  color coded states based on their population.                                 ##
##                                                                                ##
####################################################################################

## creating our imports
from turtle import color
import geopandas as gdp, json
from shapely.geometry import Point

#####################################################
# ██╗███╗   ██╗███████╗██╗██╗     ███████╗███████╗ ##
# ██║████╗  ██║██╔════╝██║██║     ██╔════╝██╔════╝ ##
# ██║██╔██╗ ██║█████╗  ██║██║     █████╗  ███████╗ ##
# ██║██║╚██╗██║██╔══╝  ██║██║     ██╔══╝  ╚════██║ ##
# ██║██║ ╚████║██║     ██║███████╗███████╗███████║ ##
# ╚═╝╚═╝  ╚═══╝╚═╝     ╚═╝╚══════╝╚══════╝╚══════╝ ##
#####################################################
                                                

# attempt to read from the input files to process our data
try:
    with open('Assignments/P08/states.geojson') as GeoStates:
        states = gdp.read_file(GeoStates)
except IOError:
    print("unable to open the file\nplease try another file")
try:
    with open('Assignments/P08/cities.json') as JsonCity:
        JsonCities = json.load(JsonCity)
except IOError:
    print("unable to open the file\nplease try another file")
try:
    with open('Assignments/P08/states.geojson') as StateDat:
        JsonStates = json.load(StateDat)
except IOError:
    print("unable to open the file\nplease try another file")

print("we done with reading from the input files now time to process some data")

JsonStates = JsonStates['features'] # get the features from the json file
DictOfStates = {} # create a dictionary to store the states
GeojsonContainer = {
            "type": "FeatureCollection",
            "features": []
         }
################################################
#  ██████╗ ██╗   ██╗███████╗██████╗ ██╗   ██╗ ##
# ██╔═══██╗██║   ██║██╔════╝██╔══██╗╚██╗ ██╔╝ ##
# ██║   ██║██║   ██║█████╗  ██████╔╝ ╚████╔╝  ##
# ██║▄▄ ██║██║   ██║██╔══╝  ██╔══██╗  ╚██╔╝   ##
# ╚██████╔╝╚██████╔╝███████╗██║  ██║   ██║    ##
#  ╚══▀▀═╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝   ╚═╝    ##
################################################
                                           
for state in JsonStates: # loop through the states
    state['properties']['population'] = 0 # add a population property to the state
    state['properties']['title'] = state['properties']['name'] # add a title property to the state
    state['properties']['stroke'] = "#555555" # add a stroke property to the state
    state['properties']['stroke-width'] = 1 # add a stroke-width property to the state
    state['properties']['fill'] = '#808000' # add a fill property olive color like a ripe little olive

for state in JsonStates: # loop through the states
    DictOfStates[state['properties']['name']] = 0 # add the state to the dictionary
StatePolyGon = gdp.GeoSeries(states['geometry']) # create a geoseries from the states geometries
for i in range(len(JsonCities)): # loop through the cities

    # as part of the geoseries we need to create a point
    CityPoint = Point(JsonCities[i]['longitude'],JsonCities[i]['latitude'])
    # spatial index PointQuery out point using predicate within
    PointQuery = StatePolyGon.sindex.query(CityPoint, predicate='within')
    if PointQuery.size == 1: # if the point is in one state

        DictOfStates[JsonStates[PointQuery.item(0)]['properties'] \
            ['name']] += JsonCities[i]['population']
    else: # if the point is in more than one state
        print("We outside our element now grab your umbrela")
############################################################################
# ██████╗  ██████╗ ██████╗      ██████╗ ██████╗ ██╗      ██████╗ ██████╗  ##
# ██╔══██╗██╔═══██╗██╔══██╗    ██╔════╝██╔═══██╗██║     ██╔═══██╗██╔══██╗ ##
# ██████╔╝██║   ██║██████╔╝    ██║     ██║   ██║██║     ██║   ██║██████╔╝ ##
# ██╔═══╝ ██║   ██║██╔═══╝     ██║     ██║   ██║██║     ██║   ██║██╔══██╗ ##
# ██║     ╚██████╔╝██║         ╚██████╗╚██████╔╝███████╗╚██████╔╝██║  ██║ ##
#╚═╝      ╚═════╝ ╚═╝          ╚═════╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═╝  ##
############################################################################
                                                                       
for Key, Value in DictOfStates.items(): # loop through the states and their populations
    for StateData in JsonStates: # loop through the states
        if StateData['properties']['name'] == Key: # the name of the state is the key
            StateData['properties']['population'] = Value # the value of the state is the value
            #set default value for the propetries fill
            

            # compare the value of the key and change the color depending on the value of the ke
            if Value < 20000000  and Value >= 15000000: # if the value is between 15 and 20 million
                        StateData['properties']['fill'] = '#FF0000' # change the fill to red'  
            elif Value < 15000000 and Value >= 10000000: # if the value is between 10 and 15 million
                        StateData['properties']['fill'] = '#FFA500' # change the fill to orange
            elif Value < 10000000 and Value >= 9000000: # if the value is between 9 and 10 million
                        StateData['properties']['fill'] = '#FFFF00' # change the fill to yellow
            elif Value < 9000000 and Value >= 8000000: # if the value is between 8 and 9 million
                        StateData['properties']['fill'] = '#008000' # change the fill to green
            elif Value < 8000000 and Value >= 7000000: # if the value is between 7 and 8 million
                        StateData['properties']['fill'] = '#0000FF' # change the fill to blue'       
            elif Value < 7000000 and Value >= 6000000: # if the value is between 6 and 7 million
                        StateData['properties']['fill'] = '#800080' # change the fill to purple
            elif Value < 6000000 and Value >= 5000000: # if the value is between 5 and 6 million
                        StateData['properties']['fill'] = '#FF00FF' # magenta 

            # after following roygbiv we do lighter colors of roygbiv
            elif Value < 5000000 and Value >= 4000000: # if the value is between 4 and 5 million
                        StateData['properties']['fill'] = '#FF6347' # tomator color
            elif Value < 4000000 and Value >= 3000000: # if the value is between 3 and 4 million
                        StateData['properties']['fill'] = '#FF8C00' # orange color lighter'        
            elif Value < 3000000 and Value >= 2000000: # if the value is between 2 and 3 million
                        StateData['properties']['fill'] = '#FFD700' # yellow color lighter' gold
            elif Value < 2000000 and Value >= 1000000: # if the value is between 1 and 2 million
                        StateData['properties']['fill'] = '#7CFC00' # green color lighter''     
            elif Value < 1000000 and Value >= 500000: # if the value is between 0.5 and 1 million
                        StateData['properties']['fill'] = '#00FFFF' # cyan color lighter''
            elif Value < 500000 and Value >= 250000: # if the value is between 0.25 and 0.5 million
                        StateData['properties']['fill'] = '#7B68EE' # blue color lighter'' more blue violet indigo color'       
            elif Value < 250000 and Value >= 100000:            # if the value is between 0.1 and 0.25 million
                        StateData['properties']['fill'] = '#EE82EE' # violet color lighter''' 
            # ran out of roygbiv color      
            elif Value < 100000: # if the value is less than 0.1 million
                        StateData['properties']['fill'] = '#FFDEAD' # brown color lighter'''
            else: 
                        StateData['properties']['fill'] = '#000000' # population greater than 20 million black color
                        
            # lets see the state and itspopulation
            print("our state is :", StateData['properties']['name'],"and the population is :", StateData['properties']['population'],'\n')
            print(" the fill is :", StateData['properties']['fill'])


for StateInfo in JsonStates:
    GeojsonContainer['features'].append(StateInfo) # append all the info for the states to the GeojsonContainer
print("now we goin to run through the city data for each city in the files")
#######################################################################
#  ██████╗██╗████████╗██╗   ██╗    ██████╗  █████╗ ████████╗ █████╗  ##
# ██╔════╝██║╚══██╔══╝╚██╗ ██╔╝    ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗ ##
# ██║     ██║   ██║    ╚████╔╝     ██║  ██║███████║   ██║   ███████║ ##
# ██║     ██║   ██║     ╚██╔╝      ██║  ██║██╔══██║   ██║   ██╔══██║ ##
# ╚██████╗██║   ██║      ██║       ██████╔╝██║  ██║   ██║   ██║  ██║ ##
#  ╚═════╝╚═╝   ╚═╝      ╚═╝       ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝ ##
#######################################################################
                                                                  
for city in JsonCities:
    CityData = {
        "type": "Feature",
        "properties":{},
        "geometry":{
            "type": "Polygon",
            "coordinates": [
                [
                    [city['longitude'] + .1, city['latitude']],
                    [city['longitude'], city['latitude']+.1],
                    [city['longitude'] - .1, city['latitude']],
                    [city['longitude'], city['latitude']-.1],
                    [city['longitude'] + .1, city['latitude']],
                ]
            ]
        }

    }
    GeojsonContainer['features'].append(CityData) # append the cities data to the features
###########################################################
#  ██████╗ ██╗   ██╗████████╗███████╗██╗██╗     ███████╗ ##
# ██╔═══██╗██║   ██║╚══██╔══╝██╔════╝██║██║     ██╔════╝ ##
# ██║   ██║██║   ██║   ██║   █████╗  ██║██║     █████╗   ##
# ██║   ██║██║   ██║   ██║   ██╔══╝  ██║██║     ██╔══╝   ##
# ╚██████╔╝╚██████╔╝   ██║   ██║     ██║███████╗███████╗ ##
#  ╚═════╝  ╚═════╝    ╚═╝   ╚═╝     ╚═╝╚══════╝╚══════╝ ##
###########################################################
                                                      
print(" now we gonna print to the output file so can visualize our data in geojson format")
# attempt to open and push the output file data to the output
try:
    with open('Assignments/P08/PopulationMap.geojson', 'w') as OutPut:
        OutPut.write(json.dumps(GeojsonContainer, indent=4)) # write to the output file
except IOError:
    print("there was some issue with the output file openeing good day pilgrim")
finally:
    print("All set Pilgrim we are done. now to plymoth rock")
