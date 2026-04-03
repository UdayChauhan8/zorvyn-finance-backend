class Role:
    """
    Single Source of Truth for Role-Based Access Control (RBAC).
    Defines the roles available in the system.
    """
    ADMIN = 'Admin'
    ANALYST = 'Analyst'
    VIEWER = 'Viewer'

    @classmethod
    def get_all_roles(cls):
        return [cls.ADMIN, cls.ANALYST, cls.VIEWER]
