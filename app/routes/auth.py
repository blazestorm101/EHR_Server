from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user import User
from app import db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided'
            }), 400

        required_fields = ['name', 'email', 'password', 'phone']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'{field} is required'
                }), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({
                'success': False,
                'message': 'User already exists with this email'
            }), 400

        user = User(
            name=data['name'],
            email=data['email'],
            phone=data['phone']
        )
        user.set_password(data['password'])

        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=user.id)

        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'data': user.to_dict(),
            'access_token': access_token
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Registration failed: {str(e)}'
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided'
            }), 400

        if not data.get('email') or not data.get('password'):
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400

        user = User.query.filter_by(email=data['email']).first()

        if not user or not user.check_password(data['password']):
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401

        access_token = create_access_token(identity=user.id)

        return jsonify({
            'success': True,
            'message': 'Login successful',
            'data': user.to_dict(),
            'access_token': access_token
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Login failed: {str(e)}'
        }), 500