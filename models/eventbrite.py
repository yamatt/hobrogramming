from urllib2 import urlopen
from urllib import urlencode
import json
from datetime import datetime

class Base(object):
    def to_json(self):
        d = self.__dict__
        results = {}
        for k,v in d.items():
            if isinstance(v, datetime):
                d[k] = v.isoformat()
            if isinstance(v, list):
                d[k] = map(lambda i: i.to_json(), v)
            elif hasattr(v, 'to_json'):
                    results[k] = v.to_json()
            else:
                results[k] = v
                
        return results

class Hacks(Base):
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
        events = map(lambda event: Event.from_dict(event), j['events'][1:])
        return events
        
class Event(Base):
    EVENT_URL = "https://www.eventbrite.com/json/event_get?app_key={0}&id={1}"
    @classmethod
    def from_dict(cls, event):
        try:
            event = event['event']
        except KeyError:
           return None
        return cls(
            id=event['id'],
            title=event['title'],
            status=event['status'],
            description=event['description'],
            start_date=datetime.strptime(event['start_date'], "%Y-%m-%d %H:%M:%S"),
            end_date=datetime.strptime(event['end_date'], "%Y-%m-%d %H:%M:%S"),
            url=event['url'],
            venue=Venue.from_dict(event.get('venue', {})),
            organizer=Organizer.from_dict(event.get('organizer', {})),
            tickets=map(lambda ticket: Ticket.from_dict(ticket), event['tickets']),
            food=None,
            check=True
        )
        
    @classmethod
    def from_id(cls, app_key, id):
        url = Event.EVENT_URL.format(app_key, id)
        r = urlopen(url)
        j = json.load(r)
        return cls.from_dict(j)
    
    def __init__(self, id, title, status, description, start_date, end_date, url, venue, organizer, tickets, food, check=True):
        self.id = id
        self.title = title
        self.status = status
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.url = url
        self.venue = venue
        self.organizer = organizer
        self.tickets = tickets
        self.food = food
        self.check = check
        
    def to_dict(self):
        return self.__dict__
        
    def get_url(self):
        pass
    
    def get_site(self):
        pass
        
    def determine_food(self):
        if check:
            pass
        else:
            return self.food
        
class Ticket(Base):
    @classmethod
    def from_dict(cls, ticket):
        ticket = ticket['ticket']
        if 'price' not in ticket:
            ticket['price'] = 0.0
        try:
            return cls(
                id=ticket['id'],
                name=ticket['name'],
                min=ticket['min'],
                max=ticket['max'],
                price=float(ticket['price']),
                currency=ticket['currency']
            )
        except KeyError:
            return None
        
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
        
class Venue(Base):
    @classmethod
    def from_dict(cls, venue):
        try:
            return cls(
                id=venue['id'],
                lon=venue['longitude'],
                lat=venue['latitude'],
                address={
                    'street': venue.get('address', ''),
                    'city': venue.get('city', ''),
                    'country': venue.get('country_code', ''),
                    'postcode': venue.get('postcode', '')
                    }
            )
        except KeyError:
            return None
        
    def __init__(self, id, lon, lat, address):
        self.id = id
        self.lon = lon
        self.lat = lat
        self.address = address

class Organizer(Base):
    @classmethod
    def from_dict(cls, organizer):
        try:
            return cls(
                id=organizer['id'],
                name=organizer['name'],
                description=organizer['description'],
                url=organizer['url']
            )
        except KeyError:
            return None

    def __init__(self, id, name, description, url):
        self.id = id
        self.name = name
        self.description = description
        self.url = url
