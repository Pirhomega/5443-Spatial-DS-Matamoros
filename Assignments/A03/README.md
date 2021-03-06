# Assignment 3 - Flask Spatial API

## Programmer(s)

Dr. Terry Griffin and Corbin Matamoros

## Description

Create a Flask backend and Javascript frontend application that displays the five closest earthquakes to the location of a click on a world map.

## Files

|   #   | Folder Link | Assignment Description |
| :---: | ----------- | ---------------------- |
|   1    | [main_flask_app.py](main_flask_app.py) | App backend that runs locally and processes requests (clicks and URLs) from the frontend |
|   2    | [world_map.html](world_map.html) | Interactive HTML map of the world that highlights earthquakes when clicked |
|   3    | [data/eq_2019_10.json](data/eq_2019_10.json) |  json FeatureCollection of some 2019 earthquakes  |

## Dependecies

1. [Flask](https://flask.palletsprojects.com/en/1.1.x/installation/#install-flask)
2. [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/)
3. Latest version of [Python](https://www.python.org/downloads/). I used Python 3.8.5.
4. [libspatialindex](https://libspatialindex.org/en/latest/install.html) and [rtree](https://anaconda.org/conda-forge/rtree). Installing `rtree` from conda includes `libspatialindex` in the build. Don't use pip for either. It was a nightmare.

## Instructions

1. Install all dependencies outlined above. Hint hint: install these using an Anaconda distribution within a custom Anaconda environment. That's the only way I got mine to work. I installed Miniconda3 and created my environment with `conda create --name <name> flask flask_cors rtree`.
2. Download the files in the File Directory above and stick them in a folder (make sure the .json file is in a folder called `data`).
3. Open a terminal in that folder and start the Flask app with `<python_dist> .\main_flask_app.py False`. The `False` prevents the app from running in debug mode. If it's `True`, the program will just run a test call on some functions, print the results to the console, then exit. Not worth your time, and I might take it out of the program maybe.
4. Open `world_map.html` in a browser. Click anywhere on the map to query for the five nearest earthquakes to the location of the click. Earthquakes are represented as tiny black circles.
