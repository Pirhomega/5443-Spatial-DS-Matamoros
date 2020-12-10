import json
with open("./Assignments/A05/assets/api/data/rails_and_roads_temp/rails_and_roads.geojson",'r') as infile:
    new_FC = {
        'type': "FeatureCollection",
        'features': []
    }
    data = json.load(infile)
    for road_feature in data['features']:
        if road_feature['geometry']['type'] == "MultiLineString":
            for linestring in road_feature['geometry']['coordinates']:
                for coord in linestring:
                    coord[0] = round(coord[0],7)
                    coord[1] = round(coord[1],7)
        else:
            for coord in road_feature['geometry']['coordinates']:
                coord[0] = round(coord[0],7)
                coord[1] = round(coord[1],7)
    json.dump(data,open("./Assignments/A05/assets/api/data/rails_and_roads_temp/rails_and_roads_rounded.geojson",'w'),indent=' ')