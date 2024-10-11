from marshmallow import Schema, fields

class UserSerializer(Schema):
    id = fields.UUID(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(load_only=True)

