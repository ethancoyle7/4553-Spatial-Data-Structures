######################################################
## Student - Ethan Coyle                            ##
## Instr.  - Dr. Griffin                            ##
## Class   - Spatial Data Structures                ##
## Assign. - Project 1                              ##
##Overview - The purpose of this program is to      ##
##           Read in a json file containing cities  ##
##           with long,lats, growth and convert to  ##
##           a geojson format for mapping out       ##
######################################################

import json# import json formatting

# first need to read in the json file 
with open("Assignments/P01/testdata.json") as f:
  data = json.load(f)
  # with the json file load the file with 
  # json format and then make a print test of 
  # the data to see if it is working first
print(data)