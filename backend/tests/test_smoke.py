import os
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app import create_app
from app.extensions import db


def _make_profile(name: str, steam_id: str) -> dict:
    return {
        "name": name,
        "steam64_id": steam_id,
        "avatar": "https://example.com/avatar.png",
        "winrate": 0.55,
        "total_matches": 120,
        "rating": {
            "aim": 75.2,
            "utility": 58.4,
            "clutch": 0.08,
            "opening": 0.02,
        },
        "stats": {
            "accuracy_head": 23.4,
            "accuracy_enemy_spotted": 37.1,
            "trade_kills_success_percentage": 49.2,
            "traded_deaths_success_percentage": 58.5,
            "ct_opening_duel_success_percentage": 38.0,
            "t_opening_duel_success_percentage": 39.4,
        },
    }


class SmokeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db_path = os.path.join(tempfile.gettempdir(), "cs2_compare_smoke.db")
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)

        cls.app = create_app()
        cls.app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI=f"sqlite:///{cls.db_path}",
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            LEETIFY_PROFILE_ENDPOINT="/v3/profile",
            LEETIFY_STATS_ENDPOINT="/v3/profile",
            LEETIFY_RECENT_MATCHES_ENDPOINT="/v3/profile/matches",
        )
        with cls.app.app_context():
            db.create_all()

        cls.client = cls.app.test_client()

    @classmethod
    def tearDownClass(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()
        if os.path.exists(cls.db_path):
            os.remove(cls.db_path)

    def test_compare_and_history(self):
        profile_a = _make_profile("Player A", "76561198000000001")
        profile_b = _make_profile("Player B", "76561198000000002")

        with patch(
            "app.services.steam_service.SteamService.resolve_steam_id",
            side_effect=[profile_a["steam64_id"], profile_b["steam64_id"]],
        ), patch(
            "app.services.leetify_service.LeetifyService.get_player_profile",
            side_effect=[profile_a, profile_b],
        ), patch(
            "app.services.leetify_service.LeetifyService.get_recent_matches",
            return_value=[],
        ):
            response = self.client.post(
                "/api/compare",
                json={
                    "playerAUrl": "https://steamcommunity.com/id/player-a",
                    "playerBUrl": "https://steamcommunity.com/id/player-b",
                },
            )

        self.assertEqual(response.status_code, 200)
        payload = response.get_json()
        self.assertIn("comparisonId", payload)
        self.assertIn("players", payload)
        self.assertGreater(len(payload.get("stats", [])), 0)

        history_response = self.client.get("/api/comparisons")
        self.assertEqual(history_response.status_code, 200)
        history_payload = history_response.get_json()
        self.assertGreaterEqual(len(history_payload), 1)


if __name__ == "__main__":
    unittest.main()
