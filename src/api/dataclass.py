from dataclasses import dataclass


@dataclass
class Student:
    id: int
    first_name: str
    last_name: str


@dataclass
class Group:
    id: int
    name: str


@dataclass
class Course:
    id: int
    name: str
    description: str
