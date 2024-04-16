#!/usr/bin/python3
"""Script for the places view"""
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def get_all_places(city_id):
    """Method that retrieves the list of all Place objects"""
    cty = storage.get(City, city_id)
    if not cty:
        abort(404)
    places = cty.places
    places_list = []
    for place in places:
        places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Method that retrieves a Place object with a specific id"""
    plce = storage.get(Place, place_id)
    if not plce:
        abort(404)
    return jsonify(plce.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """Method that deletes a Place object with a specific id"""
    plce = storage.get(Place, place_id)
    if not plce:
        abort(404)
    storage.delete(plce)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places",
                 methods=["POST"], strict_slashes=False)
def new_place(city_id):
    """Method that creates a Place object"""
    plce_data = request.get_json()
    if not plce_data:
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if "user_id" not in plce_data.keys():
        abort(400, "Missing user_id")
    user = storage.get(User, plce_data.get("user_id"))
    if not user:
        abort(404)
    if "name" not in plce_data.keys():
        abort(400, "Missing name")

    plce_data["city_id"] = city_id
    place = Place(**plce_data)
    return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def change_place(place_id):
    """Method that updates a Place object with a specific id"""
    plce_data = request.get_json()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    elif not plce_data:
        abort(400, "Not a JSON")

    for key, value in plce_data.items():
        if key not in ["id", "state_id", "city_id",
                       "created_at", "updated_at"]:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
