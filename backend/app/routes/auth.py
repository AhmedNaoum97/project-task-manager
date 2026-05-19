from flask import Blueprint, request, jsonify
from .. import db, jwt
from ..models import User
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """Register a new user"""
    try:
        data = request.get_json()

        # Validate input
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password required'}), 400

        # Check if user exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 409

        # Create new user
        user = User(email=data['email'])
        user.set_password(data['password'])

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

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user and return JWT token"""
    try:
        data = request.get_json()

        # Validate input
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({'error': 'Email and password required'}), 400

        # Find user
        user = User.query.filter_by(email=data['email']).first()

        if not user or not user.check_password(data['password']):
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

    except Exception as e:
        return jsonify({'error': str(e)}), 500