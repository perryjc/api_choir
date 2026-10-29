import sys
import json
import requests
import geopy
from geopy.geocoders import Nominatim

# Sidetrack script that tests a post request i saw in chucker to /user/update

# default cords
# latitude = 38.8845454
# longitude = -77.122171
address = input("Enter a zip code In the US or address (or 'enter' to input lat/lon manually): ")
if address:
    geolocator = Nominatim(user_agent="bird_api_choir")
    location = geolocator.geocode(address + ", USA")
    latitude = location.latitude
    longitude = location.longitude
else:
    latitude = input("Enter latitude (or hit `enter` to use default): ") or 38.8845454
    longitude = input("Enter longitude (or hit `enter` to use default): ") or -77.122171

print(latitude, longitude)
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
    "Authorization": "Bearer eyJhbGciOiJSUzUxMiJ9.eyJqdGkiOiI0YTc1ODcyMi0wYTJiLTQyNjMtOTM5Ni02ZmFiMjIzMTIxMjIiLCJzdWIiOiI1ZjM4OWI4Mi0yOTE0LTQ4MmItOTdhOC03MzI4NGM1ODczOGUiLCJuYmYiOjE3OTMwNDMxNzcsImV4cCI6MTc5MzEyOTU3NywiYXVkIjoiYmlyZC5zZXJ2aWNlcyIsImlzcyI6ImJpcmQuYXV0aCIsImlhdCI6MTc5MzA0MzE3Nywicm9sZXMiOlsiVVNFUiJdLCJhcHAiOiI3YjhlZDk1NS02ZTNhLTRlZWMtYmEyMC04OGFmOWQ3YWVhNzYiLCJ2ZXIiOiIwLjAuMiJ9.CjOXvHwXO6koBAt2dBvV_ckWccCrlg7kjXLjFHxh23Xf1wBTo9EUsnPZINk-pKNj04r_86RyQLtoYNJdwtrvOl75hitEd03hyGgC8zZjMK2kpJWeSEbQhT_W7SRuxlLHlEroCmXQjH6MWTa5mEHd6Eo3xseXCBjF3HFhr_RpE5JwJ5jp0YNsCSDhOJ6izt07qjzbdEgnXvOaKY7wFIhHSYvIROJ6Mr3z51wQOQr05JB440pNqdThtTXy8LdxDB5ABcV42PYXtgnE0-hEtzN4Hsp1vQplJhBskkD4mORXTrVjqBVL433t1lFOruq5JQEErZ3QIfRumUhOjm82nlEuqACBnwsQtMPe1oY8BqUVD8y-uiFzsQ7PBW-dcPJysT471bz1USkt3IWiveqaEjESn9TyU8nuPo1ecqALB9z4iukE8rjO4avsKFk2wcHpBnuev0Y3rAZt-wikK6KxLG_MUEsAdQC5J84ABdU7NJR0s1jNzeljThVzvF_1Td8XAKxZQjJyhKJXVYchzaNAwGK_9EbjY6bz17IcTJZAtiLWAv2o2dtYVlCtbvOZSVC8HL7gCUxvxOw5Z1Ov9lAdmgg6K7yFgEC0_8BPx8Ujvy5quwZGe-fyFfGjf2Ap7l_CXHwoDFxilpRWhPy-ZdidinGH9FrzW1EH0PhesqvGQZoseFg"
}

user_payload = {
    # default/observed payload
    # "locale": "en-US"
    "locale": "en-tt"
    # this changes the default value from en-US to en-TT
    # this endpoint has many other notible feilds like "admin", "contractor", ect that are set to false by default
    # this suggests BOLA and possible priv esculation.
    # need to test further
}

url = "https://api-bird.prod.birdapp.com/user/update"
response = requests.put(url, headers=headers, json=user_payload)
data = response.json()

print(json.dumps(data, indent=4))