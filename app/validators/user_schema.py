from marshmallow import Schema, fields, validate

class UserRegisterSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3, max=80))
    email = fields.Email(required=True)
    password = fields.String(required=True, validate=validate.Length(min=6))
    role = fields.String(validate=validate.OneOf(["Admin", "Analyst", "Viewer"]), load_default="Viewer")

class UserLoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

class UserResponseSchema(Schema):
    # 'dump_only' means these fields are only meant to be returned 
    # as out-going data, and cannot be passed as input.
    id = fields.Integer(dump_only=True)
    username = fields.String(dump_only=True)
    email = fields.Email(dump_only=True)
    role = fields.String(dump_only=True)
    is_active = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

user_register_schema = UserRegisterSchema()
user_login_schema = UserLoginSchema()
user_response_schema = UserResponseSchema()
