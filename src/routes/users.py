"""
User routes for the application
"""

from flask import Blueprint, request, jsonify
from src.models.user import User

users_bp = Blueprint('users', __name__, url_prefix='/api/users')

@users_bp.route('', methods=['POST'])
def create_user():
    user_data = request.get_json()
    new_user = User.create(user_data)
    return jsonify(new_user.to_dict()), 201

@users_bp.route('', methods=['GET'])
def get_users():
    users = User.get_all()
    return jsonify([user.to_dict() for user in users]), 200
