#!/usr/bin/python3
"""Script for the places_reviews view"""
from models import storage
from models.place import Place
from models.review import Review
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/places/<place_id>/reviews",
                 methods=["GET"], strict_slashes=False)
def get_all_reviews(place_id):
    """Method that retrieves the list of all Review objects"""
    plce = storage.get(Place, place_id)
    if not plce:
        abort(404)
    reviews = plce.reviews
    reviews_list = []
    for review in reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_reviews(review_id):
    """Method that retrieves a Review object with a specific id"""
    reviou = storage.get(Review, review_id)
    if not reviou:
        abort(404)
    return jsonify(reviou.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """Method that deletes a Review object with a specific id"""
    reviou = storage.get(Review, review_id)
    if not reviou:
        abort(404)
    storage.delete(reviou)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews",
                 methods=["POST"], strict_slashes=False)
def new_review(place_id):
    """Method that creates a Review object"""
    reviou_data = request.get_json()
    if not reviou_data:
        abort(400, 'Not a JSON')
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if "user_id" not in reviou_data.keys():
        abort(400, "Missing user_id")
    user = storage.get(User, reviou_data.get("user_id"))
    if not user:
        abort(404)
    if "text" not in reviou_data.keys():
        abort(400, "Missing text")

    reviou_data["place_id"] = place_id
    new_review = Review(**reviou_data)
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def change_review(review_id):
    """Method that updates a Review object with a specific id"""
    reviou_data = request.get_json()
    reviou = storage.get(Review, review_id)
    if not reviou:
        abort(404)
    elif not reviou_data:
        abort(400, "Not a JSON")

    for key, value in reviou_data.items():
        if key not in ["id", "user_id", "place_id",
                       "created_at", "updated_at"]:
            setattr(reviou, key, value)
    storage.save()
    return jsonify(reviou.to_dict()), 200
