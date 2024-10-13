from flask import Blueprint

hotel_bp = Blueprint('hotel_overview', __name__)

from app.hotel_overview import routes
