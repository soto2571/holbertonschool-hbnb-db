"""
User routes for the application.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from src.models.user import User
from sqlalchemy.exc import SQLAlchemyError

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.route('', methods=['POST'])
def create_user():
    """Endpoint to create a new user."""
    user_data = request.get_json()
    try:
        new_user = User.create(user_data)
        return jsonify(new_user.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error"}), 500


@users_bp.route('', methods=['GET'])
@jwt_required()
def get_users():
    """Endpoint to get all users."""
    current_user_email = get_jwt_identity()
    current_user = User.query.filter_by(email=current_user_email).first()

    if not current_user.is_admin:
        return jsonify({"error": "Admin access required"}), 403

    users = User.get_all()
    return jsonify([user.to_dict() for user in users]), 200


@users_bp.route('/login', methods=['POST'])
def login():
    """Endpoint for user login and token generation."""
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        additional_claims = {"is_admin": user.is_admin}
        access_token = create_access_token(
            identity=email, additional_claims=additional_claims)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401


@users_bp.route('/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Endpoint to update user details."""
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

    data = request.get_json()
    try:
        updated_user = User.update(user_id, data)
        if updated_user:
            return jsonify(updated_user.to_dict()), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error"}), 500


@users_bp.route('/<user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Endpoint to delete a user."""
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

    try:
        user = User.query.get(user_id)
        if user:
            user.delete()
            return jsonify({"msg": "User deleted"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except SQLAlchemyError as e:
        return jsonify({"error": "Database error"}), 500
