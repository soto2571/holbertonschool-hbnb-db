"""
This module contains the routes for the reviews blueprint
"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from src.controllers.reviews import (
    create_review,
    delete_review,
    get_review_by_id,
    get_reviews,
    update_review,
)

reviews_bp = Blueprint("reviews", __name__, url_prefix="/reviews")


@reviews_bp.route("/", methods=["GET"])
def get_reviews_route():
    return get_reviews()


@reviews_bp.route("/<review_id>", methods=["GET"])
def get_review_by_id_route(review_id):
    return get_review_by_id(review_id)


@reviews_bp.route("/<review_id>", methods=["PUT"])
@jwt_required()
def update_review_by_id_route(review_id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403
    return update_review(review_id)


@reviews_bp.route("/<review_id>", methods=["DELETE"])
@jwt_required()
def delete_review_route(review_id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403
    return delete_review(review_id)


@reviews_bp.route("/<place_id>/reviews", methods=["POST"])
@jwt_required()
def create_review_route(place_id):
    return create_review(place_id)


@reviews_bp.route("/<place_id>/reviews", methods=["PUT"])
@jwt_required()
def update_review_for_place_route(place_id):
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    review = get_review_by_id(place_id)
    if review.user_id != current_user_id and not claims.get('is_admin'):
        return jsonify({"msg": "Admin or owner rights required"}), 403
    return update_review(place_id)
