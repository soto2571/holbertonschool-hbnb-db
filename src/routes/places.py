"""
This module contains the routes for the places blueprint
"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from src.controllers.places import (
    create_place,
    delete_place,
    get_place_by_id,
    get_places,
    update_place,
)

places_bp = Blueprint("places", __name__, url_prefix="/places")


@places_bp.route("/", methods=["GET"])
def get_places_route():
    return get_places()


@places_bp.route("/", methods=["POST"])
@jwt_required()
def create_place_route():
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403
    return create_place()


@places_bp.route("/<place_id>", methods=["GET"])
def get_place_by_id_route(place_id):
    return get_place_by_id(place_id)


@places_bp.route("/<place_id>", methods=["PUT"])
@jwt_required()
def update_place_route(place_id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403
    return update_place(place_id)


@places_bp.route("/<place_id>", methods=["DELETE"])
@jwt_required()
def delete_place_route(place_id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403
    return delete_place(place_id)
