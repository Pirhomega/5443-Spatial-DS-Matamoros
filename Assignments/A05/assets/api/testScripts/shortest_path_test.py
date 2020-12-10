import geopandas
import networkx as nx
import json
from math import radians, sin, cos, asin, sqrt
# from numpy import array
# from scipy.spatial import cKDTree
# from geopandas import GeoDataFrame
import time

AVG_EARTH_RADIUS = 6371

cities = [
    (-93.246186557563533, 37.202200207372911),
    (-77.134339809533728, 40.225213299370218),
    (-111.66652125385815, 34.75667724866986),
    (-120.509260399671547, 46.629773780469961),
    (-93.147206183978767, 44.672980047650327),
    (-101.062306281635017, 32.849249578900327)
]

# # creates a geopandas dataframe with the road_data
# quakes_vols_df = geopandas.read_file("./Assignments/A05/assets/api/data/quakes_vols/quakes_vols.shp", crs="EPSG:4326")
# # since cKDTree needs an array-like object to query nearest neighbors, we create
# #   such an array
# quakes_vols_NP = array(list(quakes_vols_df.geometry.apply(lambda x: (x.x, x.y))))
# quakes_vols_tree = cKDTree(quakes_vols_NP)

source_dict = {}

def haversine(source, target, data):
    """ Calculate the great-circle distance between two points on the Earth surface.
    :input: two 2-tuples, containing the latitude and longitude of each point
    in decimal degrees.
    Example: haversine((45.7597, 4.8422), (48.8567, 2.3508))
    :output: Returns the distance between the two points.
    The default unit is kilometers. Miles can be returned
    if the ``miles`` parameter is set to True.
    """
    # print(data)
    # unpack latitude/longitude
    lng1 = source[0]
    lat1 = source[1]
    lng2 = target[0]
    lat2 = target[1]

    # convert all latitudes/longitudes from decimal degrees to radians
    lat1, lng1, lat2, lng2 = map(radians, (lat1, lng1, lat2, lng2))

    # calculate haversine
    lat = lat2 - lat1
    lng = lng2 - lng1
    d = sin(lat * 0.5) ** 2 + cos(lat1) * cos(lat2) * sin(lng * 0.5) ** 2
    h = 2 * AVG_EARTH_RADIUS * asin(sqrt(d))
    return h * 0.621371  # in miles
    # else:
    #     return h  # in kilometers

# def adjust_weight(source, target, data):
#     distance = haversine(source, target)
#     indices = quakes_vols_tree.query_ball_point(list(target), r=0.5)
#     return len(indices)/distance
#     # full_results += loads((dataset_map[dataset]['dataframe'].iloc[indices]).to_json())['features']

print("Loading the shape file.")
G = nx.to_undirected(nx.read_shp("./Assignments/A05/assets/api/data/rails_and_roads/rails_and_roads.shx", geom_attrs=True, simplify=False))
# G = nx.read_shp("./Assignments/A05/assets/api/data/primary_roads_fixed_no_multis/primary_roads_fixed_no_multis.shx",
#                 geom_attrs=True, simplify=False)

# primary_roads = geopandas.read_file("./Assignments/A05/assets/api/data/primary_roads_fixed_no_multis/primary_roads_fixed_no_multis.shp")

print("Generating MST...")
# start_time = time.time()
# for source in range(len(cities)-1):
for target in range(1):
    MST_Feature_Collection = {
        "type": 'FeatureCollection',
        'features':[]
    }
    distance_st, path_st = nx.single_source_dijkstra(G,source=(-93.246186557563533, 37.202200207372911),target=cities[target])
    distance_ts, path_ts = nx.single_source_dijkstra(G,source=cities[target],target=(-93.246186557563533, 37.202200207372911))
    print(distance_st,distance_ts)
    if distance_st < distance_ts:
        path = path_st
    else:
        path = path_ts

    feature = {
        'type': 'Feature',
        'properties': {
            'distance': min(distance_ts,distance_st)
        },
        'geometry': {
            'type': 'LineString',
            'coordinates': [ ]
        }
    }

    for coord in path:
        feature['geometry']['coordinates'].append(list(coord))
    MST_Feature_Collection['features'].append(feature)
# print("Total time (s):", time.time() - start_time)
    json.dump(MST_Feature_Collection, open("C:/Users/Owner/Desktop/5443-Spatial-DS-Matamoros/Assignments/A05/assets/api/data/shortest_path"+str(target)+".geojson", 'w'), indent='  ')

