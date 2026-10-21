from flask import Blueprint, request, jsonify, current_app
from .. import db, jwt
from ..models import User
from flask_jwt_extended import create_access_token
from datetime import timedelta
from pydantic import ValidationError
from ..schemas import AuthSchema, LoginSchema


auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """Register a new user"""
    try:
        data = request.get_json(silent=True)

        # Validate input
        try:
            payload = AuthSchema.model_validate(data)
        except ValidationError as e:
            return jsonify({'error': 'Invalid input',
                         'details': e.errors(include_url=False, include_input=False, include_context=False)}), 400
        

        # Check if user exists
        if User.query.filter_by(email=payload.email).first():
            return jsonify({'error': 'Email already registered'}), 409

        # Create new user
        user = User(email=payload.email)
        user.set_password(payload.password)

        db.session.add(user)
        db.session.commit()

        # Generate JWT token
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=24))

        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict(),
                'token': access_token
            }
        }), 201

    except Exception:
        db.session.rollback()
        current_app.logger.exception("Unhandled error in signup")
        return jsonify({'error': 'Internal server error'}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json(silent=True)

        # Validate input
        try:
            payload = LoginSchema.model_validate(data)
        except ValidationError as e:
            return jsonify({'error': 'Invalid input',
                         'details': e.errors(include_url=False, include_input=False, include_context=False)}), 400

        # Find user
        user = User.query.filter_by(email=payload.email).first()

        if not user or not user.check_password(payload.password):
            return jsonify({'error': 'Invalid email or password'}), 401

        # Generate JWT token
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=24))

        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict(),
                'token': access_token
            }
        }), 200

    except Exception:
        current_app.logger.exception("Unhandled error in login")
        return jsonify({'error': 'Internal server error'}), 500