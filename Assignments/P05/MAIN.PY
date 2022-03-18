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



HelperApi = FastAPI()# getting our api running



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
import geopandas as gdp  # for the gdp spatial data
from shapely.geometry import Polygon # for OutPut polygons
import json # json data
import pandas as pd
import math # for math calculation
import csv

class Geography:
    def __init__(self): # working 
      # for the input file try to open the file
        try:
        # try to open the inputfile
            with open('Assignments/P05/countries.geojson') as infile:
                self.DataWorld = json.load(infile)
                #print(self.DataWorld)
        # if opening unsuccessful, toss an error
        except IOError:
            print('there was an error with you file')
        # add exception handling on if there is and error opening up a outputfile
        try: 
      # open up and output file with the gejson format as a writeable file
            self.output = open('Assignments/P05/OutPutFile.geojson', 'w')
        except IOError:
      # if unsuccessful, throw and input output exception
            print("there was an issue creating the output file\n")

    def getCountryList(self): # working
        DictList=[] 
        for feature in self.DataWorld['features']:
             #print(feature['geometry']['type'])# type of the country
            DictList.append(feature['properties']['name'])# name of the country
        return(DictList) # returns the dictionary list of all the country names
                #print (feature['geometry']['coordinates']) # coordinates of the country

    def getPolyGon(self,name): # working
        for feature in self.DataWorld['features']:
             #print(feature['geometry']['type'])# type of the country
            if(feature['properties']['name']== name):
                print("The name of the country is : ",name, " the coordinates are :\n\n",feature['geometry']['coordinates']) # pass back the coordinate of the specified name 
            coordinates=feature['geometry']['coordinates']
            return coordinates 


    # neeeding work 
    def GetCenterPoint(self, name): # still testing to get the center point 
        coordinate=[]
        df1 = pd.read_csv('Assignments/P05/countries.csv')
        print(df1.head(20))
        for i in range(len(df1.COUNTRY)):
            if name == df1['COUNTRY'][i]:
                XVal=df1['longitude'][i]
                YVal=df1['latitude'][i]
                coordinate.append((XVal,YVal))
                value= print(df1['longitude'][i],',', df1['latitude'][i])

        return coordinate
        
                
    # need distance method to work something wonkey now
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

        ## by inputting a name the user can get the geojson format to use and then display the graphical data

    # working geojson # plug into geojson.io
    def OutPutGeojson(self,name):
        for feature in self.DataWorld['features']:
             #print(feature['geometry']['type'])# type of the country
            if(feature['properties']['name']== name):
                #print("The name of the country is : ",name, " the coordinates are :\n\n",feature['geometry']['coordinates']) # pass back the coordinate of the specified name 
                coordinates=feature['geometry']['coordinates']

                OutFile = {
                        "type": "FeatureCollection",
                        "features": []
                    }
                OutFile['features'].append({
                            "type": "Feature",
                            "properties": {},
                            "geometry": {
                            "type": "Polygon",
                            "coordinates": 
                                coordinates
                        
                            }
                        })
    # write to the ouput file

                self.output.write(json.dumps(OutFile, indent=4))
                return OutFile
        
    
#loads up API
if __name__ == '__main__':
    GeoCountry= Geography() # assign value object of the class 
    # print(GeoCountry.getCountryList())
    # GeoCountry.getPolyGon('Yemen')
    # ## GeoCountry.CalculateCenterPoint('Yemen')
    # GeoCountry.OutPutGeojson('Yemen')
    # second= GeoCountry.getPolyGon('United States') ## get the polygon of the united states
    # First= GeoCountry.getPolyGon('Brazil') ## get thBrazile polygon of the united states

    # GeoCountry.GetCenterPoint('Bolivia')
    ## to use the local host will be hosted on port 8080 and the MAIN.py is the api runner and it is being used as HelperApi
    ## we use the local host 127.0.0.1 for some reason vscode 
    uvicorn.run("MAIN:HelperApi",host="127.0.0.1", port=8080, log_level="debug", reload=True)
    
    
ImportedData = Geography()#our python helper class pushed into 
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
    countries = ImportedData.getCountryList() # go to the method and iterate through infile and find the countries
    OutPut = {'detail': 'Success','countries': countries} # displays list of countries from the file
    return OutPut # return the output result

# api get feature working for below
# use get method in api to get the polygon of specified country
@HelperApi.get('/PolyGon/{country}')
async def PolyGon(country: str): # pass in the string of the country
    country = country.title() # the title of the country
    country = ImportedData.getPolyGon(country) # get the polygon 
    OutPut = {'detail': 'Success','Polygon': country}# if successful, display the country polygon
    return OutPut
@HelperApi.get('/CountryCenter/{country}')
async def Country_Center(country: str): # type in a country name
    country = country.title() # will look at the title and 
    CountryCenter = ImportedData.GetCenterPoint(country) # call the center point method
    OutPut = {'detail': 'Success','point': CountryCenter} # if successful, pass back the center point of the country
    return OutPut#resturn the result
## api helper to get the distance between the polygons
@HelperApi.get('/FindDistance/{FirstPolyGon},{SecondPolyGon}')
async def Country_Distance(FirstPoly: str, SecondPoly: str):# to calculate the distance inside the api use two string country polygons
    DistanceBetween = ImportedData.CalculateDistance(FirstPoly, SecondPoly)# call the class method
    OutPut = {'detail': 'Success','distance': DistanceBetween}# if successful then print out the distance
    return OutPut# return the result
#We want to see what continet a country is located inside 
@HelperApi.get('/Geojson/{country}')# creating the index for the continet in the api pass in the country
async def GeoJson(country: str): #  type in box for executable country finder
    OutPut = ImportedData.OutPutGeojson(country) # we want the geojson file for the given country
    return OutPut# return the result