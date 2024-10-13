from flask import Blueprint

tourist_bp =Blueprint('tourist_overview', __name__)

from app.tourist_overview import routes