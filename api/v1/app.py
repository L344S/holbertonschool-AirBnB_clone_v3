#!/usr/bin/python3
"""Start of the API, first endpoint returns status of the API"""
from flask import Flask
from flask import jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views
from os import getenv


app = Flask(__name__)

app.register_blueprint(app_views)

CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(exception):
    """Method to close the session after each request"""
    storage.close()


@app.errorhandler(404)
def errorhandler(error):
    """Method to handle 404 errors with JSON response"""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    API_HOST = getenv("HBNB_API_HOST", "0.0.0.0")
    API_PORT = getenv("HBNB_API_PORT", 5000)
    app.run(host=API_HOST, port=API_PORT, threaded=True)
