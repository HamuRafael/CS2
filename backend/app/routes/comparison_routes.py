from datetime import datetime, timedelta

from flask import Blueprint, current_app, jsonify, request

from app.extensions import db
from app.models.player import Player
from app.models.comparison import Comparison
from app.services.steam_service import SteamService
from app.services.leetify_service import LeetifyService
from app.services.comparison_service import ComparisonService
from app.utils.errors import APIError
from app.utils.validators import is_valid_steam_url

comparison_bp = Blueprint("comparison", __name__, url_prefix="/api")


@comparison_bp.route("/compare", methods=["POST"])
def compare_players():
    payload = request.get_json(silent=True) or {}
    player_a_url = payload.get("playerAUrl")
    player_b_url = payload.get("playerBUrl")

    if not player_a_url or not player_b_url:
        return jsonify({"error": "Both Steam URLs are required."}), 400
    if not is_valid_steam_url(player_a_url) or not is_valid_steam_url(player_b_url):
        return jsonify({"error": "Invalid Steam profile URL."}), 400

    steam_service = SteamService()
    try:
        player_a_steam_id = steam_service.resolve_steam_id(player_a_url)
        player_b_steam_id = steam_service.resolve_steam_id(player_b_url)
    except APIError as exc:
        return jsonify({"error": exc.message}), exc.status_code

    leetify_service = LeetifyService(
        current_app.config["LEETIFY_BASE_URL"],
        current_app.config["LEETIFY_PROFILE_ENDPOINT"],
        current_app.config["LEETIFY_STATS_ENDPOINT"],
        current_app.config["LEETIFY_RECENT_MATCHES_ENDPOINT"],
        current_app.config.get("LEETIFY_API_KEY", ""),
    )

    try:
        player_a = _get_or_fetch_player(player_a_steam_id, player_a_url, leetify_service)
        player_b = _get_or_fetch_player(player_b_steam_id, player_b_url, leetify_service)
    except APIError as exc:
        return jsonify({"error": exc.message}), exc.status_code

    comparison_service = ComparisonService()
    comparison_result = comparison_service.compare(player_a.raw_data or {}, player_b.raw_data or {})

    comparison_record = Comparison(
        player_a_id=player_a.id,
        player_b_id=player_b.id,
        result_json=comparison_result,
    )
    db.session.add(comparison_record)
    db.session.commit()

    response = {
        "comparisonId": comparison_record.id,
        "players": {
            "playerA": player_a.to_public_dict(),
            "playerB": player_b.to_public_dict(),
        },
        "stats": comparison_result.get("stats", []),
        "summary": comparison_result.get("summary", []),
    }
    return jsonify(response), 200


def _get_or_fetch_player(steam_id: str, steam_url: str, leetify_service: LeetifyService) -> Player:
    ttl_minutes = current_app.config.get("PLAYER_CACHE_TTL_MINUTES", 30)
    cutoff = datetime.utcnow() - timedelta(minutes=ttl_minutes)

    player = Player.query.filter_by(steam_id=steam_id).first()
    if player and player.last_fetched_at and player.last_fetched_at > cutoff:
        return player

    profile = leetify_service.get_player_profile(steam_id)
    matches = leetify_service.get_recent_matches(steam_id)

    raw_data = {
        "profile": profile,
        "matches": matches,
    }

    if not player:
        player = Player(steam_id=steam_id, steam_url=steam_url)
        db.session.add(player)

    player.display_name = profile.get("name") if isinstance(profile, dict) else None
    player.avatar_url = profile.get("avatar") if isinstance(profile, dict) else None
    player.raw_data = raw_data
    player.last_fetched_at = datetime.utcnow()

    db.session.commit()
    return player
