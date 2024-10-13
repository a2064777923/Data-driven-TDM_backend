from flask import Blueprint

event_bp = Blueprint("event_overview", __name__)

from app.event_overview import routes
