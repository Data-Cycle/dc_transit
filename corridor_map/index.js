
const api_key = ""
mapboxgl.accessToken = 'pk.eyJ1IjoibWFoa2FoIiwiYSI6ImNqZW9zNHBvaTBhc2YzM2x0OWg3aXZ5dTAifQ.F1uwBes6jRJHdwqeSMiA-w';
bus_lines = ['A2', 'A4', 'A6', 'A7', 'A8', 'W5', 'A9', '52', '54', '59', '70',
             '74', '79', 'X1', 'X2', 'X3', 'X9', '80', 'G8', 'G9', 'S1', 'S2',
             'S4', 'S9', '90', '92', '30N', '30S', '31', '32', '33', '34', '36',
             '37', '39'];
rc = {'A2': "Anacostia/Congress Heights", 'A4': "Anacostia/Congress Heights",
      'A6': "Anacostia/Congress Heights", 'A7': "Anacostia/Congress Heights",
      'A8': "Anacostia/Congress Heights", 'W5': "Anacostia/Congress Heights",
      'A9': "Anacostia/Congress Heights", '52': "Fourteenth Street",
      '54': "Fourteenth Street", '59': "Fourteenth Street", '70': "Georgia Avenue/7th Street",
      '74': "Georgia Avenue/7th Street", '79': "Georgia Avenue/7th Street",
      'X1': "H Street/Benning Road", 'X2': "H Street/Benning Road",
      'X3': "H Street/Benning Road", 'X9': "H Street/Benning Road",
      '80': "North Capitol Street", 'G8': "Rhode Island Avenue",
      'G9': "Rhode Island Avenue", 'S1': "Sixteenth Street", 'S2': "Sixteenth Street",
      'S4': "Sixteenth Street", 'S9': "Sixteenth Street", '90': "U Street/Garfield",
      '92': "U Street/Garfield", '30N': "Wisconsin Avenue/Pennsylvania Avenue",
      '30S': "Wisconsin Avenue/Pennsylvania Avenue", '31': "Wisconsin Avenue/Pennsylvania Avenue",
      '32': "Wisconsin Avenue/Pennsylvania Avenue", '33': "Wisconsin Avenue/Pennsylvania Avenue",
      '34': "Wisconsin Avenue/Pennsylvania Avenue", '36': "Wisconsin Avenue/Pennsylvania Avenue",
      '37': "Wisconsin Avenue/Pennsylvania Avenue", '39': "Wisconsin Avenue/Pennsylvania Avenue"};
corridors = ["Anacostia/Congress Heights", "Fourteenth Street", "Georgia Avenue/7th Street", "H Street/Benning Road",
  "North Capitol Street", "Rhode Island Avenue", "Sixteenth Street", "U Street/Garfield", "Wisconsin Avenue/Pennsylvania Avenue"];
colors = ['#8dd3c7','#ffffb3','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#d9d9d9','#bc80bd','#ccebc5','#ffed6f'];

const plot = async () => {

  var routes = {};

  for (var i = 0; i < bus_lines.length; i++) {
    var wait = ms => new Promise((r, j)=>setTimeout(r, ms))
    await wait(200)
    console.log(`Starting ${bus_lines[i]}`)
    const response = await fetch(`https://api.wmata.com/Bus.svc/json/jRouteDetails?RouteID=${bus_lines[i]}&api_key=${api_key}`);
    const myJson = await response.json(); //extract JSON from the http response

    // Process Data
    routes[i] = {}
    routes[i]['routeGeojsons'] = routeToGeojson(myJson);
    routes[i]['stopGeojsons'] = stopToGeojson(myJson);
    routes[i]['name'] = bus_lines[i]
    routes[i]['corridor'] = rc[bus_lines[i]]
    routes[i]['color'] = colors[corridors.indexOf(routes[i]['corridor'])]


    // for(var i = 0; i < 10; i++) {
    //   console.log(Math.cos(Math.cos(Math.sin(Math.random())) * Math.cos(Math.sin(Math.random()))) * Math.log2(Math.random()+10) * Math.exp(Math.random()+10))
    // }
  };

  console.log(routes)

  // Mapping
  const map = new mapboxgl.Map({
    container: 'map', // container element id
    style: 'mapbox://styles/mapbox/light-v9',
    center: [-77.030034, 38.901863], // initial map center in [lon, lat]
    zoom: 11
  });

  map.on('load', function() {
    for (var i = 0; i < bus_lines.length; i++) {
      plotRoutes(map, routes[i]['name'], routes[i]['routeGeojsons'], routes[i]['color']);
      plotStops(map, routes[i]['name'], routes[i]['stopGeojsons'], routes[i]['color']);
    };
  });
}

plot()

function timeout(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

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

function plotRoutes(map, name, data, color) {
  map.addLayer({
    "id": `routes_${name}`,
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
      "line-color": color,
      "line-width": 5
    }
  })
}

function plotStops(map, name, data, color) {
  map.addLayer({
    "id": `stops_${name}`,
    "type": "circle",
    "source": {
      "type": "geojson",
      "data": data
    },
    "paint": {
      "circle-color": [
        'match',
        ['get', 'DirectionNum'],
        '0', color,
        '1', color,
        '#ccc'
        ],
      "circle-radius": 5,
      "circle-stroke-width": 1
    }
  })
}
