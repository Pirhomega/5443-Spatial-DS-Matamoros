from os import path
from json import loads
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def get_countries():
    data_file = 'data/countries.geo.json'
    if path.isfile(data_file):
        with open(data_file, 'r') as f:
            data = f.read()
    else:
        return jsonify({"Error":"countries.geo.json not there!!"})

    return loads(data)


def get_bbox(points):
    min_lat = 90
    max_lat = -90
    min_lon = 180
    max_lon = -180
    
    for point in points:
        if point[1] < min_lat:
            min_lat = point[1]
        if point[0] < min_lon:
            min_lon = point[0]
        if point[1] > max_lat:
            max_lat = point[1]
        if point[0] > max_lon:
            max_lon = point[0]
    
    return {"lon":(min_lon + max_lon)/2,"lat":(min_lat + max_lat)/2,"min_lat":min_lat,"max_lat":max_lat,"min_lon":min_lon,"max_lon":max_lon}

def within_bbox(bbox,lat,lon):
    return (lat < bbox['max_lat'] and lat > bbox['min_lat'] and lon < bbox['max_lon'] and lon > bbox['min_lon'])

@app.route('/')
def index():
    return 'This is the base route'

@app.route('/click/')
def click():
    # lat = request.args.get("lat",None)
    # lng = request.args.get("lng",None)
    # lnglat = request.args.get("lnglat",None)
    lng,lat = request.args.get("lngLat",None).split(",")

    data = get_countries()

    display_coords = None

    for country in data:
        # "geometry": {
        #     "type": "Polygon",
        #     "coordinates": [
        coords = country['geometry']['coordinates']
        kind = country['geometry']["type"]

        if kind == 'Polygon':
            for poly in coords:
                bbox = get_bbox(poly)
                inside = within_bbox(bbox,float(lat),float(lng))
                #print(bbox)
        else:
            for multi in coords:
                for poly in multi:
                    bbox = get_bbox(poly)
                    inside = within_bbox(bbox,float(lat),float(lng))
                    #print(bbox)  
        if inside:
            display_coords = country



    if display_coords:
        return jsonify({'lat':lat,'lng':lng,'country':display_coords})
    else:
        return jsonify({'lat':lat,'lng':lng})



@app.route('/test/')
def test():

    name = request.args.get("name",None)

    print(f"name: {name}")

    if name == None:
        return jsonify({"Numrow":0,"Error":True,"Message":"No name passed to test route!!"})

    return jsonify(list(request.args.keys()))

@app.route('/country/<string:name>')
def country(name):
    data_file = 'data/countries.geo.json'
    if path.isfile(data_file):
        with open(data_file,'r') as f:
            data = f.read()
    else:
        return jsonify({"Error":"countries.geo.json not there!!"})

    countries = loads(data)

    for country in countries:
        if country['properties']['name'] == name:
            return jsonify(country)

    return jsonify({"Error":"Something happened. It wasn't good!!"})

@app.route('/listcountry/')
def get_country():
    data_file = 'data/countries.geo.json'
    if path.isfile(data_file):
        with open(data_file,'r') as f:
            data = f.read()
    else:
        return jsonify({"Error":"countries.geojson not there!!"})

    countries = loads(data)

    country_names = []

    for country in countries:
        country_names.append(country['properties']['name'])

    return jsonify(country_names)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8888)