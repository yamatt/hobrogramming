import urllib2 
import json

SEARCH_STRING = "http://api.geonames.org/searchJSON?q={0}&username=yamatt&countryBias=UK"

def convert_city_to_latlon(query):
    url = SEARCH_STRING.format(query.replace(" ", "%20"))
    r = urllib2.urlopen(url)
    j = json.load(r)
    try:
        return j['geonames'][0]['lat'], j['geonames'][0]['lng']
    except IndexError:
        print j
        return None, None
