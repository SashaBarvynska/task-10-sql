import factory
from faker import Faker

from .models import CourseModel, GroupModel, StudentModel

list_course = [
        'Mathematics', 'Biology', 'Chemistry', 'Physics', 'Computer Science',
        'History', 'Literature', 'Art History', 'Psychology', 'Sociology'
    ]

fake = Faker()
list_first_name = [fake.first_name() for _ in range(20)]
list_last_name = [fake.last_name() for _ in range(20)]


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
    first_name = factory.Sequence(lambda n: fake.random_element(list_first_name))
    last_name = factory.Sequence(lambda n: fake.random_element(list_last_name))
