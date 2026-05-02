from flask import Blueprint, jsonify

from app.models.player import Player

player_bp = Blueprint("player", __name__, url_prefix="/api")


@player_bp.route("/players/<steam_id>", methods=["GET"])
def get_player(steam_id: str):
    player = Player.query.filter_by(steam_id=steam_id).first()
    if not player:
        return jsonify({"error": "Player not found."}), 404
    return jsonify(player.to_public_dict()), 200
