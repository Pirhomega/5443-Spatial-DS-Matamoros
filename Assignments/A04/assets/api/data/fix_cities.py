from json import loads, dumps
from os import path

data_file = "./Assignments/A04/assets/api/data/cities_old.geojson"
if path.isfile(data_file):
    with open(data_file, 'r') as f:
        data = f.read()
dataset = loads(data)
feature_collection = {
    "type": "FeatureCollection",
    "features": []
}
sourceCount = 0
for document in dataset:
    if document["geometry"]["type"] == "Point":
        document["properties"]["draw_type"] = "circle"
        document["properties"]["source"] = "city"+str(sourceCount)
        feature_collection["features"].append(document)
        sourceCount += 1
with open("./cities_new.geojson", 'w') as out:
    out.write(dumps(feature_collection,indent="    "))