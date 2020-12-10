import json
import geopandas

def main():
    # process the railroads
    with open("./Assignments/A05/assets/api/data/split_rails.geojson", 'r') as infile:
        railroads = json.load(infile)
        railroadname = 0
        split_rails = {
            "type": "FeatureCollection",
            "features":[]
        }
        for road in railroads['features']:
            # for linestring in road['geometry']['coordinates']:
            new_railroad_feature = {
                'type': 'Feature',
                'properties':{
                    'type': 'railroad',
                    'name': 'railroad'+str(railroadname)
                },
                'geometry':{
                    'type': "LineString",
                    'coordinates': road['geometry']['coordinates']
                }
            }
            split_rails['features'].append(new_railroad_feature)
            railroadname += 1

    # process the car roads
    with open("./Assignments/A05/assets/api/data/split_roads.geojson", 'r') as infile:
        split_roads = {
            "type": "FeatureCollection",
            "features":[]
        }
        roads = json.load(infile)
        roadname = 0
        for road in roads['features']:
            # for linestring in road['geometry']['coordinates']:
            new_road_feature = {
                'type': 'Feature',
                'properties':{
                    'type': 'carroad',
                    'name': 'carroad'+str(roadname)
                },
                'geometry':{
                    'type': "LineString",
                    'coordinates': road['geometry']['coordinates']
                }
            }
            split_roads['features'].append(new_road_feature)
            roadname += 1
        railsDF = geopandas.GeoDataFrame.from_features(split_rails, crs="epsg:4326")
        carroadsDF = geopandas.GeoDataFrame.from_features(split_roads, crs="epsg:4326")
        geopandas.GeoDataFrame.to_file(railsDF,"./Assignments/A05/assets/api/data/rails")
        geopandas.GeoDataFrame.to_file(carroadsDF,"./Assignments/A05/assets/api/data/roads")
        # geopandas.GeoDataFrame.to_file(roadsDF,"./Assignments/A05/assets/api/data/rails_and_roads.geojson",driver="GeoJSON")
        # with open("./Assignments/A05/assets/api/data/rails_and_roads.geojson", 'w') as outfile:
        #     json.dump(split_rail_and_roads_union,outfile,indent=' ')

if __name__ == "__main__":
    main()