############################################################
##                                                        ##
##                                                        ##
##  Ethan Coyle                                           ##
##  Dr. Griffin - CMPS 4551 Spatial Data Structures       ##
##  P04 - Helper Classes to help with geo spatial data    ##
##                                                        ##
############################################################
##                                                        ##
##  The purpose of this assignment is to create helper    ##
##  classes that aid in the processing of our data file   ##
##  inside of our datafale we have the coordinates of all ##
##  the WorldContinent in the world and it is a massive fi##
##  the running of this file times out due to the high    ##
##  ammount of data inside of the json file however,      ##
##  we are going to be building and API using fast api to ##
##  read the data set that will aid in the easement and   ## 
## timeout of the issues present here                     ##
##                                                        ##
############################################################

# creating our imports

import geopandas as gdp  # for the gdp spatial data
import numpy  as np# numpy and pandas array
from shapely.geometry import Polygon # for OutPut polygons
import json # json data
import math # for math calculation

#create class called geographical data that handles helping class methods for processins
# our data
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
  def CalculateDistance(self, FirstPolygon, SecondPolygon):
        # getting the PointCenter of 2 polygons to be used in the distance calculator
    Polygon2Center = self.CalculateCenterPoint(SecondPolygon)
    Polygon1Center = self.CalculateCenterPoint(FirstPolygon)
    PolygonList = [Polygon1Center, [Polygon1Center[0], Polygon2Center[1]], Polygon2Center, [Polygon2Center[0], Polygon1Center[1]]]
    PolyGonBounds = Polygon(PolygonList)# get the bounds of the polygon list by creating a giant polygon

    Continent1 = gdp.GeoSeries(gdp.points_from_xy([x[0] for x in FirstPolygon], [y[1] for y in FirstPolygon]))
    Continent2 = gdp.GeoSeries(gdp.points_from_xy([x[0] for x in SecondPolygon], [y[1] for y in SecondPolygon]))

        #creating our spatial indexing with query on the boudngin boxes
    Box1 = Continent1.sindex.query(PolyGonBounds)#Query the spatial index with a single geometry based on the bounding box:
    Box2 = Continent2.sindex.query(PolyGonBounds)#Query the spatial index with a single geometry based on the bounding box:
    DistanceList = [] # create an empty list to be appended to for the distances
        #next lets get some distances betwee the CoordinatePoints
    for point1 in Box1:
      for point2 in Box2:
                # get the distance between the CoordinatePoints between the first and second polygon based on the CoordinatePoints
        DistanceList.append(math.sqrt(((Continent1[point1].x - Continent2[point2].x)**2)+((Continent1[point1].y-Continent2[point2].y)**2))) 
    DistanceList.sort() # sort the sitances which will sort in descending order with shortes path
    PolygonList.append(PolygonList[0]) # append the polygonlist 
        # creating an empty list that gathers the CoordinatePoints in the polygon to the list to be appended and added to a list to 
        # be used later
    PolyGonPoints = []
        # iterate over each of the CoordinatePoints in both boxes
    for CoordinatePoints in Box1: # for each point x and y corrdinates of the first box, append to the polygon ppints
      PolyGonPoints.append([Continent1[CoordinatePoints].x, Continent1[CoordinatePoints].y])

      for CoordinatePoints in Box2: # for the second polygon  we do the same take the x and y coordinated and then append then 
                            # to the polygon point list
        PolyGonPoints.append([Continent2[CoordinatePoints].x, Continent2[CoordinatePoints].y])
        # call the polgyon to geojson      taking as parameters the polgyons of the first
        # polygon and the second polygon and the list that we created  of the polygonlist  as well as the CoordinatePoints for coordinates
    self.PolyGonToGeoJson(PolyGons=[FirstPolygon, SecondPolygon, PolygonList], CoordinatePoints=PolyGonPoints)
    return DistanceList[0]# returning the distance list back to the program

  def PolyGonToGeoJson(self, PolyGons = None, CoordinatePoints = None):
    # standardize our output file formatted in geojson formatting to be utilized 
    # inside of the mapping laytout of Countrys
    OutPut = {
                # we have our feature which is a collection of features
            "type": "FeatureCollection",  # and we have our feature list
            "features": [
                
            ]
        }
        # if there is a polygon and it isnt empty
    if PolyGons != None:
            # for each of the single polygons which were converted, inside of the polygons
      for SinglePolyGon in PolyGons:
              # append the features
        OutPut['features'].append({
                  # features include type, properties, geometry(whcih include the coordinate points and the polygon as its type)
                "type": "Feature",
                "properties": {},
                "geometry": {
                "type": "Polygon",
                "coordinates": [
                      SinglePolyGon
                  ]
              }
          })
        # if we have points and it is not empy
    if CoordinatePoints != None:
            # for each point in the coor points
      for point in CoordinatePoints:
                # append the features of the polys to the output file
        OutPut['features'].append({
                "type": "Feature", # include the type which is feature
                "properties": {},  # properties f the feature
                "geometry": {      # what the geometry is 
                              "type": "Point", # type is point
                              "coordinates": point #add the coordinate points
                            }
                })
        #dump the contents to geojsonoutputfile indent it 4 to make it easier to read
    self.output.write(json.dumps(OutPut, indent=4))

    #we need to find the PointCenter point of the polygon now so we create method to find 
    # he PointCenter point of the polygons which we converted to a singlepolygon passing in the parameters of the 
    # self and the singlepolygon that has all the data attached to it
  def CalculateCenterPoint(self, SinglePolyGon):
    temp = SinglePolyGon # assign to a temporary value
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
    for WorldContinent in self.DataWorld:
            # and for each of the Countrys inside of the input file
      for Countrys in self.DataWorld[WorldContinent]:
                # append the datat to the output list
        OutPut.append(Countrys['properties']['PolyGonName'])
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
    # calculate the distance points print to output file
    GeoCountry.CalculateDistance(First,second)