"""
This module contains the routes for the cities blueprint.
"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from src.controllers.cities import (
    create_city,
    delete_city,
    get_city_by_id,
    get_cities,
    update_city,
)

cities_bp = Blueprint("cities", __name__, url_prefix="/cities")


@cities_bp.route("/", methods=["GET"])
def get_all_cities():
    return get_cities()


@cities_bp.route("/", methods=["POST"])
@jwt_required()
def create_new_city():
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403
    return create_city()


@cities_bp.route("/<city_id>", methods=["GET"])
def get_single_city(city_id):
    return get_city_by_id(city_id)


@cities_bp.route("/<city_id>", methods=["PUT"])
@jwt_required()
def update_single_city(city_id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403
    return update_city(city_id)


@cities_bp.route("/<city_id>", methods=["DELETE"])
@jwt_required()
def delete_single_city(city_id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403
    return delete_city(city_id)
