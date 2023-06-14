from marshmallow import Schema, fields


class StudentResponseSchema(Schema):
    id = fields.Int(metadata={"example": 1})
    first_name = fields.Str(metadata={"example": "John"})
    last_name = fields.Str(metadata={"example": "Doe"})


class StudentRequestSchema(Schema):
    first_name = fields.Str(metadata={"example": "John"})
    last_name = fields.Str(metadata={"example": "Doe"})


class DeleteStudentSchema(Schema):
    message = fields.Str(metadata={"example": "Student by 2 has been deleted."})


class StudentNotFoundSchema(Schema):
    error = fields.Str(metadata={"example": "Student by 4 not found."})


class PatchStudentSchema(Schema):
    message = fields.Str(metadata={"example": "Student by 3 has been updated."})
