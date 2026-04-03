from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.utils.errors import ForbiddenError

def role_required(allowed_roles):
    """
    Middleware decorator to enforce Role-Based Access Control.
    :param allowed_roles: List of roles (e.g. [Role.ADMIN, Role.ANALYST])
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # 1. Verify the JWT token exists and is valid in the request
            verify_jwt_in_request()
            
            # 2. Extract claims from the JWT payload
            claims = get_jwt()
            user_role = claims.get("role")
            
            # 3. If the user's role is not in the allowed list, reject immediately
            if user_role not in allowed_roles:
                raise ForbiddenError(f"Access denied for role '{user_role}'. Required one of: {allowed_roles}")
                
            # 4. Otherwise, continue executing the route
            return fn(*args, **kwargs)
        return decorator
    return wrapper
