import geopandas
import numpy as np
import matplotlib.pyplot as plt
import json
# a sample bounding box with coordinates ordered as (lon, lat)
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
                    [-153.0531, 63.8539],
                    [-75.5336, 63.8539],
                    [-75.5336, 25.3115],
                    [-153.0531, 25.3115],
                    [-153.0531, 63.8539]
                ]
            ]
        }
    }]
}

points = geopandas.read_file("./Assignments/A04/assets/api/data/savedJSON.geojson")
bbox_df = geopandas.GeoDataFrame.from_features(bbox, crs="EPSG:4326")

convex_hull_points = (points.convex_hull).to_json()

print(convex_hull_points)

# featureC = {
#     'type': "Feature",
#     'properties': {},
#     'geometry': {
#         'type': 'Polygon',
#         'coordinates': [
#             []
#         ]
#     }
# }

# for borderCoord in convex_hull_points:
#     featureC['geometry']['coordinates'][0].append([borderCoord.x, borderCoord.y])
# featureC['geometry']['coordinates'][0].append(featureC['geometry']['coordinates'][0][0])


with open('./Assignments/A04/assets/api/data/test.geojson', 'w') as out:
    parsed = json.loads(convex_hull_points)
    json.dump(parsed, out, indent="  ")

# print(featureC)