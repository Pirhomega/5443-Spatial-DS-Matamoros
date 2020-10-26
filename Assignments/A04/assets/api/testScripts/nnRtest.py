import geopandas
import numpy as np
import matplotlib.pyplot as plt
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
      "properties": {}
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
      "properties": {}
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
      "properties": {}
    }
  ]
}

point = {
  "type": "FeatureCollection",
  "features": [
      {
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": [
          -89.2479,
          -12.9911
        ]
      },
      "properties": {}
    }
  ]
}

clusterDF = geopandas.GeoDataFrame.from_features(clusterFC, crs="EPSG:4326")
pointDF = geopandas.GeoDataFrame.from_features(point, crs="EPSG:4326")

clusterNP = np.array(list(clusterDF.geometry.apply(lambda x: (x.x, x.y))))
pointNP = np.array(list(pointDF.geometry.apply(lambda x: (x.x, x.y))))

testTree = cKDTree(clusterNP)

indices = testTree.query_ball_point(pointNP, r=20)
feature = {
  "type": "FeatureCollection",
  "features": []
}
for index in indices[0]:
  feature["features"].append({
      "type": "Feature",
      "geometry": {
        "type": "Point",
        "coordinates": list(clusterNP[index])
      },
      "properties": {}
  })

with open('./Assignments/A04/assets/api/data/test.geojson', 'w') as out:
    json.dump(feature, out, indent="  ")
