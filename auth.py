import datetime
import requests
import json
import sys

ct = datetime.datetime.now()
timestamp = ct.strftime("%Y-%m-%d")

email = input("Enter email (must be associated with an existing Bird account): ")
latitude = 38.8820057
longitude = -77.1115141
# default cords are for Ballston MU metro station

send_auth_email_url = "https://api-auth.prod.birdapp.com/api/v1/auth/email"
verify_email_url = "https://api-auth.prod.birdapp.com/api/v1/auth/magic-link/use"

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
    "Role": "operator"
}

send_auth_email_payload = {
  "email": email
}

response = requests.post(send_auth_email_url, headers=headers, json=send_auth_email_payload)

if(response.json() == {'validation_required': True}):
    print("Check your email for `Magic Link` email and copy the token under the 'verify' button.")
    print("do NOT click the 'verify' button")
    # strips spaces from the token input
    token = input("Paste the token: ").strip()
else:
    print("Error: ", response.json())
    sys.exit()

verify_email_payload = {
  "token": token,
  "email": email
}

auth_token_response = requests.post(verify_email_url, headers=headers, json=verify_email_payload)

auth_token_raw = auth_token_response.json()

AUTH_TOKEN = auth_token_raw["access"]

# write to authfile
authfile_dict = {}

authfile_dict["timestamp"] = timestamp
authfile_dict["email"] = email
authfile_dict["auth_token"] = "Bearer " + AUTH_TOKEN

newfile = open("auth_info_file.txt", "a")

# writes to file as a json object for easy parsing
with open("auth_info_file.txt", "w") as authfile:
    authfile.write(json.dumps(authfile_dict))

print("Auth token generated successfully. try running main.py now.")