import requests
import json
import sys
import geopy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

latitude = 38.8820057
longitude = -77.1115141
# default cords are for Ballston MU metro station

base_url = "https://api-bird.prod.birdapp.com"
nearby_url = base_url + "/bird/nearby-by-cells"
cells_url = base_url + "/map/rider-cells" # added
chirp_url = base_url + "/bird/chirp"
user_url = base_url + "/user"

user_coords = (latitude, longitude)

print("target cords: ",latitude, longitude)

get_cell_ids_payload = {
  "geometries": {
    "55353538521136": {
      "rect": {
        "hi": {
          "accuracy": None,
          "altitude": None,
          "heading": None,
          # orignally:
          # "latitude": 38.88999999999999
          # "longitude": -77.11
          # round latitude to 38.88 (actual, to the nearest 2 decimal places)
          # round longitude to -77.11 (actual, to the nearest 2 decimal places, minus 0.01)
          "latitude": round(latitude, 5),
          "longitude": round(longitude, 2),
          "mocked": False,
          "source": "gps",
          "speed": None,
          "timestamp": "2026-11-02T07:25:49.594-05:00"
        },
        "lo": {
          "accuracy": None,
          "altitude": None,
          "heading": None,
          # orignally:
          # "latitude": 38.879999999999995
          # "longitude": -77.12
          # round latitude to 38.87 (actual, to the nearest 2 decimal places, minus 0.01)
          # round longitude to -77.12 (actual, to the nearest 2 decimal places)
          "latitude": round(latitude, 2) - 0.01,
          "longitude": round(longitude, 2) - 0.01,
          "mocked": False,
          "source": "gps",
          "speed": None,
          "timestamp": "2026-11-02T07:25:49.594-05:00"
        }
      }
    }
  },
  "types": [
    "bird"
  ]
}

location_data = {
    "latitude": latitude,
    "longitude": longitude,
    "heading": None,
    "speed": None,
    "altitude": 60.81604766845703,
    "accuracy": 100.0,
    "mocked": False,
    "timestamp": "2026-10-26T18:27:53.352-04:00",
    "source": "gps"
}

# Headers are the same (Almost) everywhere
headers = {
    "App-Version": "4.417.1.3",
    "Accept-Language": "en-US,en",
    "Bird-Device-Id": "038abc5740cbcf96",
    "Battery-Level": "64",
    "Bluetooth-State": "disabled",
    "Carrier-Name": "Google Fi",
    "Client-Time": "2026-10-26T17:57:31.747-04:00",
    "Connection-Type": "unknown",
    "Device-Model": "Pixel 10a",
    "Device-Name": "stallion",
    "Device-Region": "US",
    "Device-Language": "en-US",
    "Device-Id": "038abc5740cbcf96",
    "Location": json.dumps(location_data),
    "Mobile-Network-Generation": "unknown",
    "OS-Version": "16",
    "Platform": "android",
    "User-Agent": "Bird/4.417.1.3 (co.bird.android; release; Android - 16)",
    "App-Name": "bird",
    "App-Type": "operator",
    "Role": "operator",
    "Authorization": "Bearer eyJhbGciOiJSUzUxMiJ9.eyJqdGkiOiIzODhhYzkwOS04MDRmLTQ4MWYtYmVjZi1hNWNkYjhhOWRlNTYiLCJzdWIiOiI1ZjM4OWI4Mi0yOTE0LTQ4MmItOTdhOC03MzI4NGM1ODczOGUiLCJuYmYiOjE3OTM2MjIzNDksImV4cCI6MTc5MzcwODc0OSwiYXVkIjoiYmlyZC5zZXJ2aWNlcyIsImlzcyI6ImJpcmQuYXV0aCIsImlhdCI6MTc5MzYyMjM0OSwicm9sZXMiOlsiVVNFUiJdLCJhcHAiOiI3YjhlZDk1NS02ZTNhLTRlZWMtYmEyMC04OGFmOWQ3YWVhNzYiLCJ2ZXIiOiIwLjAuMiJ9.IwdP6NGfXQ4zK1iVXQn7WIq_n0LRdvbIIBP5F-bhQqO52HAnaOtDhsXNYv-esM05VzehT3wkJoBKTq7H7NdZkz3wkkH_-vLUcUfBhcSdPRrWj1taQcSk8zElv3Upb_bcX6ABf-CaiTFs4K9zPu2uvCodyvbh3asFU1SK0AT17FpdRuP-GG_Gzv4jDsALj56guos8v568erjsF-E5A0yzIaDf2IrPpqQoThFupc2Ay7tbdvJf149rGYIKaFiHOoBoN3WbUt8Cvh4mskCu2kJUREaVa_A9GsVRRXcF__oVC06dEIUPStWBCQD0vpP71hff9iVHhaX6lQGE34ytfAbyGwk8mGipJlSNMsx3bPaj7zs5Onatjh2uLvd7JcIss7S4kG3cdJHcvRtGqOR1yHRSWDe412UFtGK1ScD5qC-JVQjm3pXbVwvAkxncF4dU-yAynua-yfwp0eXzKrWATf93VPjr_i0GxpkFxJ3ig5MrqQNNEpVH5JC736J7iAg1Jh4kgiFM0okvuiT7j8thJ6nyXnIQ8EnrqYuB6DZXu8qwv9AOcMxgDAr8LbGLh0W8ZaUdKa0lsqQdfG9FzA_CSjMLoj4R3YpvNvtidS3l6QbVrQY4rNFyYer-IJzwyAHt723SuEIF2SrgWJ_wRqtJYPnplwlLCCJ3B76ROONl6QH0Bvo"
}

### GET LIST OF CELL IDS 

# Send POST request with headers and Payload to the nearby-by-cells endpoint
cell_response = requests.post(cells_url, headers=headers, json=get_cell_ids_payload)

# Turn the JSON response into a list
cell_data = cell_response.json()

first_cell = next(iter(cell_data["cells"].values()))

payload_cell_ids = first_cell["birds"]["cell_ids"]

nearby_payload = {
    "map_center": {
        "latitude": latitude,
        "longitude": longitude,
        "mocked": "false",
        "timestamp": "1969-12-31T19:00:00.000-05:00",
        "source": ""
    },
    "cell_ids": payload_cell_ids
}

# DEBUG:
print("Cell Data api response:")
print(json.dumps(cell_data, indent=4))
print("clean cell ids list:")
print(payload_cell_ids)
print("nearby payload:")
print(json.dumps(nearby_payload, indent=4))

print("Starting chirp requests...")
response = requests.post(nearby_url, headers=headers, json=nearby_payload)

nearby_data = response.json()

scooters = {}
# replaces: bird_ids = [bird["id"] for bird in nearby_data["birds"]]
for bird in nearby_data["birds"]:
    scooter_id = bird["id"]
    scooter_lat = bird["location"]["latitude"]
    scooter_lng = bird["location"]["longitude"]
    
    # Calculate the distance between the user and the bird
    scooter_coords = (scooter_lat, scooter_lng)
    distance = geodesic(user_coords, scooter_coords).miles
    
    scooters[scooter_id] = {
        "code": bird["code"],
        "scooter_lat": scooter_lat,
        "scooter_lng": scooter_lng,
        "distance_miles": round(distance, 3)
    }

# sorts the dictionary based on how far from the user the scooters are.
sorted_scooters = dict(
    sorted(scooters.items(), key=lambda item: item[1]["distance_miles"])
)