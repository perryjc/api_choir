import requests
import json
import sys
import os
import geopy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic


latitude = 38.8820057
longitude = -77.1115141

if os.path.isfile("auth_info_file.txt"):
    with open("auth_info_file.txt") as auth_file:
        auth_info = json.load(auth_file)
        email = auth_info["email"]
        timestamp = auth_info["timestamp"]
        AUTH_TOKEN = auth_info["auth_token"]
else:
    print("Auth file not found. run `auth.py` to verify your email and get a auth token")
    sys.exit()

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
    "Authorization": AUTH_TOKEN
}

print(headers)