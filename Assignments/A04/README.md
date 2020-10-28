# Assignment 4 - Geospatial Data manipulation and processing

## Corbin Matamoros

## Description

This project utilizes and builds on [Portmap](https://github.com/portofportlandgis/portmap) (documentation below) to perform queries on geospatial data such as nearest neighbor queries, bounding box operations, spatial data visualization, and more (see functionality section -- WIP -- below for details). The backend is programmed in Python and run using [Flask](https://flask.palletsprojects.com/en/1.1.x/). The frontend is HTML with JQuery and Javascript.

## Files

|   #   | Folder Link | Assignment Description |
| :---: | ----------- | ---------------------- |
|   1    | [main_flask_app.py](assets/api/main_flask_app.py) | App backend that runs locally and processes requests (clicks and URLs) from the frontend |
|   2    | [index.html](index.html) | Interactive HTML map of the world. My code goes from line 445 - 762 |
|   3    | [map.js](assets/js/map.js) | The javascript/JQuery code that works with `index.html`. My code goes from line 129 - 733|

## Instructions

1. Download the repo and (optional, but __VERY__ recommended) create a conda environment with [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html). Create a new environment in the anaconda console using this method:

```txt
(base) ~/> conda create -n <environment name>
(base) ~/> conda activate <environment name>
(base) ~/> conda config --env --add channels conda-forge
(base) ~/> conda config --env --set channel_priority strict
```

2. The packages necessary to run this software are [Python](https://www.python.org/), [flask](https://flask.palletsprojects.com/en/1.1.x/), [flask-cors](https://flask-cors.readthedocs.io/en/latest/#installation), [geopandas 0.8.1](https://geopandas.org/install.html#creating-a-new-environment), [scipy](https://www.scipy.org/install.html#installation), and [numpy](https://numpy.org/install/)). I recommend using conda to install all of these. (If using the channel 'conda-forge' in a conda environment as suggested in instruction 1, numpy will be installed when you install geopandas.) Here's how I installed them:

```txt
(base) ~/> conda create -n <environment name>
(base) ~/> conda activate <environment name>
(base) ~/> conda config --env --add channels conda-forge
(base) ~/> conda config --env --set channel_priority strict
(base) ~/> conda install python
(base) ~/> conda install flask
(base) ~/> conda install flask-cors
(base) ~/> conda install python=3 geopandas
(base) ~/> conda install conda install scipy
```

3. Paste your Mapbox token on line 1 of [map.js](assets/js/map.js).

4. Run the flask app by executing it in the conda environment. Execute from the root of the repo. The command would look something like this: `~/miniconda3/env/<environment name>/python.exe ./Assignments/A04/assets/api/geotest.py False`

5. Launch the `index.html` on a server, such as [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer)

6. Hopefully everything is running. Click the buttons on the left side to access the functionality. If, however, you get an error like [this one](https://github.com/numpy/numpy/issues/14770), try following the [suggestion here](https://github.com/numpy/numpy/issues/14770#issuecomment-602181479) and see if that fixes it. That's the only problem I've run into.

## Functionality

### Available Tools

![Newly added modals and their titles](README_images/AvailModals.png)

#### Location Tools

- Enter a latitude (value between -90 and 90) and longitude (value between -180 and 180), click 'find', and a red circle will appear at that location. Repeat this as many times as you'd like. Press 'clear' to remove all points from the map. 
- Click 'save' to save all points visible on the map to a `.geojson` file. Click 'load' to load all points from that `.geojson` file onto the map. Click 'delete' to wipe the system memory of all points visible on the map. 
- Note: whenever a point is added to the map, either through loading from a `.geojson` file or manually by hitting 'find', that point is saved in memory as a `.geojson` feature. That feature is what 'delete' wipes. 'delete' does not remove points from the map or erase the `.geojson` file we can load from or save to.

#### Bounding Box Query

- Select a dataset to query by checking or unchecking its box
- To create a bounding box, click on the map where you want its top left or bottom right corner to be. Then click 'submit top left' or 'submit bottom right' to populate the bounding box inputs at the bottom. You can also input these parameters manually. For example, if you want to set (lon=-98, lat=35) as the top left position, type `-98, 35` into the 'Top Left' field. The coord order must be (lon, lat).
- Perform the bounding box query on the dataset(s) by clicking 'query'. The bounding box and all contained points will be displayed.
- Click 'convex hull' to produce the smallest convex polygon that contains all the points in the bounding box.
- Click 'clear' to remove all bounding boxes and points from the map.
- Note: There is no differentiation between points of each dataset.

#### Nearest Neighbor Query

- Select a dataset to query by checking or unchecking its box
- Select a nearest neighbor strategy, either querying for the nearest `N` neighbors or finding all neighbors within a distance `Deg` of the center. Input your values for `N` (integer from 1 to dataset_size) or `Deg` (float from 0.0 to 180.0).
- Enter the coordinates of the point from which the query will take place. Click 'query' to display results on the map. Click 'clear' to remove them from the map

#### Distance between Cities

- Type into the starting city and destination city input elements a USA city (either type a couple characters and then select from the dropdown, OR type the entire name of the city)
- Hit 'submit' to create a linear line drawn between the two cities. The distance between the two is shown at the bottom in miles. Click 'clear' to remove the lines and city markers

#### Upload GeoJSON

- Paste a valid geoJSON feature or feature collection in the text area and click 'submit' to view it on the map. If pasting a single feature, you don't need to include it in a feature collection. Pasting as is will suffice. If you want to display multiple features, though, you must use a feature collection.

## Undesired behavior

- Map does not center on newly added geometries to the map in Location Tools or Upload GeoJSON.
- There is no distinction between points from different datasets in Nearest Neighbor Query or Bounding Box Query
- Webpage refreshes when the 'save' button is clicked in Location Tools

#

# PortMap Documentation

A responsive web map application template using [Bootstrap](https://getbootstrap.com/) and [Mapbox GL](https://www.mapbox.com/mapbox-gl-js/api/)

To get started you need to generate a Mapbox ID. Get your ID by creating a Mapbox account. Insert your Mapbox ID in assets/js/map.js on line 1.

## What it does

* Layer tree allows the user to interactively organize and reposition map layers using [Mapbox-GL-JS-Layer-Tree](https://github.com/TheGartrellGroup/Mapbox-GL-JS-Layer-Tree)
* Layer Tree pulls feature symbology automatically via [Font Awesome](http://fontawesome.io/ )
* Supports drawing and editing using [Mapbox Draw API](https://github.com/mapbox/mapbox-gl-draw)
* User can calculate area and length of drawn features using [Mapbox Turf](https://www.mapbox.com/help/define-turf/)
* User can add labels directly to the map as a symbol layer using [Mapbox-GL-JS-Text-Markup](https://github.com/TheGartrellGroup/Mapbox-GL-JS-Text-Markup)
* User can easily find latitude and longitude by clicking on the map 
* Global address search using the [mapbox-gl-geocoder](https://github.com/mapbox/mapbox-gl-geocoder)
* Search JSON Properties with autocomplete and zoom to feature
* Client side Print Export to PNG or PDF with legend: [Print/Export for Mapbox GL](https://github.com/TheGartrellGroup/Mapbox-GL-Print-Export-For-Port)
* Identify multiple features and view attributes in a modal
* Bookmark drop-down list
* Disclaimer modal 
* Scale bar 
* Not included in this repo: Save Views function allows the user to save Layer Tree configuration, Mapbox drawn features, Text Markups, and Zoom and Pitch. All plugins in this repo have code pre-built to work with the Save Views plugin: [Mapbox-GL-JS-save-view](https://github.com/TheGartrellGroup/Mapbox-GL-JS-save-view)


## Demo:
[Demo](https://cdettlaff.github.io./)


## Quick Preview:

### Layer Tree 
![layers](https://user-images.githubusercontent.com/17071327/33678147-c6cf833a-da6f-11e7-9b74-b3f4fd59ea26.gif)

### Identify 
![identify](https://user-images.githubusercontent.com/17071327/33678145-c69bbfe6-da6f-11e7-89ba-08cb0b4d2827.gif)

### Draw and Text
![draw](https://user-images.githubusercontent.com/17071327/33678143-c650e782-da6f-11e7-8771-2537d8bf6c31.gif)

### Search JSON with autocomplete
![search](https://user-images.githubusercontent.com/17071327/33678150-c80cdd74-da6f-11e7-8d16-e6a9dfdbb43b.gif)

### Client Side Printing  
![print](https://user-images.githubusercontent.com/17071327/33678149-c7da0f8e-da6f-11e7-8883-6d4d06af7da5.gif)

### Mobile View   
![mobile](https://user-images.githubusercontent.com/17071327/33678148-c70a666c-da6f-11e7-81c8-cdb6e7e99de8.gif)

