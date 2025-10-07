from app import db
from app.models.user import User
from app.models.button_press import ButtonPress
from app.models.emergency_message import EmergencyMessage
from datetime import datetime, timedelta
import random


def init_db():
    """Initialize the database with required tables"""
    try:
        db.create_all()
        print("✅ Database tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating database tables: {e}")
        return False


def drop_db():
    """Drop all tables (use with caution - for testing only)"""
    try:
        db.drop_all()
        print("✅ All tables dropped!")
        return True
    except Exception as e:
        print(f"❌ Error dropping tables: {e}")
        return False


def clear_db():
    """Clear all data from database but keep tables (for testing)"""
    try:
        # Delete all records from each table
        EmergencyMessage.query.delete()
        ButtonPress.query.delete()
        User.query.delete()

        db.session.commit()
        print("✅ All data cleared from database!")
        return True
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error clearing database: {e}")
        return False


def create_sample_data():
    """Create sample data for testing"""
    try:
        # Check if we already have users
        if User.query.first():
            print("ℹ️  Sample data already exists!")
            return True

        # Create sample user
        user = User(
            name="Test User",
            email="test@example.com",
            phone="1234567890"
        )
        user.set_password("password123")

        db.session.add(user)
        db.session.commit()
        print("✅ Sample user created: test@example.com / password123")

        # Create sample button presses
        button_ids = ["BUTTON_1", "BUTTON_2", "EMERGENCY_BUTTON"]
        locations = ["Living Room", "Kitchen", "Bedroom", "Garage"]

        for i in range(10):
            button_press = ButtonPress(
                user_id=user.id,
                button_id=random.choice(button_ids),
                duration=random.randint(50, 500),
                location=random.choice(locations),
                esp32_device_id="ESP32_DEVICE_001",
                pressed_at=datetime.utcnow() - timedelta(hours=random.randint(1, 24))
            )
            db.session.add(button_press)

        # Create sample emergency messages
        emergency_messages = [
            {"message": "Help needed in living room!", "severity": "high"},
            {"message": "Low battery warning", "severity": "medium"},
            {"message": "Door left open", "severity": "low"},
            {"message": "Water leak detected", "severity": "high"},
            {"message": "Temperature too high", "severity": "medium"}
        ]

        for i, msg_data in enumerate(emergency_messages):
            emergency = EmergencyMessage(
                user_id=user.id,
                message=msg_data["message"],
                severity=msg_data["severity"],
                esp32_device_id="ESP32_DEVICE_001",
                timestamp=datetime.utcnow() - timedelta(hours=random.randint(1, 12)),
                acknowledged=i % 2 == 0  # Alternate between acknowledged and not
            )
            db.session.add(emergency)

        db.session.commit()
        print("✅ Sample button presses and emergency messages created!")
        return True

    except Exception as e:
        db.session.rollback()
        print(f"❌ Error creating sample data: {e}")
        return False


def get_database_stats():
    """Get statistics about the database"""
    try:
        user_count = User.query.count()
        button_press_count = ButtonPress.query.count()
        emergency_count = EmergencyMessage.query.count()
        unacknowledged_emergencies = EmergencyMessage.query.filter_by(acknowledged=False).count()

        stats = {
            "users": user_count,
            "button_presses": button_press_count,
            "emergency_messages": emergency_count,
            "unacknowledged_emergencies": unacknowledged_emergencies
        }

        print("📊 Database Statistics:")
        print(f"   Users: {user_count}")
        print(f"   Button Presses: {button_press_count}")
        print(f"   Emergency Messages: {emergency_count}")
        print(f"   Unacknowledged Emergencies: {unacknowledged_emergencies}")

        return stats

    except Exception as e:
        print(f"❌ Error getting database stats: {e}")
        return None


def backup_database():
    """Create a backup of current data (simple version)"""
    try:
        # This is a simple backup - in production, use proper database backup tools
        users = User.query.all()
        button_presses = ButtonPress.query.all()
        emergencies = EmergencyMessage.query.all()

        backup_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "users": [user.to_dict() for user in users],
            "button_presses": [bp.to_dict() for bp in button_presses],
            "emergency_messages": [em.to_dict() for em in emergencies]
        }

        print("✅ Database backup created in memory")
        return backup_data

    except Exception as e:
        print(f"❌ Error creating backup: {e}")
        return None


def check_database_connection():
    """Check if database connection is working"""
    try:
        # Try to execute a simple query
        result = db.session.execute("SELECT 1")
        print("✅ Database connection is working!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def reset_database():
    """Completely reset database (drop and recreate) - USE WITH CAUTION"""
    try:
        print("⚠️  Resetting database...")
        drop_db()
        init_db()
        create_sample_data()
        print("✅ Database reset complete!")
        return True
    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        return False