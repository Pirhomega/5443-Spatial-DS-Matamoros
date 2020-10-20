from json import loads, dumps
from os import path

data_file = "./Assignments/A04/assets/api/data/volcanos1.json"
data = str
if path.isfile(data_file):
    with open(data_file, 'r') as f:
        data = f.read()
dataset = loads(data)
feature_collection = {
    "type": "FeatureCollection", 
    "features": []
    }

sourceCount = 0

for document in dataset["docs"]:
    document.pop('_id', None)
    document["properties"].pop('Latitude', None)
    document["properties"].pop('Longitude', None)

    document["properties"]["image"] = "./Assignments/A04/assets/images/icons/volcano-15.svg"
    document["properties"]["draw_type"] = "symbol"
    document["properties"]["source"] = "volcano"+str(sourceCount)

    feature_collection["features"].append(document)
    sourceCount += 1
with open("./volcanos_new.geojson", 'w') as out:
    out.write(dumps(feature_collection, indent="    "))
