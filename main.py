import requests
import json
import sys
import geopy
from geopy.geocoders import Nominatim

# TODO:
# allow user spesify lat/lon
# integrate cordintate module (to get user location)

address = input("Enter a zip code In the US or address (or 'enter' to input lat/lon manually): ")
if address:
    geolocator = Nominatim(user_agent="bird_api_choir")
    location = geolocator.geocode(address + ", USA")
    latitude = location.latitude
    longitude = location.longitude
else:
    latitude = input("Enter latitude (or hit `enter` to use default): ") or 38.8845454
    longitude = input("Enter longitude (or hit `enter` to use default): ") or -77.122171

print("target cords: ",latitude, longitude)

chirp_type = input("DEBUG: enable alarm (y/n): ")
if chirp_type.lower() == "y" or chirp_type.lower() == "yes":
    alarm = True
    print("alarm enabled")
else:
    alarm = False

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
    "Authorization": "Bearer eyJhbGciOiJSUzUxMiJ9.eyJqdGkiOiIwYWY4ODcwZC01MWI1LTQ4MDgtOWRlYy02NGViNWY0NDdjMzUiLCJzdWIiOiI1ZjM4OWI4Mi0yOTE0LTQ4MmItOTdhOC03MzI4NGM1ODczOGUiLCJuYmYiOjE3OTMxMjYyNTcsImV4cCI6MTc5MzIxMjY1NywiYXVkIjoiYmlyZC5zZXJ2aWNlcyIsImlzcyI6ImJpcmQuYXV0aCIsImlhdCI6MTc5MzEyNjI1Nywicm9sZXMiOlsiVVNFUiJdLCJhcHAiOiI3YjhlZDk1NS02ZTNhLTRlZWMtYmEyMC04OGFmOWQ3YWVhNzYiLCJ2ZXIiOiIwLjAuMiJ9.bztzkksgcMgHzAQoiDdGBEHtLBRwmc4PW1JZFjJuiZcjPAkeTZkPgzx9Xujjbcvl-w15PFtlhIHh5d39tmslVqH2IhqwlHqtkhp_rSr4L7_mp1CWpDVbHbRr595FBzayK3A0eUs1w2EPUQcYOIRaaZ9eKoxvDz_tlIRd05h1vwGXRPkTKEdYODYHHps5N5FtAqub7Dh5pYJEFTBF141G2jq15oBeG02PSM7wfmmuUsf-wMhP_tcYXzKjoZUBmqmJ7MPqNbUiywuz7nRXrsMtpCATWCjYG-onR5AWjyuEdzOCHJH_sdrI81USzfYD0AqErOdr_-B06ksAHQVpNFH2f_FMdXcwcMoU4QsHUvYl_KB_xXjM2j-roFyP_uPxwPUzhLkAZt3mYv9u8mAHU0GXJQqPIRM1VQlzfsXZ5Tcp-f8dmbRzOvMPop6jwSn0Y-574QJqJf7T_a87zunkCgMR9mL6p7TTo8VJmegXT27p3IPAzPCkp9aqOpVfhK-Dxbk3e6uCi8Nf-4YedYZpqD-cBlP6MP8zwkr4b9gIQDnk1dGAVzRvGMqpTbdoB8jT52UWzs5NgDSAC3KRKTqwujsINZ8MpxuxK5EYy7bxtWWCebOgfSoggyf6iJ4R36iSykxDi2Pt9zQp4n-PAhyDwHijv8YvfJD882txmCH8QddIJQE"
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
user_url = base_url + "/user"

check_connection("https://bird.co/")
verify_headers(user_url, headers)

print("Starting chirp requests...")
response = requests.post(nearby_url, headers=headers, json=nearby_payload)

nearby_data = response.json()

bird_ids = [bird["id"] for bird in nearby_data["birds"]]

for x in range(len(bird_ids)):
    chirp_payload = {
        "alarm": alarm,
        "bird_id": bird_ids[x]
    }
    chirp_response = requests.put(chirp_url, headers=headers, json=chirp_payload)
    chirp_data = chirp_response.json()
    if(not chirp_data["down"]):
        print("Success")
    else:
        print("Failed")
