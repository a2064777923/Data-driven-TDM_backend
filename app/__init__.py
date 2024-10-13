from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from config import Config

db = SQLAlchemy()

"""
後端為了方便管理和擴展，為模块化設計，在這裏注册所有的模块並返回整個app。
"""
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)
    """為了避免循環引用，務必記得bp的導入要在使用db之後，使用bp之前"""
    from .routes import main
    app.register_blueprint(main)
    from app.hotel_overview import hotel_bp
    app.register_blueprint(hotel_bp, url_prefix='/api/hotels')
    from app.tourist_overview import tourist_bp
    app.register_blueprint(tourist_bp, url_prefix='/api/tourist')
    from app.event_overview import event_bp
    app.register_blueprint(event_bp, url_prefix='/api/event')
    from app.map_business import map_bp
    app.register_blueprint(map_bp, url_prefix='/api/map')

    return app
