# Import all blueprints to make them available when importing from app.routes
from app.routes.auth import auth_bp
from app.routes.esp32 import esp32_bp
from app.routes.data import data_bp

# This makes these blueprints available when you do: from app.routes import auth_bp, etc.
__all__ = ['auth_bp', 'esp32_bp', 'data_bp']