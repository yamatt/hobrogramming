# Hobrogrammer
Hobrogrammer is a web-app that allows users to search for events with free food in their local area.

# Setup
## Requirements
* Flask
* SQLAlchemy
* BeautifulSoup4

## Running
Copy the file `settings.private.default` to `settings.private` and edit the contents using Python format like so:
* `SECRET_KEY`: any random string to salt cookies and for form validation
* `EVENTBRITE_API_KEY`: Apply to [EventBrite for an API key](https://www.eventbrite.com/api/key/) and put it in here

Hobrogrammer will work on any WSGI enabled server but if you want to run a local instance go to `wsgi` and run `run.py`.

# API
We make use of:
* [GeoNames](http://www.geonames.org/): to do convertion of location to latitude and longitude
* [EventBrite](http://developer.eventbrite.com/doc/): to check for events in your area (within 10 miles)

# Technology
* Hobrogrammer is designed to work on OpenShift (it's free for 3 instances)
* Flask is used to dispatch the pages and handle the API calls
* SQLAlchemy is used for caching  the results from what events have free food.
* BeautifulSoup4 is used to process the results from EventBrite to determine if it has free food.
* HTML5
* jQuery to do the dynamic searching
* Backbone/Underscore used to dynamically generate results

# License
## Code
GPLv3 (see LICENSE)

## Logo
Taken from [OpenClipart](http://openclipart.org/detail/8302/baseball-cap-by-gerald_g-8302) unsure about license but assumed to allow remixes.

# Contact
* [Matt Copperwaite](http://twitter.com/mattcopp)
* [Moggers87](http://twitter.com/moggers87)

# Thanks To
* All organisers and attendees of [Hacked.IO](http://hacked.io)
