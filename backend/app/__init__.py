import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
jwt = JWTManager()
limiter = Limiter(key_func=get_remote_address, storage_uri="memory://")

def create_app():
    app = Flask(__name__)

    from .config import Config
    app.config.from_object(Config)

    # Fail fast: refuse to start without a strong JWT secret
    secret = os.getenv("JWT_SECRET")
    if not secret or len(secret) < 32:
        raise RuntimeError("JWT_SECRET must be set and at least 32 characters")
    app.config["JWT_SECRET_KEY"] = secret

    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)
    # CORS: only allow listed frontend origins
    allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    CORS(app, resources={r"/api/*": {"origins": allowed_origins}})

    # Import models AFTER db is initialized
    from .models import User

    # Import and register the blueprints
    from .routes import auth_bp, tasks_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    with app.app_context():
        db.create_all()

    @app.route('/api/v1/health', methods=['GET'])
    def health():
        return {'status': 'ok', 'message': 'API is live'}, 200

    return app