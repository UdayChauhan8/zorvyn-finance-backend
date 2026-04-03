from flask import Flask, jsonify
from flask_cors import CORS
from .config import config_by_name
from app.extensions import db, jwt
from app.utils.errors import AppError

def create_app(config_name="development"):
    # 1. Initialize the Flask application
    app = Flask(__name__)
    
    # 2. Load configuration from our config.py class
    app.config.from_object(config_by_name.get(config_name, config_by_name["development"]))
    
    # 3. Initialize third-party extensions with the flask application
    CORS(app)      # Allows cross-origin requests
    db.init_app(app) # Binds SQLAlchemy to Flask app
    jwt.init_app(app) # Binds JWT Extended to Flask app
    
    # Import models here so SQLAlchemy knows about them before creation
    from app.models import User, Transaction
    
    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()

    # 4. Global Error Handling
    @app.errorhandler(AppError)
    def handle_app_error(e):
        """Catches all our custom exceptions (AppError) and formats them cleanly as JSON."""
        return jsonify(e.to_dict()), e.status_code

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404
        
    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal server error"}), 500

    # 5. Simple test route
    @app.route('/ping', methods=['GET'])
    def ping():
        return {
            "status": "success",
            "message": "Zorvyn Finance Backend API is up and running!",
            "environment": config_name
        }, 200
        
    # We will register our blueprints/routes here in later phases
        
    return app
