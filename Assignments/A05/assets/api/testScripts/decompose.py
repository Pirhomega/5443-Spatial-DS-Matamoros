from os import path
from json import loads
from numpy import array
from scipy.spatial import cKDTree
from geopandas import GeoDataFrame
from shapely.geometry.point import Point

def load_data_into_KDtree(path_to_dataset, datatype):
    road_data = ''
    if path.isfile(path_to_dataset):
        with open(path_to_dataset, 'r') as f:
            road_data = f.read()
    else:
        print("Incorrect path to dataset. Check DATASET_MAP and see if the path is correct.")

    dataset = loads(road_data)
    datasetNP = array([])
    datasetDF = True

    if datatype == "Point":
        # creates a geopandas dataframe with the road_data
        datasetDF = GeoDataFrame.from_features(dataset, crs="EPSG:4326")
        # since cKDTree needs an array-like object to query nearest neighbors, we create
        #   such an array
        datasetNP = array(list(datasetDF.geometry.apply(lambda x: (x.x, x.y))))
    elif datatype == "MultiLineString":
        dataset_list = []
        for feature_document in dataset['features']:
            for line in feature_document['geometry']['coordinates']:
                for point in line:
                    # print(point)
                    dataset_list.append({
                        'FULLNAME': feature_document['properties']['FULLNAME'],
                        'GEOMETRY': Point(point)
                    })
        datasetDF = GeoDataFrame(dataset_list)
        datasetDF = datasetDF.set_geometry('GEOMETRY', crs="EPSG:4326")
        # datasetDF = datasetDF.set_crs(epsg=4326)
        # creates a geopandas dataframe with the road_data
        datasetNP = array(list(datasetDF.geometry.apply(lambda x: (x.x, x.y))))
    # populate the KD tree
    datasetKD = cKDTree(datasetNP)
    return (datasetKD, datasetDF, datasetNP)

if __name__ == "__main__":
    path_to_dataset = "./Assignments/A05/assets/api/data/grouped_roads.geojson"
    tree, dataframe, numpyarray = load_data_into_KDtree(path_to_dataset, "MultiLineString")
    print(dataframe)