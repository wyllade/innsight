from flask import Flask, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from .config import Config
from .extensions import db, migrate, jwt, cors

from .routes.auth import auth_bp
from .routes.hotel import hotel_bp

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

    @app.route("/")
    def home():
        return {
            "message": "Innsight API running"
        }

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