#!/usr/bin/python3
"""Script for the cities view"""
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, abort, request


@app_views.route("/states/<state_id>/cities",
                 methods=["GET"], strict_slashes=False)
def get_all_cities(state_id):
    """Method that retrieves the list of all City objects"""
    st = storage.get(State, state_id)
    if not st:
        abort(404)
    cities = st.cities
    cities_list = []
    for city in cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """Method that retrieves a City object with a specific id"""
    ct = storage.get(City, city_id)
    if not ct:
        abort(404)
    return jsonify(ct.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """Method that deletes a City object with a specific id"""
    ct = storage.get(City, city_id)
    if not ct:
        abort(404)
    storage.delete(ct)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states/<state_id>/cities",
                 methods=["POST"], strict_slashes=False)
def new_city(state_id):
    """Method that creates a City object"""
    ct_data = request.get_json()
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    elif not ct_data:
        abort(400, "Not a JSON")
    elif "name" not in ct_data:
        abort(400, "Missing name")

    ct_data["state_id"] = state_id
    new_city = City(**ct_data)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def change_city(city_id):
    """Method that updates a City object with a specific id"""
    ct_data = request.get_json()
    ct = storage.get(City, city_id)
    if not ct:
        abort(404)
    elif not ct_data:
        abort(400, "Not a JSON")

    for key, value in ct_data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(ct, key, value)
    storage.save()
    return jsonify(ct.to_dict()), 200
