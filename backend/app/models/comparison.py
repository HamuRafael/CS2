from datetime import datetime
from app.extensions import db


class Comparison(db.Model):
    __tablename__ = "comparisons"

    id = db.Column(db.Integer, primary_key=True)
    player_a_id = db.Column(db.Integer, db.ForeignKey("players.id"), nullable=False)
    player_b_id = db.Column(db.Integer, db.ForeignKey("players.id"), nullable=False)
    result_json = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
