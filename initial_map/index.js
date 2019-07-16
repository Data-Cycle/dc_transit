
const api_key = ""
mapboxgl.accessToken = 'pk.eyJ1IjoibWFoa2FoIiwiYSI6ImNqZW9zNHBvaTBhc2YzM2x0OWg3aXZ5dTAifQ.F1uwBes6jRJHdwqeSMiA-w';


const plot = async () => {
  const response = await fetch(`https://api.wmata.com/Bus.svc/json/jRouteDetails?RouteID=70&api_key=${api_key}`);
  const myJson = await response.json(); //extract JSON from the http response

  // Process Data
  console.log(response);
  console.log(myJson);
  var routeGeojson = routeToGeojson(myJson);
  console.log(routeGeojson)
  var stopGeojson = stopToGeojson(myJson);
  console.log(stopGeojson)
  testData = stopGeojson;

  // Mapping
  const map = new mapboxgl.Map({
    container: 'map', // container element id
    style: 'mapbox://styles/mapbox/light-v9',
    center: [-77.030034, 38.901863], // initial map center in [lon, lat]
    zoom: 11
  });

  map.on('load', function() {
    plotRoutes(map, routeGeojson);
    plotStops(map, stopGeojson);
  });
}

plot()

function routeToGeojson(json) {
  var geojson = {
      "name":"Routes",
      "type":"FeatureCollection",
      "features":[]
  };
  for (var i = 0; i < 2; i++) {
    var route = {
        "type":"Feature",
        "geometry":{
            "type":"LineString",
            "coordinates":[]
        },
        "properties": {
            "DirectionNum": json[`Direction${i}`].DirectionNum,
            "DirectionText": json[`Direction${i}`].DirectionText,
            "Name": json.Name,
            "RouteID": json.RouteID
        }
    };
    for (var j = 0; j < json[`Direction${i}`].Shape.length; j++) {
      route.geometry.coordinates.push([
        json[`Direction${i}`].Shape[j].Lon,
        json[`Direction${i}`].Shape[j].Lat
      ]);
    };
    geojson.features.push(route);
  };
  return geojson;
};



function stopToGeojson(json) {
  var geojson = {
      "name":"Stops",
      "type":"FeatureCollection",
      "features":[]
  };
  for (var i = 0; i < 2; i++) {
    for (var j = 0; j < json[`Direction${i}`].Stops.length; j++) {
      var stop = {
          "type":"Feature",
          "geometry":{
              "type":"Point",
              "coordinates":[
                json[`Direction${i}`].Stops[j].Lon,
                json[`Direction${i}`].Stops[j].Lat
              ]
          },
          "properties": {
              "DirectionNum": json[`Direction${i}`].DirectionNum,
              "DirectionText": json[`Direction${i}`].DirectionText,
              "Route Name": json.Name,
              "RouteID": json.RouteID,
              "StopID": json[`Direction${i}`].Stops[j].StopID,
              "Routes Stopping": json[`Direction${i}`].Stops[j].Routes,
              "Stop Name": json[`Direction${i}`].Stops[j].Name

          }
      };
    geojson.features.push(stop);
    };
  };
  return geojson;
};


function plotRoutes(map, data) {
  map.addLayer({
    "id": "routes",
    "type": "line",
    "source": {
      "type": "geojson",
      "data": data
    },
    "layout": {
      "line-join": "round",
      "line-cap": "round"
    },
    "paint": {
      "line-color": "#888",
      "line-width": 5
    }
  })
}

function plotStops(map, data) {
  map.addLayer({
    "id": "stops",
    "type": "circle",
    "source": {
      "type": "geojson",
      "data": data
    },
    "paint": {
      "circle-color": [
        'match',
        ['get', 'DirectionNum'],
        '0', '#fbb03b',
        '1', '#223b53',
        '#ccc'
        ],
      "circle-radius": 5
    }
  })
}
