from app import db
from datetime import datetime
import uuid


class EmergencyMessage(db.Model):
    __tablename__ = 'emergency_messages'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    severity = db.Column(db.String(20), default='medium')
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    acknowledged = db.Column(db.Boolean, default=False)
    esp32_device_id = db.Column(db.String(100))

    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'severity': self.severity,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'acknowledged': self.acknowledged,
            'deviceId': self.esp32_device_id
        }