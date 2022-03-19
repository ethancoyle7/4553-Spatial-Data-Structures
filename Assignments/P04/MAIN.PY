############################################################
##                                                        ##
##                                                        ##
##  Ethan Coyle                                           ##
##  Dr. Griffin - CMPS 4551 Spatial Data Structures       ##
##  P04 - Helper Class Program for Spatial Data           ##
##                                                        ##
############################################################
##                                                        ##
##  The purpose of this assignment is to create helper    ##
##  classes that aid in the processing of our data file   ##
##  by creating a healper class that helps to iterate     ##
##  through and pull out veairous items from our data file##
##  including polygons a geojson loader and the center    ##
##  of the countries the next assignment will propogate   ##
##  and API using FastAPI to listen on port 8080 for this ##
##                                                        ##
##                                                        ##
############################################################
import geopandas as gdp  # for the gdp spatial data
from shapely.geometry import Polygon # for OutPut polygons
import json # json data
import pandas as pd
import math # for math calculation
import csv


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
            with open('Assignments/P04/countries.geojson') as infile:
                self.DataWorld = json.load(infile)
                print(self.DataWorld)
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
        df1 = pd.read_csv('Assignments/P04/countries.csv')
        #print(df1.head(20))
        for i in range(len(df1.COUNTRY)):# for the length of the file
            if name == df1['COUNTRY'][i]: # if the name matches the data name
                XVal=df1['longitude'][i] # the lognitude is the  x coord
                YVal=df1['latitude'][i]  # lat is the y coord
                coordinate.append((XVal,YVal)) # append these values to the list
                #value= print(df1['longitude'][i],',', df1['latitude'][i])

        return coordinate# return the list with the coordinates for center point

    # returning the country to the user read in the data name and return the continent it islocated on
    def GetContinent(self, name): # still testing to get the center point 
        df2 = pd.read_csv('Assignments/P04/continents.csv')# read in the other data file
        for i in range(len(df2.Country)): # for the whole length of the file checking
            if name == df2['Country'][i]: # if the name match the continent in the data file, 
               continent= df2['Continent'][i] # that continent is where is located 
                #value= print(df2['longitude'][i],',', df2['latitude'][i])
        return continent # return the continent name for better understanding of location
                
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
                print("The name of the country is : ",name, " the coordinates are :\n\n",feature['geometry']['coordinates']) # pass back the coordinate of the specified name 
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
    print(GeoCountry.getCountryList()) # get a list of the country names
    GeoCountry.getPolyGon('Yemen') # lets get the polygon for yemen
    ## GeoCountry.CalculateCenterPoint('Yemen')
    GeoCountry.OutPutGeojson('Yemen') # get an output geojson file for yemen
    second= GeoCountry.getPolyGon('United States') ## get the polygon of the united states
    First= GeoCountry.getPolyGon('Brazil') ## get thBrazile polygon of the united states

    GeoCountry.GetCenterPoint('Bolivia') # get the center point for yemen
    print(GeoCountry.GetContinent('United States'))