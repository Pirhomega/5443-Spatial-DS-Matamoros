import json
# import volcano data
data =  json.load(open("C:/Users/Owner/Desktop/5443-Spatial-DS-Matamoros/Assignments/A05/assets/api/data/volcanos_us/volcanos_us.geojson",'r'))['features'] + \
        json.load(open("C:/Users/Owner/Desktop/5443-Spatial-DS-Matamoros/Assignments/A05/assets/api/data/ufos_us/ufos_us.geojson",'r'))['features'] +  \
        json.load(open("C:/Users/Owner/Desktop/5443-Spatial-DS-Matamoros/Assignments/A05/assets/api/data/earthquakes_us/earthquakes_us.geojson",'r'))['features']
combo_FC = {
    'type': 'FeatureCollection',
    'features':data
}
json.dump(combo_FC,open("C:/Users/Owner/Desktop/5443-Spatial-DS-Matamoros/Assignments/A05/assets/api/data/vols_eq_ufo.geojson",'w'),indent='  ')