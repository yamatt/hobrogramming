
from flask import Blueprint, abort, g, session, jsonify, request, redirect, url_for, flash, current_app
from models.eventbrite import Hacks
from models.geonames import convert_city_to_latlon

api = Blueprint('api', __name__)

@api.before_request
def setup_hacks():
    g.hacks = Hacks(current_app.config['EVENTBRITE_API_KEY']) # this will probably bite me in the arse

@api.route("/get", methods=["GET"])
def get_events():
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    location = request.args.get("location")
    if location:
        lat, lon = convert_city_to_latlon(location)
    if lat and lon:
        events = g.hacks.get_hacks_for_location(lat, lon)
        return jsonify({
            'events': map(lambda event: event.to_json(), events)
        })
        
    return jsonify({'success': False, 'message': "Need lat/lon as query string."})

@api.route("/update", methods=["POST", "PUT"])
def update_event():
    pass
