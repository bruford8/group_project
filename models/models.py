from dataclasses import dataclass
from datetime import date
from enum import Enum
from typing import Optional, List

class UserRole(Enum):
    """Роли пользователей в системе"""
    ADMIN = "admin"
    TEACHER = "teacher"
    STUDENT = "student"
    PARENT = "parent"
    STAFF = "staff"

class GradeValue(Enum):
    """Значения оценок"""
    FIVE = 5
    FOUR = 4
    THREE = 3
    TWO = 2
    ONE = 1

@dataclass
class User:
    """Модель пользователя"""
    id: int
    username: str
    full_name: str
    role: UserRole
    class_id: Optional[int] = None
    children_ids: List[int] = None
    email: Optional[str] = None
    phone: Optional[str] = None

    def __post_init__(self):
        if self.children_ids is None:
            self.children_ids = []

@dataclass
class Subject:
    """Модель предмета"""
    id: int
    name: str
    teacher_id: int

@dataclass
class Grade:
    """Модель оценки"""
    id: int
    student_id: int
    subject_id: int
    grade: GradeValue
    date: date
    comment: str = ""
    created_at: Optional[date] = None

@dataclass
class Homework:
    """Модель домашнего задания"""
    id: int
    subject_id: int
    class_id: int
    assignment_date: date
    due_date: date
    description: str
    attachments: List[str] = None

    def __post_init__(self):
        if self.attachments is None:
            self.attachments = []

@dataclass
class SchoolClass:
    """Модель школьного класса"""
    id: int
    name: str
    teacher_id: int

@dataclass
class Attendance:
    """Модель посещаемости"""
    id: int
    student_id: int
    date: date
    status: str  # 'present', 'absent', 'late'
    reason: Optional[str] = None
