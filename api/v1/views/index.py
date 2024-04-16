#!/usr/bin/python3
"""Script that will create a route
that returns the status of the API"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", strict_slashes=False)
def status():
    """Method that returns the status of the API"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats():
    """Method that retrieves the number of each objects by type
    ex: {
        "amenities": 3,
        "cities": 4,
        "places": 7,
        "reviews": 6,
        "states": 27,
        "users": 15
    }
    """
    from models.amenity import Amenity
    from models.city import City
    from models.place import Place
    from models.review import Review
    from models.state import State
    from models.user import User
    from models import storage
    import json
    dico = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    json_dict = json.dumps(dico, indent=2)
    return json_dict
