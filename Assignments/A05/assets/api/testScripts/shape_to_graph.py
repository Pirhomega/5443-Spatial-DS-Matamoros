import networkx as nx
import json
from math import radians, sin, cos, asin, sqrt

AVG_EARTH_RADIUS = 6371

# front_end_dict = {
#     'datasets': {
#         'railroads': 0,
#         'primary_roads': 1
#     },
#     'cities': ["Wichita Falls", "Wichita"]
# }

def haversine(source, target, data):
    """ Calculate the great-circle distance between two points on the Earth surface.
    :input: two 2-tuples, containing the latitude and longitude of each point
    in decimal degrees.
    Example: haversine((45.7597, 4.8422), (48.8567, 2.3508))
    :output: Returns the distance between the two points.
    The default unit is kilometers. Miles can be returned
    if the ``miles`` parameter is set to True.
    """
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

G = nx.read_shp("./Assignments/A05/assets/api/data/primary_roads_fixed_no_multis/primary_roads_fixed_no_multis.shx",geom_attrs=True,simplify=False)
G_undirected = nx.to_undirected(G)
# results = list(nx.neighbors(G,(-117.064855,34.003941)))
# print(results)
distance = lambda u, v, d: haversine(u,v,d)
path = nx.dijkstra_path(G_undirected,source=(-75.615623, 38.625174),target=(-75.610675, 38.62546),weight=distance)
feature = {
    'type':'Feature',
    'properties':{},
    'geometry': {
        'type':'LineString',
        'coordinates':[

        ]
    }
}
# results = nx.info(G_undirected, (-87.669486, 41.80473599906245))
for coord in path:
    feature['geometry']['coordinates'].append(list(coord))
json.dump(feature, open("C:/Users/Owner/Desktop/5443-Spatial-DS-Matamoros/Assignments/A05/assets/api/data/shortest_path.geojson",'w'),indent='  ')