from os import path
from sys import argv
from json import loads
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from geopandas import GeoDataFrame
import json
import numpy as np
from scipy.spatial import cKDTree
from urllib.parse import unquote

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return 'This is the base route'

"""
 /$$                                       /$$     /$$                           /$$$$$$$$                  /$$          
| $$                                      | $$    |__/                          |__  $$__/                 | $$          
| $$        /$$$$$$   /$$$$$$$  /$$$$$$  /$$$$$$   /$$  /$$$$$$  /$$$$$$$          | $$  /$$$$$$   /$$$$$$ | $$  /$$$$$$$
| $$       /$$__  $$ /$$_____/ |____  $$|_  $$_/  | $$ /$$__  $$| $$__  $$         | $$ /$$__  $$ /$$__  $$| $$ /$$_____/
| $$      | $$  \ $$| $$        /$$$$$$$  | $$    | $$| $$  \ $$| $$  \ $$         | $$| $$  \ $$| $$  \ $$| $$|  $$$$$$ 
| $$      | $$  | $$| $$       /$$__  $$  | $$ /$$| $$| $$  | $$| $$  | $$         | $$| $$  | $$| $$  | $$| $$ \____  $$
| $$$$$$$$|  $$$$$$/|  $$$$$$$|  $$$$$$$  |  $$$$/| $$|  $$$$$$/| $$  | $$         | $$|  $$$$$$/|  $$$$$$/| $$ /$$$$$$$/
|________/ \______/  \_______/ \_______/   \___/  |__/ \______/ |__/  |__/         |__/ \______/  \______/ |__/|_______/ 
"""

saveCoords_featurecollection = {
            'type': 'FeatureCollection',
            'features': []
            }

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
    global saveCoords_featurecollection
    # the longitude and latitude values from the frontend
    lon, lat = request.args.get("lngLat",None).split(',')
    # append the properly formatted geojson object with the above coords
    #    to the feature collection
    saveCoords_featurecollection['features'].append({
        'type': 'Feature',
        'geometry': {
            'type': 'Point',
            'coordinates': [float(lon), float(lat)]
        },
        'properties': {}
    })
    # send the source ID to the frontend for when it creates a layer to
    #   show the coord on the map
    return jsonify(saveCoords_featurecollection['features'])

@app.route('/saveJSON/')
def saveJSON():
    """
    Purpose:    Saves feature collection saved in `results_featurecollection`
                to a .geojson file

    Input:      None

    Output:     A trivial integer that the frontend needs so the backend doesn't crash.
                    (The backend needs to return something, apparently)
    """
    with open('./Assignments/A04/assets/api/data/savedJSON.geojson', 'w') as out:
        json.dump(saveCoords_featurecollection, out, indent="  ")
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
    with open('./Assignments/A04/assets/api/data/savedJSON.geojson', 'r') as infile:
        global saveCoords_featurecollection
        # store the .geojson contents into `saveCoords_featurecollection`
        jsonFeatureCollection = json.load(infile)
        saveCoords_featurecollection["features"] += jsonFeatureCollection["features"]

        return jsonify(saveCoords_featurecollection['features'])

@app.route('/deleteJSON/')
def deleteCoord():
    """
    Purpose:    Remove all features from the `results_featurecollection` geojson object

    Input:      None

    Output:     A dictionary with a key equal to the number of coords the frontend
                    will delete from the map and a value equal to a list of the
                    feature objects the frontend will delete (these feature objects 
                    are properly formatted geojson features)
    """
    global saveCoords_featurecollection
    saveCoords_featurecollection['features'] = []

    return "1"

"""
 /$$   /$$                                                     /$$           /$$   /$$           /$$           /$$       /$$                          
| $$$ | $$                                                    | $$          | $$$ | $$          |__/          | $$      | $$                          
| $$$$| $$  /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$$ /$$$$$$        | $$$$| $$  /$$$$$$  /$$  /$$$$$$ | $$$$$$$ | $$$$$$$   /$$$$$$   /$$$$$$ 
| $$ $$ $$ /$$__  $$ |____  $$ /$$__  $$ /$$__  $$ /$$_____/|_  $$_/        | $$ $$ $$ /$$__  $$| $$ /$$__  $$| $$__  $$| $$__  $$ /$$__  $$ /$$__  $$
| $$  $$$$| $$$$$$$$  /$$$$$$$| $$  \__/| $$$$$$$$|  $$$$$$   | $$          | $$  $$$$| $$$$$$$$| $$| $$  \ $$| $$  \ $$| $$  \ $$| $$  \ $$| $$  \__/
| $$\  $$$| $$_____/ /$$__  $$| $$      | $$_____/ \____  $$  | $$ /$$      | $$\  $$$| $$_____/| $$| $$  | $$| $$  | $$| $$  | $$| $$  | $$| $$      
| $$ \  $$|  $$$$$$$|  $$$$$$$| $$      |  $$$$$$$ /$$$$$$$/  |  $$$$/      | $$ \  $$|  $$$$$$$| $$|  $$$$$$$| $$  | $$| $$$$$$$/|  $$$$$$/| $$      
|__/  \__/ \_______/ \_______/|__/       \_______/|_______/    \___/        |__/  \__/ \_______/|__/ \____  $$|__/  |__/|_______/  \______/ |__/      
                                                                                                     /$$  \ $$                                        
                                                                                                    |  $$$$$$/                                        
                                                                                                     \______/                                         
"""


# the commented key-value pairs in `dataset_map` represent fields that will be added
#   once the nearest neighbor function is called and the datasets are loaded
dataset_map = {
    "earthquakes": {
        "path": "./Assignments/A04/assets/api/data/earthquakes.geojson",
        "loaded": False
        # "kdtree": scipy.cKDTree()
        # "dataframe": GeoDataFrame()
        # "npArray": np.array()
        },
    "volcanos": {
        "path": "./Assignments/A04/assets/api/data/volcanos.geojson",
        "loaded": False
        # "kdtree": scipy.cKDTree()
        # "dataframe": GeoDataFrame()
        # "npArray": np.array()
        }
}

# datasets is dictionary of the selected datasets from the frontend: {"earthquakes": 1, "volcanos": 0, "ufos": 0}
def process_datasets(datasets):
    """
    Purpose:    To load queriable datasets into a KDtree, geopandas dataframe, 
                numpy array and store these in a global dictionary

    Inputs:     `datasets`: a dictionary with a dataset name and a value of either 0 or 1
                (indicating the dataset must be loaded)

    Outputs:    None
    """
    global dataset_map
    # iterate through each dataset check-boxed in the front end, load the data
    #   from the dataset geojson file, create a KD tree from the data
    for dataset in datasets:
        # if the dataset checkbox was checked (i.e. the dataset key has a value of 1),
        #   check `dataset_map` if the data has been loaded already. If not, load it
        if datasets[dataset]:
            if not dataset_map[dataset]["loaded"]:
                # create a KD tree with the data and store it and the 
                loaded_dataset_with_properties = load_data_into_KDtree(dataset_map[dataset]["path"])

                dataset_map[dataset]["loaded"] = True
                dataset_map[dataset]["kdtree"] = loaded_dataset_with_properties[0]
                dataset_map[dataset]["dataframe"] = loaded_dataset_with_properties[1]
                dataset_map[dataset]["npArray"] = loaded_dataset_with_properties[2]
    
def load_data_into_KDtree(path_to_dataset):
    """
    Purpose:    Reads geospatial data from a file and store it in a KD-tree, 
                numpy array, and geopandas dataframe

    Inputs:     `path_to_dataset`: A string of the path to the 'dataset.geojson' file

    Outputs:    `datasetKD`: A KD-tree of the .geojson data
                `datasetDF`: A Geopandas dataframe of the .geojson data
                `datasetNP': A numpy array of the .geojson data points
    """
    data = ''
    if path.isfile(path_to_dataset):
        with open(path_to_dataset, 'r') as f:
            data = f.read()
    else:
        print("Incorrect path to dataset. Check DATASET_MAP and see if the path is correct.")
    dataset = loads(data)
    # creates a geopandas dataframe with the data
    datasetDF = GeoDataFrame.from_features(dataset, crs="EPSG:4326")
    # since cKDTree needs an array-like object to query nearest neighbors, we create
    #   such an array
    datasetNP = np.array(list(datasetDF.geometry.apply(lambda x: (x.x, x.y))))
    # populate the KD tree
    datasetKD = cKDTree(datasetNP)
    return (datasetKD, datasetDF, datasetNP)

# call process_datasets --> [(datasetRtree1, Rtree2DatasetMap1),(datasetRtree2, Rtree2DatasetMap2),(datasetRtree3, Rtree2DatasetMap3)]
# query rtree --> [id1, id2, id3]
# map all id's to id's in Rtree2DatasetMap -> [geojsondocument1, geojsondocument2, geojsondocument3]
# append all results to feature collection -> {geojson feature collection}
# send to frontend -> {query number, feature collection}

@app.route('/nnQuery/')
def nnQuery():
    """
    Purpose:    Performs a nearest neighbor query, returning either the 'N' closest points
                to a geometry, or all points within a certain radius of a geometry
    
    Input:     `NNparams`: a dictionary containing the datasets to be queried, the geometry
                from which the query must be, and the type of query (N nearest neighbors, or
                all within a radius)
    
    Output:     `full_results`: a list of JSON features of all points returned from the nearest
                neighbor query
    """
    full_results = []

    # Input
    #   queryDict = {"datasets":{}, "geojson":{}, "queryType":{}}
    queryDict = json.loads(request.args.get("NNparams"))

    # load all datasets to be queried for querying
    process_datasets(queryDict["datasets"])
    # store the longitude and latitude of the point from the which nearest neighbor query shall be made
    lng, lat = queryDict["geojson"]["geometry"]["coordinates"][0], queryDict["geojson"]["geometry"]["coordinates"][1]
    # if the query is to return the N nearest neighbors
    if queryDict["queryType"]["name"] == "nearestN":
        # iterating through the dataset dictionary
        for dataset in dataset_map:
            # only query the datasets that were checkboxed in the frontend
            if queryDict['datasets'][dataset]:
                # returns the numpy array indices of the nearest neighbors of `[lng, lat]`, nearest to farthest
                _, indices = dataset_map[dataset]['kdtree'].query([lng, lat], k=int(queryDict["queryType"]["value"]))
                # `dataset_map[dataset]['dataframe'].iloc[indices]` produces a dataframe ONLY OF the nearest neighbors 
                #   (each nearest neighbor has the properties data from the dataset input file). 
                #   The dataframe is then converted to a JSON string, which is then parsed into a python dict
                full_results += json.loads((dataset_map[dataset]['dataframe'].iloc[indices]).to_json())['features']
    # if the query is to return all neighbors within a radius
    else:
        for dataset in dataset_map:
            if queryDict['datasets'][dataset]:
                # the only difference between this block and the one up there is the `query_ball_point` call, which takes
                #   the center of the query circle `[lng, lat]` and the radius, `r`
                indices = dataset_map[dataset]['kdtree'].query_ball_point([lng, lat], r=int(queryDict["queryType"]["value"]))
                full_results += json.loads((dataset_map[dataset]['dataframe'].iloc[indices]).to_json())['features']
    return jsonify(full_results)

"""
  /$$$$$$  /$$   /$$                     /$$$$$$$  /$$             /$$                                            
 /$$__  $$|__/  | $$                    | $$__  $$|__/            | $$                                            
| $$  \__/ /$$ /$$$$$$   /$$   /$$      | $$  \ $$ /$$  /$$$$$$$ /$$$$$$    /$$$$$$  /$$$$$$$   /$$$$$$$  /$$$$$$ 
| $$      | $$|_  $$_/  | $$  | $$      | $$  | $$| $$ /$$_____/|_  $$_/   |____  $$| $$__  $$ /$$_____/ /$$__  $$
| $$      | $$  | $$    | $$  | $$      | $$  | $$| $$|  $$$$$$   | $$      /$$$$$$$| $$  \ $$| $$      | $$$$$$$$
| $$    $$| $$  | $$ /$$| $$  | $$      | $$  | $$| $$ \____  $$  | $$ /$$ /$$__  $$| $$  | $$| $$      | $$_____/
|  $$$$$$/| $$  |  $$$$/|  $$$$$$$      | $$$$$$$/| $$ /$$$$$$$/  |  $$$$/|  $$$$$$$| $$  | $$|  $$$$$$$|  $$$$$$$
 \______/ |__/   \___/   \____  $$      |_______/ |__/|_______/    \___/   \_______/|__/  |__/ \_______/ \_______/
                         /$$  | $$                                                                                
                        |  $$$$$$/                                                                                
                         \______/                                                                                 
"""

# dictionary of the USA city data which holds the path to the geojson file,
#   a bool for whether the data is stored in memory, and the mapped data itself
distance_map = {
    "cities": {
        "path": "./Assignments/A04/assets/api/data/cities.geojson",
        "loaded": False,
        "map": {}
    }
}

def load_cities():
    """
    Purpose:    Organizes a data file of USA cities by their first letter within a dictionary

    Input:      None

    Output:     None
    """
    global distance_map
    # creates a dict mapping cities to a key equal to the first character in their name
    city_letter_map = {}
    data = json.loads(open(distance_map["cities"]["path"], 'r').read())
    for document in data["features"]:
        first_letter_of_name = document["properties"]["name"][0]
        # if the first character of that city has not been added to the map
        #   add it
        if first_letter_of_name not in city_letter_map:
            city_letter_map[first_letter_of_name] = []
        city_letter_map[first_letter_of_name].append(document)
    distance_map["cities"]["map"] = city_letter_map
    distance_map["cities"]["loaded"] = True

@app.route('/cities/')
def cities():
    """
    Purpose:    Returns a list of cities that begin with the character input from the frontend

    Input:      `city_prompt`: a string of QWERTY chars

    Output:     `search_results`: a list of city names that begin with `city_prompt`
    """
    # `city_prompt` is whatever the user has typed into the search field on the front end.
    #   For example, they are trying to type "Wichita", so the instant they type the 'W', 
    #   this function gets called with 'W' as `city_prompt` and grabs all the cities that
    #   start with 'W'. Then they type the 'i', which calls this function with `city_prompt`
    #   now "Wi", grabbing all the cities that start with 'Wi'. Rinse and repeat.
    city_prompt = unquote(request.args.get("hint")).title()
    # if the cities are not loaded into `distance_map`, do so
    if not distance_map["cities"]["loaded"]:
        load_cities()
    search_results = []
    # `distance_map["cities"]["map"][city_prompt[0]]` is the first character of the `city_prompt` argument
    # The `if (city_prompt)` prevents all cities being returned as suggestions if the user
    #   deleted their prompt by pressing backspace. The second part of the if statement
    #   after the 'and' prevents any characters other than english letters found on a 
    #   QWERTY keyboard from returning suggestions
    if (city_prompt) and (city_prompt[0] in distance_map["cities"]["map"]):
        for city_document in distance_map["cities"]["map"][city_prompt[0]]:
            if city_prompt in city_document["properties"]["name"]:
                # append any suggestions that contain the prompt to the search results list
                search_results.append(city_document["properties"]["name"])
    # of course, if there are no suggestions, let the user know
    if search_results == []:
        search_results.append("No results")
    return jsonify(search_results)

@app.route('/cityDist/')
def cityDist():
    """
    Purpose:    Process a request from the frontend that returns the goejson features
                of two queried cities, as well as a LineString feature representing the
                'as-the-crows-flies' path between the two
    
    Input:      `citySource`: The name of the source city
                `cityDest`: The name of the destination city
    
    Output:     `cityDist_Features`: a list of the feature documents of the two cities -
                `citySource` and `cityDest` - and the linear LineString connecting them
    """
    citySource, cityDest = request.args.get("cityArgs",None).split(',')
    citySource = (unquote(citySource)).title()
    cityDest = (unquote(cityDest)).title()
    cityDist_Features = []
    # only run if both source and destination cities are populated with text
    if citySource and cityDest:
        # find the cities and append the JSON object to `cityDist_Features`
        #   to send back to the front end
        for city_document in distance_map["cities"]["map"][citySource[0]]:
            if city_document["properties"]["name"] == citySource:
                cityDist_Features.append(city_document)
                break
        for city_document in distance_map["cities"]["map"][cityDest[0]]:
            if city_document["properties"]["name"] == cityDest:
                cityDist_Features.append(city_document)
                break
        # append the LineString connecting both cities to `cityDist_Features`
        cityDist_Features.append({
            'type': "feature",
            'properties': {},
            'geometry': {
                'type': "LineString",
                "coordinates": [
                    cityDist_Features[0]['geometry']['coordinates'],
                    cityDist_Features[1]['geometry']['coordinates']
                ]
            }
        })
    return jsonify(cityDist_Features)

"""
 /$$$$$$$  /$$$$$$$                             /$$$$$$                                         
| $$__  $$| $$__  $$                           /$$__  $$                                        
| $$  \ $$| $$  \ $$  /$$$$$$  /$$   /$$      | $$  \ $$ /$$   /$$  /$$$$$$   /$$$$$$  /$$   /$$
| $$$$$$$ | $$$$$$$  /$$__  $$|  $$ /$$/      | $$  | $$| $$  | $$ /$$__  $$ /$$__  $$| $$  | $$
| $$__  $$| $$__  $$| $$  \ $$ \  $$$$/       | $$  | $$| $$  | $$| $$$$$$$$| $$  \__/| $$  | $$
| $$  \ $$| $$  \ $$| $$  | $$  >$$  $$       | $$/$$ $$| $$  | $$| $$_____/| $$      | $$  | $$
| $$$$$$$/| $$$$$$$/|  $$$$$$/ /$$/\  $$      |  $$$$$$/|  $$$$$$/|  $$$$$$$| $$      |  $$$$$$$
|_______/ |_______/  \______/ |__/  \__/       \____ $$$ \______/  \_______/|__/       \____  $$
                                                    \__/                               /$$  | $$
                                                                                      |  $$$$$$/
                                                                                       \______/ 
"""

def queryBBoxIntersection(BBparams):
    """
    Purpose:    Performs a bounding box query on all selected datasets

    Input:      `BBparams`: a dictionary of the datasets to be queried, and the 
                top left and bottom right corners of the bounding box
    
    Output:     `full_results`: a list of the feature documents of all points
                contained within the bounding box
                `bbox['features']`: a feature document of the bounding box
    """
    # store the top, left, bottom, and right coordinate borders of the bounding box
    top, left, bottom, right = \
        float(BBparams["bbox"][0].split(',')[0]), \
        float(BBparams["bbox"][0].split(',')[1]), \
        float(BBparams["bbox"][1].split(',')[0]), \
        float(BBparams["bbox"][1].split(',')[1])
    # the bounding box's polygon feature
    bbox = {
    'type':"FeatureCollection",
    "features": [{
        "type": "Feature",
        "properties": {
            "name": "United States"
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [
                [
                    [top, left],
                    [top, right],
                    [bottom, right],
                    [bottom, left],
                    [top, left]
                ]
            ]
        }
    }]
    }
    # create a dataframe of the `bbox` feature
    bbox_df = GeoDataFrame.from_features(bbox, crs="EPSG:4326")
    # load the datasets into memory
    process_datasets(BBparams["datasets"])

    full_results = []
    for dataset in dataset_map:
        # only query the datasets that were checkboxed in the frontend
        if BBparams['datasets'][dataset]:
            # queries the dataset dataframe for all points in `bbox_df`'s bounding box
            points_in_bbox, _ = bbox_df.sindex.query_bulk(dataset_map[dataset]["dataframe"].geometry, predicate='intersects')
            # create a dataframe of all the intersecting points in dataset dataframe
            matches = dataset_map[dataset]["dataframe"].iloc[points_in_bbox]
            full_results += json.loads(matches.to_json())['features']
    return full_results, bbox['features']

@app.route('/boundingBoxQuery/')
def boundingBoxQuery():
    """
    Purpose:    To receive a request from the frontend to perform a bounding box
                query on datasets

    Input:      `BBparams`: a dictionary of the datasets to be queried, and the 
                top left and bottom right corners of the bounding box

    Output:     `features + bbox_feature`: a list of all feature documents of points
                contained by the bbox, and the bbox feature document
    """
    BBparams = json.loads(request.args.get("BBparams", None))
    features, bbox_feature = queryBBoxIntersection(BBparams)
    return jsonify(features + bbox_feature)

def createPolygonFromPoints(features):
    """
    Purpose:    Convert a Feature Collection of many features of points
                into a single feature of a polygon

    Input:      `features`: A list of features of points

    Output:     `polygon`: A feature polygon made of the points
    """
    polygon = {
        'type':'Feature',
        'properties': {},
        'geometry': {
            'type': 'Polygon',
            'coordinates': [
                []
            ]
        }
    }
    for feature in features:
        polygon['geometry']['coordinates'][0].append(feature['geometry']['coordinates'])
    return polygon

@app.route("/convexQuery/")
def convexQuery():
    """
    Purpose:    Return the smallest convex polygon that contains a set of points

    Input:      `BBparams`: a dictionary of the datasets to be queried, and the 
                top left and bottom right corners of the bounding box

    Output:     `convex_full_results['features']+intersections`: a list of the
                feature polygon of the convex hull and the points contained by it
    """
    convexFC = {
        'type': "FeatureCollection",
        'features': []
    }

    BBparams = json.loads(request.args.get("BBparams", None))
    # store a feature list of points contained by the bounding box
    intersections, _ = queryBBoxIntersection(BBparams)
    # append to `convexFC` the polygon formed by all the points within the bbox
    convexFC['features'] = [createPolygonFromPoints(intersections)]
    # create a dataframe with the polygon
    convexParams = GeoDataFrame.from_features(convexFC, crs="EPSG:4326")
    # create a geoseries of points that form the smallest convex Polygon
    #   "The convex hull of a geometry is the smallest convex Polygon containing 
    #   all the points in each geometry, unless the number of points in the geometric 
    #   object is less than three. For two points, the convex hull collapses to a 
    #   LineString; for 1, a Point. 
    #       - https://geopandas.readthedocs.io/en/latest/docs/reference/api/geopandas.GeoSeries.convex_hull.html
    convex_full_results = json.loads((convexParams.convex_hull).to_json())
    # return a list of the convex hull and the intersecting points found within the bounding box
    return jsonify(convex_full_results['features']+intersections)

"""
 /$$      /$$           /$$          
| $$$    /$$$          |__/          
| $$$$  /$$$$  /$$$$$$  /$$ /$$$$$$$ 
| $$ $$/$$ $$ |____  $$| $$| $$__  $$
| $$  $$$| $$  /$$$$$$$| $$| $$  \ $$
| $$\  $ | $$ /$$__  $$| $$| $$  | $$
| $$ \/  | $$|  $$$$$$$| $$| $$  | $$
|__/     |__/ \_______/|__/|__/  |__/
"""

if __name__ == '__main__':
    # if the user launched the script in debugger mode
    #       run these tests
    debug = argv[1]
    if debug == "True":
        print("debug on")
        # print(geopandas.read_file("Assignments/A04/assets/api/data/cities.geojson"))
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