from flask import Blueprint

api = Blueprint('api', __name__)

from . import verify, passport, profile, houses, orders
