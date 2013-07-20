from bs4 import BeautifulSoup
from urllib2 import urlopen

def find_food(data):
    """
    Give me a file like object or a URL, returns True or False based on if it finds
    food
    """

    if type(data) == str or type(data) == unicode:
        data = urlopen(data)
    soup = BeautifulSoup(data)

    for p in soup.findAll('p'):
        if "food" in str(p) or "Food" in str(p):
            return True

    return False

def give_food(events):
    """Go through a list of events and return the ones that have food"""

    output = []

    for event in events:
        if find_food(event.url):
            output.append(event)

    return output
