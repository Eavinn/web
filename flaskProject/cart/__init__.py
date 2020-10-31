from flask import Blueprint

cart_blu = Blueprint("cart", __name__,
                     template_folder="templates",
                     static_folder="static",
                     static_url_path="/static",
                     url_prefix="/cart"
                     )

from . import views


