import requests
import json
import datetime
import os
import sys
import art
import rich
from rich import print
import geopy
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

base_url = "https://api-bird.prod.birdapp.com"
cells_url = base_url + "/map/rider-cells" # added
nearby_url = base_url + "/bird/nearby-by-cells"
chirp_url = base_url + "/bird/chirp"
user_url = base_url + "/user"

# render ASCII banner
art.render_banner()
print("")

ct = datetime.datetime.now()
timestamp = ct.strftime("%Y-%m-%d")

if os.path.isfile("auth_info_file.txt"):
    with open("auth_info_file.txt") as auth_file:
        auth_info = json.load(auth_file)
        email = auth_info["email"]
        auth_timestamp = auth_info["timestamp"]
        AUTH_TOKEN = auth_info["auth_token"]
else:
    print("[bold bright_red]ERROR: Auth file not found. run `auth.py` to verify your email and get a auth token[/bold bright_red]")
    sys.exit()

if auth_timestamp != timestamp:
    print("[bold bright_red]ERROR: Auth token is expired. re-run `auth.py`[/bold bright_red]")
    sys.exit()

print("email: ", email)

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
    print("[bright_cyan]alarm disabled[/bright_cyan]")
else:
    alarm = True
    print("[bright_cyan]alarm enabled[/bright_cyan]")

# first payload used to get the cell ids list from the endpoint: /map/rider-cells
get_cell_ids_payload = {
  "geometries": {
    "55353538521136": { #this might be a problom if its also dynamic like the cell ids. monitoring
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
    "Authorization": AUTH_TOKEN
}

# get cell ids from the /map/rider-cells endpoint (see dynamic_cellids_test.py for more details)
cell_response = requests.post(cells_url, headers=headers, json=get_cell_ids_payload)
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

def check_connection(url):
    print("[bold bright_yellow]Checking connection to API...[/bold bright_yellow]")
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        print("Connection active")
    else: 
        print("[bold bright_red]ERROR: Connection failed with status code: [/bold bright_red]", response.status_code)
        sys.exit()

def verify_headers(url, headers):
    print("[bold bright_yellow]Verifying headers...[/bold bright_yellow]")
    response = requests.get(url, headers=headers, timeout=5)
    server_responce = response.json()
    if "code" in server_responce:
        responce_code = server_responce["code"]
        print("[bold bright_red]Header verification failed with status code: [/bold bright_red]", responce_code)
        print("Is auth token valid?")
        sys.exit()
    else:
        print("Headers are valid")

check_connection("https://bird.co/")
verify_headers(user_url, headers)

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

art.print_user_selections(email, alarm, latitude, longitude, auth_timestamp)
print("\n[bold bright_yellow]Starting chirp requests...[/bold bright_yellow]")

# Exits script cleanly if user presses ctrl+c
try:
    for scooter_id, info in sorted_scooters.items():
        chirp_payload = {
            "alarm": alarm,
            "bird_id": scooter_id
        }
        chirp_response = requests.put(chirp_url, headers=headers, json=chirp_payload)
        chirp_data = chirp_response.json()
        scooter_code = info["code"]
        
        if not chirp_data["down"]:
            print(f"[bold bright_cyan]Bird [/bold bright_cyan]- [bold green]Success: {scooter_code}[/bold green]")
        else:
            print(f"[bold bright_cyan]Bird [/bold bright_cyan]- [bold red]Failed: {scooter_code}[/bold red]")
except KeyboardInterrupt:
    print("\nEXITING SCRIPT...")
    sys.exit()