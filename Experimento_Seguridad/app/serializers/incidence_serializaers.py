from marshmallow import Schema, fields

class IncidenceSerializer(Schema):
    id = fields.UUID(dump_only=True)
    user_id = fields.Str(required=True)
    creation_date = fields.Date(dump_only=True)
    description = fields.Str(required=True)
