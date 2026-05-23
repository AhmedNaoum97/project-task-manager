from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS


db = SQLAlchemy()
jwt = JWTManager()


def create_app():
    app = Flask(__name__)

    from .config import Config
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Import models AFTER db is initialized
    from .models import User

    # Import and register blueprints
    from .routes import auth_bp, tasks_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    with app.app_context():
        db.create_all()

    @app.route('/api/v1/health', methods=['GET'])
    def health():
        return {'status': 'ok', 'message': 'API is live'}, 200

    return app