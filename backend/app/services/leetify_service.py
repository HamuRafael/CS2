import requests

from app.utils.errors import APIError


class LeetifyService:
    def __init__(
        self,
        base_url: str,
        profile_endpoint: str,
        stats_endpoint: str,
        recent_matches_endpoint: str,
        api_key: str = "",
    ):
        self.base_url = base_url.rstrip("/")
        self.profile_endpoint = profile_endpoint
        self.stats_endpoint = stats_endpoint
        self.recent_matches_endpoint = recent_matches_endpoint
        self.api_key = api_key

    def _require_config(self, endpoint: str, name: str) -> str:
        if not self.base_url or not endpoint:
            raise APIError(f"Leetify endpoint missing for {name}.", 500)
        return endpoint

    def _get(self, endpoint: str, steam_id: str) -> dict:
        url = f"{self.base_url}{endpoint}"
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        try:
            response = requests.get(
                url,
                params={"steam64_id": steam_id},
                headers=headers,
                timeout=15,
            )
        except requests.RequestException as exc:
            raise APIError("Leetify API request failed.", 502) from exc

        if response.status_code == 404:
            raise APIError("Player not found on Leetify.", 404)
        if response.status_code == 429:
            raise APIError("Leetify API rate limit reached.", 429)
        if response.status_code >= 500:
            raise APIError("Leetify API error.", 502)

        try:
            return response.json()
        except ValueError as exc:
            raise APIError("Leetify API returned invalid JSON.", 502) from exc

    def get_player_profile(self, steam_id: str) -> dict:
        endpoint = self._require_config(self.profile_endpoint, "profile")
        return self._get(endpoint, steam_id)

    def get_player_stats(self, steam_id: str) -> dict:
        endpoint = self._require_config(self.stats_endpoint, "stats")
        return self._get(endpoint, steam_id)

    def get_recent_matches(self, steam_id: str) -> dict:
        endpoint = self._require_config(self.recent_matches_endpoint, "recent matches")
        return self._get(endpoint, steam_id)
