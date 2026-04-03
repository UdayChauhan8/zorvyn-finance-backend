from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Initialize the SQLAlchemy and JWT Manager extensions here.
# By keeping them in extensions.py, we avoid circular import bugs 
# between models (which need 'db') and the app factory (which initializes 'db').
db = SQLAlchemy()
jwt = JWTManager()
