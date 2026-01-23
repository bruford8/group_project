from datetime import date, timedelta
from typing import List, Dict, Optional
import json
import random
from models import *


class DiaryService:
    def __init__(self, db):
        self.db = db
        self.cache = {
            'users': {},
            'subjects': {},
            'grades': {},
            'homework': {},
            'classes': {}
        }
        self.load_initial_data()

    def load_initial_data(self):
        """Загрузка начальных данных из базы"""
        with self.db.get_connection() as conn:
            self._load_users(conn)
            self._load_subjects(conn)
            self._load_classes(conn)
            self._load_grades(conn)
            self._load_homework(conn)

    def _load_users(self, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        for row in cursor.fetchall():
            user = User(
                id=row['id'],
                username=row['username'],
                full_name=row['full_name'],
                role=UserRole(row['role']),
                class_id=row['class_id'],
                email=row['email'],
                phone=row['phone']
            )
            self.cache['users'][user.id] = user

    def _load_subjects(self, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM subjects")
        for row in cursor.fetchall():
            subject = Subject(
                id=row['id'],
                name=row['name'],
                teacher_id=row['teacher_id']
            )
            self.cache['subjects'][subject.id] = subject

    def _load_classes(self, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM classes")
        for row in cursor.fetchall():
            school_class = SchoolClass(
                id=row['id'],
                name=row['name'],
                teacher_id=row['teacher_id']
            )
            self.cache['classes'][school_class.id] = school_class

    def _load_grades(self, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM grades")
        for row in cursor.fetchall():
            grade = Grade(
                id=row['id'],
                student_id=row['student_id'],
                subject_id=row['subject_id'],
                grade=GradeValue(row['grade']),
                date=date.fromisoformat(row['date']) if row['date'] else date.today(),
                comment=row['comment'] or ""
            )
            self.cache['grades'][grade.id] = grade

    def _load_homework(self, conn):
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM homework")
        for row in cursor.fetchall():
            attachments = json.loads(row['attachments']) if row['attachments'] else []
            homework = Homework(
                id=row['id'],
                subject_id=row['subject_id'],
                class_id=row['class_id'],
                assignment_date=date.fromisoformat(row['assignment_date']) if row['assignment_date'] else date.today(),
                due_date=date.fromisoformat(row['due_date']) if row['due_date'] else date.today(),
                description=row['description'],
                attachments=attachments
            )
            self.cache['homework'][homework.id] = homework

    def add_grade(self, student_id: int, subject_id: int,
                  grade_value: GradeValue, comment: str = "") -> Optional[Grade]:
        """Добавление новой оценки"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("""
                    INSERT INTO grades (student_id, subject_id, grade, date, comment)
                    VALUES (?, ?, ?, ?, ?)
                """, (student_id, subject_id, grade_value.value, date.today(), comment))

                grade_id = cursor.lastrowid
                grade = Grade(
                    id=grade_id,
                    student_id=student_id,
                    subject_id=subject_id,
                    grade=grade_value,
                    date=date.today(),
                    comment=comment
                )
                self.cache['grades'][grade_id] = grade
                return grade
            except Exception as e:
                print(f"Ошибка добавления оценки: {e}")
                return None

    def get_student_grades(self, student_id: int) -> List[Grade]:
        """Получение оценок ученика"""
        return [g for g in self.cache['grades'].values()
                if g.student_id == student_id]

    def get_student_average_grade(self, student_id: int) -> Dict[int, float]:
        """Средний балл по предметам"""
        student_grades = self.get_student_grades(student_id)
        subject_grades = {}

        for grade in student_grades:
            if grade.subject_id not in subject_grades:
                subject_grades[grade.subject_id] = []
            subject_grades[grade.subject_id].append(grade.grade.value)

        averages = {}
        for subject_id, grades in subject_grades.items():
            averages[subject_id] = sum(grades) / len(grades)

        return averages

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.cache['users'].get(user_id)

    def get_subject_by_id(self, subject_id: int) -> Optional[Subject]:
        return self.cache['subjects'].get(subject_id)

    def create_test_data(self):
        """Создание тестовых данных"""
        with self.db.get_connection() as conn:
            cursor = conn.cursor()

            # Создание тестовых предметов
            subjects = [
                ("Математика", 1),
                ("Физика", 1),
                ("Литература", 1),
                ("История", 1),
                ("Химия", 1)
            ]

            for name, teacher_id in subjects:
                cursor.execute("""
                    INSERT OR IGNORE INTO subjects (name, teacher_id)
                    VALUES (?, ?)
                """, (name, teacher_id))

            # Создание тестового класса
            cursor.execute("""
                INSERT OR IGNORE INTO classes (name, teacher_id)
                VALUES (?, ?)
            """, ("10А", 1))

            # Загружаем обновленные данные
            self.load_initial_data()
