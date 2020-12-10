import json
import geopandas

def main():
    # process the railroads
    with open("./Assignments/A05/assets/api/data/split_rails.geojson", 'r') as infile1:
        railroads = json.load(infile1)
        railroad_name = 0
        for railroad in railroads['features']:
            railroad['properties']['name'] = "railroad"+str(railroad_name)
            railroad_name += 1
        with open("./Assignments/A05/assets/api/data/split_roads.geojson", 'r') as infile2:
            roads = json.load(infile2)
            road_name = 0
            for carroad in roads['features']:
                carroad['properties']['name'] = "carroad"+str(road_name)
                road_name += 1
            union = {
                "type": "FeatureCollection",
                "features":[]
            }
            union['features'] = railroads['features'] + roads['features']
            unionDF = geopandas.GeoDataFrame.from_features(union, crs="epsg:4326")
            geopandas.GeoDataFrame.to_file(unionDF,"./Assignments/A05/assets/api/data/rails_and_roads")
            geopandas.GeoDataFrame.to_file(unionDF,"./Assignments/A05/assets/api/data/rails_and_roads.geojson",driver="GeoJSON")

if __name__ == "__main__":
    main()