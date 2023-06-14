from marshmallow import Schema, fields


class CourseResponseSchema(Schema):
    id = fields.Int(metadata={"example": 1})
    name = fields.Str(metadata={"example": "AA"})
    description = fields.Str(metadata={"example": "None"})


class StudentsIdSchema(Schema):
    student_id = fields.Int(metadata={"example": 1})


class CourseRequestSchema(Schema):
    name = fields.Str(metadata={"example": "AA"})
    description = fields.Str(metadata={"example": "None"})


class DeleteCourseSchema(Schema):
    message = fields.Str(metadata={"example": "Course with id 1 has been deleted."})


class DeleteCourseStudentSchema(Schema):
    message = fields.Str(
        metadata={"example": "Course by id 3 has been deleted from student with id 7."}
    )


class CourseNotFoundSchema(Schema):
    error = fields.Str(
        metadata={"example": "Student with id 2 is not assigned to course with id 3"}
    )


class AddCourseRequestSchema(Schema):
    message = fields.Str(
        metadata={"example": "Course with name Biology was created successfully."}
    )


class AddCourseStudentRequestSchema(Schema):
    message = fields.Str(metadata={"example": "Сourse has been successfully added."})
