from marshmallow import Schema, fields


class GroupResponseSchema(Schema):
    id = fields.Int(metadata={"example": 1})
    name = fields.Str(metadata={"example": "AA"})


class GroupRequestSchema(Schema):
    name_group = fields.Str(metadata={"example": "AA"})


class DeleteGroupSchema(Schema):
    message = fields.Str(metadata={"example": "Group with id 1 has been deleted."})


class GroupNotFoundSchema(Schema):
    error = fields.Str(metadata={"example": "Group with id 17 not found."})
