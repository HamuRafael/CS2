import xml.etree.ElementTree as ET
import requests

from app.utils.errors import APIError
from app.utils.validators import extract_steam_id64, extract_custom_id


class SteamService:
    def resolve_steam_id(self, steam_url: str, timeout: int = 10) -> str:
        steam_id = extract_steam_id64(steam_url)
        if steam_id:
            return steam_id

        custom_id = extract_custom_id(steam_url)
        if not custom_id:
            raise APIError("Invalid Steam profile URL.", 400)

        profile_url = f"https://steamcommunity.com/id/{custom_id}?xml=1"
        try:
            response = requests.get(profile_url, timeout=timeout)
        except requests.RequestException as exc:
            raise APIError("Failed to resolve custom Steam URL.", 502) from exc

        if response.status_code == 404:
            raise APIError("Steam profile not found.", 404)

        try:
            root = ET.fromstring(response.text)
            steam_id64 = root.findtext("steamID64")
        except ET.ParseError as exc:
            raise APIError("Unable to parse Steam profile response.", 502) from exc

        if not steam_id64:
            raise APIError("Steam profile not found or private.", 404)

        return steam_id64
