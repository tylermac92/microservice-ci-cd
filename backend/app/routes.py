from flask import Blueprint, jsonify

bp = Blueprint("routes", __name__)

@bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok"})

@bp.route("/api/data", methods=["GET"])
def get_data():
    return jsonify({"items": ["foo", "bar", "baz"]})
