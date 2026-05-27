from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.user import User
from app.utils.security import generate_token

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "User already exists"}), 400

    if User.query.filter_by(username=data["username"]).first():
        return jsonify({"error": "Username already exists"}), 400

    user = User(
        username=data["username"],
        email=data["email"]
    )

    user.set_password(data["password"])

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data["email"]).first()

    if not user or not user.check_password(data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user.id)

    return jsonify({
        "access_token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email
        }
    }), 200