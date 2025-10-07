from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.button_press import ButtonPress
from app.models.emergency_message import EmergencyMessage
from app.models.user import User
from app import db

data_bp = Blueprint('data', __name__)


@data_bp.route('/button-presses', methods=['GET'])
@jwt_required()
def get_button_presses():
    try:
        user_id = get_jwt_identity()

        limit = request.args.get('limit', type=int, default=100)
        device_id = request.args.get('device_id')

        query = ButtonPress.query.filter_by(user_id=user_id)

        if device_id:
            query = query.filter_by(esp32_device_id=device_id)

        button_presses = query.order_by(ButtonPress.pressed_at.desc()).limit(limit).all()

        return jsonify({
            'success': True,
            'data': [bp.to_dict() for bp in button_presses]
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get button presses: {str(e)}'
        }), 500


@data_bp.route('/emergency-messages', methods=['GET'])
@jwt_required()
def get_emergency_messages():
    try:
        user_id = get_jwt_identity()

        limit = request.args.get('limit', type=int, default=100)
        acknowledged = request.args.get('acknowledged', type=bool)
        device_id = request.args.get('device_id')

        query = EmergencyMessage.query.filter_by(user_id=user_id)

        if acknowledged is not None:
            query = query.filter_by(acknowledged=acknowledged)

        if device_id:
            query = query.filter_by(esp32_device_id=device_id)

        emergency_messages = query.order_by(EmergencyMessage.timestamp.desc()).limit(limit).all()

        return jsonify({
            'success': True,
            'data': [em.to_dict() for em in emergency_messages]
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get emergency messages: {str(e)}'
        }), 500


@data_bp.route('/emergency-messages/<message_id>/acknowledge', methods=['POST'])
@jwt_required()
def acknowledge_emergency(message_id):
    try:
        user_id = get_jwt_identity()

        emergency_message = EmergencyMessage.query.filter_by(
            id=message_id,
            user_id=user_id
        ).first()

        if not emergency_message:
            return jsonify({
                'success': False,
                'message': 'Emergency message not found'
            }), 404

        emergency_message.acknowledged = True
        db.session.commit()

        return jsonify({
            'success': True,
            'message': 'Emergency message acknowledged',
            'data': emergency_message.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to acknowledge emergency message: {str(e)}'
        }), 500