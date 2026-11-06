# api_choir

## NEED TO ADD DISCRIPTION AND INSTRUCTIONS

## TODO:
- [x] allow user specify lat/lon
- [x] allow user specify location/zipcode
- [x] add debug feture that switches bettween `"alarm": False` and `"alarm": True`
- [x] order scooters by how close they are to the user (i.e: chirp the closest scooter first) ***
- [x] ignore every scooter with "battery_level": 0 (i have no clue but nearby_data has no dead ones)
- [x] make output look more pretty when interupted
- [ ] allow user to specify how many scooters to try (1, 5, 10, all, ect)
- [x] cell_ids is dynamic, have script make an enpoint request to get cell_ids
- [ ] identify responce codes (check for ratelimit or invalid prams)
- [ ] add more debug logs
- [ ] add utils.py file with helper functions
- [x] add ascii art when script is ran
- [ ] display options user selected and then ask "do you want to continue?"
- [ ] split diffrent steps of the script into seprate files
- [x] color "success" and "failure" messages
- [ ] the bird app does a POST to `/user/session-start` every time the app is open, implement this (header check)
- [x] make `verify_headers` parse responce insted of just checking if server responds
- [ ] add script breakdown/walkthrough
- [ ] talk about apk mods that enable chucker among other things
- [ ] make output ... (i forgot)
- [x] make output show the 5 character code of each chirped scooter
- [ ] try to cut down nonrequired headers (clean up)
- [ ] limit api chirp requests only to scooters within 0.5 miles of user.
- [ ] talk about how bird has the issue of allowing users to chirp scooters from anywhere
- [ ] integrate other scooter brands (lime, hop, ect)
- [ ] integrate esp32 tracker/opensorce airtag (to get dynamic user location)

- [x] add function that takes user email and makes auth token, insted of mine (POST to "/api/v1/auth/email")
    - [x] check if theres an existing auth token file. 
    - [x] if there isnt, prompt user to use "auth.py" and exit script
    - [x] open and assign values to veribles 
    - [x] otherwise check if "auth timestamp" is more then 24 hours old (end script if it is)
    - [x] put "auth token" into a veriable
    - [x] run script normally
- [x] add "auth.py" script that creates an auth token from users email
    - [x] prompt user for email 
    - [x] send POST to /api/v1/auth/email (with email as payload)
    - [x] if returns `"validation_required": true` tell user to check email
    - [x] prompt user to copy "magic link token" from email
    - [x] have the token prompt strip spaces/junk
    - [x] send POST to /api/v1/auth/magic-link/use (with email and magic token as payload)
    - [x] api will return "access" and "refresh" tokens, place "access" into a veriable
    - [x] create a object with: auth timestamp, and auth token
    - [x] create "auth_info_file.txt" (placeholder name) and remove old ones if they exist
    - [x] write auth object to file and save
    - [x] prompt user to try main script again

## POC Video:

[![POC Video](https://img.youtube.com/vi/Tuyi8vloYf4/0.jpg)](https://youtube.com/shorts/Tuyi8vloYf4)

## Required librarys
- geopy
- rich

## Resorces
- https://github.com/ubahnverleih/WoBike/tree/master (unoffical bird api docs)
- https://github.com/api-evangelist/bird-rides/tree/main (independent third-party profile of bird api profile)
- https://www.geeksforgeeks.org/python/python-sort-python-dictionaries-by-key-or-value/ (sorting is wild)
- https://github.com/aarsaputra/php2shell/blob/main/lib/banner.py (banner/ascii inspo and example)
- https://www.instagram.com/dayofexploits/ (more CLI tool design references and inspiration)
- https://colordesigner.io/gradient-generator (Gradent generator)