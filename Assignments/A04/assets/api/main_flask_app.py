from os import path
from sys import argv
from json import loads
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import rtree
import json
from urllib.parse import unquote

app = Flask(__name__)
CORS(app)

##############################################################################

# # loads a GeoJSON file into memory and stores it as a dictionary
# # Here, we load a file of countries
# def get_countries():
#     data_file = 'data/countries.geo.json'
#     if path.isfile(data_file):
#         with open(data_file, 'r') as f:
#             data = f.read()
#     else:
#         return jsonify({"Error":"countries.geo.json not there!!"})
#     return loads(data)

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

results_featurecollection = {
            'type': 'FeatureCollection',
            'features': []
            }
source = -1

@app.route('/')
def index():
    return 'This is the base route'


@app.route('/saveCoord/')
def saveCoord():
    """
    Purpose:    Receives a latitude and longtitude value from the frontend
                    and uses it to append a properly-formatted geojson feature
                    to the feature collection `results_featurecollection`.
    Input:      Two strings equivalent to a longitude and latitude value
    Output:     A source ID integer that the frontend will use to name the spot
                    on the map represented by the longitude and latitude inputted.
    """
    global source, results_featurecollection
    # the source integer the frontend will use to identify the spot with `lat, lon`
    source += 1
    # the longitude and latitude values from the frontend
    lon, lat = request.args.get("lngLat",None).split(',')
    # append the properly formatted geojson object with the above coords
    #    to the feature collection
    results_featurecollection['features'].append({
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [int(lon), int(lat)]
        },
        'properties': {
            'source': str(source)
        }
    })
    # send the source ID to the frontend for when it creates a layer to
    #   show the coord on the map
    return (str(source))

@app.route('/deleteCoord/')
def deleteCoord():
    """
    Purpose:    Remove all features from the `results_featurecollection` geojson object
                    This is called whenever the frontend erases all spots/layers from
                    map.
    Input:      None
    Output:     A dictionary with a key equal to the number of coords the frontend
                    will delete from the map and a value equal to a list of the
                    feature objects the frontend will delete (these feature objects 
                    are properly formatted geojson features)
    """
    global source, results_featurecollection
    # reset source's value so the next coord to be added to the map will have a source
    #   value of zero
    source = -1
    # the number of coords to erase from the map and results_featurecollection
    coordCount = len(results_featurecollection['features'])
    # save the list of features to be erased to a temp variable.
    #   Then set the 'features' list to be empty
    json_coords_to_be_deleted = results_featurecollection['features']
    results_featurecollection['features'] = []

    return jsonify(coordCount,json_coords_to_be_deleted)

@app.route('/saveJSON/')
def saveJSON():
    """
    Purpose:    Saves feature collection saved in `results_featurecollection`
                    to a .geojson file
    Input:      None
    Output:     A trivial integer that the frontend needs so the backend doesn't crash.
                (The backend needs to return something, apparently)
    """
    with open('./Assignments/A04/assets/api/data/mapCoords.geojson', 'w') as out:
        json.dump(results_featurecollection, out, indent="    ")
    return "1"

@app.route('/loadJSON/')
def loadJSON():
    """
    Purpose:    Loads a properly formatted geojson file into `results_featurecollection`
                    passing the number of feature objects in it and the list of feature
                    objects to the frontend for loading onto a map
    Input:      None
    Output:     A python dictionary with the key equal to the number of feature objects,
                    and a value of a list of feature objects
    """
    with open('./Assignments/A04/assets/api/data/mapCoords.geojson', 'r') as infile:
        global source, results_featurecollection
        # store the .geojson contents into `results_featurecollection`
        results_featurecollection = json.load(infile)
        coordCount = len(results_featurecollection['features'])
        # update source to be equal to the number of feature objects loaded
        #   into the feature collection. That way, the user can add more coords
        #   to the map and the source values resume from the last feature object
        #   loaded here
        source = coordCount
        return jsonify(coordCount,results_featurecollection['features'])

###############################################################################################

dataset_map = {
    "earthquakes": {
        "path": "./Assignments/A04/assets/api/data/earthquakes.geojson",
        "loaded": False,
        "rtree": rtree.index.Index(),
        "idmap": {}
        },
    "volcanos": {
        "path": "./Assignments/A04/assets/api/data/volcanos.geojson",
        "loaded": False,
        "rtree": rtree.index.Index(),
        "idmap": {}
        },
    "ufos": {
        "path": "./Assignments/A04/assets/api/data/ufos.geojson",
        "loaded": False,
        "rtree": rtree.index.Index(),
        "idmap": {}
        }
}

# datasets is dictionary of the selected datasets from the frontend: {"earthquakes": 1, "volcanos": 0, "ufos": 0}
def process_datasets(datasets):
    global dataset_map
    searchable_datasets = []
    for dataset in datasets:
        if datasets[dataset]:
            if not dataset_map[dataset]["loaded"]:
                # CAUSES ERROR BECAUSE IF THIS IF STATEMENT DOESN'T RUN, WE GET A "VARIABLE REFERENCED BEFORE ASSIGNMENT" ERROR DOWN THERE
                loaded_dataset_with_properties = load_data_into_Rtree(dataset_map[dataset]["path"])
                dataset_map[dataset]["loaded"] = True
                dataset_map[dataset]["rtree"] = loaded_dataset_with_properties[0]
                dataset_map[dataset]["idmap"] = loaded_dataset_with_properties[1]
            else:
                loaded_dataset_with_properties = (dataset_map[dataset]["rtree"], dataset_map[dataset]["idmap"])
            # HERE IS WHERE THE ERROR GETS CAUGHT
            searchable_datasets.append(loaded_dataset_with_properties)
    return searchable_datasets
    
def load_data_into_Rtree(path_to_dataset):
    if path.isfile(path_to_dataset):
        with open(path_to_dataset, 'r') as f:
            data = f.read()
    else:
        print("Incorrect path to dataset. Check DATASET_MAP.")
    dataset = loads(data)

    # an rtree that can hold a geometric data structure, like a rectangle or a point,
    #       and an id (which does not have to be unique, but we will make it so). 
    dataset_rtree = rtree.index.Index()
    # since we can't store any more data in the rtree's nodes, we will keep a dictionary
    #       to map the rtree node id's and the id's of the earthquake (in the .json file
    #       we loaded back in `get_earthquakes`)
    rtreeID_to_id = {}
    # the unique id for each node in the R-tree
    id = 0
    for document in dataset["features"]:
        # for every document in the dataset's dictionary, if the coord is
        #       a point, load it into the rtree
        if document["type"] == "Feature" and document["geometry"]["type"] == "Point":
            # 2D coordinates must be loaded into the R-tree as `(topleft_x, topleft_y, bottomright_x, bottomright_y)`
            #       For a point, that's just (x, y, x, y)
            dataset_coord = (document["geometry"]["coordinates"][0], document["geometry"]["coordinates"][1], \
                                document["geometry"]["coordinates"][0], document["geometry"]["coordinates"][1])
            dataset_rtree.insert(id, dataset_coord)
            # map the R-tree id with the actual json data file document
            rtreeID_to_id[id] = document
            id += 1
    return (dataset_rtree, rtreeID_to_id)

# call process_datasets --> [(datasetRtree1, Rtree2DatasetMap1),(datasetRtree2, Rtree2DatasetMap2),(datasetRtree3, Rtree2DatasetMap3)]
# query rtree --> [id1, id2, id3]
# map all id's to id's in Rtree2DatasetMap -> [geojsondocument1, geojsondocument2, geojsondocument3]
# append all results to feature collection -> {geojson feature collection}
# send to frontend -> {query number, feature collection}

queryNum = -1

NN_featurecollection = {
        'type': 'FeatureCollection',
        'features': []
        }

@app.route('/nnQuery/')
def nnQuery():
    global queryNum, NN_featurecollection
    queryNum += 1
    # queryDict = {"datasets":{}, "geojson":{}, "queryType":{}}
    queryDict = json.loads(request.args.get("NNparams"))
    # searchable_datasets = [(datasetRtree1, Rtree2DatasetMap1),(datasetRtree2, Rtree2DatasetMap2),(datasetRtree3, Rtree2DatasetMap3)]
    searchable_datasets = process_datasets(queryDict["datasets"])
    lng = queryDict["geojson"]["geometry"]["coordinates"][0]
    lat = queryDict["geojson"]["geometry"]["coordinates"][1]
    if queryDict["queryType"]["name"] == "nearestN":
        # iterating through a list of tuples
        for dataset in searchable_datasets:
            nearest = list(dataset[0].nearest((float(lng),float(lat),float(lng),float(lat)),int(queryDict["queryType"]["value"])))
            # loop through all five nearest points and append them to `all_nearest_neighbors`
            for coordID in nearest:
                # since the format of the json data is not GeoJSON (it has an 'id' field), 
                #       we create a GeoJSON-friendly dict and append it to `all_nearest_neighbors`
                #       Remember, `dataset[1]` is `rtreeID_to_id` which maps the rtree id to the geojson document
                #       from the original .geojson file
                NN_featurecollection['features'].append({
                        'type': 'Feature',
                        'geometry': dataset[1][coordID]['geometry'],
                        'properties': dataset[1][coordID]['properties']
                    })
    return jsonify(str(queryNum), NN_featurecollection)

@app.route('/deleteNNCoord/')
def deleteNNCoord():
    """
    Purpose:    Remove all features from the `results_featurecollection` geojson object
                    This is called whenever the frontend erases all spots/layers from
                    map.
    Input:      None
    Output:     A dictionary with a key equal to the number of coords the frontend
                    will delete from the map and a value equal to a list of the
                    feature objects the frontend will delete (these feature objects 
                    are properly formatted geojson features)
    """
    global queryNum, NN_featurecollection
    # reset source's value so the next coord to be added to the map will have a source
    #   value of zero
    number_of_queries_to_delete = queryNum + 1
    queryNum = -1
    # save the list of features to be erased to a temp variable.
    #   Then set the 'features' list to be empty
    json_coords_to_be_deleted = NN_featurecollection['features']
    NN_featurecollection['features'] = []

    return str(number_of_queries_to_delete)

distance_map = {
    "cities": {
        "path": "./Assignments/A04/assets/api/data/cities.geojson",
        "loaded": False,
        "map": {}
    }
}

added_cities = []

def load_cities():
    global distance_map
    city_letter_map = {}
    data = json.loads(open(distance_map["cities"]["path"], 'r').read())
    for document in data["features"]:
        first_letter_of_name = document["properties"]["name"][0]
        if first_letter_of_name not in city_letter_map:
            city_letter_map[first_letter_of_name] = []
        city_letter_map[first_letter_of_name].append(document)
    distance_map["cities"]["map"] = city_letter_map
    distance_map["cities"]["loaded"] = True

@app.route('/cities/')
def cities():
    # `city_prompt` is whatever the user has typed into the search field on the front end.
    #   For example, they are trying to type "Wichita", so the instant they type the 'W', 
    #   this function gets called with 'W' as `city_prompt` and grabs all the cities that
    #   start with 'W'. Then they type the 'i', which calls this function with `city_prompt`
    #   now "Wi", grabbing all the cities that start with 'Wi'. Rinse and repeat.
    city_prompt = unquote(request.args.get("hint")).title()
    print(city_prompt)
    # search cities.geojson for all cities that begin with the string `city_prompt`.
    #   Then return those cities as a list. After the user has clicked on the city they want, 
    #   we query the cities.geojson again to grab the coordinates of the city and draw it on
    #   on the map.
    if not distance_map["cities"]["loaded"]:
        load_cities()
    search_results = []
    # `distance_map["cities"]["map"][city_prompt[0]]` is the first letter of the `city_prompt` argument
    if (city_prompt) and (city_prompt[0] in distance_map["cities"]["map"]):
        for city_document in distance_map["cities"]["map"][city_prompt[0]]:
            if city_prompt in city_document["properties"]["name"]:
                search_results.append(city_document["properties"]["name"])
    if search_results == []:
        search_results.append("No results")
    return jsonify(search_results)

@app.route('/cityDist/')
def cityDist():
    global added_cities
    citySource, cityDest = request.args.get("cityArgs",None).split(',')
    citySource = (unquote(citySource)).title()
    cityDest = (unquote(cityDest)).title()
    if citySource and cityDest:
        cityDist_FeatureCollection = {
            "type": "FeatureCollection",
            "features": []
        }
        both_city_coords = []
        for city_document in distance_map["cities"]["map"][citySource[0]]:
            if city_document["properties"]["name"] == citySource:
                added_cities.append(city_document["properties"]["source"])
                cityDist_FeatureCollection["features"].append(city_document)
                both_city_coords.append(city_document["geometry"]["coordinates"])
                break
        for city_document in distance_map["cities"]["map"][cityDest[0]]:
            if city_document["properties"]["name"] == cityDest:
                added_cities.append(city_document["properties"]["source"])
                cityDist_FeatureCollection["features"].append(city_document)
                both_city_coords.append(city_document["geometry"]["coordinates"])
                break
        cityDist_FeatureCollection["features"].append( {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": both_city_coords
                },
                "properties": {
                    "draw_type": "line",
                    "source": citySource+cityDest
                }
            }
        )
        added_cities.append(citySource+cityDest)
    return jsonify(cityDist_FeatureCollection)

@app.route('/deleteCities/')
def deleteCities():
    global added_cities
    added_cities = []
    return jsonify(added_cities)

######################################################################################

if __name__ == '__main__':
    # if the user launched the script in debugger mode
    #       run these tests
    debug = argv[1]
    if debug == "True":
        print("debug on")
        # new_data = get_earthquakes()
        # new_rtree, rtree_map = load_into_rtree(new_data)
        # nearest = list(new_rtree.nearest((-154.4373,57.4443,-154.4373,57.4443),5))
        # for item in nearest:
        #     print(rtree_map[item])
        # loadJSON()
        # load_cities()
    # otherwise, run the app. Open the `world_map.html` in your favorite browser to
    #       begin visualization and interation with the app
    else:
        app.run(host='0.0.0.0', port=8888, debug=True)