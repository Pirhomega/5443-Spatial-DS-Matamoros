from types import BuiltinMethodType
from networkx import read_shp, single_source_dijkstra, has_path, write_shp
from geopandas import GeoDataFrame, sjoin
from numpy import array
from scipy.spatial import cKDTree
from json import load, dump, loads, dumps
from time import time
from vincenty import vincenty

def add_city_to_graph(city_coords,city_name,nearest_roads, graph):
    # add the city to the graph
    graph.add_node(city_coords,name=city_name)
    # graph.remove_node(source_city_coords)
    #initialize `closest_point` to be the first point in `nearest_road`
    closest_point = nearest_roads[0][0]
    # initialize `closest_distance` to be the distance between the first
    #   point in `nearest_road` and the city
    # Must be careful!!! `vincenty` accepts coordinates in (lat,lon) instead
    #   of (lon,lat). I do the switching here, hence the indexing, but I still 
    #   return the closest point as (lon,lat).
    closest_distance = vincenty((nearest_roads[0][0][1],nearest_roads[0][0][0]),(city_coords[1],city_coords[0]))
        # for every point in the road, calculate its distance from the city
        #   node and return the point that's closest to the city
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

# if __name__ == "__main__":
# maps the coordinates of cities in the cities dataset to 
# create an undirected graph from the combined railroad and normal roads dataset
print("Creating graph. Takes about 6 minutes.")
begin = time()
US_road_graph = read_shp("./Assignments/A05/assets/api/data/rails_and_roads_temp/rails_and_roads_rounded.shx", geom_attrs=True, simplify=False).to_undirected()
print("Total time:", time()-begin)

# create a KD tree of locations of natural disasters
disasters_KD = cKDTree(array(list(GeoDataFrame.from_file("./Assignments/A05/assets/api/data/vols_eq_ufo/vols_eq_ufo1.shp").geometry.apply(lambda x: (x.x, x.y)))))

# create a dataframe of the us lakes
uslakes_DF = GeoDataFrame.from_file("./Assignments/A05/assets/api/data/na_lakes/na_lakes.shp")

# create a dataframe of the smaller roads dataset
usrails_and_roads_DF = GeoDataFrame.from_file("./Assignments/A05/assets/api/data/rails_and_roads_temp/rails_and_roads_rounded.shp")

# create a spatial indices of the lakes and roads datasets
uslakes_SI = uslakes_DF.sindex
usrail_and_roads_SI = usrails_and_roads_DF.sindex

# load the cities into a dictionary
cities = load(open('./Assignments/A05/assets/api/data/cities.geojson','r'))

# identify the source city
source_city = cities['features'][8]
source_city_coords = tuple(source_city['geometry']['coordinates'])
source_city_name = source_city['properties']['name']
# locate the nearest road segments to New York and...
nearest_roads_to_source = [list(linestring.coords) for linestring in list(usrails_and_roads_DF.iloc[list(usrail_and_roads_SI.nearest((source_city_coords[0],source_city_coords[1],source_city_coords[0],source_city_coords[1]), num_results=1))].geometry)]
# ...add the Point representing New York to the graph, creating an edge between it and the closest point in the closest road segement
# `nearest_roads_to_source` and `nearest_roads_to_target` are Pandas Series
source_nearest_json = loads(usrails_and_roads_DF.iloc[list(usrail_and_roads_SI.nearest((source_city_coords[0],source_city_coords[1],source_city_coords[0],source_city_coords[1]), num_results=1))].to_json())
dump(source_nearest_json,open("./Assignments/A05/assets/api/data/nearest_to_source.geojson",'w'))

if source_city_coords not in US_road_graph:
# find the point in the nearest road LineString to the source and target cities
    add_city_to_graph(source_city_coords, source_city_name, nearest_roads_to_source, US_road_graph)
# # add the city to the graph and connect it to the closest point in the closest road
# US_road_graph.add_node(source_city_coords,name=source_city_name)
# # US_road_graph.remove_node(source_city_coords)
# US_road_graph.add_edge(source_city_coords,closest_to_source,type="Unpaved")
# # US_road_graph.remove_edge(source_city_coords,closest_to_source)

with open("./Assignments/A05/assets/api/data/NewYork2All_logfile.txt",'w') as logfile:
    # find the shortest path from New York to all cities in USA
    # for city_num in range(len(cities['features'])):
    target_city = cities['features'][268]
    target_city_coords = tuple(target_city['geometry']['coordinates'])
    target_city_name = target_city['properties']['name']
    # find the closest road segment to the target city
    nearest_roads_to_target = [list(linestring.coords) for linestring in list(usrails_and_roads_DF.iloc[list(usrail_and_roads_SI.nearest((target_city_coords[0],target_city_coords[1],target_city_coords[0],target_city_coords[1]), num_results=1))].geometry)]

    if target_city_coords not in US_road_graph:
        add_city_to_graph(target_city_coords,target_city_name,nearest_roads_to_target,US_road_graph)
        # # add the city to the graph and connect it to the closest point in the closest road
        # US_road_graph.add_node(target_city_coords,name=target_city_name)
        # # US_road_graph.remove_node(target_city_coords)
        # US_road_graph.add_edge(target_city_coords,closest_to_target,type='Unpaved')
        # # US_road_graph.remove_edge(target_city_coords,closest_to_target)

    print("Finding shortest path from Dallas to Wichita Falls")
    # if has_path(US_road_graph,source_city_coords,target_city_coords):
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
    print("Finding all disasters within 0.5 degrees of path")
    # loads in my file of ufo sightings, earthquakes, etc
    disasters_DF = GeoDataFrame.from_file("./Assignments/A05/assets/api/data/vols_eq_ufo/vols_eq_ufo1.shp").to_crs(crs="epsg:4326")
    # here is a sample path from Wichita Falls to Amarillo that I'm loading as a GeoDataFrame
    path_df = GeoDataFrame.from_features([path_geojson],crs="epsg:4326")
    # I create a buffer from the path, where a buffer is a polygon 0.1 degrees in radius from the path
    buffered_path = (path_df.buffer(0.5)).to_crs(crs="epsg:4326")
    # create a dataframe from the buffered path
    buffered_path_df = GeoDataFrame(buffered_path,geometry=buffered_path.geometry)
    buffered_path_df[0] = None
    # perform a spatial join of the buffered path and the ufo sighting, earthquakes, etc dataframe.
    #   This will return all disasters within 0.1 degrees of the path
    join_results = GeoDataFrame(sjoin(disasters_DF,buffered_path_df,lsuffix="left"))
    # from here, dump the path, the buffered path, and the disasters 0.1 degrees from the path to files
    print("Creating files")
    dump(path_geojson,open('./Assignments/A05/assets/api/data/shortest_paths/'+str(target_city_name)+'.geojson','w'))
    dump(loads(buffered_path.to_json()),open('./Assignments/A05/assets/api/data/shortest_paths/buffered.geojson','w'))
    dump(loads(join_results.to_json(show_bbox=False)),open('./Assignments/A05/assets/api/data/shortest_paths/closest_points.geojson','w'))
    # else:
    #     logfile.write("No path from "+source_city_name+" to "+target_city_name+'\n')
    # print(city_num*100/998, "percent done.")
        
# write_shp(US_road_graph,"./Assignments/A05/assets/api/data/test")
