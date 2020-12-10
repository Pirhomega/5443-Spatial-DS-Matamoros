from os import path
from sys import argv
from json import load, loads, dump
from urllib.parse import unquote

from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
from numpy import array
from numpy.lib.utils import source
from scipy.spatial import cKDTree
from geopandas import GeoDataFrame, read_file, sjoin
from networkx import read_shp, single_source_dijkstra, has_path, write_shp
from vincenty import vincenty
from time import time, sleep

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
        dump(saveCoords_featurecollection, out, indent="  ")
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
        jsonFeatureCollection = load(infile)
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
        "path": "./Assignments/A05/assets/api/data/earthquakes.geojson",
        "loaded": False
        # "kdtree": scipy.cKDTree()
        # "dataframe": GeoDataFrame()
        # "npArray": np.array()
        },
    "volcanos": {
        "path": "./Assignments/A05/assets/api/data/volcanos.geojson",
        "loaded": False
        # "kdtree": scipy.cKDTree()
        # "dataframe": GeoDataFrame()
        # "npArray": np.array()
        },
    "railroads": {
        "path": "./Assignments/A05/assets/api/data/us_railroads/us_railroads",
        "loaded": True
        # "dataframe": GeoDataFrame()
        # "index": GeoDataFrame.sindex
        # "graph": nx.Graph
    },
    "primary_roads": {
        "path": "./Assignments/A05/assets/api/data/primary_roads_fixed_no_multis/primary_roads_fixed_no_multis",
        "loaded": False
        # "dataframe": GeoDataFrame()
        # "index": GeoDataFrame.sindex
    }
}

# datasets is dictionary of the selected datasets from the frontend: {"earthquakes": 1, "volcanos": 0, "ufos": 0}
def process_datasets(query_datasets, datatype):
    """
    Purpose:    To load queriable datasets into a KDtree, geopandas dataframe, 
                numpy array and store these in a global dictionary

    Inputs:     `query_datasets`: a dictionary with a dataset name and a value of either 0 or 1,
                indicating the dataset must be loaded (e.g. {"earthquakes": 1, "volcanos": 0, "ufos": 0})

    Outputs:    None
    """
    global dataset_map
    # iterate through each dataset check-boxed in the front end, load the data
    #   from the dataset geojson file, create a KD tree from the data
    for dataset in query_datasets:
        # if the dataset checkbox was checked (i.e. the dataset key has a value of 1),
        #   check `dataset_map` if the data has been loaded already. If not, load it
        if query_datasets[dataset]:
            if not dataset_map[dataset]["loaded"]:
                # create a KD tree with the data and store it and the 
                loaded_dataset_with_properties = load_data_into_KDtree(dataset_map[dataset]["path"], datatype)

                dataset_map[dataset]["loaded"] = True
                dataset_map[dataset]["kdtree"] = loaded_dataset_with_properties[0]
                dataset_map[dataset]["dataframe"] = loaded_dataset_with_properties[1]
                # dataset_map[dataset]["npArray"] = loaded_dataset_with_properties[2]
    
def load_data_into_KDtree(path_to_dataset, datatype):
    """
    Purpose:    Reads geospatial data from a file and store it in a KD-tree, 
                numpy array, and geopandas dataframe

    Inputs:     `path_to_dataset`: A string of the path to the 'dataset.geojson' file
                `datatype`: A string indicating the geospatial data stored in the dataset
                    (e.g. Point, MultiPoint, LineString, MultiLineString, Polygon, Multipolygon)

    Outputs:    `datasetKD`: A KD-tree of the .geojson data
                `datasetDF`: A Geopandas dataframe of the .geojson data
                `datasetNP': A numpy array of the .geojson data points
    """
    road_data = ''
    if path.isfile(path_to_dataset):
        with open(path_to_dataset, 'r') as f:
            road_data = f.read()
    else:
        print("Incorrect path to dataset. Check DATASET_MAP and see if the path is correct.")

    dataset = loads(road_data)
    datasetNP = array([])
    datasetDF = True

    if datatype == "Point":
        # creates a geopandas dataframe with the road_data
        datasetDF = GeoDataFrame.from_features(dataset, crs="EPSG:4326")
        # since cKDTree needs an array-like object to query nearest neighbors, we create
        #   such an array
        datasetNP = array(list(datasetDF.geometry.apply(lambda x: (x.x, x.y))))

    elif datatype == "MultiLineString":
        dataset_list = []
        for feature_document in dataset['features']:
            for line in feature_document['geometry']['coordinates']:
                for point in line:
                    dataset_list.append({
                        'type': 'Feature',
                        'properties': {
                            'FULLNAME': feature_document['properties']['FULLNAME'],
                        },
                        'geometry': {
                            'type': 'Point',
                            'coordinates': point
                        }
                    })
        print("Creating dataframe")
        # creates a geopandas dataframe with the road_data
        datasetDF = GeoDataFrame.from_features(dataset_list, crs="EPSG:4326")
        datasetDF.drop_duplicates(inplace=True)
        # datasetDF = datasetDF.set_geometry('GEOMETRY', crs="EPSG:4326")


        ### MAYBE CREATE A DATASET OF JUST INTERSECTIONS AND ROAD-TO-ROAD CONNECTIONS, SO WHEN I DO
        ###     THIS BINARY SPLITTING TECHNIQUE, IT FIRST SEARCHES FOR INTERSECTIONS (WHICH I ASSUME
        #       WOULD BE FEWER THAN THE NUMBER OF POINTS IN A GIVEN ROAD)


        print("done")
        print("Creating numpy array of road data")
        print(datasetDF.geometry)
        datasetNP = list(datasetDF.geometry.apply(lambda x: (x.x, x.y)))
        # print(datasetNP)
        print("done")

    # populate the KD tree
    print("Creating k-d tree")
    datasetKD = cKDTree(datasetNP)
    print("done")
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
    queryDict = loads(request.args.get("NNparams"))

    # load all datasets to be queried for querying
    process_datasets(queryDict["datasets"], "Point")
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
                print(indices)
                full_results += loads((dataset_map[dataset]['dataframe'].iloc[indices]).to_json())['features']
    # if the query is to return all neighbors within a radius
    else:
        for dataset in dataset_map:
            if queryDict['datasets'][dataset]:
                # the only difference between this block and the one up there is the `query_ball_point` call, which takes
                #   the center of the query circle `[lng, lat]` and the radius, `r`
                indices = dataset_map[dataset]['kdtree'].query_ball_point([lng, lat], r=int(queryDict["queryType"]["value"]))
                full_results += loads((dataset_map[dataset]['dataframe'].iloc[indices]).to_json())['features']
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

direction_dataset_map = {}

def load_cities():
    """
    Purpose:    Organizes a data file of USA cities by their first letter within a dictionary

    Input:      None

    Output:     None
    """
    global distance_map
    # creates a dict mapping cities to a key equal to the first character in their name
    city_letter_map = {}
    data = loads(open(distance_map["cities"]["path"], 'r').read())
    for document in data["features"]:
        first_letter_of_name = document["properties"]["name"][0]
        # if the first character of that city has not been added to the map
        #   add it
        if first_letter_of_name not in city_letter_map:
            city_letter_map[first_letter_of_name] = []
        city_letter_map[first_letter_of_name].append(document)
    distance_map["cities"]["map"] = city_letter_map
    distance_map["cities"]["loaded"] = True

def load_city_docs(source, dest):
    # find the cities and append the JSON object to `cityDist_Features`
    #   to send back to the front end
    features = []
    for city_document in distance_map["cities"]["map"][source[0]]:
        if city_document["properties"]["name"] == source:
            features.append(city_document)
            break
    for city_document in distance_map["cities"]["map"][dest[0]]:
        if city_document["properties"]["name"] == dest:
            features.append(city_document)
            break
    return features

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
        cityDist_Features = load_city_docs(citySource, cityDest)
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

def add_city_to_graph(city_coords,city_name,nearest_roads, graph):
    """
    Purpose:    Creates a node in the NA roads graph to represent a city,
                    finds the closest points in each of the closest road
                    segments to that city node, and creates an edge between them
    Input:      `city_coords`: a tuple (lon, lat) of the coordinates of a city
                `city_name`: the name of the city to be used to identify the node
                `nearest_roads`: a list of LineStrings representing the nearest roads
                    to the `city_coords`
                `graph`: the NA roads graph
    """
    # add the city to the graph
    graph.add_node(city_coords,name=city_name)
    # graph.remove_node(source_city_coords)
    # initialize `closest_point` to be the first point in `nearest_road`
    closest_point = nearest_roads[0][0]
    # initialize `closest_distance` to be the distance between the first
    #   point in `nearest_road` and the city
    # Must be careful!!! `vincenty` accepts coordinates in (lat,lon) instead
    #   of (lon,lat). I do the switching here, hence the indexing, but I still 
    #   return the closest point as (lon,lat).
    closest_distance = vincenty((nearest_roads[0][0][1],nearest_roads[0][0][0]),(city_coords[1],city_coords[0]))
    # for every point in the road, calculate its distance from the city
    #   node and find the point that's closest to the city
    for road in nearest_roads:
        closest_distance = vincenty((road[0][1],road[0][0]),(city_coords[1],city_coords[0]))
        for vertex_tuple in road:
            current_distance = vincenty((city_coords[1],city_coords[0]),(vertex_tuple[1],vertex_tuple[0]))
            if current_distance < closest_distance:
                closest_distance = current_distance
                closest_point = vertex_tuple
        graph.add_edge(city_coords,closest_point,type="Unpaved")
        # graph.remove_edge(source_city_coords,closest_to_source)

def distance(u,v,d):
    """
    Purpose:    to ultimately determine the distance between two coordinates in a graph
    Inputs:     `u`: a tuple (lon,lat) of a source node
                `v`: a tuple (lon,lat) of a target node
                `d`: the data assigned to the edge between `u` and `v`
    Outputs:    `distance_uv`: the distance in miles between `u` and `v`
    """
    # this function must accept three parameters if called in `single_source_dijkstra`.
    #   `single_source_dijkstra` automatically sends those arguments
    #   `u`: a tuple (lon,lat) of a source node
    #   `v`: a tuple (lon,lat) of a target node
    #   `d`: the data assigned to the edge between `u` and `v`
    distance_uv = vincenty((u[1],u[0]),(v[1],v[0]))
    # since when I loaded the roads shapefile with `geom_attrs=True`,
    #   any data stored for each LineString in the shapefile gets assigned
    #   to the respective graph edges. I use that data here to halve the
    #   distance between `u` and `v` if the road is a railroad
    if d['type'] == "Railroad":
        distance_uv /= 2.0
    # you can do much more here, e.g. if the road is a secondary road,
    #   run a nearest neighbor query for all ufo sightings; depending on
    #   the results, change the `distance_uv` value by a certain amount, like
    #   I did for railroads. Or, for every X number of roads, search for a body
    #   of water. If the body of water is Y miles away, call a function that
    #   creates an edge between two vertices (`v` to `z`, where `z` is the vertex
    #   on the other side of the water) that crosses the body of water with type=bridge.
    return distance_uv

@app.route('/cityDirections/')
def city_directions():
    """
    Purpose:    To create a path between any two USA cities using the NA roads dataset
    Input:      None
    Output:     The path distance in miles OR -1 if no path exists
    """
    # data looks like this: [ "cityname1", "cityname2" ]
    citySource, cityDest = request.args.get("cityArgs",None).split(',')
    citySource = (unquote(citySource)).title()
    cityDest = (unquote(cityDest)).title()
    source_target_list = []
    # only run if both source and destination cities are populated with text
    if citySource and cityDest:
        source_target_list = load_city_docs(citySource, cityDest)
        # identify the source city
        source_city = source_target_list[0]
        source_city_coords = tuple(source_city['geometry']['coordinates'])
        source_city_name = source_city['properties']['name']
        # locate the nearest road segment(s) to source city
        nearest_roads_to_source = [list(linestring.coords) for linestring in list(usrails_and_roads_DF.iloc[list(usrail_and_roads_SI.nearest((source_city_coords[0],source_city_coords[1],source_city_coords[0],source_city_coords[1]), num_results=1))].geometry)]
        
        target_city = source_target_list[1]
        target_city_coords = tuple(target_city['geometry']['coordinates'])
        target_city_name = target_city['properties']['name']
        # find the closest road segment(s) to the target city
        nearest_roads_to_target = [list(linestring.coords) for linestring in list(usrails_and_roads_DF.iloc[list(usrail_and_roads_SI.nearest((target_city_coords[0],target_city_coords[1],target_city_coords[0],target_city_coords[1]), num_results=1))].geometry)]
        
        # adds the source city to the NA roads graph
        if source_city_coords not in US_road_graph:
            add_city_to_graph(source_city_coords, source_city_name, nearest_roads_to_source, US_road_graph)
        
        # adds the target city to the NA roads graph
        if target_city_coords not in US_road_graph:
            add_city_to_graph(target_city_coords,target_city_name,nearest_roads_to_target,US_road_graph)
        
        # if a path exists between the two cities, create a geojson feature of it
        if has_path(US_road_graph,source_city_coords,target_city_coords):
            total_distance, path = single_source_dijkstra(US_road_graph,source_city_coords,target_city_coords,weight=distance)
            path_geojson = {
                'type':'feature',
                'properties':{
                    'source': source_city_name,
                    'destination':target_city_name,
                    'distance': total_distance
                },
                'geometry':{
                    'type':'LineString',
                    'coordinates': [list(point) for point in path]
                }
            }
            # load the path into a GeoDataFrame for processing
            path_df = GeoDataFrame.from_features([path_geojson],crs="epsg:4326")
            # use the buffer method to produce a Polygon of 0.2 degrees thickness surrounding the path
            buffered_path = (path_df.buffer(0.2)).to_crs(crs="epsg:4326")
            # create a dataframe from the buffered path
            buffered_path_df = GeoDataFrame(buffered_path,geometry=buffered_path.geometry)
            buffered_path_df[0] = None
            # perform a spatial join of the buffered path and the ufo sightings, earthquakes, etc dataframe.
            #   This will return all disasters within 0.2 degrees of the path
            join_results = GeoDataFrame(sjoin(disasters_DF,buffered_path_df,lsuffix="left"))
            # from here, dump the path, the buffered path, and the disasters 0.2 degrees from the path to files
            #   for the front end to visualize
            dump(path_geojson,open('./Assignments/A05/assets/api/data/shortest_paths/'+source_city_name+'_'+target_city_name+'.geojson','w'))
            dump(loads(buffered_path.to_json()),open('./Assignments/A05/assets/api/data/shortest_paths/buffered.geojson','w'))
            dump(loads(join_results.to_json(show_bbox=False)),open('./Assignments/A05/assets/api/data/shortest_paths/closest_points.geojson','w'))
            return str(total_distance)
        else:
            return "-1"


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
    process_datasets(BBparams["datasets"], "Point")

    full_results = []
    for dataset in dataset_map:
        # only query the datasets that were checkboxed in the frontend
        if BBparams['datasets'][dataset]:
            # queries the dataset dataframe for all points in `bbox_df`'s bounding box
            points_in_bbox, _ = bbox_df.sindex.query_bulk(dataset_map[dataset]["dataframe"].geometry, predicate='intersects')
            # create a dataframe of all the intersecting points in dataset dataframe
            matches = dataset_map[dataset]["dataframe"].iloc[points_in_bbox]
            full_results += loads(matches.to_json())['features']
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
    BBparams = loads(request.args.get("BBparams", None))
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

    BBparams = loads(request.args.get("BBparams", None))
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
    convex_full_results = loads((convexParams.convex_hull).to_json())
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
        # print("Creating graph. Takes about 4 minutes.")     
        # begin = time()
        # US_road_graph = read_shp("./Assignments/A05/assets/api/data/rails_and_roads/rails_and_roads_rounded.shx", geom_attrs=True, simplify=False).to_undirected()
        # print("Total time:", time()-begin)

        # # loads in my file of ufo sightings, earthquakes, etc
        # disasters_DF = GeoDataFrame.from_file("./Assignments/A05/assets/api/data/vols_eq_ufo/vols_eq_ufo_fixed.shp").to_crs(crs="epsg:4326")

        # # create a dataframe of the us lakes
        # uslakes_DF = GeoDataFrame.from_file("./Assignments/A05/assets/api/data/na_lakes/na_lakes.shp")

        # # create a dataframe of the smaller roads dataset
        # usrails_and_roads_DF = GeoDataFrame.from_file("./Assignments/A05/assets/api/data/rails_and_roads/rails_and_roads_rounded.shp")

        # # create a spatial indices of the lakes and roads datasets
        # uslakes_SI = uslakes_DF.sindex
        # usrail_and_roads_SI = usrails_and_roads_DF.sindex

        app.run(host='0.0.0.0', port=8888, debug=False)
