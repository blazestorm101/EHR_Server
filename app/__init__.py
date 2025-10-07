from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import timedelta

# Initialize extensions
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'jwt-secret-key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)

    # Database configuration for Render
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app)

    # Import and register blueprints
    from app.routes.auth import auth_bp
    from app.routes.esp32 import esp32_bp
    from app.routes.data import data_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(esp32_bp, url_prefix='/api/esp32')
    app.register_blueprint(data_bp, url_prefix='/api')

    # Health check endpoint
    @app.route('/')
    def home():
        return {
            'success': True,
            'message': 'ESP32 Monitor Server is running on Render!',
            'endpoints': {
                'register': '/api/auth/register',
                'login': '/api/auth/login',
                'button_press': '/api/esp32/button-press',
                'emergency': '/api/esp32/emergency',
                'button_presses': '/api/button-presses',
                'emergency_messages': '/api/emergency-messages'
            }
        }

    @app.route('/api/health')
    def health_check():
        return {
            'success': True,
            'message': 'Server is healthy',
            'status': 'operational'
        }

    # Create tables
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")

    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")

        # Optional: Create sample data in development
        if os.environ.get('FLASK_ENV') == 'development':
            from app.utils import create_sample_data
            create_sample_data()


    return app