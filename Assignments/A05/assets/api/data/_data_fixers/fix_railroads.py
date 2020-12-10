from json import loads, dumps
from os import path

data_file = "./Assignments/A04/assets/api/data/us_railroads.geojson"
data = str
if path.isfile(data_file):
    with open(data_file, 'r') as f:
        data = f.read()
dataset = loads(data)

sourceCount = 0
for document in dataset["features"]:
    for point in document["geometry"]["coordinates"]:
        point[0], point[1] = point[1], point[0]
    # document["properties"]["draw_type"] = "line"
    # document["properties"]["source"] = "rail"+str(sourceCount)
    # sourceCount += 1
with open("./us_railroads.geojson", 'w') as out:
    out.write(dumps(dataset, indent="    "))
