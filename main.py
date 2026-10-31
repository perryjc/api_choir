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
    "Authorization": "Bearer eyJhbGciOiJSUzUxMiJ9.eyJqdGkiOiJjNmRlNTY2Mi0wMDMwLTQ4NTQtOGYzZi1iNzIzYjViMzE3NTgiLCJzdWIiOiI1ZjM4OWI4Mi0yOTE0LTQ4MmItOTdhOC03MzI4NGM1ODczOGUiLCJuYmYiOjE3OTM0NTUzNjgsImV4cCI6MTc5MzU0MTc2OCwiYXVkIjoiYmlyZC5zZXJ2aWNlcyIsImlzcyI6ImJpcmQuYXV0aCIsImlhdCI6MTc5MzQ1NTM2OCwicm9sZXMiOlsiVVNFUiJdLCJhcHAiOiI3YjhlZDk1NS02ZTNhLTRlZWMtYmEyMC04OGFmOWQ3YWVhNzYiLCJ2ZXIiOiIwLjAuMiJ9.b4yDzAz9hiNbLNwDCaLdOqT1HdmmPKXL1miwZ-pqUfTW4vDehJYfZvSwC24Ldxk8vzl9Wa4PDIqhdDbsBLdqp7CzBoJ4AoGZMVcRzlU8gLa_djvtJsGQV1AVtQiqol1fG1NNqkku1SSL1__VuTmkIRAN4uCDa9FvvISRoTmeq20mwQzBJNBkrB94jgHdQzus68X2SenzfzlnxhHdL4fxiXPB26Gj9usne1m-zexmc2b6U0fvhgG71-ScCDTKRWFFRo6Wj0SNG1zGaBGovq4MmmjS7uztgVMQhMGhYXAfZCCC6OVPy8NP0hXeF30fjSpxK7lSLQ6rTlxdBoTmCRfZYCn3R7TF7xQeR5j4_C-TPT0PyGqp6HillHDtuPARezC_zGrg0v4bnT9qczWD9QVyD_nBc3q6EEuAZvX0CeEKQrnWZR9anLF-8cKibVadlfS4qrr5WIgCv1u1LpCsWHYjUBsy8X07tnIdMZunpkl_8b_NtJ_azKr3u9vGSkbSxYNp26tXGN-MrslypZmorBtChq7-y0-aY0J5CcQsv_RXCQqLEPIM42F83X0W3iWp48N4hN6WONXW-yg56AumRAhgyll8Yg-Omo7ZqHUUDkVcYY5e85K9hzMnu_H2iYcLrpg_Bg1bCyQGgfL4QZn7P3tNsaJNApg4ULDFaUfyNgMMGAU"
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
        # POST to /nest/parking-nests-by-cell with i think this payload
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