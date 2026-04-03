import warnings
# Suppress the flask_sqlalchemy warning regarding track modifications
warnings.filterwarnings('ignore')

from app import create_app
from app.extensions import db
from app.models import User, Transaction
from app.validators import user_register_schema

# We initialize a test application context so we can interact with the DB
app = create_app('development')

def run_tests():
    with app.app_context():
        print("====== TEST 1: DATABASE & MODEL INTEGRITY ======")
        print("Creating a test User and committing to DB...")
        
        # 1. Ensure clean slate (for testing purposes only)
        db.drop_all()
        db.create_all()
        
        # 2. Setup a User
        test_user = User(username="UdayTest", email="uday@zorvyn.com", role="Admin")
        test_user.set_password("SecurePass123!")
        
        db.session.add(test_user)
        db.session.commit()
        
        # 3. Retrieve User from Database
        retrieved_user = User.query.filter_by(username="UdayTest").first()
        if retrieved_user:
            print(f"✅ Success! User '{retrieved_user.username}' (ID: {retrieved_user.id}) was fetched from SQLite.")
            print(f"✅ Password Check: {retrieved_user.check_password('SecurePass123!')}")
        else:
            print("❌ Failed to query user.")


        print("\n====== TEST 2: MARSHMALLOW SCHEMAS ======")
        print("Sending bad data to the Schema to check if it gets explicitly rejected...")
        
        bad_payload = {
            "username": "ab",           # Too short! (requires min=3)
            "email": "not-an-email",    # Invalid email syntax!
            "password": "123"           # Too short! (requires min=6)
        }
        
        errors = user_register_schema.validate(bad_payload)
        
        if errors:
            print(f"✅ Success! Schema correctly identified all bad inputs and blocked them:")
            for field, error_msgs in errors.items():
                print(f"   -> {field}: {error_msgs[0]}")
        else:
            print("❌ Failed: Schema accepted bad data!")

if __name__ == '__main__':
    run_tests()
