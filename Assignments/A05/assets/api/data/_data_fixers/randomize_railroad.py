import json

road_data = json.load(open("./Assignments/A05/assets/api/data/detailed_roads.geojson",'r'))
new_feature_collection = {
    'type':'FeatureCollection',
    'features':[]
}
for road in road_data['features']:
    if road['properties']['type'] == 'Secondary':
        road['properties']['type'] = 'Railroad'
    for linestring in road['geometry']['coordinates']:
        new_feature_collection['features'].append({
                'type':'Feature',
                'properties':road['properties'],
                'geometry': {
                    'type':'LineString',
                    'coordinates':linestring
                }
            }
        )
json.dump(new_feature_collection,open("./Assignments/A05/assets/api/data/detailed_roads_split.geojson",'w'))