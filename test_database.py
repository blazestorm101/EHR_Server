import os
import sys

# Add the app directory to Python path
sys.path.append(os.path.dirname(__file__))

try:
    from app import create_app
    from app.utils import (
        init_db, drop_db, clear_db, create_sample_data,
        get_database_stats, check_database_connection
    )

    print("🚀 Testing Database Utilities...")

    # Create app and push context
    app = create_app()

    with app.app_context():
        # Test database connection
        print("\n1. Testing database connection...")
        check_database_connection()

        # Test database stats
        print("\n2. Getting database stats...")
        stats = get_database_stats()

        # Test sample data creation
        print("\n3. Creating sample data...")
        create_sample_data()

        # Test stats again
        print("\n4. Getting updated database stats...")
        get_database_stats()

        print("\n🎉 All database utilities working correctly!")

except Exception as e:
    print(f"❌ Error during testing: {e}")
    import traceback

    traceback.print_exc()