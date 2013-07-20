import imp
PRIVATE = imp.load_source("settings", "settings.private")

DEBUG = True
HOST = "0.0.0.0"
PORT = 5000

SECRET_KEY = PRIVATE.SECRET_KEY
EVENTBRITE_API_KEY = PRIVATE.EVENTBRITE_API_KEY
