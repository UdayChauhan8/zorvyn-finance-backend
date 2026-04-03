from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import dashboard_service
from app.middlewares import role_required
from app.utils.permissions import Role
from app.validators import transaction_responses_schema

dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route('/summary', methods=['GET'])
@jwt_required()
@role_required([Role.ADMIN, Role.ANALYST, Role.VIEWER])
def summary():
    user_id = int(get_jwt_identity())
    data = dashboard_service.get_summary(user_id)
    return jsonify(data), 200

@dashboard_bp.route('/category-breakdown', methods=['GET'])
@jwt_required()
@role_required([Role.ADMIN, Role.ANALYST, Role.VIEWER])
def breakdown():
    user_id = int(get_jwt_identity())
    data = dashboard_service.get_category_breakdown(user_id)
    return jsonify(data), 200

@dashboard_bp.route('/recent', methods=['GET'])
@jwt_required()
@role_required([Role.ADMIN, Role.ANALYST, Role.VIEWER])
def recent_activity():
    user_id = int(get_jwt_identity())
    data = dashboard_service.get_recent_activity(user_id)
    return jsonify(transaction_responses_schema.dump(data)), 200
