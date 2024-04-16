#!/usr/bin/python3
"""Script that creates a blueprint for the API"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


def register_views():
    """Method that registers the views"""
    import api.v1.views.index
    import api.v1.views.states
    import api.v1.views.cities
    import api.v1.views.amenities


register_views()
