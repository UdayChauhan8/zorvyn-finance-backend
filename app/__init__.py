from flask import Flask
from .config import config_by_name

def create_app(config_name="development"):
    # Initialize the Flask application
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_by_name.get(config_name, config_by_name["development"]))
    
    # A simple test route to verify the app is running
    @app.route('/ping', methods=['GET'])
    def ping():
        return {
            "status": "success",
            "message": "Zorvyn Finance Backend API is up and running!",
            "environment": config_name
        }, 200
        
    return app
