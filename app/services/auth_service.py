from app.models import User
from app.extensions import db
from app.utils.errors import UnauthorizedError, ConflictError

def register_user(data):
    # Check if the user already exists to prevent duplicate failures
    if User.query.filter_by(email=data['email']).first() or User.query.filter_by(username=data['username']).first():
        raise ConflictError("Email or username already exists.")
        
    user = User(
        username=data['username'], 
        email=data['email'], 
        role=data.get('role', 'Viewer') # Defaults to Viewer if not passed
    )
    user.set_password(data['password'])
    
    db.session.add(user)
    db.session.commit()
    return user

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    # Check if user exists and password is correct securely
    if not user or not user.check_password(password):
        raise UnauthorizedError("Invalid email or password.")
    return user
