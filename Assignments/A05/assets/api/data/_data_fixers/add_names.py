import json

with open("C:/Users/Owner/Desktop/5443-Spatial-DS-Matamoros/Assignments/A05/assets/api/data/vols_eq_ufo/vols_eq_ufo.geojson", 'r') as infile:
    data = json.load(infile)
    for feature in data["features"]:
        if "volcano" in feature['properties']['source']:
            feature['properties']['source'] = "volcano"
        elif "ufo" in feature['properties']['source']:
            feature['properties']['source'] = "ufo"
        else:
            feature['properties']['source'] = "earthquake"