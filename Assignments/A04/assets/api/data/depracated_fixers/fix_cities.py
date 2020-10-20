from json import loads, dumps
from os import path

data_file = "./Assignments/A04/assets/api/data/cities.geojson"
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
for document in dataset["features"]:
    document["properties"].pop("marker-color", None)
    document["properties"]["draw_type"] = "symbol"
    document["properties"]["image"] = "./Assignments/A04/assets/images/icons/city-15.svg"
with open("./cities_new.geojson", 'w') as out:
    out.write(dumps(dataset,indent="    "))