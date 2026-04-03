from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from app.services import auth_service
from app.validators import user_register_schema, user_login_schema, user_response_schema
from app.utils.errors import ValidationError
from datetime import timedelta

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    
    # 1. Validation Layer (Marshmallow)
    errors = user_register_schema.validate(data)
    if errors:
        raise ValidationError("Invalid input", payload=errors)
        
    # 2. Service Layer (Business Logic)
    user = auth_service.register_user(data)
    
    # 3. View Layer (JSON Response formatting)
    return jsonify({
        "message": "User registered successfully", 
        "user": user_response_schema.dump(user)
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    errors = user_login_schema.validate(data)
    if errors:
        raise ValidationError("Invalid input", payload=errors)
        
    user = auth_service.authenticate_user(data['email'], data['password'])
    
    # Pass the role as an 'additional claim' so our Role Guard middleware can lock routes later!
    access_token = create_access_token(
        identity=str(user.id), 
        additional_claims={"role": user.role}, 
        expires_delta=timedelta(days=1)
    )
    
    return jsonify({"access_token": access_token, "user": user_response_schema.dump(user)}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    claims = get_jwt()
    return jsonify({
        "user_id": int(get_jwt_identity()),
        "role": claims.get("role")
    }), 200
