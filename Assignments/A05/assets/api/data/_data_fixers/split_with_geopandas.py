import geopandas
import json

vector = []
intersects = {}
intersections = {}

for i in range(38991):
    intersects[i] = []

for i in range(38992):
    vector.append(geopandas.GeoDataFrame.from_file("C:/Users/Owner/Documents/split/"+str(i)+".geojson"))
    if not i % 1000:
        print(i)

for i in range(38990):
    for j in range(i+1,38991):
        if (vector[i].crosses(vector[j]).iloc[0]):
            intersects[i].append(j)
    print(i,end='\r')

json.dump(intersects,open("C:/Users/Owner/Documents/split/0.json",'w'),indent=' ')

###########################################################################################################
#   After splitting, perform this in QGIS console
###########################################################################################################

import processing
import shutil
import os
import json

with open("C:/Users/Owner/Documents/split/0.json",'r') as infile:
    lines = json.load(infile)
new_road_FC = {
    'type':'FeatureCollection',
    'features':[]
}

for i in lines:
    k = int(i)
    for j in lines[i]:
        processing.run("qgis:splitwithlines",{'INPUT':'./split/'+str(k+1)+'.geojson','LINES':'./split/'+str(j+1)+'.geojson','OUTPUT':'./act_split/temp'+str(k+1)+'.geojson'})
        processing.run("qgis:splitwithlines",{'INPUT':'./split/'+str(j+1)+'.geojson','LINES':'./split/'+str(k+1)+'.geojson','OUTPUT':'./act_split/temp'+str(j+1)+'.geojson'})
        shutil.copyfile('./act_split/temp'+str(k+1)+'.geojson','./split/'+str(k+1)+'.geojson')
        shutil.copyfile('./act_split/temp'+str(j+1)+'.geojson','./split/'+str(j+1)+'.geojson')
        os.remove('./act_split/temp'+str(k+1)+'.geojson')
        os.remove('./act_split/temp'+str(j+1)+'.geojson')
    with open('./split/'+str(k+1)+'.geojson','r') as infile1:
        road = json.load(infile1)
        if lines[i] == []:
            new_road_FC['features'].append(road)
        else:
            new_road_FC['features']+=road['features']
            # for linestring in road['features'][0]['geometry']['coordinates']:
            #     new_road_FC['features'].append({
            #         'type':'Feature',
            #         'properties':road['properties'],
            #         'geometry': {
            #             'type':'LineString',
            #             'coordinates':linestring
            #         }
            #     })
json.dump(new_road_FC,open("./split/split_final.geojson",'w'),indent=' ')

with open("C:/Users/Owner/Documents/split/split_final.geojson",'r') as infile:
    new_FC = {
        'type': "FeatureCollection",
        'features': []
    }
    data = json.load(infile)
    for i in range(1,38992):
        with open("C:/Users/Owner/Documents/split/"+str(i)+".geojson",'r') as infile:
            road_data = json.load(infile)
            if road_data['type'] == "FeatureCollection":
                for feature in road_data['features']:
                    new_FC['features'].append(feature)
            if road_data['type'] == "Feature":
                new_FC['features'].append(road_data)
    json.dump(new_FC,open("C:/Users/Owner/Documents/split/temp_split.geojson",'w'),indent=' ')

# with open("C:/Users/Owner/Desktop/5443-Spatial-DS-Matamoros/Assignments/A05/assets/api/data/rails_and_roads/rails_and_roads.geojson",'r') as infile1:
#     road = json.load(infile1)