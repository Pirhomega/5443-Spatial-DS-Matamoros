from os import path
from json import loads, dump

data_file = "./Assignments/A04/assets/api/data/earthquakes.geojson"
data = str
if path.isfile(data_file):
    with open(data_file, "r") as f:
        data = f.read()
else:
    print("Incorrect path to earthquakes")
earthquakes = loads(data)

source = 0

for earthquake in earthquakes["features"]:
    earthquake["geometry"]["coordinates"].pop(2)
    # earthquake["properties"]["draw_type"] = "symbol"
    # earthquake["properties"]["image"] = "./Assignments/A04/assets/images/icons/danger-15.svg"
    # earthquake["properties"]["source"] = "eq" + str(source)
    # source += 1

with open("./earthquakes.geojson", "w") as outfile:
    dump(earthquakes, outfile, indent="    ")
