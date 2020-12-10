import json

def main():
    # process the car roads
    with open("./Assignments/A05/assets/api/data/roads.geojson", 'r') as infile:
        car_roads = json.load(infile)
        # wipe the properties tag in each document
        for road in car_roads['features']:
            road['properties'] = {'type': 'carroad'}
        with open("./Assignments/A05/assets/api/data/roads_wiped.geojson", 'w') as outfile:
            json.dump(car_roads,outfile,indent='  ')
    
    # process the rail roads
    with open("./Assignments/A05/assets/api/data/railroads.geojson", 'r') as infile:
        rail_roads = json.load(infile)
        # wipe the properties tag in each document
        for road in rail_roads['features']:
            road['properties'] = {'type': 'railroad'}
        with open("./Assignments/A05/assets/api/data/railroads_wiped.geojson", 'w') as outfile:
            json.dump(rail_roads,outfile,indent='  ')

if __name__ == "__main__":
    main()