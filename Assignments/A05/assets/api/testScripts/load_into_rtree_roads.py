import geopandas as geo
import json
from geopandas.sindex import rtree

with open("./assignments/a05/assets/api/data/grouped_roads_test.geojson", 'r') as infile:
    road_data = json.loads(infile.read())

datasetDF = geo.GeoDataFrame.from_features(road_data, crs="EPSG:4326")
# print(datasetDF)
spatial_index = datasetDF.sindex
# print("number of groups:", len(spatial_index.leaves()))
# for i, group in enumerate(spatial_index.leaves()):
#     group_idx, indices, bbox = group
#     print("Group", group_idx, "contains ", len(indices), "geometries, bounding box:", bbox)
#     i+=1
#     if i == 10:
#         break
nearest = datasetDF.iloc[list(spatial_index.nearest((-101.3363, 32.4112, -101.3363, 32.4112), num_results=1))]
print(nearest)
nearest.to_file("./assignments/a05/assets/api/data/nearest_roads2")