from flask import Flask, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from .config import Config
from .extensions import db, migrate, jwt, cors

from .routes.auth import auth_bp
from .routes.booking import booking_bp
from .routes.search import search_bp

from .models.user import User
from .models.booking import Booking


def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(booking_bp, url_prefix="/api/bookings")
    app.register_blueprint(search_bp, url_prefix="/api/search")

    @app.route("/")
    def home():
        return {"message": "Innsight API running"}

    @app.route("/api/profile")
    @jwt_required()
    def profile():
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        return jsonify({
            "id": user.id,
            "username": user.username,
            "email": user.email
        })

    return app