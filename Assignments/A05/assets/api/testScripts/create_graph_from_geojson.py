# import geopy.distance
import networkx as nx
import geopandas
import matplotlib.pyplot as plt

major_roads = geopandas.GeoSeries.from_file("./assignments/A05/assets/api/data/Primary_Roads.geojson")
major_roads_union = major_roads.unary_union
print(type(major_roads_union))
# G = nx.Graph()
# for line in major_roads_union:
#     for seg_start, seg_end in zip(list(line.coords),list(line.coords)[1:]):
#         G.add_edge(seg_start, seg_end) 

# pos = nx.spring_layout(G)
# nx.draw_networkx_edges(G, pos, width=0.25, arrowsize=1)
# plt.title("Test me daddy")
# plt.show()
# coords_1 = (52.2296756, 21.0122287)
# coords_2 = (52.406374, 16.9251681)

# print(geopy.distance.distance(coords_1, coords_2).miles)


