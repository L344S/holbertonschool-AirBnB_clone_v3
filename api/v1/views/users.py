#!/usr/bin/python3
"""Script for the users view"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """Method that retrieves the list of all User objects"""
    usrs = storage.all(User).values()
    users_list = []
    for user in usrs:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """Method that retrieves a User object with a specific id"""
    usr = storage.get(User, user_id)
    if not usr:
        abort(404)
    return jsonify(usr.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """Method that deletes a User object with a specific id"""
    usr = storage.get(User, user_id)
    if not usr:
        abort(404)
    storage.delete(usr)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def new_user():
    """Method that creates a User object"""
    usr_data = request.get_json()
    if not usr_data:
        abort(400, "Not a JSON")
    elif "email" not in usr_data:
        abort(400, "Missing email")
    elif "password" not in usr_data:
        abort(400, "Missing password")
    new_user = User(**usr_data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def change_user(user_id):
    """Method that updates a User object with a specific id"""
    usr_data = request.get_json()
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    elif not usr_data:
        abort(400, "Not a JSON")
    for key, value in usr_data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
