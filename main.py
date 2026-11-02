import requests
import json
import sys
import geopy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


address = input("Enter a zip code In the US or address (or 'enter' to input lat/lon manually): ")
if address:
    geolocator = Nominatim(user_agent="bird_api_choir")
    location = geolocator.geocode(address + ", USA")
    latitude = location.latitude
    longitude = location.longitude
else:
    latitude = input("Enter latitude (or hit `enter` to use default): ") or 38.8820057
    longitude = input("Enter longitude (or hit `enter` to use default): ") or -77.1115141

# default cords are for Ballston MU metro station

user_coords = (latitude, longitude)

print("target cords: ",latitude, longitude)

chirp_type = input("DEBUG: enable alarm (y/n): ")
if chirp_type.lower() == "n" or chirp_type.lower() == "no":
    alarm = False
    print("alarm disabled")
else:
    alarm = True
    print("alarm enabled")

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

nearby_payload = {
    "map_center": {
        "latitude": latitude,
        "longitude": longitude,
        "mocked": "false",
        "timestamp": "1969-12-31T19:00:00.000-05:00",
        "source": ""
    },
    "cell_ids": [
        # NEED TO ADD A CALL THAT FINDS CELL IDS FROM USER LAT/LON
        # POST to /map/rider-cells (i think, see chucker_exports/map_ridercells.txt) 
        # or just added manually (witch is what i did. but will fail if its supposed dynamic)
        # It looks like something breaks when i add more then 3 "cell_ids" so...
        # no clue, still broken
        "-8523145651523944448",
        "-8523145514084990976",
        "-8523142902744875008"
    ]
}

def check_connection(url):
    print("Checking connection to API...")
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        print("Connection active")
    else: 
        print("Connection failed with status code:", response.status_code)
        sys.exit()

def verify_headers(url, headers):
    print("Verifying headers...")
    response = requests.get(url, headers=headers, timeout=5)
    server_responce = response.json()
    if "code" in server_responce:
        responce_code = server_responce["code"]
        print("Header verification failed with status code:", responce_code)
        print("Is auth token valid?")
        sys.exit()
    else:
        print("Headers are valid")

base_url = "https://api-bird.prod.birdapp.com"
nearby_url = base_url + "/bird/nearby-by-cells"
chirp_url = base_url + "/bird/chirp"
user_url = base_url + "/user"

check_connection("https://bird.co/")
verify_headers(user_url, headers)

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

for scooter_id, info in sorted_scooters.items():
    chirp_payload = {
        "alarm": alarm,
        "bird_id": scooter_id
    }
    chirp_response = requests.put(chirp_url, headers=headers, json=chirp_payload)
    chirp_data = chirp_response.json()
    scooter_code = info["code"]
    
    if not chirp_data["down"]:
        print(f"Success: {scooter_code}")
    else:
        print(f"Failed: {scooter_code}")