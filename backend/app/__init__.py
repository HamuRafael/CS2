from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.extensions import db
from app.routes.comparison_routes import comparison_bp
from app.routes.player_routes import player_bp
from app.routes.history_routes import history_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    CORS(app, origins=app.config.get("CORS_ORIGINS") or None)

    app.register_blueprint(comparison_bp)
    app.register_blueprint(player_bp)
    app.register_blueprint(history_bp)

    return app
