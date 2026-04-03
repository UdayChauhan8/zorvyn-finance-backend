from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import transaction_service
from app.validators import transaction_create_schema, transaction_update_schema, transaction_response_schema, transaction_responses_schema
from app.utils.errors import ValidationError
from app.middlewares import role_required
from app.utils.permissions import Role

transaction_bp = Blueprint('transaction_bp', __name__)

@transaction_bp.route('/', methods=['POST'])
@jwt_required()
@role_required([Role.ADMIN, Role.ANALYST]) # Strict rule applied via Role Guard!
def create_txn():
    data = request.get_json() or {}
    errors = transaction_create_schema.validate(data)
    if errors: 
        raise ValidationError("Invalid input", payload=errors)
    
    user_id = int(get_jwt_identity())
    txn = transaction_service.create_transaction(user_id, data)
    return jsonify(transaction_response_schema.dump(txn)), 201

@transaction_bp.route('/', methods=['GET'])
@jwt_required()
@role_required([Role.ADMIN, Role.ANALYST, Role.VIEWER])
def get_txns():
    user_id = int(get_jwt_identity())
    txns = transaction_service.get_user_transactions(user_id)
    return jsonify(transaction_responses_schema.dump(txns)), 200

@transaction_bp.route('/<int:txn_id>', methods=['PUT', 'PATCH'])
@jwt_required()
@role_required([Role.ADMIN, Role.ANALYST])
def update_txn(txn_id):
    data = request.get_json() or {}
    errors = transaction_update_schema.validate(data)
    if errors: 
        raise ValidationError("Invalid input", payload=errors)
    
    user_id = int(get_jwt_identity())
    txn = transaction_service.update_transaction(txn_id, user_id, data)
    return jsonify(transaction_response_schema.dump(txn)), 200

@transaction_bp.route('/<int:txn_id>', methods=['DELETE'])
@jwt_required()
@role_required([Role.ADMIN, Role.ANALYST])
def delete_txn(txn_id):
    user_id = int(get_jwt_identity())
    # Notice the route just calls delete. If not found, the service throws the 404!
    transaction_service.delete_transaction(txn_id, user_id)
    return jsonify({"message": "Transaction deleted successfully"}), 200
