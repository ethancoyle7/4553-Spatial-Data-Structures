############################################################
##                                                        ##
##                                                        ##
##  Ethan Coyle                                           ##
##  Dr. Griffin - CMPS 4551 Spatial Data Structures       ##
##  P05 - APIHelper Class o help with geo spatial data    ##
##                                                        ##
############################################################
##                                                        ##
##  The purpose of this assignment is to create helper    ##
##  classes that aid in the processing of our data file   ##
##  by using fast API to process data this is working by  ##
##  running through port 8080 by calling the main python  ##
##  as helper api and importing the class inside of the data
##                                                        ##
############################################################
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn

#from the geohelper python import our class to be utilizes in our api
#from GeoHelper import GeoraphicData

#loads up API
if __name__ == '__main__':
    ## to use the local host will be hosted on port 8080 and the MAIN.py is the api runner and it is being used as HelperApi
    ## we use the local host 127.0.0.1 for some reason vscode 
    uvicorn.run("MAIN:HelperApi",host="127.0.0.1", port=8080, log_level="debug", reload=True)

HelperApi = FastAPI()# getting our api running
# creating our imports
import geopandas as gdp  # for the gdp spatial data
from shapely.geometry import Polygon # for OutPut polygons
import json # json data
import math # for math calculation

#create class called geographical data that handles helping class methods for processins
# our data

################################################
##                                            ##
##   ██████╗██╗      █████╗ ███████╗███████╗  ##
##  ██╔════╝██║     ██╔══██╗██╔════╝██╔════╝  ##
##  ██║     ██║     ███████║███████╗███████╗  ##
##  ██║     ██║     ██╔══██║╚════██║╚════██║  ##
##  ╚██████╗███████╗██║  ██║███████║███████║  ##
##   ╚═════╝╚══════╝╚═╝  ╚═╝╚══════╝╚══════╝  ##
##                                            ##
################################################
                                        
class GeoraphicData:
    #opening up the input and ouput with try except handling 
  def __init__(self):
      # for the input file try to open the file
    try:
        # try to open the inputfile
        with open('Assignments/P04/GeographicData.json') as infile:
          self.DataWorld = json.load(infile)
        # if opening unsuccessful, toss an error
    except IOError:
        print('there was an error with you file')
        # add exception handling on if there is and error opening up a outputfile
    try: 
      # open up and output file with the gejson format as a writeable file
      self.output = open('Assignments/P04/OutPutFile.geojson', 'w')
    except IOError:
      # if unsuccessful, throw and input output exception
      print("there was an issue creating the output file\n")

  # function definition to determin the polygon of the given country and
  # return the geometry and coordinates from multipolygon to a single polygon
  def PolyGon(self, NameOfCountry):
    PolyGonName = self.CountryListNames(NameOfCountry)
    MultiPolyGon = PolyGonName['geometry']['coordinates']
    SinglePolyGon = self.ToSinglePolygon(MultiPolyGon)
    return SinglePolyGon # return the polygon back
    #finds the DistanceList between 2 nations with a reduction formula using a box to reduce bordering CoordinatePoints
    # read in the first and second polygon and then perform task of finding the PointCenter and then some distance calculations
  #creation of conversion from multi to single poly
  def ToSinglePolygon(self, MultiPolyGon):
    i = 0
    max = 0
    IndexVal = 0  
    for PolyGons in MultiPolyGon:
      if len(PolyGons[0]) > max:
        max = len(PolyGons[0])
        IndexVal = i
        i += 1
    return MultiPolyGon[IndexVal][0]
  def CalculateDistance(self, FirstPolyGon, SecondPolyGon):
    

    Container1 = gdp.GeoSeries(gdp.points_from_xy([x[0] for x in FirstPolyGon], [y[1] for y in FirstPolyGon]))
    Container2 = gdp.GeoSeries(gdp.points_from_xy([x[0] for x in SecondPolyGon], [y[1] for y in SecondPolyGon]))
    DistanceList = []# empty distance list
    for firstpoint in Container1:
        for secondpoint in Container2: # appending the difference in CoordPoints x and y coords
            DistanceList.append(math.sqrt(((firstpoint.x - secondpoint.x)**2)+((firstpoint.y-secondpoint.y)**2)))
    # we need to sort all the distances that we calculated to find the shortest distance and return it back
    DistanceList.sort()
    return DistanceList[0]

    #we need to find the PointCenter point of the polygon now so we create method to find 
    # he PointCenter point of the polygons which we converted to a singlepolygon passing in the parameters of the 
    # self and the singlepolygon that has all the data attached to it
  def CalculateCenterPoint(self, SinglePolyGon):
    GeoData = gdp.GeoSeries(Polygon(SinglePolyGon)) # using gdp geoseries of each polygon of the singlepolygon list 
                                                        # assign it to geodata
        # using the geoseries , utilize pythons built in center calculator centroid to determine the center x and y coord
    PointCenter = [GeoData.centroid[0].x, GeoData.centroid[0].y]
        # passing this back, we has the x and y coordinate of the countrys center point in x and y and we return it
    return PointCenter

    # now we need to find about getting the country
  def FetchCountrys(self):
        # create an empty list for the data 
    OutPut = []
        # for each of the Continent inside of the input file
    for continents in self.DataWorld:
            # and for each of the Countrys inside of the input file
      for name in self.DataWorld[continents]:
                # append the datat to the output list
        OutPut.append(name['properties']['name'])
        # return the list 
    return OutPut
  #find the specified country
  def CountryListNames(self, NameOfCountry):
    for WorldContinent in self.DataWorld:
      for Countrys in self.DataWorld[WorldContinent]:
        if Countrys['properties']['name'] == NameOfCountry:
          return Countrys
  # finding the
  def FetchContinent(self, name):
      # for each of the continets inside of the input file
    for WorldContinent in self.DataWorld:
            # read the countrys inside of the data file and 
      for Countrys in self.DataWorld[WorldContinent]:
                # if the name of the polygon matches the name of th inputted name then return the data
        if name == Countrys['properties']['name']:
          return WorldContinent
# now to test out our helper class lets test some stuff
# start main driver of the porgram 
if __name__ == "__main__":
    GeoCountry= GeoraphicData() # assign value object of the class 
    # for testing sake lets try out four different Countrys and print out
    # to the terminal and see what we get
    print("the data for the country Africa is :\n",GeoCountry.FetchContinent('China'))
    print("the data for the united states is :\n",GeoCountry.FetchContinent('United States'))
    print("the data for the Russia is :\n",GeoCountry.FetchContinent('Russia'))
    print("the data for the United Kingdom is :\n",GeoCountry.FetchContinent('United Kingdom'))
    second= GeoCountry.PolyGon('United States') ## get the polygon of the united states
    First= GeoCountry.PolyGon('Brazil') ## get thBrazile polygon of the united states
    # calculate the distance CoordPoints print to output file
    GeoCountry.CalculateDistance(First,second)
## assign the api to read from the 
ImportedData = GeoraphicData()#our python helper class pushed into 
##############################################################################################
#  █████╗ ██████╗ ██╗        ███╗   ███╗███████╗████████╗██╗  ██╗ ██████╗ ██████╗ ███████╗  ##
# ██╔══██╗██╔══██╗██║        ████╗ ████║██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔══██╗██╔════╝  ##
# ███████║██████╔╝██║        ██╔████╔██║█████╗     ██║   ███████║██║   ██║██║  ██║███████╗  ##
# ██╔══██║██╔═══╝ ██║        ██║╚██╔╝██║██╔══╝     ██║   ██╔══██║██║   ██║██║  ██║╚════██║  ##
# ██║  ██║██║     ██║        ██║ ╚═╝ ██║███████╗   ██║   ██║  ██║╚██████╔╝██████╔╝███████║  ##
# ╚═╝  ╚═╝╚═╝     ╚═╝        ╚═╝     ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═════╝ ╚══════╝  ##
##############################################################################################
                                                                            
#path through the api that leads to all the doc files inside of the requester root directory
@HelperApi.get('/')
async def RootFolder():# create a root folder for all the documents grabbed by the api
    return RedirectResponse(url="/docs")# direct response to the documents folder ending in docs

## use api get method to retrieve the countires
@HelperApi.get('/ListOfCountries/') # api helper getter to get the countries
async def countries(): # we need to give definition to the countries
    countries = ImportedData.FetchCountrys() # go to the method and iterate through infile and find the countries
    OutPut = {'detail': 'Success','countries': countries} # displays list of countries from the file
    return OutPut # return the output result

# api get feature working for below
# use get method in api to get the polygon of specified country
@HelperApi.get('/PolyGon/{country}')
async def PolyGon(country: str): # pass in the string of the country
    country = country.title() # the title of the country
    country = ImportedData.PolyGon(country) # get the polygon 
    OutPut = {'detail': 'Success','polygon': country}# if successful, display the country polygon
    return OutPut

## this api method below working 
#we need to find the center point of the given country
@HelperApi.get('/CountryCenter/{country}')
async def Country_Center(country: str): # type in a country name
    country = country.title() # will look at the title and 
    country = ImportedData.PolyGon(country)# find the polygon of the country
    CountryCenter = ImportedData.CalculateCenterPoint(country) # call the center point method
    OutPut = {'detail': 'Success','point': CountryCenter} # if successful, pass back the center point of the country
    return OutPut#resturn the result

## api get is working on the distance now
## api helper to get the distance between the polygons
@HelperApi.get('/DistanceBetweenCountries/{FirstPolyGon},{SecondPolyGon}')
async def Country_Distance(FirstPolyGon: str, SecondPolyGon: str):# to calculate the distance inside the api use two string country polygons
    SecondPoly= ImportedData.PolyGon(SecondPolyGon) ## get the polygon of the speicifed country
    FirstPoly= ImportedData.PolyGon(FirstPolyGon) ## get polygon of the other country inputted
    DistanceBetween = ImportedData.CalculateDistance(FirstPoly, SecondPoly)# call the class method
    OutPut = {'detail': 'Success','distance': DistanceBetween}# if successful then print out the distance
    return OutPut# return the result

#We want to see what continet a country is located inside 
@HelperApi.get('/Continent/{country}')# creating the index for the continet in the api pass in the country
async def Country_Continet(country: str): #  type in box for executable country finder
    OutPut = {'detail': 'Success','continent': ImportedData.FetchContinent(country.title())} # looks at the continent inside of the geospatial data
    return OutPut# return the result