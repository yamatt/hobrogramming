from urllib2 import urlopen
from urllib import urlencode
import json

class Hacks(object):
    SEARCH_URL = "https://www.eventbrite.com/json/event_search?app_key={0}&keywords={1}&date=This+month{2}"
    SEARCH_STRINGS = ["hack", "code"]
    def __init__(self, pass_key):
        self.pass_key = pass_key
        
    def generate_url(self, url, keywords, extra_values={}):
        keywords = "%20OR%20" .join(keywords)
        if extra_values:
            qs = "&" + urlencode(extra_values)
        else:
            qs = ""
            
        return url.format(self.pass_key, keywords, qs)

    def get_hacks_for_location(self, lat, lon):
        url = self.generate_url(self.SEARCH_URL, self.SEARCH_STRINGS, {'latitude': lat, 'longitude': lon})
        r = urlopen(url)
        j = json.load(r)
        events = map(lambda event: Event.from_dict(event), j['events'])
        return events
        
class Event(object):
    EVENT_URL = "https://www.eventbrite.com/json/event_get?id={0}"
    @classmethod
    def from_dict(cls, event):
        event = event['event']
        return cls(
            id=event['id'],
            title=event['title'],
            status=event['status'],
            description=event['description'],
            start_date=datetime.strptime(event['start_time'], "%Y-%m-%d %H:%M:%S"),
            end_date=datetime.strptime(event['end_time'], "%Y-%m-%d %H:%M:%S"),
            url=event['url'],
            venue=Venue.from_dict(event['venue']),
            tickets=map(lambda ticket: Ticket.from_dict(ticket), event['tickets'])
        )
        
    @classmethod
    def from_id(cls, id):
        url = self.EVENT_URL.format(id)
        r = urlopen(url)
        j = json.load(r)
        return cls.from_dict(j)
    
    def __init__(self, id, title, status, description, start_date, end_date, url, venue, tickets):
        self.id = id
        self.title = title
        self.status = status
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.url = url
        self.venue = venue
        self.tickets = tickets
        
    def get_url(self):
        pass
    
    def get_site(self):
        pass
        
    def determine_food(self):
        pass
        
class Ticket(object):
    @classmethod
    def from_dict(cls, ticket):
        ticket = ticket['ticket']
        return cls(
            id=ticket['id'],
            name=ticket['name'],
            min=ticket['min'],
            max=ticket['max'],
            price=float(ticket['price']),
            currency=ticket['currency']
        )
        
    def __init__(self, id, name, min, max, price, currency):
        self.id = id
        self.name = name
        self.min = min
        self.max = max
        self.price = price
        self.currency = currency
        
    def is_free(self):
        if self.price == 0.0:
            return True
        return False
        
class Venue(object):
    @classmethod
    def from_dict(self, venue):
        return cls(
            id=venue['id'],
            lon=venue['longitude'],
            lat=venue['latitude'],
            country_code=venue['GB'],
            city=venue['city'],
        )
        
    def __init__(self, id, lon, lat, country_code, city):
        self.id = id
        self.lon = lon
        self.lat = lat
        self.country_code = country_code
        self.city = city
