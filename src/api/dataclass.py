from dataclasses import dataclass


@dataclass
class StudentDataclass:
    id: int
    first_name: str
    last_name: str

    @classmethod
    def from_sqlalchemy(cls, obj):
        return cls(id=obj.id, first_name=obj.first_name, last_name=obj.last_name)


@dataclass
class GroupDataclass:
    id: int
    name: str

    @classmethod
    def from_sqlalchemy(cls, obj):
        return cls(id=obj.id, name=obj.name)


@dataclass
class CourseDataclass:
    id: int
    name: str
    description: str

    @classmethod
    def from_sqlalchemy(cls, obj):
        return cls(id=obj.id, name=obj.name, description=obj.description)
