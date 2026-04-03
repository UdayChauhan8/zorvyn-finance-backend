from marshmallow import Schema, fields, validate

class TransactionCreateSchema(Schema):
    amount = fields.Float(required=True, validate=lambda x: x > 0)
    type = fields.String(required=True, validate=validate.OneOf(["income", "expense"]))
    category = fields.String(required=True, validate=validate.Length(min=1, max=50))
    description = fields.String(validate=validate.Length(max=255))
    date = fields.DateTime()

class TransactionUpdateSchema(Schema):
    amount = fields.Float(validate=lambda x: x > 0)
    type = fields.String(validate=validate.OneOf(["income", "expense"]))
    category = fields.String(validate=validate.Length(min=1, max=50))
    description = fields.String(validate=validate.Length(max=255))
    date = fields.DateTime()

class TransactionResponseSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer(dump_only=True)
    amount = fields.Float(dump_only=True)
    type = fields.String(dump_only=True)
    category = fields.String(dump_only=True)
    description = fields.String(dump_only=True)
    date = fields.DateTime(dump_only=True)

transaction_create_schema = TransactionCreateSchema()
transaction_update_schema = TransactionUpdateSchema()
transaction_response_schema = TransactionResponseSchema()
transaction_responses_schema = TransactionResponseSchema(many=True) # Used for listing multiple records
