from flask import Blueprint, request, jsonify
from app.models.button_press import ButtonPress
from app.models.emergency_message import EmergencyMessage
from app.models.user import User
from app import db

esp32_bp = Blueprint('esp32', __name__)


@esp32_bp.route('/button-press', methods=['POST'])
def receive_button_press():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided'
            }), 400

        if not data.get('button_id') or not data.get('device_id'):
            return jsonify({
                'success': False,
                'message': 'button_id and device_id are required'
            }), 400

        first_user = User.query.first()
        if not first_user:
            return jsonify({
                'success': False,
                'message': 'No users registered in system'
            }), 400

        button_press = ButtonPress(
            user_id=first_user.id,
            button_id=data['button_id'],
            duration=data.get('duration'),
            location=data.get('location'),
            esp32_device_id=data['device_id']
        )

        db.session.add(button_press)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Button press recorded successfully',
            'data': button_press.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to record button press: {str(e)}'
        }), 500


@esp32_bp.route('/emergency', methods=['POST'])
def receive_emergency():
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided'
            }), 400

        if not data.get('message') or not data.get('device_id'):
            return jsonify({
                'success': False,
                'message': 'message and device_id are required'
            }), 400

        first_user = User.query.first()
        if not first_user:
            return jsonify({
                'success': False,
                'message': 'No users registered in system'
            }), 400

        emergency_message = EmergencyMessage(
            user_id=first_user.id,
            message=data['message'],
            severity=data.get('severity', 'medium'),
            esp32_device_id=data['device_id']
        )

        db.session.add(emergency_message)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Emergency message recorded successfully',
            'data': emergency_message.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to record emergency message: {str(e)}'
        }), 500

@esp32_bp.route('/health-data', methods=['POST'])
def receive_health_data():
    try:
        data = request.get_json()
        
        # Validate admin token
        token = request.headers.get('Authorization')
        if not validate_admin_token(token):
            return jsonify({
                'success': False,
                'message': 'Unauthorized'
            }), 401
        
        # Store health data
        health_record = {
            'device_id': data['device_id'],
            'heart_rate': data.get('heart_rate'),
            'spo2': data.get('spo2'),
            'latitude': data.get('latitude'),
            'longitude': data.get('longitude'),
            'timestamp': data.get('timestamp')
        }
        
        # Save to database or process as needed
        print(f"Health data received: {health_record}")
        
        return jsonify({
            'success': True,
            'message': 'Health data recorded'
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error: {str(e)}'
        }), 500

def validate_admin_token(token):
    # Implement your admin token validation
    # This could check against a database of admin tokens
    valid_tokens = ["YOUR_ADMIN_TOKEN_1", "YOUR_ADMIN_TOKEN_2"]
    return token in valid_tokens
