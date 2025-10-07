from app import db
from datetime import datetime
import uuid


class ButtonPress(db.Model):
    __tablename__ = 'button_presses'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    button_id = db.Column(db.String(50), nullable=False)
    pressed_at = db.Column(db.DateTime, default=datetime.utcnow)
    duration = db.Column(db.Integer)
    location = db.Column(db.String(100))
    esp32_device_id = db.Column(db.String(100))

    def to_dict(self):
        return {
            'id': self.id,
            'buttonId': self.button_id,
            'pressedAt': self.pressed_at.isoformat() if self.pressed_at else None,
            'duration': self.duration,
            'location': self.location,
            'deviceId': self.esp32_device_id
        }