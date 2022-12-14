###source venv/local/bin/activate
        sudo lsof -t -i tcp:8000 | xargs kill -9


Create a location. Enter this mutation in the left pane and hit CTRL+ENTER:
mutation {
  createLocation(name: "my first location", lat: 1, lon: 2) {
    location {
      id
    }
  }
}
See the response:
{
  "data": {
    "createLocation": {
      "location": {
        "id": "1"
      }
    }
  }
}
Query all locations:
query {
  allLocations {
    createdAt
    id
    lat
    lon
    name
  }
}
See the response:
{
  "data": {
    "allLocations": [
      {
        "createdAt": "2019-02-22T06:39:08.512197+00:00",
        "id": "1",
        "lat": 1,
        "lon": 2,
        "name": "my first location"
      }
    ]
  }
}