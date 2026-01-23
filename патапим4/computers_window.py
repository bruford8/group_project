import sqlite3

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem,
    QLabel, QPushButton,
    QLineEdit, QDialog
)
from PyQt6.QtCore import Qt


DB_NAME = "schedule.db"


# -------------------- Диалог добавления урока --------------------

class AddLessonDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить урок")
        self.setFixedWidth(300)

        layout = QVBoxLayout(self)

        self.class_input = QLineEdit()
        self.subject_input = QLineEdit()
        self.teacher_input = QLineEdit()
        self.classroom_input = QLineEdit()
        self.day_input = QLineEdit()
        self.lesson_input = QLineEdit()

        fields = [
            ("Класс", self.class_input),
            ("Предмет", self.subject_input),
            ("Учитель", self.teacher_input),
            ("Кабинет", self.classroom_input),
            ("День недели", self.day_input),
            ("Номер урока", self.lesson_input),
        ]

        for text, field in fields:
            layout.addWidget(QLabel(text))
            layout.addWidget(field)

        btn_add = QPushButton("Добавить")
        btn_add.clicked.connect(self.accept)
        layout.addWidget(btn_add)

    def get_data(self):
        return (
            self.class_input.text(),
            self.subject_input.text(),
            self.teacher_input.text(),
            self.classroom_input.text(),
            self.day_input.text(),
            self.lesson_input.text(),
        )


# -------------------- Главное окно --------------------

class Schedule(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Расписание")
        self.resize(900, 500)

        self.init_ui()
        self.init_db()
        self.load_data()

    # ---------- UI ----------

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        self.btn_add = QPushButton("Добавить урок")
        self.btn_add.setFixedSize(150, 35)
        self.btn_add.clicked.connect(self.add_lesson)

        self.btn_back = QPushButton("Назад")
        self.btn_back.setFixedSize(150, 35)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Класс", "Предмет", "Учитель", "Кабинет", "День", "Урок"]
        )
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        left_layout.addWidget(self.btn_add)
        left_layout.addWidget(self.table)
        left_layout.addWidget(self.btn_back)

        main_layout.addWidget(left_widget)

    # ---------- База данных ----------

    def init_db(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schedule (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                class_id TEXT,
                subject_id TEXT,
                teacher_id TEXT,
                classroom_id TEXT,
                day_of_week TEXT,
                lesson_number TEXT
            )
        """)

        conn.commit()
        conn.close()

    def load_data(self):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM schedule")
        rows = cursor.fetchall()

        self.table.setRowCount(0)

        for row_index, row in enumerate(rows):
            self.table.insertRow(row_index)
            for col_index, value in enumerate(row):
                self.table.setItem(
                    row_index, col_index, QTableWidgetItem(str(value))
                )

        conn.close()

    # ---------- Добавление урока ----------

    def add_lesson(self):
        dialog = AddLessonDialog(self)

        if dialog.exec():
            data = dialog.get_data()

            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO schedule (
                    class_id, subject_id, teacher_id,
                    classroom_id, day_of_week, lesson_number
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, data)

            conn.commit()
            conn.close()

            self.load_data()
