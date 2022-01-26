######################################################
## Student - Ethan Coyle                            ##
## Instr.  - Dr. Griffin                            ##
## Class   - Spatial Data Structures                ##
## Assign. - Project 1                              ##
##Overview - The purpose of this program is to      ##
##           Read in a json file containing cities  ##
##           with long,lats, growth and convert to  ##
##           a geojson format for mapping out       ##
##         find highest population state order(1-49)##
##   sort cities west to east on the x coordingate  ##
##   and number 
######################################################

import json
### from rich import print
import random

def randColor():
  r = lambda: random.randint(0,255)
  print('#%02X%02X%02X' % (r(),r(),r()))


def makeFeature(city):
  feature = {
    "type": "Feature",
    "properties": {},
    "geometry": {
      "type": "Point",
      "coordinates": [0,0]
    }
  }

  for key,val in city.items():
    if key == 'latitude':
      feature['geometry']['coordinates'][1] = val
    elif key == 'longitude':
      feature['geometry']['coordinates'][0] = val
    else:
      feature['properties'][key] = val

  return feature

with open("Assignments/P01/testdata.json") as f:
  data = json.load(f)

states = {}

for item in data:
  if not item["state"] in states:
    states[item["state"]] = []

  states[item["state"]].append(item)


for state in states:
  print(f"{state} = {len(states[state])}")

for stateInfo in data:
  print(makeFeature(stateInfo))
  
