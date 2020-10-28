mapboxgl.accessToken = 'pk.eyJ1IjoicGlyaG9tZWdhIiwiYSI6ImNrMW1uMGhsMzAwMGszaW11OXZhempxMTMifQ.tQp7BareQGxwalQvIQvBsw';

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v9',
    center: [-69.0297, 7.61],
    zoom: 2,
    attributionControl: true,
    preserveDrawingBuffer: true,
});

// handles click/touch event across devices 
let touchEvent = 'ontouchstart' in window ? 'touchstart' : 'click';

// navigation controls
map.addControl(new mapboxgl.NavigationControl()); // zoom controls

// scale bar
map.addControl(new mapboxgl.ScaleControl({
    maxWidth: 90,
    unit: 'imperial',
    position: 'bottom-right'
}));

// geolocate control
map.addControl(new mapboxgl.GeolocateControl());

//This overides the Bootstrap modal "enforceFocus" to allow user interaction with main map
$.fn.modal.Constructor.prototype.enforceFocus = function () { };

// print function
var printBtn = document.getElementById('mapboxgl-ctrl-print');
var exportView = document.getElementById('export-map');

var printOptions = {
    disclaimer: "print output disclaimer",
    northArrow: 'assets/plugins/print-export/north_arrow.svg'
}

printBtn.onclick = function (e) {
    PrintControl.prototype.initialize(map, printOptions)
}

exportView.onclick = function (e) {
    PrintControl.prototype.exportMap();
    e.preventDefault();
}


// Layer Search Event Handlers
$('#search_general').on('click', function (e) {

    var criteria = $('#general_search').val();
    var prop = $('#property-descr').text();
    var layer_mapfile = $('#json_layer').val();

    addJsonLayerFilter(layer_mapfile, prop, criteria);

});

$('#clear_general').on('click', function (e) {

    $("#general_search").val("");
    $("#property-descr").html("<br />");
    clearFilterLayer();

});

$('#search_general').on('click', function (e) {

    var criteria = $('#general_search').val();
    var prop = $('#property-descr').text();
    var layer_mapfile = $('#json_layer').val();

    addJsonLayerFilter(layer_mapfile, prop, criteria);

});

$('#clear_general').on('click', function (e) {

    $("#general_search").val("");
    $("#property-descr").html("<br />");
    clearFilterLayer();

});

// Geocoder API
// Geocoder API
// Geocoder API
var geocoder = new MapboxGeocoder({
    accessToken: mapboxgl.accessToken
});

var addressTool = document.getElementById('addressAppend');
addressTool.appendChild(geocoder.onAdd(map))

map.on('load', function () {
    map.addSource('geocode-point', {
        "type": "geojson",
        "data": {
            "type": "FeatureCollection",
            "features": []
        }
    });

    map.addLayer({
        "id": "geocode-point",
        "source": "geocode-point",
        "type": "circle",
        "paint": {
            "circle-radius": 20,
            "circle-color": "dodgerblue",
            'circle-opacity': 0.5,
            'circle-stroke-color': 'white',
            'circle-stroke-width': 3,
        }
    });

    geocoder.on('result', function (ev) {
        map.getSource('geocode-point').setData(ev.result.geometry);
    });

});

/*
 /$$$$$$$                      /$$                  /$$$$$$                      /$$       /$$          /$$               /$$$$$$                  /$$          
| $$__  $$                    |__/                 /$$__  $$                    | $$      |__/         | $/              /$$__  $$                | $$          
| $$  \ $$  /$$$$$$   /$$$$$$  /$$ /$$$$$$$       | $$  \__/  /$$$$$$   /$$$$$$ | $$$$$$$  /$$ /$$$$$$$|_//$$$$$$$      | $$  \__/  /$$$$$$   /$$$$$$$  /$$$$$$ 
| $$$$$$$  /$$__  $$ /$$__  $$| $$| $$__  $$      | $$       /$$__  $$ /$$__  $$| $$__  $$| $$| $$__  $$ /$$_____/      | $$       /$$__  $$ /$$__  $$ /$$__  $$
| $$__  $$| $$$$$$$$| $$  \ $$| $$| $$  \ $$      | $$      | $$  \ $$| $$  \__/| $$  \ $$| $$| $$  \ $$|  $$$$$$       | $$      | $$  \ $$| $$  | $$| $$$$$$$$
| $$  \ $$| $$_____/| $$  | $$| $$| $$  | $$      | $$    $$| $$  | $$| $$      | $$  | $$| $$| $$  | $$ \____  $$      | $$    $$| $$  | $$| $$  | $$| $$_____/
| $$$$$$$/|  $$$$$$$|  $$$$$$$| $$| $$  | $$      |  $$$$$$/|  $$$$$$/| $$      | $$$$$$$/| $$| $$  | $$ /$$$$$$$/      |  $$$$$$/|  $$$$$$/|  $$$$$$$|  $$$$$$$
|_______/  \_______/ \____  $$|__/|__/  |__/       \______/  \______/ |__/      |_______/ |__/|__/  |__/|_______/        \______/  \______/  \_______/ \_______/
                     /$$  \ $$                                                                                                                                  
                    |  $$$$$$/                                                                                                                                  
                     \______/                                                                                                                                   
*/
//Enter Lon Lat
//Enter Lon Lat
//Enter Lon Lat
/*
/$$                                       /$$     /$$                           /$$$$$$$$                  /$$          
| $$                                      | $$    |__/                          |__  $$__/                 | $$          
| $$        /$$$$$$   /$$$$$$$  /$$$$$$  /$$$$$$   /$$  /$$$$$$  /$$$$$$$          | $$  /$$$$$$   /$$$$$$ | $$  /$$$$$$$
| $$       /$$__  $$ /$$_____/ |____  $$|_  $$_/  | $$ /$$__  $$| $$__  $$         | $$ /$$__  $$ /$$__  $$| $$ /$$_____/
| $$      | $$  \ $$| $$        /$$$$$$$  | $$    | $$| $$  \ $$| $$  \ $$         | $$| $$  \ $$| $$  \ $$| $$|  $$$$$$ 
| $$      | $$  | $$| $$       /$$__  $$  | $$ /$$| $$| $$  | $$| $$  | $$         | $$| $$  | $$| $$  | $$| $$ \____  $$
| $$$$$$$$|  $$$$$$/|  $$$$$$$|  $$$$$$$  |  $$$$/| $$|  $$$$$$/| $$  | $$         | $$|  $$$$$$/|  $$$$$$/| $$ /$$$$$$$/
|________/ \______/  \_______/ \_______/   \___/  |__/ \______/ |__/  |__/         |__/ \______/  \______/ |__/|_______/ 
*/

   map.on('load', function () {

    $(document).ready(function () {

        var displayCoordsFC = {
            "type": "FeatureCollection",
            "features": []
        }

        // Purpose:     Creates a map source and layer if they don't already exist
        //              Otherwise, it modifies the existing source
        // Input:       None
        // Output:      None
        function loadSourceLayer() {
            if (!map.getSource("displayCoords")) {
                map.addSource("displayCoords", {
                    'type': 'geojson',
                    'data': displayCoordsFC
                });
            } else {
                map.getSource("displayCoords").setData(
                    displayCoordsFC
                )
            }

            if (!map.getLayer("displayCoordsLayer")) {
                map.addLayer({
                    'id': "displayCoordsLayer",
                    'type': 'circle',
                    'source': "displayCoords",
                    'layout': {},
                    'paint': {
                        "circle-color": 'red',
                        "circle-radius": 8,
                    }
                })
            }
        };

        // Purpose:     Removes a map source and layer
        // Input:       None
        // Output:      None
        function clearSourceLayer() {
            if (map.getLayer("displayCoordsLayer")) {
                map.removeLayer("displayCoordsLayer");
            }
            if (map.getSource("displayCoords")) {
                map.removeSource("displayCoords")
            }
        };

        // Purpose:     Events triggered when the `findLLButton` is pressed
        //              Queries the backend to save the inputted coordinate
        //              to a geojson feature list and return that list for displaying
        // Input:       None
        // Output:      None
        $('#findLLButton').click(function () {
            // grabs the number input from the lngInput-latInput inputs
            var enterLng = +document.getElementById('lngInput').value
            var enterLat = +document.getElementById('latInput').value

            // makes a call to the backend to process the coordinate
            $.getJSON("http://localhost:8888/saveCoord/?lngLat=" + [enterLng, enterLat])
                .done(function (coordFeature) {
                    // assign the coordinate array (a geojson feature array) to
                    //  the feature array of `displayCoordsFC` and display
                    displayCoordsFC.features = coordFeature
                    console.log(displayCoordsFC)
                    loadSourceLayer()
                    // clear the lat and lng input fields
                    $('#lngInput').val('')
                    $('#latInput').val('')

                    // center the view on the newly-added coordinate
                    map.flyTo({
                        center: turf.center(displayCoordsFC).geometry.coordinates
                    });
                    if (turf.area(turf.bboxPolygon(turf.bbox(displayCoordsFC))) > 1000000) {
                        map.fitBounds(turf.bbox(displayCoordsFC), {padding: 100})
                    }
                });
        });

        // Purpose:     Events triggered when the `findLLButtonClear` is pressed.
        //              Clears `displayCoordsFC`, removes map source and map layer
        // Input:       None
        // Output:      None
        $('#findLLButtonClear').click(function () {
            // remove all features from the `displayCoordsFC` feature collection
            displayCoordsFC.features = []
            // remove the source and layers associated with `displayCoordsFC`
            clearSourceLayer()

            // clear the lat and lng input fields
            $('#lngInput').val('')
            $('#latInput').val('')
            // adjusts the map view to be centered on lng=0,lat=0
            map.flyTo({
                center: [0, 0],
                zoom: 3
            });
        });

        // Purpose:     Events triggered when the `saveJSONButton` is pressed.
        //              Saves all points displaying on the map to a geojson file
        // Input:       None
        // Output:      None
        $('#saveJSONButton').click(function () {
            $.getJSON("http://localhost:8888/saveJSON/")
                .done(function (response) {
                    if (parseInt(response)) {
                        console.log("Saved to ./Assignments/A04/assets/api/data/mapCoords.geojson")
                    } else {
                        console.log("File couldn't be saved. Server was interrupted, perhaps?")
                    }
                })
        })

        // Purpose:     Events triggered when the `loadJSONButton` is pressed.
        //              Displays all points stored in ./Assignments/A04/assets/api/data/mapCoords.geojson
        //              to the map
        // Input:       None
        // Output:      None
        $('#loadJSONButton').click(function () {
            $.getJSON("http://localhost:8888/loadJSON/")
                .done(function (loadedPlusExisting) {
                    displayCoordsFC.features = loadedPlusExisting
                    loadSourceLayer()

                    // center the view on the newly-added coordinate
                    map.flyTo({
                        center: turf.center(displayCoordsFC).geometry.coordinates
                    });
                    if (turf.area(turf.bboxPolygon(turf.bbox(displayCoordsFC))) > 1000000) {
                        map.fitBounds(turf.bbox(displayCoordsFC), {padding: 100})
                    }
                })
        })

        // Purpose:     Events triggered when the `deleteJSONButton` is pressed.
        //              Queries the backend to delete all points cached (a point
        //              is cached when it is displayed on the screen)
        // Input:       None
        // Output:      None
        $('#deleteJSONButton').click(function () {
            $.getJSON("http://localhost:8888/deleteJSON/")
                .done(function (response) {
                    if (parseInt(response)) {
                        console.log("Deleted point history successfully!")
                    }
                })
        })
    });
});

// Bounding Box Query
// Bounding Box Query
// Bounding Box Query

/*
 /$$$$$$$  /$$$$$$$                             /$$$$$$                                         
| $$__  $$| $$__  $$                           /$$__  $$                                        
| $$  \ $$| $$  \ $$  /$$$$$$  /$$   /$$      | $$  \ $$ /$$   /$$  /$$$$$$   /$$$$$$  /$$   /$$
| $$$$$$$ | $$$$$$$  /$$__  $$|  $$ /$$/      | $$  | $$| $$  | $$ /$$__  $$ /$$__  $$| $$  | $$
| $$__  $$| $$__  $$| $$  \ $$ \  $$$$/       | $$  | $$| $$  | $$| $$$$$$$$| $$  \__/| $$  | $$
| $$  \ $$| $$  \ $$| $$  | $$  >$$  $$       | $$/$$ $$| $$  | $$| $$_____/| $$      | $$  | $$
| $$$$$$$/| $$$$$$$/|  $$$$$$/ /$$/\  $$      |  $$$$$$/|  $$$$$$/|  $$$$$$$| $$      |  $$$$$$$
|_______/ |_______/  \______/ |__/  \__/       \____ $$$ \______/  \_______/|__/       \____  $$
                                                    \__/                               /$$  | $$
                                                                                      |  $$$$$$/
                                                                                       \______/ 
*/
map.on('load', function () {

    $(document).ready(function () {

        var bBoxFeature_Collection = {
            "type": "FeatureCollection",
            "features": []
        }

        // Purpose:     Creates a map source and layer if they don't already exist
        //              Otherwise, it modifies the existing source
        // Input:       None
        // Output:      None
        function loadSourceLayer() {
            if (!map.getSource("coordsBB")) {
                map.addSource("coordsBB", {
                    'type': 'geojson',
                    'data': bBoxFeature_Collection
                });
            } else {
                map.getSource("coordsBB").setData(
                    bBoxFeature_Collection
                )
            }
            if (!map.getLayer("bBoxContained")) {
                map.addLayer({
                    'id': "bBoxContained",
                    'type': 'circle',
                    'source': "coordsBB",
                    'layout': {},
                    'paint': {
                        "circle-color": 'red',
                        "circle-radius": 8,
                    },
                    'filter': ['==', '$type', 'Point']
                })
            }
            if (!map.getLayer("bBoxOutline")) {
                map.addLayer({
                    'id': "bBoxOutline",
                    'type': 'fill',
                    'source': "coordsBB",
                    'layout': {},
                    'paint': {
                        'fill-color': 'white',
                        'fill-opacity': 0.4,
                        'fill-outline-color': 'gray'
                    },
                    'filter': ['==', '$type', 'Polygon']
                })
            }
        };

        // Purpose:     Removes a map source and layer
        // Input:       None
        // Output:      None
        function clearSourceLayer() {
            if (map.getLayer("bBoxOutline")) {
                map.removeLayer("bBoxOutline");
            }
            if (map.getLayer("bBoxContained")) {
                map.removeLayer("bBoxContained");
            }
            if (map.getSource("coordsBB")) {
                map.removeSource("coordsBB");
            }
        };

        // Purpose:     Events triggered when the `fillTopLeft` is pressed.
        //              Populates the `topLeftBB` input field with the contents
        //              from the `pointBB` field
        // Input:       None
        // Output:      None
        $('#fillTopLeft').click(function () {
            $('#topLeftBB').val($('#pointBB').text())
        });

        // Purpose:     Events triggered when the `fillBottomRight` is pressed.
        //              Populates the `bottomRightBB` input field with the contents
        //              from the `pointBB` field
        // Input:       None
        // Output:      None
        $('#fillBottomRight').click(function () {
            $('#bottomRightBB').val($('#pointBB').text())
        });

        // Purpose:     Creates a JSON document with the name of a dataset and
        //              a boolean indicated its checkbox was checked
        // Input:       None
        // Output:      JSON document
        function chooseDataset() {
            return {
                "datasets": {
                    "earthquakes": document.getElementById("earthquakes").checked,
                    "volcanos": document.getElementById("volcanos").checked
                    // "planes": document.getElementById("planes").checked,
                    // "ufos": document.getElementById("ufos").checked
                }
            }
        };

        // Purpose:     Events triggered when the `queryBBButton` is pressed.
        //              Queries the backend with bounding box parameters to display
        //              the bounding box and the geometries contained by it
        // Input:       None
        // Output:      None
        $('#queryBBButton').click(function () {
            // only query the backend if the both bounding box input fields are populated
            if ($('#topLeftBB').val() && $('#bottomRightBB').val()) {
                let topLeft = $('#topLeftBB').val()
                let bottomRight = $('#bottomRightBB').val()

                // create a JSON object of the bounding box topleft and bottom right coords
                //  and the datasets to be queried
                let BBparams = $.extend({ "bbox": [topLeft, bottomRight] }, chooseDataset())

                // query and display results
                $.getJSON("http://localhost:8888/boundingBoxQuery/?BBparams=" + JSON.stringify(BBparams))
                    .done(function (bboxAndResults) {
                        bBoxFeature_Collection.features = bboxAndResults
                        loadSourceLayer()

                        // center the view on the newly-added feature collection
                        map.flyTo({
                            center: turf.center(bBoxFeature_Collection).geometry.coordinates
                        });
                        map.fitBounds(turf.bbox(bBoxFeature_Collection), {padding: 200})
                    })
            }
        });

        // Purpose:     Events triggered when the `convBBButton` is pressed.
        //              Queries the backend with bounding box parameters to display
        //              the bounding box and the convex polygon formed by the points
        //              contained by the bounding box
        // Input:       None
        // Output:      None
        $('#convBBButton').click(function () {
            // only query the backend if the both bounding box input fields are populated
            if ($('#topLeftBB').val() && $('#bottomRightBB').val()) {
                let topLeft = $('#topLeftBB').val()
                let bottomRight = $('#bottomRightBB').val()

                // create a JSON object of the bounding box topleft and bottom right coords
                //  and the datasets to be queried
                let BBparams = $.extend({ "bbox": [topLeft, bottomRight] }, chooseDataset())

                // query and display results
                $.getJSON("http://localhost:8888/convexQuery/?BBparams=" + JSON.stringify(BBparams))
                    .done(function (convexHull) {
                        bBoxFeature_Collection.features = convexHull
                        loadSourceLayer()
                        // center the view on the newly-added feature collection
                        map.flyTo({
                            center: turf.center(bBoxFeature_Collection).geometry.coordinates
                        });
                        map.fitBounds(turf.bbox(bBoxFeature_Collection), {padding: 200})
                    })
            }
        });

        // Purpose:     Events triggered when the `queryBBButtonClear` is pressed.
        //              Removes the bounding box and intersecting points source and
        //              layers from the map view
        // Input:       None
        // Output:      None
        $('#queryBBButtonClear').click(function () {
            bBoxFeature_Collection.features = []
            clearSourceLayer()
            $('#topLeftBB').val('')
            $('#bottomRightBB').val('')
            // adjusts the map view to be centered on lng=0,lat=0
            map.flyTo({
                center: [0, 0],
                zoom: 3
            });
        });

        // Bounding Box Creator Tool
        // Bounding Box Creator Tool
        // Bounding Box Creator Tool
        // Purpose:     Populates the `pointBB` element with the world coordinate location of a user's click
        map.on(touchEvent, function (e) {
            document.getElementById('pointBB').innerHTML =
                JSON.stringify(e.lngLat, function (key, val) { return val.toFixed ? Number(val.toFixed(4)) : val; }).replace('{"lng":', '').replace('"lat":', ' ').replace('}', '')
        });
    });
});

//Nearest Neighbor Query
//Nearest Neighbor Query
//Nearest Neighbor Query

/*
 /$$   /$$                                                     /$$           /$$   /$$           /$$           /$$       /$$                          
| $$$ | $$                                                    | $$          | $$$ | $$          |__/          | $$      | $$                          
| $$$$| $$  /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$$ /$$$$$$        | $$$$| $$  /$$$$$$  /$$  /$$$$$$ | $$$$$$$ | $$$$$$$   /$$$$$$   /$$$$$$ 
| $$ $$ $$ /$$__  $$ |____  $$ /$$__  $$ /$$__  $$ /$$_____/|_  $$_/        | $$ $$ $$ /$$__  $$| $$ /$$__  $$| $$__  $$| $$__  $$ /$$__  $$ /$$__  $$
| $$  $$$$| $$$$$$$$  /$$$$$$$| $$  \__/| $$$$$$$$|  $$$$$$   | $$          | $$  $$$$| $$$$$$$$| $$| $$  \ $$| $$  \ $$| $$  \ $$| $$  \ $$| $$  \__/
| $$\  $$$| $$_____/ /$$__  $$| $$      | $$_____/ \____  $$  | $$ /$$      | $$\  $$$| $$_____/| $$| $$  | $$| $$  | $$| $$  | $$| $$  | $$| $$      
| $$ \  $$|  $$$$$$$|  $$$$$$$| $$      |  $$$$$$$ /$$$$$$$/  |  $$$$/      | $$ \  $$|  $$$$$$$| $$|  $$$$$$$| $$  | $$| $$$$$$$/|  $$$$$$/| $$      
|__/  \__/ \_______/ \_______/|__/       \_______/|_______/    \___/        |__/  \__/ \_______/|__/ \____  $$|__/  |__/|_______/  \______/ |__/      
                                                                                                     /$$  \ $$                                        
                                                                                                    |  $$$$$$/                                        
                                                                                                     \______/                                         
*/
map.on('load', function () {

    $(document).ready(function () {

        var nearestNeighborsFC = {
            "type": "FeatureCollection",
            "features": []
        }

        // Purpose:     Creates a map source and layer if they don't already exist
        //              Otherwise, it modifies the existing source
        // Input:       None
        // Output:      None
        function loadSourceLayer() {
            if (!map.getSource("nnCoords")) {
                map.addSource("nnCoords", {
                    'type': 'geojson',
                    'data': nearestNeighborsFC
                });
            } else {
                map.getSource("nnCoords").setData(
                    nearestNeighborsFC
                )
            }

            if (!map.getLayer("nnCoordsLayer")) {
                map.addLayer({
                    'id': "nnCoordsLayer",
                    'type': 'circle',
                    'source': "nnCoords",
                    'layout': {},
                    'paint': {
                        "circle-color": 'blue',
                        "circle-radius": 8,
                    }
                })
            }
        };

        // Purpose:     Removes a map source and layer
        // Input:       None
        // Output:      None
        function clearSourceLayer() {
            if (map.getLayer("nnCoordsLayer")) {
                map.removeLayer("nnCoordsLayer");
            }
            if (map.getSource("nnCoords")) {
                map.removeSource("nnCoords")
            }
        }

        // Purpose:     Creates a JSON document with the name of a dataset and
        //              a boolean indicated its checkbox was checked
        // Input:       None
        // Output:      JSON document
        function chooseDataset() {
            return {
                "datasets": {
                    "earthquakes": document.getElementById("earthquakes").checked,
                    "volcanos": document.getElementById("volcanos").checked,
                    // "planes": document.getElementById("planes").checked,
                    // "ufos": document.getElementById("ufos").checked
                }
            }
        };

        // Purpose:     Creates a JSON document with the nearest neighbor query
        //              type as well as the value
        // Input:       None
        // Output:      JSON document
        function chooseQueryType() {
            // If the user wants to query the N nearest neighbors, return a document
            //      with that query type and the value of N
            if (document.getElementById("nearestN").checked)
                return {
                    "queryType": {
                        "name": "nearestN",
                        "value": document.getElementById('nearestNValue').value
                    }
                }
            // If the user wants to query all neighbors within a circular radius R,
            //      return a document with that query type and the value of R
            else
                return {
                    "queryType": {
                        "name": "radiusKm",
                        "value": document.getElementById('radiusKm').value
                    }
                }
        };

        // Purpose:     Events triggered when the `queryNN` is pressed.
        //              Queries the backend for a nearest neighbor query on
        //              the user's selected datasets, receiving a feature list
        //              from the backend to display on the map
        // Input:       None
        // Output:      None
        $('#queryNN').click(function () {
            var selectedDatasets = chooseDataset()
            var selectQueryType = chooseQueryType()

            // grabs the number input from the lngInput-latInput fields
            var enterLng = +document.getElementById('lngInputQ').value
            var enterLat = +document.getElementById('latInputQ').value

            // creates a geojson feature object with the lng and lat values
            var enterLL = { "geojson": turf.point([enterLng, enterLat]) }
            // creates a JSON document of the user's selected datasets to query, the query
            //      type selected, and the coords of the point from which the query will
            //      take place
            var NNparams = $.extend({}, selectedDatasets, selectQueryType, enterLL)

            // query the backend and display results
            $.getJSON("http://localhost:8888/nnQuery/?NNparams=" + JSON.stringify(NNparams))
                .done(function (nnFeatures) {
                    nearestNeighborsFC.features = nnFeatures
                    loadSourceLayer()
                    // center the view on the newly-added feature collection
                    map.flyTo({
                        center: turf.center(nearestNeighborsFC).geometry.coordinates
                    });
                    if (turf.area(turf.bboxPolygon(turf.bbox(nearestNeighborsFC))) > 1000000) {
                        map.fitBounds(turf.bbox(nearestNeighborsFC), {padding: 200})
                    }
                });
        });

        // Purpose:     Events triggered when the `queryNNClear` is pressed.
        //              Clears the map of the nearest neighbors layer and source
        // Input:       None
        // Output:      None
        $('#queryNNClear').click(function () {
            clearSourceLayer()
            // adjusts the map view to be centered on lng=0,lat=0
            map.flyTo({
                center: [0, 0],
                zoom: 3
            });
        });
    });
});


//Distance between cities
//Distance between cities
//Distance between cities
/*
  /$$$$$$  /$$   /$$                     /$$$$$$$  /$$             /$$                                            
 /$$__  $$|__/  | $$                    | $$__  $$|__/            | $$                                            
| $$  \__/ /$$ /$$$$$$   /$$   /$$      | $$  \ $$ /$$  /$$$$$$$ /$$$$$$    /$$$$$$  /$$$$$$$   /$$$$$$$  /$$$$$$ 
| $$      | $$|_  $$_/  | $$  | $$      | $$  | $$| $$ /$$_____/|_  $$_/   |____  $$| $$__  $$ /$$_____/ /$$__  $$
| $$      | $$  | $$    | $$  | $$      | $$  | $$| $$|  $$$$$$   | $$      /$$$$$$$| $$  \ $$| $$      | $$$$$$$$
| $$    $$| $$  | $$ /$$| $$  | $$      | $$  | $$| $$ \____  $$  | $$ /$$ /$$__  $$| $$  | $$| $$      | $$_____/
|  $$$$$$/| $$  |  $$$$/|  $$$$$$$      | $$$$$$$/| $$ /$$$$$$$/  |  $$$$/|  $$$$$$$| $$  | $$|  $$$$$$$|  $$$$$$$
 \______/ |__/   \___/   \____  $$      |_______/ |__/|_______/    \___/   \_______/|__/  |__/ \_______/ \_______/
                         /$$  | $$                                                                                
                        |  $$$$$$/                                                                                
                         \______/                                                                                 
*/
map.on('load', function () {

    $(document).ready(function () {
        var cityDistFC = {
            "type": "FeatureCollection",
            "features": []
        }

        // Purpose:     Creates a map source and layer if they don't already exist
        //              Otherwise, it modifies the existing source
        // Input:       None
        // Output:      None
        function loadSourceLayer() {
            if (!map.getSource("cityDistCoords")) {
                map.addSource("cityDistCoords", {
                    'type': 'geojson',
                    'data': cityDistFC
                });
            } else {
                map.getSource("cityDistCoords").setData(
                    cityDistFC
                )
            }

            if (!map.getLayer("cityDistCoordsLayer")) {
                map.addLayer({
                    'id': "cityDistLineLayer",
                    'type': 'line',
                    'source': "cityDistCoords",
                    'layout': {
                        'line-join': 'round',
                        'line-cap': 'round'
                    },
                    'paint': {
                        "line-color": 'black',
                        "line-width": 3,
                    },
                    'filter': ['==', '$type', 'LineString']
                })
                map.addLayer({
                    'id': "cityDistCoordsLayer",
                    'type': 'circle',
                    'source': "cityDistCoords",
                    'layout': {},
                    'paint': {
                        "circle-color": 'green',
                        "circle-radius": 8,
                    },
                    'filter': ['==', '$type', 'Point']
                })
            }
        };

        // Purpose:     Removes a map source and layer
        // Input:       None
        // Output:      None
        function clearSourceLayer() {
            if (map.getLayer("cityDistCoordsLayer")) {
                map.removeLayer("cityDistCoordsLayer");
            }
            if (map.getLayer("cityDistLineLayer")) {
                map.removeLayer("cityDistLineLayer");
            }
            if (map.getSource("cityDistCoords")) {
                map.removeSource("cityDistCoords")
            }
        }

        // Purpose:     Events triggered when the `cityDist` is pressed.
        //              Queries the backend for the feature documents of two cities,
        //              draws a line between the two and calculates the as-the-crow-flies
        //              distance between them as well
        // Input:       None
        // Output:      None
        $('#cityDist').click(function () {
            // get the source and destination city names from their input elements
            let citynameSource = $('#inputCitiesSource').val()
            let citynameDest = $('#inputCitiesDest').val()
            // perform the backend query and draw to the map
            $.get("http://localhost:8888/cityDist/?cityArgs=" + [citynameSource, citynameDest], function (cityDistJSON) {
                cityDistFC.features = cityDistJSON
                loadSourceLayer()
                // center the view on the newly-added feature collection
                map.flyTo({
                    center: turf.center(cityDistFC).geometry.coordinates
                });
                if (turf.area(turf.bboxPolygon(turf.bbox(cityDistFC))) > 1000000) {
                    map.fitBounds(turf.bbox(cityDistFC), {padding: 200})
                }
                // calculate the distance between the two cities in miles
                length = turf.distance(cityDistJSON[0].geometry.coordinates, cityDistJSON[1].geometry.coordinates, 'miles');
                // restrict  to 2 decimal points
                rounded_distance = Math.round(length * 100) / 100;
                lineAnswer = document.getElementById('calculated-distance');
                lineAnswer.innerHTML = '<p>' + rounded_distance + ' mi</p>';
            });

        });

        // Purpose:     Events triggered when the `clearCities` is pressed.
        //              Removes the city distance value from `calculated-distance`
        //              and removes the associated source and layer from the map
        // Input:       None
        // Output:      None
        $('#clearCities').click(function () {
            $('#calculated-distance p').remove();
            clearSourceLayer()
            map.flyTo({
                center: [-98,40],
                zoom: 3
            })
        });

        /***********************************************************************************/

        // Purpose:     Queries the backend with whatever characters were typed into the
        //              source or destination city input fields and displays the results
        //              as recommendations in a 'select' element
        // Input:       None
        // Output:      None
        function populateCitiesSelect(whichSelect, whichinput) {
            let cityname = $(whichinput).val()
            let html = ''
            // this backend call will return a list of cities that begin with the characters
            //      typed into the source/destination city input fields
            $.get("http://localhost:8888/cities/?hint=" + cityname, function (data) {
                // for every recommended city returned, add an option to the respective city's
                //      'select' element
                for (var i = 0; i < data.length; ++i) {
                    html += '<option>' + data[i] + '</option>'
                }
                // modify the select
                $(whichSelect).attr("size", data.length)
                $(whichSelect).html(html)
            })
        };

        // Purpose:     Events triggered when the `inputCitiesSource` has something typed in it
        //              Calls `populateCitiesSelect` each time an ASCII character is typed in
        // Input:       None
        // Output:      None
        $("#inputCitiesSource").keyup(function (event) {
            if ((event.which > 64 && event.which < 91) || event.which == 32 || event.which == 8)
                populateCitiesSelect("#citySelectSource", "#inputCitiesSource")
        });

        // Purpose:     Events triggered when the `inputCitiesDest` has something typed in it
        //              Calls `populateCitiesSelect` each time an ASCII character is typed in
        // Input:       None
        // Output:      None
        $("#inputCitiesDest").keyup(function (event) {
            if ((event.which > 64 && event.which < 91) || event.which == 32 || event.which == 8)
                populateCitiesSelect("#citySelectDest", "#inputCitiesDest")
        });

        /***********************************************************************************/

        // Purpose:     Removes all options from a 'select' element
        // Input:       None
        // Output:      None
        function emptySelectOptions(whichSelect) {
            // modify the select
            $(whichSelect).attr("size", "0")
            $(whichSelect).html('<option></option>')
        };

        // Purpose:     Events triggered when the `citySelectDest` has something typed in it
        //              Autofills the citySelectDest box when one of the selector options is clicked
        // Input:       None
        // Output:      None
        $("#citySelectDest")
            .change(function () {
                var str = ""
                $("#citySelectDest option:selected").each(function () {
                    str = $(this).text()
                });
                $("#inputCitiesDest").val(str);
                emptySelectOptions("#citySelectDest")
            })
            .trigger("change");

        // Purpose:     Events triggered when the `citySelectDest` has something typed in it
        //              Autofills the citySelectSource box when one of the selector options is clicked
        // Input:       None
        // Output:      None
        $("#citySelectSource")
            .change(function () {
                let str = ""
                $("#citySelectSource option:selected").each(function () {
                    str = $(this).text()
                });
                $("#inputCitiesSource").val(str);
                emptySelectOptions("#citySelectSource")
            })
            .trigger("change");
        });
    });


//Upload GeoJSON
//Upload GeoJSON
//Upload GeoJSON

/*
 /$$   /$$           /$$                           /$$        /$$$$$$                         /$$$$$  /$$$$$$   /$$$$$$  /$$   /$$
| $$  | $$          | $$                          | $$       /$$__  $$                       |__  $$ /$$__  $$ /$$__  $$| $$$ | $$
| $$  | $$  /$$$$$$ | $$  /$$$$$$   /$$$$$$   /$$$$$$$      | $$  \__/  /$$$$$$   /$$$$$$       | $$| $$  \__/| $$  \ $$| $$$$| $$
| $$  | $$ /$$__  $$| $$ /$$__  $$ |____  $$ /$$__  $$      | $$ /$$$$ /$$__  $$ /$$__  $$      | $$|  $$$$$$ | $$  | $$| $$ $$ $$
| $$  | $$| $$  \ $$| $$| $$  \ $$  /$$$$$$$| $$  | $$      | $$|_  $$| $$$$$$$$| $$  \ $$ /$$  | $$ \____  $$| $$  | $$| $$  $$$$
| $$  | $$| $$  | $$| $$| $$  | $$ /$$__  $$| $$  | $$      | $$  \ $$| $$_____/| $$  | $$| $$  | $$ /$$  \ $$| $$  | $$| $$\  $$$
|  $$$$$$/| $$$$$$$/| $$|  $$$$$$/|  $$$$$$$|  $$$$$$$      |  $$$$$$/|  $$$$$$$|  $$$$$$/|  $$$$$$/|  $$$$$$/|  $$$$$$/| $$ \  $$
 \______/ | $$____/ |__/ \______/  \_______/ \_______/       \______/  \_______/ \______/  \______/  \______/  \______/ |__/  \__/
          | $$                                                                                                                    
          | $$                                                                                                                    
          |__/                                                                                                                    
*/
map.on('load', function () {

    $(document).ready(function () {
        // Purpose:     Creates a map source and layer if they don't already exist
        //              Otherwise, it modifies the existing source
        // Input:       None
        // Output:      None
        function loadSourceLayer(geoJSONFC) {
            if (!map.getSource("geoJSONCoords")) {
                map.addSource("geoJSONCoords", {
                    'type': 'geojson',
                    'data': geoJSONFC
                });
            } else {
                map.getSource("geoJSONCoords").setData(
                    geoJSONFC
                )
            }

            if (!map.getLayer("geoJSONCoordsLayer")) {
                map.addLayer({
                    'id': "geoJSONPolyLayer",
                    'type': 'fill',
                    'source': "geoJSONCoords",
                    'layout': {},
                    'paint': {
                        'fill-color': 'white',
                        'fill-opacity': 0.4,
                        'fill-outline-color': 'gray'
                    },
                    'filter': ['==', '$type', 'Polygon']
                })
                map.addLayer({
                    'id': "geoJSONLineLayer",
                    'type': 'line',
                    'source': "geoJSONCoords",
                    'layout': {
                        'line-join': 'round',
                        'line-cap': 'round'
                    },
                    'paint': {
                        "line-color": 'black',
                        "line-width": 3,
                    },
                    'filter': ['==', '$type', 'LineString']
                })
                map.addLayer({
                    'id': "geoJSONPointLayer",
                    'type': 'circle',
                    'source': "geoJSONCoords",
                    'layout': {},
                    'paint': {
                        "circle-color": 'yellow',
                        "circle-radius": 8,
                    },
                    'filter': ['==', '$type', 'Point']
                })
            }
        };

        // Purpose:     Removes a map source and layer
        // Input:       None
        // Output:      None
        function clearSourceLayer() {
            if (map.getLayer("geoJSONPolyLayer")) {
                map.removeLayer("geoJSONPolyLayer");
            }
            if (map.getLayer("geoJSONLineLayer")) {
                map.removeLayer("geoJSONLineLayer");
            }
            if (map.getLayer("geoJSONPointLayer")) {
                map.removeLayer("geoJSONPointLayer");
            }
            if (map.getSource("geoJSONCoords")) {
                map.removeSource("geoJSONCoords")
            }
        }

        // Purpose:     Events triggered when the `submitGJ` button is pressed
        //              Displays the geojson data pasted into `geoJSONTextBox`
        // Input:       None
        // Output:      None
        $('#submitGJ').click(function () {
            // grabs the number input from the lngInput-latInput fields
            let submitted_geojson = JSON.parse(document.getElementById('geoJSONTextBox').value)
            clearSourceLayer()
            loadSourceLayer(submitted_geojson)
            // center the view on the newly-added feature collection
            map.flyTo({
                center: turf.center(submitted_geojson).geometry.coordinates
            });
            if (turf.area(turf.bboxPolygon(turf.bbox(submitted_geojson))) > 1000000) {
                map.fitBounds(turf.bbox(submitted_geojson), {padding: 200})
            }
        });

        // Purpose:     Events triggered when the `clearGJ` button is pressed
        //              Removes the geojson data displayed on the map
        // Input:       None
        // Output:      None
        $('#clearGJ').click(function () {
            clearSourceLayer()
            // adjusts the map view to be centered on lng=0,lat=0
            map.flyTo({
                center: [0, 0],
                zoom: 3
            });
        });
    });
});

/*
 /$$$$$$$$                 /$$        /$$$$$$                      /$$       /$$          /$$               /$$$$$$                  /$$          
| $$_____/                | $$       /$$__  $$                    | $$      |__/         | $/              /$$__  $$                | $$          
| $$       /$$$$$$$   /$$$$$$$      | $$  \__/  /$$$$$$   /$$$$$$ | $$$$$$$  /$$ /$$$$$$$|_//$$$$$$$      | $$  \__/  /$$$$$$   /$$$$$$$  /$$$$$$ 
| $$$$$   | $$__  $$ /$$__  $$      | $$       /$$__  $$ /$$__  $$| $$__  $$| $$| $$__  $$ /$$_____/      | $$       /$$__  $$ /$$__  $$ /$$__  $$
| $$__/   | $$  \ $$| $$  | $$      | $$      | $$  \ $$| $$  \__/| $$  \ $$| $$| $$  \ $$|  $$$$$$       | $$      | $$  \ $$| $$  | $$| $$$$$$$$
| $$      | $$  | $$| $$  | $$      | $$    $$| $$  | $$| $$      | $$  | $$| $$| $$  | $$ \____  $$      | $$    $$| $$  | $$| $$  | $$| $$_____/
| $$$$$$$$| $$  | $$|  $$$$$$$      |  $$$$$$/|  $$$$$$/| $$      | $$$$$$$/| $$| $$  | $$ /$$$$$$$/      |  $$$$$$/|  $$$$$$/|  $$$$$$$|  $$$$$$$
|________/|__/  |__/ \_______/       \______/  \______/ |__/      |_______/ |__/|__/  |__/|_______/        \______/  \______/  \_______/ \_______/
*/


// Coordinates Tool
// Coordinates Tool
// Coordinates Tool
map.on(touchEvent, function (e) {
    document.getElementById('info').innerHTML =
        JSON.stringify(e.lngLat, function (key, val) { return val.toFixed ? Number(val.toFixed(4)) : val; }).replace('{"lng":', '').replace('"lat":', ' ').replace('}', '')
});

//Layer Tree
//Layer Tree
//Layer Tree

//Load Layers
// Layers that load first will be at the bottom of the root directory within the Layer Tree

var emptyGJ = {
    'type': 'FeatureCollection',
    'features': []
};

map.on('load', function () {

    //monster layers
    //Mr. Claw layer sources
    map.addSource('monster', { type: 'geojson', data: emptyGJ });
    map.addSource('mouth', { type: 'geojson', data: emptyGJ });
    map.addSource('water-line', { type: 'geojson', data: emptyGJ });
    map.addSource('eyes', { type: 'geojson', data: emptyGJ });

    map.addLayer({
        "id": "monster",
        "type": "fill",
        "source": "monster",
        "layout": {
            //"visibility": 'none'
        },
        "paint": {
            'fill-color': '#b30000',
            'fill-opacity': 1.0
        }
    });

    map.addLayer({
        "id": "mouth",
        "type": "fill",
        "source": "mouth",
        "layout": {
            //"visibility": 'none'
        },
        "paint": {
            'fill-color': 'white',
            'fill-opacity': 1.0
        }
    });

    map.addLayer({
        "id": "water-line",
        "type": "line",
        "source": "water-line",
        "layout": {
            // "visibility": 'none'
        },
        "paint": {
            'line-color': '#0099ff',
            'line-opacity': 1.0,
            "line-width": 9,
        },
    });

    map.addLayer({
        "id": "eyes",
        "type": "circle",
        "source": "eyes",
        "layout": {
            //"visibility": 'none'
        },
        "paint": {
            'circle-color': 'white',
            'circle-opacity': 1.0,
            'circle-stroke-color': 'black',
            'circle-stroke-width': 3,
            'circle-stroke-opacity': 1.0,
        }
    });

    //monster layers
    //Mr. Octo layer sources
    map.addSource('octo', { type: 'geojson', data: emptyGJ });
    map.addSource('water-line-2', { type: 'geojson', data: emptyGJ });
    map.addSource('mouth2', { type: 'geojson', data: emptyGJ });
    map.addSource('eyes2', { type: 'geojson', data: emptyGJ });

    map.addLayer({
        "id": "octo",
        "type": "fill",
        "source": "octo",
        "layout": {
            //"visibility": 'none'
        },
        "paint": {
            'fill-color': 'black',
            'fill-opacity': 1.0
        }
    });

    map.addLayer({
        "id": "water-line-2",
        "type": "line",
        "source": "water-line-2",
        "layout": {
            // "visibility": 'none'
        },
        "paint": {
            'line-color': '#0099ff',
            'line-opacity': 1.0,
            "line-width": 9,
        },
    });
    map.addLayer({
        "id": "mouth2",
        "type": "fill",
        "source": "mouth2",
        "layout": {
            //"visibility": 'none'
        },
        "paint": {
            'fill-color': 'white',
            'fill-opacity': 1.0
        }
    });

    map.addLayer({
        "id": "eyes2",
        "type": "circle",
        "source": "eyes2",
        "layout": {
            //"visibility": 'none'
        },
        "paint": {
            'circle-color': 'red',
            'circle-opacity': 1.0,
            'circle-stroke-color': 'lightblue',
            'circle-stroke-width': 4,
            'circle-stroke-opacity': 1.0,
        }
    });

    //cultural layers
    //cultural layers
    map.addSource('country', { type: 'geojson', data: emptyGJ });
    map.addLayer({
        "id": "country",
        "type": "fill",
        "source": "country",
        "layout": {
            //"visibility": 'none'
        },
        "paint": {
            'fill-color': '#595959',
            'fill-opacity': .5,
            'fill-outline-color': '#333333',
        }
    });


    map.addSource('populated', { type: 'geojson', data: emptyGJ });
    map.addLayer({
        "id": "populated",
        "type": "circle",
        "source": "populated",
        "layout": {
            "visibility": 'none'
        },
        "paint": {
            'circle-color': 'white',
            'circle-opacity': 1.0,
            'circle-stroke-color': '#ff8c1a',
            'circle-stroke-width': 2,
            'circle-stroke-opacity': 1.0,
        }
    });


    //physical layers
    //physical layers
    map.addSource('ocean', { type: 'geojson', data: emptyGJ });
    map.addLayer({
        "id": "ocean",
        "type": "fill",
        "source": "ocean",
        "layout": {
            "visibility": 'none'
        },
        "paint": {
            'fill-color': '#00334d',
            'fill-opacity': 0.5,
            'fill-outline-color': '#00111a',
        }
    });

    map.addSource('river', { type: 'geojson', data: emptyGJ });
    map.addLayer({
        "id": "river",
        "type": "line",
        "source": "river",
        "layout": {
            "visibility": 'none'
        },
        "paint": {
            'line-color': '#0099cc',
            'line-opacity': .8,
            "line-width": 4,
        },
    });

    //Layer Info function
    //Layer Info function
    //Layer Info function
    //Layer Info function
    map.on(touchEvent, function (e) {

        document.getElementById("layer-attribute").innerHTML = "";

    });

    map.on(touchEvent, function (e) {

        var popup = new mapboxgl.Popup();
        var feature;
        var append = document.getElementById('layer-attribute');

        //Cultural - Layer Info
        //Cultural - Layer Info

        if (map.queryRenderedFeatures(e.point, { layers: ['populated'] }).length) {

            feature = map.queryRenderedFeatures(e.point, { layers: ['populated'] })[0];

            append.innerHTML +=
                '<h5>Populated Places</h5>' +
                '<hr>' +
                '<b>City: </b>' + feature.properties.name +
                '<hr>' +
                '<b>Country: </b>' + feature.properties.sov0name +
                '<hr>'
        }

        if (map.queryRenderedFeatures(e.point, { layers: ['country'] }).length) {

            feature = map.queryRenderedFeatures(e.point, { layers: ['country'] })[0];

            append.innerHTML +=
                '<h5>Country</h5>' +
                '<hr>' +
                '<b>Port Name </b>' + feature.properties.admin +
                '<hr>' +
                '<b>Code: </b>' + feature.properties.adm0_a3 +
                '<hr>'
        }

        //Monster - Layer Info
        //Monster - Layer Info
        if (map.queryRenderedFeatures(e.point, { layers: ['monster'] }).length) {

            feature = map.queryRenderedFeatures(e.point, { layers: ['monster'] })[0];

            append.innerHTML +=
                '<h5>Monster Info</h5>' +
                '<hr>' +
                '<b>Name: </b>' + 'Mr. Claw' +
                '<hr>' +
                '<b>Place of Birth: </b>' + 'Atlantic Ocean' +
                '<hr>' +
                '<b>Likes: </b>' + 'Birthday Parties' +
                '<hr>' +
                '<b>Dislikes: </b>' + 'Seafood Festivals' +
                '<hr>'
        }

        //Monster - Layer Info
        //Monster - Layer Info
        if (map.queryRenderedFeatures(e.point, { layers: ['octo'] }).length) {

            feature = map.queryRenderedFeatures(e.point, { layers: ['octo'] })[0];

            append.innerHTML +=
                '<h5>Monster Info</h5>' +
                '<hr>' +
                '<b>Name: </b>' + 'Mr. Octo' +
                '<hr>' +
                '<b>Place of Birth: </b>' + 'Pacific Ocean' +
                '<hr>' +
                '<b>Likes: </b>' + 'Big Salads' +
                '<hr>' +
                '<b>Dislikes: </b>' + 'Jules Verne' +
                '<hr>'
        }


        //Physical - Layer Info
        //Physical  - Layer Info
        if (map.queryRenderedFeatures(e.point, { layers: ['ocean'] }).length) {

            feature = map.queryRenderedFeatures(e.point, { layers: ['ocean'] })[0];

            append.innerHTML +=
                '<h5>Oceans</h5>' +
                '<hr>' +
                '<b>Name: </b>' + feature.properties.name +
                '<hr>'
        }

        if (map.queryRenderedFeatures(e.point, { layers: ['river'] }).length) {

            feature = map.queryRenderedFeatures(e.point, { layers: ['river'] })[0];

            append.innerHTML +=
                '<h5>Major Rivers</h5>' +
                '<hr>' +
                '<b>Name: </b>' + feature.properties.name +
                '<hr>'
        }
    });

    //cursor = pointer on hover configuration
    map.on('mousemove', function (e) {
        var features = map.queryRenderedFeatures(e.point, {
            layers: ['ocean', 'river', 'country', 'populated', 'monster', 'octo']
        });
        map.getCanvas().style.cursor = (features.length) ? 'default' : '';
    });

    //Highlight Features Function
    //Highlight Features Function
    //Highlight Features Function
    //Highlight Features Function
    map.on(touchEvent, function (e) {
        var features = map.queryRenderedFeatures(e.point, { layers: ["populated"] });

        if (map.getLayer("populated_hl")) {
            map.removeLayer("populated_hl");
        }

        if (features.length) {

            map.addLayer({
                "id": "populated_hl",
                "type": "circle",
                "source": "populated",
                "layout": {},
                "paint": {
                    "circle-color": "cyan",
                    "circle-radius": 7
                },
                "filter": ["==", "name", features[0].properties.name],
            });
        }
    });

    map.on(touchEvent, function (e) {
        var features = map.queryRenderedFeatures(e.point, { layers: ["country"] });

        if (map.getLayer("country_hl")) {
            map.removeLayer("country_hl");
        }

        if (features.length) {

            map.addLayer({
                "id": "country_hl",
                "type": "line",
                "source": "country",
                "layout": {},
                "paint": {
                    "line-color": "cyan",
                    "line-width": 3
                },
                "filter": ["==", "sovereignt", features[0].properties.sovereignt],
            });
        }
    });

    //Highlight - Mr. Claw
    map.on(touchEvent, function (e) {
        var features = map.queryRenderedFeatures(e.point, { layers: ["monster"] });

        if (map.getLayer("monster_hl")) {
            map.removeLayer("monster_hl");
        }

        if (features.length) {

            map.addLayer({
                "id": "monster_hl",
                "type": "line",
                "source": "monster",
                "layout": {},
                "paint": {
                    "line-color": "cyan",
                    "line-width": 3
                },
                "filter": ["==", "Id", features[0].properties.Id],
            });
        }
    });

    //Highlight - Mr. Octo
    map.on(touchEvent, function (e) {
        var features = map.queryRenderedFeatures(e.point, { layers: ["octo"] });

        if (map.getLayer("octo_hl")) {
            map.removeLayer("octo_hl");
        }

        if (features.length) {

            map.addLayer({
                "id": "octo_hl",
                "type": "line",
                "source": "octo",
                "layout": {},
                "paint": {
                    "line-color": "cyan",
                    "line-width": 3
                },
                "filter": ["==", "Id", features[0].properties.Id],
            });
        }
    });

    //Highlight - Physical
    map.on(touchEvent, function (e) {
        var features = map.queryRenderedFeatures(e.point, { layers: ["river"] });

        if (map.getLayer("river_hl")) {
            map.removeLayer("river_hl");
        }

        if (features.length) {

            map.addLayer({
                "id": "river_hl",
                "type": "line",
                "source": "river",
                "layout": {},
                "paint": {
                    "line-color": "cyan",
                    "line-width": 4
                },
                "filter": ["==", "name", features[0].properties.name],
            });
        }
    });

    map.on(touchEvent, function (e) {
        var features = map.queryRenderedFeatures(e.point, { layers: ["ocean"] });

        if (map.getLayer("ocean_hl")) {
            map.removeLayer("ocean_hl");
        }

        if (features.length) {

            map.addLayer({
                "id": "ocean_hl",
                "type": "line",
                "source": "ocean",
                "layout": {},
                "paint": {
                    "line-color": "cyan",
                    "line-width": 3
                },
                "filter": ["==", "name", features[0].properties.name],
            });
        }
    });
});

// Directory Options
// Directory Options
// Directory Options - open or closed by defualt (true/false)
var directoryOptions =
    [
        {
            'name': 'Monsters',
            'open': true
        },
        {
            'name': 'Cultural',
            'open': true
        },
        {
            'name': 'Physical',
            'open': true
        },

    ];

// organize layers in the layer tree
var layers =

    [
        // Mr Claw LAYER TREE CONFIG
        // Mr Claw LAYER TREE CONFIG
        {
            'name': 'Mr Claw',
            'id': 'monster_group',
            'hideLabel': ['mouth', 'water-line', 'eyes', 'monster'],
            'icon': 'assets/images/layer-stack-15.svg',
            'layerGroup': [
                {
                    'id': 'monster',
                    'source': 'monster',
                    'name': 'Mr. Claw',
                    'path': 'assets/json/monster.json',
                },
                {
                    'id': 'mouth',
                    'source': 'mouth',
                    'name': 'Mouth',
                    'path': 'assets/json/mouth.json',
                },
                {
                    'id': 'water-line',
                    'source': 'water-line',
                    'name': 'Water',
                    'path': 'assets/json/water.json',
                },
                {
                    'id': 'eyes',
                    'source': 'eyes',
                    'name': 'Eyes',
                    'path': 'assets/json/eyes.json',
                },

            ],
            'directory': 'Monsters'
        },

        // Mr Octo LAYER TREE CONFIG
        // Mr Octo LAYER TREE CONFIG
        {
            'name': 'Mr. Octo',
            'id': 'monster_group_2',
            'hideLabel': ['octo', 'water-line-2', 'eyes2', 'mouth2'],
            'icon': 'assets/images/layer-stack-15.svg',
            'layerGroup': [
                {
                    'id': 'octo',
                    'source': 'octo',
                    'name': 'Mr. Octo',
                    'path': 'assets/json/octo.json',
                },
                {
                    'id': 'water-line-2',
                    'source': 'water-line-2',
                    'name': 'Water',
                    'path': 'assets/json/water2.json',
                },
                {
                    'id': 'mouth2',
                    'source': 'mouth2',
                    'name': 'Mouth',
                    'path': 'assets/json/mouth2.json',
                },
                {
                    'id': 'eyes2',
                    'source': 'eyes2',
                    'name': 'Eyes',
                    'path': 'assets/json/eyes2.json',
                },
            ],
            'directory': 'Monsters'
        },

        // Cultural LAYER TREE CONFIG
        // Cultural LAYER TREE CONFIG

        {
            'name': 'Populated Places',
            'id': 'populated',
            'source': "populated",
            'path': 'https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_populated_places_simple.geojson',
            'directory': 'Cultural',
        },
        {
            'name': 'Countries',
            'id': 'country',
            'source': 'country',
            'path': 'https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_admin_0_map_units.geojson',
            'directory': 'Cultural',
        },


        // Physical LAYER TREE CONFIG
        // Physical LAYER TREE CONFIG

        {
            'name': 'Major Rivers',
            'id': 'river',
            'source': 'river',
            'path': 'https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_rivers_lake_centerlines.geojson',
            'directory': 'Physical',
        },
        {
            'name': 'Oceans',
            'id': 'ocean',
            'source': 'ocean',
            'path': 'https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_110m_geography_marine_polys.geojson',
            'directory': 'Physical',
        },

    ];


var layerList = new LayerTree({ layers: layers, directoryOptions: directoryOptions, onClickLoad: true });

var layerTool = document.getElementById('menu');
layerTool.appendChild(layerList.onAdd(map))


//BOOKMARKS
//BOOKMARKS
//BOOKMARKS

document.getElementById('icelandBookmark').addEventListener('click', function () {

    map.flyTo({
        center: [-18.7457, 65.0662],
        zoom: 5,
    });
});

document.getElementById('safricaBookmark').addEventListener('click', function () {

    map.flyTo({
        center: [23.9417, -29.5353],
        zoom: 5,
    });
});

document.getElementById('japanBookmark').addEventListener('click', function () {

    map.flyTo({
        center: [138.6098, 36.3223],
        zoom: 4,
    });
});

document.getElementById('australiaBookmark').addEventListener('click', function () {

    map.flyTo({
        center: [134.1673, -25.6855],
        zoom: 3

    });
});



//TEXT TOOL
//TEXT TOOL
//TEXT TOOL

var MAP_DIV = map.getCanvasContainer();
var EDIT_NODE = document.getElementById('editTextTool');
var LABEL_NODE = document.getElementById('textTool');

//set user defined sizes/colors in palette
var TEXT_SIZES = [24, 20, 16, 12];
var TEXT_COLORS = ['#000', '#c12123', '#ee4498', '#00924d', '#00afde', '#ccbe00'];

//char count limit
var CHAR_LIMIT = 20;

//drag status
var isDragging = false;


function activateTool(el) {
    if (el.getAttribute('active') === 'true') {
        el.setAttribute('active', false);

        if (el.isEqualNode(EDIT_NODE)) {
            var activeInput = document.querySelector('.label-marker.active span');
            if (activeInput) {
                activeInput.focus();
                activeInput.blur();
            }
        }
        MAP_DIV.style.cursor = '';

    } else {
        el.isEqualNode(EDIT_NODE) ? LABEL_NODE.setAttribute('active', false) : EDIT_NODE.setAttribute('active', false);
        el.setAttribute('active', true);

        MAP_DIV.style.cursor = 'crosshair';
    }
}

//generate unique layer ids for text-labels
function generateTextID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

//convert marker DOM elements to symbol layers
function markerToSymbol(e, elm) {
    if (isDragging) return;

    MAP_DIV.style.cursor = '';

    var that = this instanceof Element ? this : elm;
    var childSpan = document.querySelector('.marker-text-child');

    if (childSpan) var parent = childSpan.parentNode;

    if (that.innerText !== '' && that.innerText.length > 0) {
        parent ? parent.classList.remove('active') : that.classList.remove('active');

        var fontSize = that.style['font-size'] === '' ? TEXT_SIZES[1] : parseInt(that.style['font-size'].split('px')[0]); //textSize[1] is default
        var fontColor = that.style.color === '' ? '#000' : that.style.color;
        var coords = [that.getAttribute('lng'), that.getAttribute('lat')];

        var labelGJ = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {},
                    "geometry": {
                        "type": "Point",
                        "coordinates": coords
                    }
                }
            ]
        };

        var id = generateTextID();
        var lyrID = id + '-custom-text-label';

        map.addSource(id, { type: 'geojson', data: labelGJ });

        map.addLayer({
            "id": lyrID,
            "type": "symbol",
            "source": id,
            "layout": {
                "text-field": that.innerText,
                "text-size": fontSize,
                "symbol-placement": "point",
                "text-keep-upright": true
            },
            "paint": {
                "text-color": fontColor,
                "text-halo-color": '#FFF',
                "text-halo-width": 2,
            },
        });

        //removes text-input marker after clicking off
        LABEL_NODE.setAttribute('active', false);

        that.removeEventListener('blur', markerToSymbol);
    }

    parent ? parent.remove() : that.remove();
}

//label text limit/prevent event keys
function inputText(e) {

    console.log(e.key, e.keyCode)

    //arrow keys
    if ([32, 37, 38, 39, 40, 8].indexOf(e.keyCode) > -1) {
        e.stopPropagation();
        //enter key

    } else if (e.keyCode === 13 && this.innerText.length <= CHAR_LIMIT) {
        this.blur();

        MAP_DIV.style.cursor = '';

        e.preventDefault();
        //limit
    } else if (this.innerText.length >= CHAR_LIMIT && e.keyCode !== 8) {
        e.preventDefault();
        alert(keycode);
    }
}


//pasting text into requires additional handling
//for text limit
function handlePaste(e) {
    var clipboardData, pastedData;

    e.stopImmediatePropagation();
    e.preventDefault();

    clipboardData = e.clipboardData || window.clipboardData;
    pastedData = clipboardData.getData('text/plain').slice(0, CHAR_LIMIT);

    this.innerText = pastedData;
}

function createMarker(e, el) {

    new mapboxgl.Marker(el)
        .setLngLat(e.lngLat)
        .addTo(map);
}

//populates edit palette with user defined colors/sizes
function populatePalette() {
    var palette = document.getElementById('customTextPalette');
    var textSizeDiv = document.getElementById('customTextSize');
    var textColorDiv = document.getElementById('customTextColor');

    for (var s = 0; s < TEXT_SIZES.length; s++) {
        var sElm = document.createElement('div');
        sElm.className = 'font-size-change';
        sElm.id = 'font-' + TEXT_SIZES[s];
        sElm.innerText = 'T'; //change to whatever font/image
        sElm.style['font-size'] = TEXT_SIZES[s] + 'px';
        sElm.addEventListener('mousedown', changeFontStyle);

        textSizeDiv.appendChild(sElm);
    };

    for (var c = 0; c < TEXT_COLORS.length; c++) {
        var cElm = document.createElement('div');
        cElm.className = 'font-color-change';
        cElm.id = 'font-' + TEXT_COLORS[c];
        cElm.style['background-color'] = TEXT_COLORS[c];
        cElm.addEventListener('mousedown', changeFontStyle);

        textColorDiv.appendChild(cElm);
    };
}

//update marker font styles
function changeFontStyle(e) {
    e.preventDefault();
    e.stopPropagation();

    var labelDiv = document.querySelector('.label-marker');
    var childSpan = document.querySelector('.marker-text-child');

    var mark = childSpan ? childSpan : labelDiv;

    if (mark) {
        labelDiv.classList.add('active');
        if (e.target.classList.contains('font-size-change')) {
            mark.style['font-size'] = e.target.style['font-size'];
        } else if (e.target.classList.contains('font-color-change')) {
            mark.style.color = e.target.style['background-color'];
        }

        mark.focus();
    }

    MAP_DIV.style.cursor = 'text';
}

//marker move functionality - modified GL example
//https://www.mapbox.com/mapbox-gl-js/example/drag-a-point/
function beginDrag(e) {
    e.stopImmediatePropagation();

    map.dragPan.disable();

    isDragging = true;

    MAP_DIV.style.cursor = 'cursor:-moz-grab;cursor:-webkit-grab;cursor:grab';

    map.on('mousemove', onDrag);
    map.on('touchmove', onDrag);

    map.once('mouseup', stopDrag);
    map.once('touchend', stopDrag);
}

function onDrag(e) {
    if (!isDragging) return;

    var label = document.querySelector('.label-marker');

    MAP_DIV.style.cursor = 'cursor:-moz-grabbing;cursor:-webkit-grabbing;cursor:grabbing';

    map.dragPan.disable();

    createMarker(e, label);
}

function stopDrag(e) {
    if (!isDragging) return;

    var textSpan = document.querySelector('.marker-text-child');

    textSpan.setAttribute('lng', e.lngLat.lng);
    textSpan.setAttribute('lat', e.lngLat.lat);

    isDragging = false;

    textSpan.parentNode.style.cursor = '';
    MAP_DIV.style.cursor = '';

    map.dragPan.enable();

    setTimeout(function () {
        markerToSymbol(e, textSpan);
    }, 50)

    // Unbind move events
    map.off('mousemove', onDrag);
    map.off('touchmove', onDrag);
}

function addEditLabels(e) {
    e.originalEvent.preventDefault();
    e.originalEvent.stopPropagation();

    if (isDragging) return;

    //create a large bounding box for capture
    var clickBBox = [[e.point.x - 2, e.point.y - 2], [e.point.x + 2, e.point.y + 2]];

    //adding text
    if (LABEL_NODE.getAttribute('active') === 'true') {

        var el = document.createElement('div');
        el.className = 'label-marker';

        el.setAttribute('contenteditable', 'true');
        el.setAttribute('autocorrect', 'off');
        el.setAttribute('spellcheck', 'false');
        el.setAttribute('lng', e.lngLat.lng);
        el.setAttribute('lat', e.lngLat.lat);
        el.style['font-size'] = TEXT_SIZES[1] + 'px';  //defaulting to second size

        map.marker = createMarker(e, el);

        el.addEventListener("blur", markerToSymbol);
        el.addEventListener("keydown", inputText);
        el.addEventListener("paste", handlePaste);

        el.focus();

        //editting text
    } else if (EDIT_NODE.getAttribute('active') === 'true') {

        //filters layers for custom text labels
        function isCustomText(item) {
            return item.layer.id.indexOf('-custom-text-label') > -1
        }

        var features = map.queryRenderedFeatures(clickBBox);
        var activeInput = document.querySelector('.marker-text-child');

        if (features.length) {
            var customLabels = features.filter(isCustomText);

            if (customLabels.length) {
                //only returning the first feature
                //user is going to have to zoom in further
                var feature = customLabels[0].layer;

                var lyrID = feature.id;
                var sourceID = feature.source;
                var text = feature.layout['text-field'];
                var featureFontSize = feature.layout['text-size'] + 'px';
                var featureFontColor = feature.paint['text-color'];

                var mapSource = map.getSource(sourceID);
                var coords = mapSource._data.features[0].geometry.coordinates;

                var container = document.createElement('div');
                container.className = 'label-marker label-container active';

                var el = document.createElement('span');
                el.className = 'marker-text-child';
                el.innerText = text;

                el.style['font-size'] = featureFontSize;
                el.style.color = featureFontColor;

                el.setAttribute('lng', coords[0]);
                el.setAttribute('lat', coords[1]);
                el.setAttribute('contenteditable', 'true');
                el.setAttribute('autocorrect', 'off');
                el.setAttribute('spellcheck', 'false');

                //drag icon - using FontAwesome as an example
                var dragUI = document.createElement('i');
                dragUI.className = 'fa fa-arrows-alt fa-lg drag-icon';
                dragUI.setAttribute('aria-hidden', true);

                container.appendChild(dragUI);
                container.appendChild(el);

                map.removeSource(sourceID);
                map.removeLayer(lyrID);

                createMarker(e, container);

                dragUI.addEventListener("mousedown", beginDrag);
                dragUI.addEventListener("touchstart", beginDrag);

                el.addEventListener("blur", markerToSymbol);
                el.addEventListener("keydown", inputText);
                el.addEventListener("paste", handlePaste);

            } else if (activeInput) {
                activeInput.isEqualNode(e.originalEvent.target) ? activeInput.focus() : markerToSymbol(e, activeInput);
            }
        }
    }
}

//fire function to populate text/color custom pallete
populatePalette();

map.on('click', addEditLabels);


// custom draw styles paramaters
// custom draw styles paramaters
// custom draw styles paramaters
var drawFeatureID = '';
var newDrawFeature = false;
var trackDrawnPolygons = [];
var getLastDrawnPoly = false;

//Draw Tools function
//Draw Tools function
//Draw Tools function
var draw = new MapboxDraw({
    // this is used to allow for custom properties for styling draw features
    // it appends the word "user_" to the property
    userProperties: true,
    displayControlsDefault: false,
    controls: {
        polygon: true,
        point: true,
        line_string: true,
        trash: true,
    },
    styles: [
        // default themes provided by MB Draw
        // default themes provided by MB Draw
        // default themes provided by MB Draw
        // default themes provided by MB Draw


        {
            'id': 'gl-draw-polygon-fill-inactive',
            'type': 'fill',
            'filter': ['all', ['==', 'active', 'false'],
                ['==', '$type', 'Polygon'],
                ['!=', 'mode', 'static']
            ],
            'paint': {
                'fill-color': '#3bb2d0',
                'fill-outline-color': '#3bb2d0',
                'fill-opacity': 0.1
            }
        },
        {
            'id': 'gl-draw-polygon-fill-active',
            'type': 'fill',
            'filter': ['all', ['==', 'active', 'true'],
                ['==', '$type', 'Polygon']
            ],
            'paint': {
                'fill-color': '#fbb03b',
                'fill-outline-color': '#fbb03b',
                'fill-opacity': 0.1
            }
        },
        {
            'id': 'gl-draw-polygon-midpoint',
            'type': 'circle',
            'filter': ['all', ['==', '$type', 'Point'],
                ['==', 'meta', 'midpoint']
            ],
            'paint': {
                'circle-radius': 3,
                'circle-color': '#fbb03b'
            }
        },
        {
            'id': 'gl-draw-polygon-stroke-inactive',
            'type': 'line',
            'filter': ['all', ['==', 'active', 'false'],
                ['==', '$type', 'Polygon'],
                ['!=', 'mode', 'static']
            ],
            'layout': {
                'line-cap': 'round',
                'line-join': 'round'
            },
            'paint': {
                'line-color': '#3bb2d0',
                'line-width': 2
            }
        },
        {
            'id': 'gl-draw-polygon-stroke-active',
            'type': 'line',
            'filter': ['all', ['==', 'active', 'true'],
                ['==', '$type', 'Polygon']
            ],
            'layout': {
                'line-cap': 'round',
                'line-join': 'round'
            },
            'paint': {
                'line-color': '#fbb03b',
                'line-dasharray': [0.2, 2],
                'line-width': 2
            }
        },
        {
            'id': 'gl-draw-line-inactive',
            'type': 'line',
            'filter': ['all', ['==', 'active', 'false'],
                ['==', '$type', 'LineString'],
                ['!=', 'mode', 'static']
            ],
            'layout': {
                'line-cap': 'round',
                'line-join': 'round'
            },
            'paint': {
                'line-color': '#3bb2d0',
                'line-width': 2
            }
        },
        {
            'id': 'gl-draw-line-active',
            'type': 'line',
            'filter': ['all', ['==', '$type', 'LineString'],
                ['==', 'active', 'true']
            ],
            'layout': {
                'line-cap': 'round',
                'line-join': 'round'
            },
            'paint': {
                'line-color': '#fbb03b',
                'line-dasharray': [0.2, 2],
                'line-width': 2
            }
        },
        {
            'id': 'gl-draw-polygon-and-line-vertex-stroke-inactive',
            'type': 'circle',
            'filter': ['all', ['==', 'meta', 'vertex'],
                ['==', '$type', 'Point'],
                ['!=', 'mode', 'static']
            ],
            'paint': {
                'circle-radius': 5,
                'circle-color': '#fff'
            }
        },
        {
            'id': 'gl-draw-polygon-and-line-vertex-inactive',
            'type': 'circle',
            'filter': ['all', ['==', 'meta', 'vertex'],
                ['==', '$type', 'Point'],
                ['!=', 'mode', 'static']
            ],
            'paint': {
                'circle-radius': 3,
                'circle-color': '#fbb03b'
            }
        },
        {
            'id': 'gl-draw-point-point-stroke-inactive',
            'type': 'circle',
            'filter': ['all', ['==', 'active', 'false'],
                ['==', '$type', 'Point'],
                ['==', 'meta', 'feature'],
                ['!=', 'mode', 'static']
            ],
            'paint': {
                'circle-radius': 5,
                'circle-opacity': 1,
                'circle-color': '#fff'
            }
        },
        {
            'id': 'gl-draw-point-inactive',
            'type': 'circle',
            'filter': ['all', ['==', 'active', 'false'],
                ['==', '$type', 'Point'],
                ['==', 'meta', 'feature'],
                ['!=', 'mode', 'static']
            ],
            'paint': {
                'circle-radius': 3,
                'circle-color': '#3bb2d0'
            }
        },
        {
            'id': 'gl-draw-point-stroke-active',
            'type': 'circle',
            'filter': ['all', ['==', '$type', 'Point'],
                ['==', 'active', 'true'],
                ['!=', 'meta', 'midpoint']
            ],
            'paint': {
                'circle-radius': 7,
                'circle-color': '#fff'
            }
        },
        {
            'id': 'gl-draw-point-active',
            'type': 'circle',
            'filter': ['all', ['==', '$type', 'Point'],
                ['!=', 'meta', 'midpoint'],
                ['==', 'active', 'true']
            ],
            'paint': {
                'circle-radius': 5,
                'circle-color': '#fbb03b'
            }
        },
        {
            'id': 'gl-draw-polygon-fill-static',
            'type': 'fill',
            'filter': ['all', ['==', 'mode', 'static'],
                ['==', '$type', 'Polygon']
            ],
            'paint': {
                'fill-color': '#404040',
                'fill-outline-color': '#404040',
                'fill-opacity': 0.1
            }
        },
        {
            'id': 'gl-draw-polygon-stroke-static',
            'type': 'line',
            'filter': ['all', ['==', 'mode', 'static'],
                ['==', '$type', 'Polygon']
            ],
            'layout': {
                'line-cap': 'round',
                'line-join': 'round'
            },
            'paint': {
                'line-color': '#404040',
                'line-width': 2
            }
        },
        {
            'id': 'gl-draw-line-static',
            'type': 'line',
            'filter': ['all', ['==', 'mode', 'static'],
                ['==', '$type', 'LineString']
            ],
            'layout': {
                'line-cap': 'round',
                'line-join': 'round'
            },
            'paint': {
                'line-color': '#404040',
                'line-width': 2
            }
        },
        {
            'id': 'gl-draw-point-static',
            'type': 'circle',
            'filter': ['all',
                ['==', 'mode', 'static'],
                ['==', '$type', 'Point']
            ],
            'paint': {
                'circle-radius': 5,
                'circle-color': '#404040'
            }
        },

        // end default themes provided by MB Draw
        // end default themes provided by MB Draw
        // end default themes provided by MB Draw
        // end default themes provided by MB Draw




        // new styles for toggling colors
        // new styles for toggling colors
        // new styles for toggling colors
        // new styles for toggling colors

        {
            'id': 'gl-draw-polygon-fill-inactive-color-picker',
            'type': 'fill',
            'filter': ['all', ['==', 'active', 'false'],
                ['==', '$type', 'Polygon'],
                ['!=', 'mode', 'static'],
                ['has', 'user_portColor']
            ],
            'paint': {
                'fill-color': ['get', 'user_portColor'],
                'fill-outline-color': ['get', 'user_portColor'],
                'fill-opacity': 0.1
            }
        },
        {
            'id': 'gl-draw-polygon-fill-active-color-picker',
            'type': 'fill',
            'filter': ['all', ['==', 'active', 'true'],
                ['==', '$type', 'Polygon'],
                ['has', 'user_portColor']
            ],
            'paint': {
                'fill-color': ['get', 'user_portColor'],
                'fill-outline-color': ['get', 'user_portColor'],
                'fill-opacity': 0.1
            }
        },
        {
            'id': 'gl-draw-polygon-midpoint-color-picker',
            'type': 'circle',
            'filter': ['all', ['==', '$type', 'Point'],
                ['==', 'meta', 'midpoint']
            ],
            'paint': {
                'circle-radius': 3,
                'circle-color': '#fbb03b'
            }
        },
        {
            'id': 'gl-draw-polygon-stroke-inactive-color-picker',
            'type': 'line',
            'filter': ['all', ['==', 'active', 'false'],
                ['==', '$type', 'Polygon'],
                ['!=', 'mode', 'static'],
                ['has', 'user_portColor']
            ],
            'layout': {
                'line-cap': 'round',
                'line-join': 'round'
            },
            'paint': {
                'line-color': ['get', 'user_portColor'],
                'line-width': 2
            }
        },
        {
            'id': 'gl-draw-polygon-stroke-active-color-picker',
            'type': 'line',
            'filter': ['all', ['==', 'active', 'true'],
                ['==', '$type', 'Polygon'],
                ['has', 'user_portColor']
            ],
            'layout': {
                'line-cap': 'round',
                'line-join': 'round'
            },
            'paint': {
                'line-color': ['get', 'user_portColor'],
                'line-dasharray': [0.2, 2],
                'line-width': 2
            }
        },
        {
            'id': 'gl-draw-line-inactive-color-picker',
            'type': 'line',
            'filter': ['all', ['==', 'active', 'false'],
                ['==', '$type', 'LineString'],
                ['!=', 'mode', 'static'],
                ['has', 'user_portColor']
            ],
            'layout': {
                'line-cap': 'round',
                'line-join': 'round'
            },
            'paint': {
                'line-color': ['get', 'user_portColor'],
                'line-width': 2
            }
        },
        {
            'id': 'gl-draw-line-active-color-picker',
            'type': 'line',
            'filter': ['all', ['==', '$type', 'LineString'],
                ['==', 'active', 'true'],
                ['has', 'user_portColor']
            ],
            'layout': {
                'line-cap': 'round',
                'line-join': 'round'
            },
            'paint': {
                'line-color': ['get', 'user_portColor'],
                'line-dasharray': [0.2, 2],
                'line-width': 2
            }
        },
        {
            'id': 'gl-draw-polygon-and-line-vertex-stroke-inactive-color-picker',
            'type': 'circle',
            'filter': ['all', ['==', 'meta', 'vertex'],
                ['!=', 'active', 'true'],
                ['==', '$type', 'Point'],
                ['!=', 'mode', 'static']
            ],
            'paint': {
                'circle-radius': 5,
                'circle-color': '#fff'
            }
        },
        {
            'id': 'gl-draw-polygon-and-line-vertex-inactive-color-picker',
            'type': 'circle',
            'filter': ['all', ['==', 'meta', 'vertex'],
                ['!=', 'active', 'true'],
                ['==', '$type', 'Point'],
                ['!=', 'mode', 'static']
            ],
            'paint': {
                'circle-radius': 3,
                'circle-color': '#fbb03b'
            }
        },
        {
            'id': 'gl-draw-polygon-and-line-vertex-stroke-active-color-picker',
            'type': 'circle',
            'filter': ['all', ['==', 'meta', 'vertex'],
                ['==', 'active', 'true'],
                ['==', '$type', 'Point'],
                ['!=', 'mode', 'static']
            ],
            'paint': {
                'circle-radius': 7,
                'circle-color': '#fff'
            }
        },
        {
            'id': 'gl-draw-polygon-and-line-vertex-active-color-picker',
            'type': 'circle',
            'filter': ['all', ['==', 'meta', 'vertex'],
                ['==', 'active', 'true'],
                ['==', '$type', 'Point'],
                ['!=', 'mode', 'static']
            ],
            'paint': {
                'circle-radius': 5,
                'circle-color': '#fbb03b'
            }
        },
        {
            'id': 'gl-draw-point-point-stroke-inactive-color-picker',
            'type': 'circle',
            'filter': ['all', ['==', 'active', 'false'],
                ['==', '$type', 'Point'],
                ['==', 'meta', 'feature'],
                ['!=', 'mode', 'static'],
                ['has', 'user_portColor']
            ],
            'paint': {
                'circle-radius': 5,
                'circle-opacity': 1,
                'circle-color': '#fff'
            }
        },
        {
            'id': 'gl-draw-point-inactive-color-picker',
            'type': 'circle',
            'filter': ['all', ['==', 'active', 'false'],
                ['==', '$type', 'Point'],
                ['==', 'meta', 'feature'],
                ['!=', 'mode', 'static'],
                ['has', 'user_portColor']
            ],
            'paint': {
                'circle-radius': 3,
                'circle-color': ['get', 'user_portColor']
            }
        },
        {
            'id': 'gl-draw-point-stroke-active-color-picker',
            'type': 'circle',
            'filter': ['all', ['==', '$type', 'Point'],
                ['==', 'active', 'true'],
                ['!=', 'meta', 'midpoint'],
                ['has', 'user_portColor']
            ],
            'paint': {
                'circle-radius': 7,
                'circle-color': '#fff'
            }
        },
        {
            'id': 'gl-draw-point-active-color-picker',
            'type': 'circle',
            'filter': ['all', ['==', '$type', 'Point'],
                ['!=', 'meta', 'midpoint'],
                ['==', 'active', 'true'],
                ['has', 'user_portColor']
            ],
            'paint': {
                'circle-radius': 5,
                'circle-color': ['get', 'user_portColor']
            }
        },
        {
            'id': 'gl-draw-polygon-fill-static-color-picker',
            'type': 'fill',
            'filter': ['all', ['==', 'mode', 'static'],
                ['==', '$type', 'Polygon'],
                ['has', 'user_portColor']
            ],
            'paint': {
                'fill-color': ['get', 'user_portColor'],
                'fill-outline-color': ['get', 'user_portColor'],
                'fill-opacity': 0.1
            }
        },
        {
            'id': 'gl-draw-polygon-stroke-static-color-picker',
            'type': 'line',
            'filter': ['all', ['==', 'mode', 'static'],
                ['==', '$type', 'Polygon'],
                ['has', 'user_portColor']
            ],
            'layout': {
                'line-cap': 'round',
                'line-join': 'round'
            },
            'paint': {
                'line-color': ['get', 'user_portColor'],
                'line-width': 2
            }
        },
        {
            'id': 'gl-draw-line-static-color-picker',
            'type': 'line',
            'filter': ['all', ['==', 'mode', 'static'],
                ['==', '$type', 'LineString'],
                ['has', 'user_portColor']
            ],
            'layout': {
                'line-cap': 'round',
                'line-join': 'round'
            },
            'paint': {
                'line-color': ['get', 'user_portColor'],
                'line-width': 2
            }
        },
        {
            'id': 'gl-draw-point-static-color-picker',
            'type': 'circle',
            'filter': ['all',
                ['==', 'mode', 'static'],
                ['==', '$type', 'Point'],
                ['has', 'user_portColor']
            ],
            'paint': {
                'circle-radius': 5,
                'circle-color': ['get', 'user_portColor']
            }
        }
    ]
});

var drawTool = document.getElementById('drawAppend');
drawTool.appendChild(draw.onAdd(map)).setAttribute("style", "display: inline-flex;", "border: 0;");

// create draw palette
function populateDrawPalette() {
    var drawFeatureColor = document.getElementById('customDrawColor');

    for (var c = 0; c < TEXT_COLORS.length; c++) {
        var cElm = document.createElement('div');
        cElm.className = 'draw-color-change';
        cElm.id = 'draw-' + TEXT_COLORS[c];
        cElm.style['background-color'] = TEXT_COLORS[c];
        cElm.addEventListener('mousedown', changeDrawColor);

        drawFeatureColor.appendChild(cElm);
    };
}

function handlePolygonOrder(clickedFeats) {
    if (clickedFeats.length > 1) {
        var tempTrack = trackDrawnPolygons.filter(function (p) {
            return clickedFeats.indexOf(p) > -1;
        });

        var lastPoly = tempTrack[tempTrack.length - 1];
        draw.changeMode('direct_select', { featureId: lastPoly });

        var feat = draw.get(lastPoly);
        var c = feat.properties.portColor ? feat.properties.portColor : '#fbb03b';
        handleVerticesColors(c);

    } else if (clickedFeats.length === 1) {

        var feat = draw.get(clickedFeats[0]);
        var c = feat.properties.portColor ? feat.properties.portColor : '#fbb03b';
        handleVerticesColors(c);
    }

    getLastDrawnPoly = false;
}


// vertices and midpoints don't inherit their parent properties
// so we need to handle those edge cases
function handleVerticesColors(color) {
    // midppoints
    map.setPaintProperty('gl-draw-polygon-midpoint-color-picker.hot', 'circle-color', color);
    map.setPaintProperty('gl-draw-polygon-midpoint-color-picker.cold', 'circle-color', color);

    // vertices
    map.setPaintProperty('gl-draw-polygon-and-line-vertex-inactive-color-picker.cold', 'circle-color', color);
    map.setPaintProperty('gl-draw-polygon-and-line-vertex-inactive-color-picker.hot', 'circle-color', color);

    //active vertex
    map.setPaintProperty('gl-draw-polygon-and-line-vertex-active-color-picker.cold', 'circle-color', color);
    map.setPaintProperty('gl-draw-polygon-and-line-vertex-active-color-picker.hot', 'circle-color', color);
}

// color change function of draw features
var changeDrawColor = function (e) {

    if (e.target.id && e.target.id.indexOf('draw-') === -1) return;

    var color = e.target.id.replace(/draw-/, '');

    if (drawFeatureID !== '' && typeof draw === 'object') {

        draw.setFeatureProperty(drawFeatureID, 'portColor', color);
        var feat = draw.get(drawFeatureID);
        draw.add(feat);

        // race conditions exist between events
        // and draw's transitions between .hot and .cold layers
        setTimeout(function () {
            handleVerticesColors(color);
        }, 50);
    }

};

// callback for draw.update and draw.selectionchange
var setDrawFeature = function (e) {
    if (e.features.length && e.features[0].type === 'Feature') {
        var feat = e.features[0];
        drawFeatureID = feat.id;

        if (feat.geometry.type === 'Polygon' && trackDrawnPolygons.length > 1 && draw.getMode() !== 'draw_polygon' &&
            feat.id !== trackDrawnPolygons[trackDrawnPolygons.length - 1]) {
            getLastDrawnPoly = true;
        } else {
            var c = feat.properties.portColor ? feat.properties.portColor : '#fbb03b';

            // race conditions exist between events
            // and draw's transitions between .hot and .cold layers
            setTimeout(function () {
                handleVerticesColors(c);
            }, 50);
        }
    }
};

// Event Handlers for Draw Tools
map.on('draw.create', function (e) {
    newDrawFeature = true;
    if (e.features.length && e.features[0].geometry.type === 'Polygon') {
        trackDrawnPolygons.push(e.features[0].id);
    }
});

// track handling for polygon features
map.on('draw.delete', function (e) {
    if (e.features.length) {
        var feats = e.features;
        var featsToRemove = [];

        for (var i = feats.length - 1; i >= 0; i--) {
            featsToRemove.push(feats[i].id);
        }

        var tempTrack = trackDrawnPolygons.filter(function (p) {
            return featsToRemove.indexOf(p) < 0;
        });

        trackDrawnPolygons = tempTrack;
    }
});

map.on('draw.update', setDrawFeature);
map.on('draw.selectionchange', setDrawFeature);

map.on('click', function (e) {
    if (getLastDrawnPoly) {
        var clickedFeats = draw.getFeatureIdsAt(e.point);
        handlePolygonOrder(clickedFeats);
    } else if (!newDrawFeature) {

        handleVerticesColors('#fbb03b');
        var drawFeatureAtPoint = draw.getFeatureIdsAt(e.point);

        //if another drawFeature is not found - reset drawFeatureID
        drawFeatureID = drawFeatureAtPoint.length ? drawFeatureAtPoint[0] : '';
    }

    newDrawFeature = false;
});


//// Turf Area Calc
var selectedUnits = '';
var selectedMeasuredFeature = '';
var measurementActive = false;


function removeMeasurementValues() {
    $('#calculated-area p').remove();
    $('#calculated-length p').remove();
}

function calculateDimensions(data) {
    if (!data.id) return;

    var area, rounded_area, areaAnswer, length, rounded_length, lineAnswer;
    //FEET
    if (selectedUnits === 'feet') {

        area = turf.area(data) / 0.09290304;
        // restrict to 2 decimal points
        rounded_area = Math.round(area * 100) / 100;
        areaAnswer = document.getElementById('calculated-area');
        areaAnswer.innerHTML = '<p>' + rounded_area + ' ft<sup>2</sup></p>';

        length = turf.lineDistance(data, 'meters') / 0.3048;
        // restrict to 2 decimal points
        rounded_length = Math.round(length * 100) / 100;
        lineAnswer = document.getElementById('calculated-length');
        lineAnswer.innerHTML = '<p>' + rounded_length + ' ft</p>';

        //METER
    } else if (selectedUnits === 'meter') {

        area = turf.area(data);
        // restrict to 2 decimal points
        rounded_area = Math.round(area * 100) / 100;
        areaAnswer = document.getElementById('calculated-area');
        areaAnswer.innerHTML = '<p>' + rounded_area + ' m<sup>2</sup></p>';

        length = turf.lineDistance(data, 'meters');
        // restrict to 2 decimal points
        rounded_length = Math.round(length * 100) / 100;
        lineAnswer = document.getElementById('calculated-length');
        lineAnswer.innerHTML = '<p>' + rounded_length + ' m</p>';

        //MILE
    } else if (selectedUnits === 'mile') {

        area = turf.area(data) / 2589988.11;
        // restrict to 4 decimal points
        rounded_area = Math.round(area * 10000) / 10000;
        areaAnswer = document.getElementById('calculated-area');
        areaAnswer.innerHTML = '<p>' + rounded_area + ' mi<sup>2</sup></p>';

        length = turf.lineDistance(data, 'meters') / 1609.344;
        // restrict  to 2 decimal points
        rounded_length = Math.round(length * 100) / 100;
        lineAnswer = document.getElementById('calculated-length');
        lineAnswer.innerHTML = '<p>' + rounded_length + ' mi</p>';

        //KILOMETER
    } else if (selectedUnits === 'kilometer') {

        area = turf.area(data) / 1000000;
        // restrict to 4 decimal points
        rounded_area = Math.round(area * 10000) / 10000;
        areaAnswer = document.getElementById('calculated-area');
        areaAnswer.innerHTML = '<p>' + rounded_area + ' km<sup>2</sup></p>';

        length = turf.lineDistance(data, 'meters') / 1000;
        // restrict to 2 decimal points
        rounded_length = Math.round(length * 100) / 100;
        lineAnswer = document.getElementById('calculated-length');
        lineAnswer.innerHTML = '<p>' + rounded_length + ' km</p>';

        //ACRE
    } else if (selectedUnits === 'acre') {

        area = turf.area(data) / 4046.85642;
        // restrict  to 4 decimal points
        rounded_area = Math.round(area * 10000) / 10000;
        areaAnswer = document.getElementById('calculated-area');
        areaAnswer.innerHTML = '<p>' + rounded_area + ' acres</p>';

        length = turf.lineDistance(data, 'meters') / 0.3048;
        // restrict to 2 decimal points
        rounded_length = Math.round(length * 100) / 100;
        lineAnswer = document.getElementById('calculated-length');
        lineAnswer.innerHTML = '<p>' + rounded_length + ' ft</p>';

    }
}

// callback fires on the events listed below and fires the
// above calculateDimensions function
var calculateCallback = function (e) {
    if (e.features.length && (e.features[0].geometry.type === 'Polygon' || e.features[0].geometry.type === 'LineString')) {
        measurementActive = true;
        selectedMeasuredFeature = e.features[0].id;
        calculateDimensions(e.features[0]);
    }
}

map.on('draw.create', calculateCallback);
map.on('draw.update', calculateCallback);
map.on('draw.selectionchange', calculateCallback);

map.on('draw.delete', function (e) {
    selectedMeasuredFeature = '';
    measurementActive = false;
    removeMeasurementValues();
});

// apparently there's no method to track/watch a drag or vertex
// of a newly instantiated feature that has yet to be 'created'
// or perhaps it's not documented anywhere in GL Draw
// so we have to make our own
map.on('mousemove', function (e) {
    if (draw.getMode() === 'draw_line_string' || draw.getMode() === 'draw_polygon') {
        var linePts = draw.getFeatureIdsAt(e.point);

        if (linePts.length) {
            // some draw features return back as undefined
            var activeID = linePts.filter(function (feat) {
                return typeof feat === 'string';
            })

            if (activeID.length) {
                measurementActive = true;
                selectedMeasuredFeature = activeID[0];

                var fc = draw.get(selectedMeasuredFeature);
                calculateDimensions(fc);
            }
        }
    } else if (draw.getMode() === 'direct_select' && selectedMeasuredFeature !== '') {
        var fc = draw.get(selectedMeasuredFeature);

        if (fc.geometry.type === 'LineString' || fc.geometry.type === 'Polygon') {
            calculateDimensions(fc);
        }

    }
});

// remove measurements from input
map.on('click', function (e) {
    if (measurementActive) {
        var measuredFeature = draw.getFeatureIdsAt(e.point);

        if (measuredFeature.length) {
            // some draw features return back as undefined
            var mF = measuredFeature.filter(function (feat) {
                return typeof feat === 'string';
            })

            selectedMeasuredFeature = mF.length ? mF[0] : '';

        } else {
            removeMeasurementValues();
        }
    } else {
        removeMeasurementValues();
    }

    measurementActive = false;
});


$(function () {
    // set unit value
    selectedUnits = $('input[type=radio][name=unit]:checked').val();

    $('input[type=radio][name=unit]').change(function () {
        selectedUnits = this.value;

        //update values based on new units
        if (selectedMeasuredFeature !== '' || measurementActive) {
            var gj = draw.get(selectedMeasuredFeature);
            calculateDimensions(gj);
        }
    })

    populateDrawPalette();
});
