from flask import Blueprint, jsonify

from app.models.comparison import Comparison

history_bp = Blueprint("history", __name__, url_prefix="/api")


@history_bp.route("/comparisons", methods=["GET"])
def list_comparisons():
    comparisons = Comparison.query.order_by(Comparison.created_at.desc()).limit(20).all()
    payload = [
        {
            "comparisonId": item.id,
            "playerAId": item.player_a_id,
            "playerBId": item.player_b_id,
            "createdAt": item.created_at.isoformat() if item.created_at else None,
        }
        for item in comparisons
    ]
    return jsonify(payload), 200


@history_bp.route("/comparisons/<int:comparison_id>", methods=["GET"])
def get_comparison(comparison_id: int):
    comparison = Comparison.query.get(comparison_id)
    if not comparison:
        return jsonify({"error": "Comparison not found."}), 404
    return jsonify({"comparisonId": comparison.id, "result": comparison.result_json}), 200
