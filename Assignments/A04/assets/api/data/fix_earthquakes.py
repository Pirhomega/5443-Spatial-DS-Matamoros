from os import path
from json import loads, dump

data_file = 'Assignments/A04/assets/api/data/earthquakesold.geojson'
if path.isfile(data_file):
    with open(data_file, 'r') as f:
        data = f.read()
else:
    print("Incorrect path to earthquakes")
earthquakes = loads(data)

new_earthquakes = []

earthquake_fc = {
    "type":"FeatureCollection",
    "metadata": {
        "generated":1597559525000,
        "url":"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime=2019-10-01&endtime=2019-10-31",
        "title":"USGS Earthquakes",
        "status":200,
        "api":"1.10.3",
        "count":14492},
    "features":[]
}


for earthquake in earthquakes["features"]:
    earthquake["properties"]["ids"] = earthquake["id"]
    earthquake_fc["features"].append({
        "type":"Feature",
        "properties":earthquake["properties"],
        "geometry":earthquake["geometry"]
        }
    )

with open('Assignments/A04/assets/api/data/earthquakes.geojson', 'w') as outfile:
    dump(earthquake_fc,outfile, indent="    ")