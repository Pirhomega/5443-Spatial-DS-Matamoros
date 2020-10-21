from json import loads, dumps
from os import path

data_file = "./Assignments/A04/assets/api/data/ufos.geojson"
data = str
if path.isfile(data_file):
    with open(data_file, 'r') as f:
        data = f.read()
dataset = loads(data)

sourceCount = 0
for document in dataset["features"]:
    document["properties"]["draw_type"] = "symbol"
    document["properties"]["image"] = "./Assignments/A04/assets/images/icons/globe-15.svg"
    document["properties"]["source"] = "ufo"+str(sourceCount)
    sourceCount += 1
with open("./cities_new.geojson", 'w') as out:
    out.write(dumps(dataset, indent="    "))
