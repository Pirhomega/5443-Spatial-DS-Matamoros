# import json
# with open("./Assignments/A05/assets/api/data/rails_and_roads/rails_and_roads.geojson",'r') as infile:
#     features = json.load(infile)['features']
#     counter = 0
#     for road in features:
#         with open("./Assignments/A05/assets/api/data/rails_and_roads/split/"+str(counter)+".geojson",'w') as outfile:
#             json.dump(road,outfile,indent=' ')
#             counter += 1

##########################################################################################
# execute from QGIS console
##########################################################################################

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
        for j in lines[i]:
            processing.run("qgis:splitwithlines",{'INPUT':'./split/'+str(i+1)+'.geojson','LINES':'./split/'+str(j+1)+'.geojson','OUTPUT':'./act_split/temp'+str(i+1)+'.geojson'})
            processing.run("qgis:splitwithlines",{'INPUT':'./split/'+str(j+1)+'.geojson','LINES':'./split/'+str(i+1)+'.geojson','OUTPUT':'./act_split/temp'+str(j+1)+'.geojson'})
            shutil.copyfile('./act_split/temp'+str(i+1)+'.geojson','./split/'+str(i+1)+'.geojson')
            shutil.copyfile('./act_split/temp'+str(j+1)+'.geojson','./split/'+str(j+1)+'.geojson')
            os.remove('./act_split/temp'+str(i+1)+'.geojson')
            os.remove('./act_split/temp'+str(j+1)+'.geojson')
        with open('./split/'+str(i+1)+'.geojson','r') as infile1:
            road = json.load(infile1)
            if lines[i] == []:
                new_road_FC['features']+=[road]
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

##########################################################################################
# execute from vscode
##########################################################################################

# import geopandas
# road_vector = []
# lake_vector = []
# with open("./split/split_final.geojson",'r') as infile:
#     features = json.load(infile)['features']
#     for road in features:
#         road_vector.append(geopandas.GeoDataFrame.from_features([road],crs="epsg:4326"))
# with open("./Assignments/A05/assets/api/data/na_lakes/na_lakes.geojson",'r') as infile:
#     features = json.load(infile)['features']
#     for lake in features:
#         lake_vector.append(geopandas.GeoDataFrame.from_features([lake],crs="epsg:4326"))

# for road in road_vector:
#     for lake in lake_vector:
#         if (road.intersects(lake).iloc[0]):
#             road[0]['type'] = "Bridge"


# for i in range(1,38991):
#     for j in range(i+1,38992):
#         processing.run("qgis:splitwithlines",{'INPUT':'./split/'+str(i)+'.geojson','LINES':'./split/'+str(j)+'.geojson','OUTPUT':'./act_split/temp1.geojson'})
#         processing.run("qgis:splitwithlines",{'INPUT':'./split/'+str(j)+'.geojson','LINES':'./split/'+str(i)+'.geojson','OUTPUT':'./act_split/temp2.geojson'})
#         shutil.copyfile('./act_split/temp1.geojson','./split/'+str(i)+'.geojson')
#         shutil.copyfile('./act_split/temp2.geojson','./split/'+str(j)+'.geojson')
#         os.remove('./act_split/temp1.geojson')
#         os.remove('./act_split/temp2.geojson')