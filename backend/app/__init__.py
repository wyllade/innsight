from flask import Flask
from .config import Config
from .extensions import db, migrate, jwt, cors

from .routes.auth import auth_bp
from .routes.hotel import hotel_bp
from .routes.search import search_bp

from .models.user import User
from .models.hotel import Hotel


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(hotel_bp, url_prefix="/api/hotels")
    app.register_blueprint(search_bp, url_prefix="/api/search")

    @app.route("/")
    def home():
        return {"message": "Innsight API running"}

    return app