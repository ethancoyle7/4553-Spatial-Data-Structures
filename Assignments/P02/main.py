###################################################################
##                  Author - Ethan Coyle                          #
##                  Instr  - Dr. Griffin                          #
##                  Class  - CMPS 4553 Spatial DS                 #
##                  Assign - Convert JSON to GEOJSON              #
##                  Due    - 2/15/2022                            #
##                                                                #
###################################################################
## About  - the purpose of this program is to read in a csv file  #
#           and the city geojson file to calculate the ufo stats  #
#           and pull out the top 100 clostest ufo data  and print #
#           it to a json file to see which are the closest        #
##                                                                #
## Instructions:                                                  #
##       click run on the program(no special tasks needed)        #
##       try excepts added for input and output checking for      #
##       valid files  and the associated output  will print output#
##       so the user can assimilate which are the closts ufo      #
##       sightings                                                #
##                                                                #
## Note - if user working in geo env might have to pip install    #
##        shapely or if using conda use conda install shapely     #
##                                                                #
###################################################################

#############################################################
# ██╗███╗   ███╗██████╗  ██████╗ ██████╗ ████████╗███████╗  #
# ██║████╗ ████║██╔══██╗██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝  #
# ██║██╔████╔██║██████╔╝██║   ██║██████╔╝   ██║   ███████╗  #
# ██║██║╚██╔╝██║██╔═══╝ ██║   ██║██╔══██╗   ██║   ╚════██║  #
# ██║██║ ╚═╝ ██║██║     ╚██████╔╝██║  ██║   ██║   ███████║  #
# ╚═╝╚═╝     ╚═╝╚═╝      ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝  #
#############################################################
                                                        
import csv, json , geopandas
from numpy import sort
from statistics import mean
from shapely.geometry import Point
############################################################################
# ██████╗  █████╗ ████████╗ █████╗     ███████╗██╗██╗     ███████╗███████╗ #
# ██╔══██╗██╔══██╗╚══██╔══╝██╔══██╗    ██╔════╝██║██║     ██╔════╝██╔════╝ #
# ██║  ██║███████║   ██║   ███████║    █████╗  ██║██║     █████╗  ███████╗ #
# ██║  ██║██╔══██║   ██║   ██╔══██║    ██╔══╝  ██║██║     ██╔══╝  ╚════██║ #
# ██████╔╝██║  ██║   ██║   ██║  ██║    ██║     ██║███████╗███████╗███████║ #
# ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝    ╚═╝     ╚═╝╚══════╝╚══════╝╚══════╝ #
############################################################################                                                                   
try:
  with open('Assignments/P02/cities.geojson') as CityInFile:
       CityData= json.load(CityInFile)
except IOError:
  print("there was an error reading in the data!!!")
# now lets try to open up the csv file that has our csv ufo data
try:
  with open('Assignments/P02/UFOSightings.csv') as CSVInFile:
    CsvData = csv.DictReader(CSVInFile, delimiter = ',')
    UFOList = [] # creating an empty list for our uf data
    for row in CsvData:
        #loads csv dictionary into an array
        UFOList.append(row) # for each row inside of our csv file lets append each
                            # row to the list of ufo data so we can use it later
except IOError:
  print("that did not work maybe issue with the file name or path?")

########################################
# ██╗     ██╗███████╗████████╗███████╗ #
# ██║     ██║██╔════╝╚══██╔══╝██╔════╝ #
# ██║     ██║███████╗   ██║   ███████╗ #
# ██║     ██║╚════██║   ██║   ╚════██║ #
# ███████╗██║███████║   ██║   ███████║ #
# ╚══════╝╚═╝╚══════╝   ╚═╝   ╚══════╝ #
########################################                                 
DataPoints = [] #  empty list for the data entry points
DataNames = []  # empty list for our data names of cities
AverageDistances = [] # empty list of the average ufo distances
UFOPointList = [] # lets create a list for the points of the ufo sightings
CityList= [] # empty list to hold our cities from the ufo data
#########################################################################
# ███╗   ███╗ █████╗ ██╗███╗   ██╗     ██████╗ ██████╗ ██████╗ ███████╗ #
# ████╗ ████║██╔══██╗██║████╗  ██║    ██╔════╝██╔═══██╗██╔══██╗██╔════╝ #
# ██╔████╔██║███████║██║██╔██╗ ██║    ██║     ██║   ██║██║  ██║█████╗   #
# ██║╚██╔╝██║██╔══██║██║██║╚██╗██║    ██║     ██║   ██║██║  ██║██╔══╝   #
# ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║    ╚██████╗╚██████╔╝██████╔╝███████╗ #
# ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝     ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝ #
  #######################################################################
                                                                                   
# now that our infiles are read in properly remember out empty lists?
# we now need to read in the features of the data and append some
# values to the empty lists
for CityFeature in CityData["features"]:
    if CityFeature["geometry"]["type"] == "Point": # if the type of geometry is of type point
      # append the coordinates to the the  datapoints list for each occurance 
      DataPoints.append(CityFeature["geometry"]["coordinates"]) 
      # for our empty list DataNames, append the ciy to the empty list
      DataNames.append(CityFeature['properties']['city'])
# for each point inside of the data points list, we append the converted point to points and 
# add it to our list of cities
for point in DataPoints:
    CityList.append(Point(point))
# using geopandas, we need to call geopandas and the geoseries from our recently appended
  # list and then assign it to a geodata 
GeoData = geopandas.GeoSeries(CityList)
OutPutList = [] # empty list to be appended to later
# loop through our geodata within the range of our geodata length
for i in range(len(GeoData)):
    # create and empty list called distance list that will hold our current distances 
    # within the range of our geopandas geo frame 
    DistanceList= []
    # since our data was done using geopandas, we can use .distance to calculate the distance
    GeoArray = GeoData.distance(GeoData[i])
    # for easement sake, lets convert our values to an array
    GeoArray = GeoArray.values 
    # for i in the range of the length of our created geopandas data array
    for i in range(len(GeoArray)):
        if GeoArray[i] != 0: # if the value is not equal to 0
            # we append the data names of that and the geoarray value and append it to the                  
            # # distane we created forming a tuple that is appended to our distance list
            DistanceList.append((DataNames[i], GeoArray[i]))
    #we need to sort by the nearest city using lambda key expression
    DistanceList.sort(key= lambda x: x[1])
    #lets create a format for us to outpue to our json file
    CityInformation = {
        'City': DataNames[i], # pass in the city from datamames at that index
        'Longitude': GeoData[i].x, # pass in the x value
        'Latitude': GeoData[i].y, # pass in that y value
        'Distance': DistanceList  # pass in the distance list associated with that
    }
    # append each of our data for the city to our outputlist
    OutPutList.append(CityInformation)

# we need to iterate through our ufo list data
for point in UFOList: # for the values iterating through the ufo data,
                      # append the longitude and latitude value to our ufo point list
    UFOPointList.append(Point(float(point['lon']), float(point['lat'])))
# lets create a geopandas series of our list of points
UFOGeoData = geopandas.GeoSeries(UFOPointList)

# lets loop through in the range of our geodata
for i in range(len(GeoData)):
    DataArray = UFOGeoData.distance(GeoData[i])
    DataVals = DataArray.values
    #we need to sort based on the closest so using sort function
    # sorts in descending order
    DataVals = sort(DataVals)
    #we need to get the closest  from 0 to 100
    ClosestDistances = DataVals[0:100]
    #next we need to calculate the average of the closest 100 ufos
    Average = round(mean(ClosestDistances), 18)
    # we need to create another block to hold our city data with t     # the editted vales
    CityData = {
        'City': DataNames[i],# read in the data name
        'Longitude': GeoData[i].x, # read in the x point
        'Latitude': GeoData[i].y,  # read in the y point
        'Average UFO': Average # read in the average ufo data
    }
    # now this is done created, append this to the average distance list 
    AverageDistances.append(CityData)

#########################################################
#  ██████╗ ██╗   ██╗████████╗██████╗ ██╗   ██╗████████╗ #
# ██╔═══██╗██║   ██║╚══██╔══╝██╔══██╗██║   ██║╚══██╔══╝ #
# ██║   ██║██║   ██║   ██║   ██████╔╝██║   ██║   ██║    #
# ██║   ██║██║   ██║   ██║   ██╔═══╝ ██║   ██║   ██║    #
# ╚██████╔╝╚██████╔╝   ██║   ██║     ╚██████╔╝   ██║    #
#  ╚═════╝  ╚═════╝    ╚═╝   ╚═╝      ╚═════╝    ╚═╝    #
#########################################################
                                                     
# lets ouput the calculated distance
try:
  with open('Assignments/P02/DISTANCES.json', 'w') as DistanceOutPut:
    # dump out calculated distance to an output file
    DistanceOutPut.write(json.dumps(OutPutList,indent = 4))    
except IOError:
  print('there was an error trying to create the output\n')
finally:
  print("Done with the distance output(hope that worked bonehead), now on to the ufo data\n")
# finally, now that this is all done, lets open up an output file and add this to json output
try:
  with open('Assignments/P02/AVGUFODISTANCES.json', 'w') as FinalOutPut:
    FinalOutPut.write(json.dumps(AverageDistances,indent = 4))    
except IOError:
  print('there was an error trying to create the output\n')
finally:
  print(" we are out of the try except block and done with the problem. I hope that all worked!")

#######################################################################################
# ███████╗███╗   ██╗██████╗      ██████╗ ███████╗    ███╗   ███╗ █████╗ ██╗███╗   ██╗ #
# ██╔════╝████╗  ██║██╔══██╗    ██╔═══██╗██╔════╝    ████╗ ████║██╔══██╗██║████╗  ██║ #
# █████╗  ██╔██╗ ██║██║  ██║    ██║   ██║█████╗      ██╔████╔██║███████║██║██╔██╗ ██║ #
# ██╔══╝  ██║╚██╗██║██║  ██║    ██║   ██║██╔══╝      ██║╚██╔╝██║██╔══██║██║██║╚██╗██║ #
# ███████╗██║ ╚████║██████╔╝    ╚██████╔╝██║         ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║ #
# ╚══════╝╚═╝  ╚═══╝╚═════╝      ╚═════╝ ╚═╝         ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ #
#######################################################################################
                                                                                   