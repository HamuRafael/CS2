import os
from dotenv import load_dotenv

_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_ENV_PATH = os.path.join(_ROOT_DIR, ".env")
load_dotenv(_ENV_PATH)


def _split_origins(value: str) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LEETIFY_BASE_URL = os.getenv("LEETIFY_BASE_URL", "")
    LEETIFY_PROFILE_ENDPOINT = os.getenv("LEETIFY_PROFILE_ENDPOINT", "")
    LEETIFY_STATS_ENDPOINT = os.getenv("LEETIFY_STATS_ENDPOINT", "")
    LEETIFY_RECENT_MATCHES_ENDPOINT = os.getenv("LEETIFY_RECENT_MATCHES_ENDPOINT", "")
    LEETIFY_API_KEY = os.getenv("LEETIFY_API_KEY", "")
    PLAYER_CACHE_TTL_MINUTES = int(os.getenv("PLAYER_CACHE_TTL_MINUTES", "30"))
    CORS_ORIGINS = _split_origins(os.getenv("CORS_ORIGINS", ""))
