# Using Python requests and the Google Maps Geocoding API.
#
# References:
#
# * http://docs.python-requests.org/en/latest/
# * https://developers.google.com/maps/

import requests

GOOGLE_MAPS_API_URL = 'https://maps.googleapis.com/maps/api/geocode/json'

params = {
    #'address': '221B Baker Street, London, United Kingdom',
    'address': 'wellington, new zealand',
    'sensor': 'false',
    #'region': 'uk',
    'key': 'AIzaSyAzbpDPFJ4xudZnqIsjLH3ltL9og-Sihsk',
}

# Do the request and get the response data
#my API key for all dem requests brah
#key_append = &key=
req = requests.get(GOOGLE_MAPS_API_URL, params=params)
res = req.json()

# Use the first result
#print (res)

result = res['results'][0]

geodata = dict()
geodata['lat'] = result['geometry']['location']['lat']
geodata['lng'] = result['geometry']['location']['lng']
geodata['address'] = result['formatted_address']

print(geodata["lat"])
print('{address}. (lat, lng) = ({lat}, {lng})'.format(**geodata))
# 221B Baker Street, London, Greater London NW1 6XE, UK. (lat, lng) = (51.5237038, -0.1585531)
