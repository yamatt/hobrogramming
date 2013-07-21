
from flask import Blueprint, abort, g, session, jsonify, request, redirect, url_for, flash, current_app
from models.eventbrite import Hacks
from models.geonames import convert_city_to_latlon
import json

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
        for event in events:
            db_event = g.database.get_event(event.id)
            if db_event:
                event.food = db_event.has_food
            else:
                food = event.determine_food()
                event.food = food
                g.database.set_food(event.id, food)
                
        return jsonify({
            'events': map(lambda event: event.to_json(), events)
        })
        
    return jsonify({'success': False, 'message': "Need lat/lon as query string."})

@api.route("/update/<id>", methods=["POST", "PUT"])
def update_event(id):
    response = request.data
    j = json.loads(response)
    g.database.update_food(id, j['food'])
    return jsonify({'success': True})
