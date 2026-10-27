import requests
import json
import sys

# TODO:
# allow user spesify lat/lon
# integrate cordintate module (to get user location)

location_data = {
    "latitude": 38.8845454,
    "longitude": -77.122171,
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
    "Authorization": "Bearer eyJhbGciOiJSUzUxMiJ9.eyJqdGkiOiI0YTc1ODcyMi0wYTJiLTQyNjMtOTM5Ni02ZmFiMjIzMTIxMjIiLCJzdWIiOiI1ZjM4OWI4Mi0yOTE0LTQ4MmItOTdhOC03MzI4NGM1ODczOGUiLCJuYmYiOjE3OTMwNDMxNzcsImV4cCI6MTc5MzEyOTU3NywiYXVkIjoiYmlyZC5zZXJ2aWNlcyIsImlzcyI6ImJpcmQuYXV0aCIsImlhdCI6MTc5MzA0MzE3Nywicm9sZXMiOlsiVVNFUiJdLCJhcHAiOiI3YjhlZDk1NS02ZTNhLTRlZWMtYmEyMC04OGFmOWQ3YWVhNzYiLCJ2ZXIiOiIwLjAuMiJ9.CjOXvHwXO6koBAt2dBvV_ckWccCrlg7kjXLjFHxh23Xf1wBTo9EUsnPZINk-pKNj04r_86RyQLtoYNJdwtrvOl75hitEd03hyGgC8zZjMK2kpJWeSEbQhT_W7SRuxlLHlEroCmXQjH6MWTa5mEHd6Eo3xseXCBjF3HFhr_RpE5JwJ5jp0YNsCSDhOJ6izt07qjzbdEgnXvOaKY7wFIhHSYvIROJ6Mr3z51wQOQr05JB440pNqdThtTXy8LdxDB5ABcV42PYXtgnE0-hEtzN4Hsp1vQplJhBskkD4mORXTrVjqBVL433t1lFOruq5JQEErZ3QIfRumUhOjm82nlEuqACBnwsQtMPe1oY8BqUVD8y-uiFzsQ7PBW-dcPJysT471bz1USkt3IWiveqaEjESn9TyU8nuPo1ecqALB9z4iukE8rjO4avsKFk2wcHpBnuev0Y3rAZt-wikK6KxLG_MUEsAdQC5J84ABdU7NJR0s1jNzeljThVzvF_1Td8XAKxZQjJyhKJXVYchzaNAwGK_9EbjY6bz17IcTJZAtiLWAv2o2dtYVlCtbvOZSVC8HL7gCUxvxOw5Z1Ov9lAdmgg6K7yFgEC0_8BPx8Ujvy5quwZGe-fyFfGjf2Ap7l_CXHwoDFxilpRWhPy-ZdidinGH9FrzW1EH0PhesqvGQZoseFg"
}

nearby_payload = {
    "map_center": {
        "latitude": 38.88454525398748,
        "longitude": -77.12217086926103,
        "mocked": "false",
        "timestamp": "1969-12-31T19:00:00.000-05:00",
        "source": ""
    },
    "cell_ids": [
        "-8523145651523944448",
        "-8523145514084990976"
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
    if response.status_code == 200:
        print("Headers are valid")
    else:
        print("Header verification failed with status code:", response.status_code)
        sys.exit()

base_url = "https://api-bird.prod.birdapp.com"
nearby_url = base_url + "/bird/nearby-by-cells"
chirp_url = base_url + "/bird/chirp"
config_url = base_url + "/config"

check_connection("https://bird.co/")
verify_headers(config_url, headers)

print("Starting chirp requests...")
response = requests.post(nearby_url, headers=headers, json=nearby_payload)

nearby_data = response.json()

bird_ids = [bird["id"] for bird in nearby_data["birds"]]

for x in range(len(bird_ids)):
    chirp_payload = {
        "bird_id": bird_ids[x],
        "alarm": True
    }
    chirp_response = requests.put(chirp_url, headers=headers, json=chirp_payload)
    chirp_data = chirp_response.json()
    if(not chirp_data["down"]):
        print("Success")
    else:
        print("Failed")
