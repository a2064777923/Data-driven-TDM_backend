from flask import Blueprint

map_bp = Blueprint("map_business",__name__)

from app.map_business import routes