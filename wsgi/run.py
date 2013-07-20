#!/usr/bin/env python2

from flask import Flask, g, request, session, flash, current_app
from apps.frontpage import frontpage
from apps.api import api

import settings

app = Flask(__name__)
app.config.from_object(settings)

#database = Interface()

#@app.before_request
#def setup_database():
    #if not hasattr(g, "database"):
        #g.database = database
    
app.register_blueprint(frontpage)
app.register_blueprint(api, url_prefix="/api")

if __name__ == "__main__":
    app.run()
