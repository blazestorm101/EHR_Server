# Import all models to make them available when importing from app.models
from app.models.user import User
from app.models.button_press import ButtonPress
from app.models.emergency_message import EmergencyMessage

# This makes these classes available when you do: from app.models import User, ButtonPress, etc.
__all__ = ['User', 'ButtonPress', 'EmergencyMessage']