import factory
from faker import Faker

from .models import CourseModel, GroupModel, StudentModel

list_course = [
        'Mathematics', 'Biology', 'Chemistry', 'Physics', 'Computer Science',
        'History', 'Literature', 'Art History', 'Psychology', 'Sociology'
    ]

fake = Faker()


class GroupFactory(factory.Factory):
    class Meta:
        model = GroupModel
    name = factory.Sequence(lambda n: fake.bothify(text="??-##").upper())


class CreateTestCourse(factory.Factory):
    class Meta:
        model = CourseModel
    name = factory.Iterator(list_course, cycle=False)


class CreateTestStudent(factory.Factory):
    class Meta:
        model = StudentModel
    first_name = factory.Sequence(lambda n: fake.first_name())
    last_name = factory.Sequence(lambda n: fake.last_name())
