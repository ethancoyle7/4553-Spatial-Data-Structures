# creating our imports
import geopandas as gdp  # for the gdp spatial data
from shapely.geometry import Polygon # for OutPut polygons
import json # json data
import math # for math calculation

class Geography:
    def __init__(self):
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

    def getCountryList(self):
        DictList=[] 
        for feature in self.DataWorld['features']:
             #print(feature['geometry']['type'])# type of the country
            DictList.append(feature['properties']['name'])# name of the country
        return(DictList) # returns the dictionary list of all the country names
                #print (feature['geometry']['coordinates']) # coordinates of the country
    def getPolyGon(self,name):
        for feature in self.DataWorld['features']:
             #print(feature['geometry']['type'])# type of the country
            if(feature['properties']['name']== name):
                print("The name of the country is : ",name, " the coordinates are :\n\n",feature['geometry']['coordinates']) # pass back the coordinate of the specified name 
            coordinates=feature['geometry']['coordinates']
            return coordinates 
    def CalculateCenterPoint(self, name):
       
        MultiPolyGon= self.getPolyGon(name)
        print(" our multi is \n\n",len(MultiPolyGon))
        print(type(MultiPolyGon))
        for x in MultiPolyGon:
            print(x[20])
        X_Y = []
        for i in range(len(MultiPolyGon)):
            X_Y.append((MultiPolyGon[i], MultiPolyGon[i]))
        print(X_Y)
        for coords in range(len(MultiPolyGon)):
       
            print(coords)
            
        ## by inputting a name the user can get the geojson format to use and then display the graphical data
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
        
    
if __name__ == "__main__":
    GeoCountry= Geography() # assign value object of the class 
    print(GeoCountry.getCountryList())
    GeoCountry.getPolyGon('Yemen')
    ## GeoCountry.CalculateCenterPoint('Yemen')
    GeoCountry.OutPutGeojson('Yemen')