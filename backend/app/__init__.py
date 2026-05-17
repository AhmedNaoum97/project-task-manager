from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS


db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    # Do not forget .config not app.config since it is in app already
    from .config import Config
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Import models so they are registered with SQLAlchemy
    from app.models import User

    with app.app_context():
        db.create_all()

    # Health check route
    @app.route('/api/v1/health', methods=['GET'])
    def health():
        return {'status': 'ok', 'message': 'API is live'}, 200

    return app