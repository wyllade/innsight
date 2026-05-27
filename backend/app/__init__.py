<<<<<<< HEAD
try:
 from flask import Flask
except ImportError:
    raise ImportError("Flask is not installed. Install it using 'pip install flask'")
=======
from flask import Flask, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
>>>>>>> 58fbc37 (feat: prepare base for Amadeus hotel API integration and cleanup local hotel dependency)

from .config import Config
from .extensions import db, migrate, jwt, cors

from .routes.auth import auth_bp
from .routes.hotel import hotel_bp
<<<<<<< HEAD
from .routes.search import search_bp
from .routes.bookings import bookings_bp
=======
from .routes.booking import booking_bp
>>>>>>> 58fbc37 (feat: prepare base for Amadeus hotel API integration and cleanup local hotel dependency)

from .models.user import User
from .models.hotel import Hotel
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
    app.register_blueprint(hotel_bp, url_prefix="/api/hotels")
    app.register_blueprint(search_bp, url_prefix="/api/search")
    app.register_blueprint(bookings_bp, url_prefix="/api/bookings")

    with app.app_context():
        db.create_all()

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