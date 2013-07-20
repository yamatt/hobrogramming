from bs4 import BeautifulSoup
from urllib2 import urlopen

def find_food(data):
    """Give me a file like object or a URL"""
    if type(data) == str or type(data) == unicode:
        data = urlopen(data)
    soup = BeautifulSoup(data)

    for p in soup.findAll('p'):
        if "food" in str(p) or "Food" in str(p):
            return True

    return False
