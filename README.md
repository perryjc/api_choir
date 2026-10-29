# api_choir

## TODO:
- [x] allow user specify lat/lon
- [x] allow user specify location/zipcode
- [x] add debug feture that switches bettween `"alarm": False` and `"alarm": True`
- [x] order scooters by how close they are to the user (i.e: chirp the closest scooter first) ***
- [x] ignore every scooter with "battery_level": 0 (i have no clue but nearby_data has no dead ones)
- [ ] make output look more pretty when interupted
- [ ] identify responce codes (check for ratelimit or invalid prams)
- [ ] split diffrent steps of the script into seprate files
- [ ] color "success" and "failure" messages
- [ ] the bird app does a POST to `/user/session-start` every time the app is open, implement this (header check)
- [x] make `verify_headers` parse responce insted of just checking if server responds
- [ ] add script breakdown/walkthrough
- [ ] talk about apk mods that enable chucker among other things
- [ ] make output ... (i forgot)
- [ ] make output show the 5 character code of each chirped scooter
- [ ] add function that takes user email and makes auth token, insted of mine (POST to "/api/v1/auth/email")
- [ ] try to cut down nonrequired headers (clean up)
- [ ] integrate esp32 tracker/opensorce airtag (to get dynamic user location)

## Required librarys
- geopy

## Resorces
- https://github.com/ubahnverleih/WoBike/tree/master (unoffical bird api docs)
- https://github.com/api-evangelist/bird-rides/tree/main (independent third-party profile of bird api profile)
- https://www.geeksforgeeks.org/python/python-sort-python-dictionaries-by-key-or-value/ (sorting is wild)