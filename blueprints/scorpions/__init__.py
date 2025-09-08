from flask import Blueprint
scorpions_bp = Blueprint("scorpions", __name__, url_prefix="/Escorpiones")
from . import routes
