import geopandas
import numpy as np
import matplotlib.pyplot as plt
from numpy.core.numeric import full
from shapely import geometry
from scipy.spatial import cKDTree
import json

clusterFC = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          -112.2719,
          37.0089
        ]
      },
      "properties": {
        "name": "Ooga"
      }
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          -148.6924,
          -1.7586
        ]
      },
      "properties": {
        "name": "Booga"}
    },
    {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          -91.8538,
          -8.7021
        ]
      },
      "properties": {
        "name": "Chooga"}
    }
  ]
}

# point = {
#   "type": "FeatureCollection",
#   "features": [
#       {
#       "type": "Feature",
#       "geometry": {
#         "type": "Point",
#         "coordinates": [
#           -93.3476, 
#           -39.5749
#         ]
#       },
#       "properties": {}
#     }
#   ]
# }

point = geometry.Point([-93.3476,-39.5749])

clusterDF = geopandas.GeoDataFrame.from_features(clusterFC, crs="EPSG:4326")
# pointDF = geopandas.GeoDataFrame.from_features(point, crs="EPSG:4326")

clusterNP = np.array(list(clusterDF.geometry.apply(lambda x: (x.x, x.y))))
# pointNP = np.array(list(pointDF.geometry.apply(lambda x: (x.x, x.y))))

testTree = cKDTree(clusterNP)

_, indices = testTree.query([-93.3476,-39.5749], k=3)
print(indices)
# full_results = (clusterDF.iloc[indices[0]]).to_json()
# print(full_results)

# feature = {
#   "type": "FeatureCollection",
#   "features": []
# }
# for index in indices[0]:
#   feature["features"].append({
#       "type": "Feature",
#       "geometry": {
#         "type": "Point",
#         "coordinates": list(clusterNP[index])
#       },
#       "properties": {}
# #   })

# with open('./Assignments/A04/assets/api/data/test.geojson', 'w') as out:
#   parsed = json.loads(full_results)
#   json.dump(parsed, out, indent="  ")
