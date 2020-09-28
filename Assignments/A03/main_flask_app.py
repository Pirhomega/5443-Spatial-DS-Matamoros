from os import path
from sys import argv
from json import loads
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import rtree
import json

app = Flask(__name__)
CORS(app)

##############################################################################

# loads a GeoJSON file into memory and stores it as a dictionary
# Here, we load a file of countries
def get_countries():
    data_file = 'data/countries.geo.json'
    if path.isfile(data_file):
        with open(data_file, 'r') as f:
            data = f.read()
    else:
        return jsonify({"Error":"countries.geo.json not there!!"})
    return loads(data)

# loads a JSON file into memory and stores it as a dictionary
# Here, we load a file of earthquakes
# The only problem with this file is it is not a GeoJSON file, so
#       we must make one from scratch and pass it to the frontend
#       whenever we query this earthquake data
def get_earthquakes():
    data_file = 'data/eq_2019_10.json'
    if path.isfile(data_file):
        with open(data_file, 'r') as f:
            data = f.read()
    else:
        return jsonify({"Error":f"{data_file} does not exist!"})
    return loads(data)

# loads all earthquake location data into a R-tree with a unique id
def load_into_rtree(earthquakes):
    # an rtree that can hold a geometric data structure, like a rectangle or a point,
    #       and an id (which does not have to be unique, but we will make it so). 
    earthquake_rtree = rtree.index.Index()
    # since we can't store any more data in the rtree's nodes, we will keep a dictionary
    #       to map the rtree node id's and the id's of the earthquake (in the .json file
    #       we loaded back in `get_earthquakes`)
    rtreeID_to_id = {}
    # the unique id for each node in the R-tree
    id = 0
    for document in earthquakes["features"]:
        # for every document in the earthquakes dictionary, if the location of the earthquakes is
        #       a point, load it into the rtree
        if document["type"] == "Feature" and document["geometry"]["type"] == "Point":
            # 2D coordinates must be loaded into the R-tree as `(topleft_x, topleft_y, bottomright_x, bottomright_y)`
            #       For a point, that's just (x, y, x, y)
            earthquake_coord = (document["geometry"]["coordinates"][0], document["geometry"]["coordinates"][1], \
                                document["geometry"]["coordinates"][0], document["geometry"]["coordinates"][1])
            earthquake_rtree.insert(id, earthquake_coord)
            # map the R-tree id with the actual json data file document
            rtreeID_to_id[id] = document
            id += 1
    return earthquake_rtree, rtreeID_to_id

##############################################################################

@app.route('/')
def index():
    return 'This is the base route'

# when the user clicks the mouse inside the map, grab the N nearest neighbors
#       to the location of the click (location is in world coordinates: lat/lon)
@app.route('/click/')
def click():
    # we use `query_num` to create a unique source for any set of five nearest points
    global query_num
    # ask for the location of the mouse in world coordinates (lon, lat) from the frontend
    lon, lat = request.args.get("lngLat",None).split(",")
    # what we will be passing to the frontend for visualization of the earthquakes
    results_featurecollection = {
                'type': 'FeatureCollection',
                'features': []
                }
    # grabs the five nearest nodes to the click location and returns a list of the R-tree id's
    nearest = list(earthquake_rtree.nearest((float(lon),float(lat),float(lon),float(lat)),5))
    nearest_full = []
    # loop through all five nearest points and append them to `nearest_full`
    for item in nearest:
        # since the format of the json data is not GeoJSON (it has an 'id' field), 
        #       we create a GeoJSON-friendly dict and append it to `nearest_full`
        nearest_full.append({
                'type': 'Feature',
                'geometry': rtreeID_to_id[item]['geometry'],
                'properties': rtreeID_to_id[item]['properties']
            })
    # the FeatureCollection is complete and can be passed to the frontend for visualization
    results_featurecollection['features'] = nearest_full
    query_num += 1
    return jsonify([str(query_num), results_featurecollection])

######################################################################################

# earthquakes rtree and mapping dictionary
earthquake_data = get_earthquakes()
earthquake_rtree, rtreeID_to_id = load_into_rtree(earthquake_data)

query_num = 0

if __name__ == '__main__':
    # if the user launched the script in debugger mode
    #       run these tests
    debug = argv[1]
    if debug == "True":
        print("debug on")
        new_data = get_earthquakes()
        new_rtree, rtree_map = load_into_rtree(new_data)
        nearest = list(new_rtree.nearest((-154.4373,57.4443,-154.4373,57.4443),5))
        for item in nearest:
            print(rtree_map[item])
    # otherwise, run the app. Open the `world_map.html` in your favorite browser to
    #       begin visualization and interation with the app
    else:
        app.run(host='0.0.0.0', port=8888)