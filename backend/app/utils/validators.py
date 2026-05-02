import re
from urllib.parse import urlparse

STEAM_PROFILE_RE = re.compile(r"^https?://steamcommunity\.com/profiles/(?P<steam_id>\d+)(/.*)?$")
STEAM_CUSTOM_RE = re.compile(r"^https?://steamcommunity\.com/id/(?P<custom_id>[A-Za-z0-9_-]+)(/.*)?$")


def is_valid_steam_url(url: str) -> bool:
    if not url:
        return False
    try:
        parsed = urlparse(url)
    except ValueError:
        return False
    if parsed.scheme not in {"http", "https"}:
        return False
    return bool(STEAM_PROFILE_RE.match(url) or STEAM_CUSTOM_RE.match(url))


def extract_steam_id64(url: str) -> str | None:
    match = STEAM_PROFILE_RE.match(url)
    if match:
        return match.group("steam_id")
    return None


def extract_custom_id(url: str) -> str | None:
    match = STEAM_CUSTOM_RE.match(url)
    if match:
        return match.group("custom_id")
    return None
