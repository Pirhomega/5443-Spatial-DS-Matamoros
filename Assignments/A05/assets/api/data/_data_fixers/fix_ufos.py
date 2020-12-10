import json
with open("C:/Users/Owner/Desktop/5443-Spatial-DS-Matamoros/Assignments/A05/assets/api/data/ufos_us1.geojson",'r') as infile:
    ufo_dict = json.load(infile)
    counter = 0
    for ufo_document in ufo_dict['features']:
        ufo_document['properties']['source'] = "ufo"+str(counter)
        counter += 1
    json.dump(ufo_dict,open("C:/Users/Owner/Desktop/5443-Spatial-DS-Matamoros/Assignments/A05/assets/api/data/ufos_us.geojson",'w'),indent='  ')