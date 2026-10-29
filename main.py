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
    "Authorization": "Bearer eyJhbGciOiJSUzUxMiJ9.eyJqdGkiOiI5MGZiMjQ3Zi1jMDBiLTQ1NjMtODBmNC1jNzMzOWVmZWExNjciLCJzdWIiOiI1ZjM4OWI4Mi0yOTE0LTQ4MmItOTdhOC03MzI4NGM1ODczOGUiLCJuYmYiOjE3OTMyODQ2MDAsImV4cCI6MTc5MzM3MTAwMCwiYXVkIjoiYmlyZC5zZXJ2aWNlcyIsImlzcyI6ImJpcmQuYXV0aCIsImlhdCI6MTc5MzI4NDYwMCwicm9sZXMiOlsiVVNFUiJdLCJhcHAiOiI3YjhlZDk1NS02ZTNhLTRlZWMtYmEyMC04OGFmOWQ3YWVhNzYiLCJ2ZXIiOiIwLjAuMiJ9.EsZKMo530g-1FeGuuOXHh0yfEDuxom0MN9cd5-_6YEcMvmmc_IH-2fvHdZPOHY0AXiZQW9mOIm7bZk_cHeysL70x-vcqhxgyyEsasAaRJY9AdavZ0ThImi1fMsy4sUqy4orKrdJLd5bcIzG7hd5BVk9vw2NUPIU3S00IGmyCkzEmEVl63VNOyPhZklpClWP7r3wRfi6GNCQMi7zAqAkkr_fmzH_n6MikFw3cEU0uaXcVdSREalpDx-T3ck21g6gkHqaiyzR1wldSNcaCZkl1O0u5xQCiyjGBp37uOfqdrLGbli6ZE8T63Pzl1_qygAqf75kO96eyIaebQJczsbMLzkYEjn6YVnY61MZDvTsbAnUyMYxRJxz7jCJObwyd3Z0BnAYhgcaR53ao_Pc77-exOeWOTRKS-fPze0WrjW80xooQiTA899is-AnYa2FnIa2WB4l01pwELSBBEB59b1W4wNiyAxFUBSodk5efgsLGlVU68iSIqib76QFgyAHT-VKW0ME7CC8aHA3txZlgoa3F2unPl_OzlG-GfEHm5UadbWEb6MhJkfqndKhdHhQhj8jKZOaz1TGSsUPnjIJ6RTiMLIwF6-dSnsZtcpGG99yeb7BbKaWz58mNT-jQjLUmGWES9QlmVR5p8EkNROzQcMpMw-thtb1d04jzjWvbPeWRzP4"
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
        "-8523145651523944448",
        "-8523145514084990976",
        "-8523142902744875008",
        "-8523142851205267456",
        "-8523142885565005824"
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
    if(not chirp_data["down"]):
        print("Success")
    else:
        print("Failed")
