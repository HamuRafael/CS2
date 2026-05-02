from datetime import datetime
from app.extensions import db


class Player(db.Model):
    __tablename__ = "players"

    id = db.Column(db.Integer, primary_key=True)
    steam_id = db.Column(db.String(32), unique=True, nullable=False)
    steam_url = db.Column(db.String(255), nullable=False)
    display_name = db.Column(db.String(120))
    avatar_url = db.Column(db.String(255))
    last_fetched_at = db.Column(db.DateTime)
    raw_data = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_public_dict(self) -> dict:
        return {
            "steamId": self.steam_id,
            "steamUrl": self.steam_url,
            "displayName": self.display_name,
            "avatarUrl": self.avatar_url,
            "lastFetchedAt": self.last_fetched_at.isoformat() if self.last_fetched_at else None,
        }
