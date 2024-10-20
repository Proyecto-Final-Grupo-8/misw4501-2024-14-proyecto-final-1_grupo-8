from marshmallow import Schema, fields

class incidentrializer(Schema):
    id = fields.UUID(dump_only=True)
    users_id = fields.Str(required=True)
    creation_date = fields.Date(dump_only=True)
    description = fields.Str(required=True)
