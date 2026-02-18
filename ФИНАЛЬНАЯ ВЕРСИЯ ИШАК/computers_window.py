import sqlite3
from PyQt6.QtCore import *

from PyQt6.QtWidgets import *

DB_NAME = "schedule.db"

teachers_by_subject = {
    "Русский язык": [
        "Иванова О.С.",
        "Смирнова А.П.",
        "Кузнецова М.И.",
        "Попова Е.А.",
        "Васильева Н.В."
    ],
    "Литература": [
        "Петрова Е.М.",
        "Соколова Т.Н.",
        "Михайлова И.В.",
        "Новикова С.Ю.",
        "Фёдорова Л.А."
    ],
    "Математика": [
        "Смирнов А.И.",
        "Кузнецов Д.С.",
        "Иванов А.П.",
        "Попов С.В.",
        "Волков М.Н."
    ],
    "Алгебра": [
        "Смирнов А.И.",
        "Кузнецов Д.С.",
        "Иванов А.П.",
        "Лебедев В.Г.",
        "Орлов П.Е."
    ],
    "Геометрия": [
        "Смирнов А.И.",
        "Кузнецов Д.С.",
        "Попов С.В.",
        "Николаев К.А.",
        "Морозов Р.В."
    ],
    "Вероятность и статистика": [
        "Кузнецов Д.С.",
        "Волков М.Н.",
        "Зайцев Р.Е.",
        "Орлов П.А.",
        "Лебедев И.В."
    ],
    "Информатика": [
        "Орлов П.А.",
        "Зайцев Р.Е.",
        "Николаев А.Д.",
        "Морозов К.А.",
        "Лебедев И.В."
    ],
    "Английский язык": [
        "Сидорова Е.О.",
        "Козлова В.С.",
        "Алексеева М.П.",
        "Егорова А.Р.",
        "Степанова Ю.К."
    ],
    "Немецкий язык": [
        "Мюллер А.К.",
        "Шмидт Е.В.",
        "Вагнер О.П.",
        "Бауэр Н.А.",
        "Фишер И.С."
    ],
    "Французский язык": [
        "Дюпон М.Л.",
        "Леруа Е.П.",
        "Мартен А.В.",
        "Бернар С.Н.",
        "Ламберт Ю.О."
    ],
    "Испанский язык": [
        "Гарсия М.А.",
        "Родригес Е.И.",
        "Лопес О.П.",
        "Мартinez Н.В.",
        "Фернандес А.С."
    ],
    "История России": [
        "Соколов В.И.",
        "Павлов Г.М.",
        "Фёдоров А.С.",
        "Макаров Д.А.",
        "Никитин О.В."
    ],
    "Всеобщая история": [
        "Соколов В.И.",
        "Павлов Г.М.",
        "Кравцов С.Ю.",
        "Громов Д.Н.",
        "Егоров А.В."
    ],
    "Обществознание": [
        "Козлова И.П.",
        "Васильева О.Д.",
        "Новикова Т.С.",
        "Морозова Е.В.",
        "Семёнова Н.А."
    ],
    "География": [
        "Зайцев Д.Ю.",
        "Орлов С.Н.",
        "Волков А.М.",
        "Лебедев П.В.",
        "Гусев Р.И."
    ],
    "Биология": [
        "Смирнова С.В.",
        "Попова М.А.",
        "Кузнецова А.С.",
        "Иванова Е.П.",
        "Петрова О.Н."
    ],
    "Физика": [
        "Иванов С.А.",
        "Кузнецов В.П.",
        "Смирнов М.И.",
        "Попов Д.В.",
        "Соколов А.Н."
    ],
    "Химия": [
        "Васильева Т.Ю.",
        "Фёдорова Н.М.",
        "Новикова Е.С.",
        "Михайлова О.Д.",
        "Алексеева И.П."
    ],
    "Астрономия": [
        "Соколов А.Н.",
        "Лебедев П.В.",
        "Зверев Д.И.",
        "Кравцов В.С.",
        "Орлов М.Е."
    ],
    "Экология": [
        "Попова М.А.",
        "Смирнова С.В.",
        "Кузнецова А.С.",
        "Зайцева Е.В.",
        "Морозова Н.П."
    ],
    "Физическая культура": [
        "Степанов И.В.",
        "Николаев А.С.",
        "Орлов Д.А.",
        "Зайцев Р.П.",
        "Морозов П.Е."
    ],
    "Основы безопасности и защиты Родины": [
        "Петров С.И.",
        "Козлов М.Ю.",
        "Волков А.Н.",
        "Лебедев В.П.",
        "Гусев О.С."
    ],
    "Изобразительное искусство": [
        "Сидорова М.В.",
        "Кравцова А.П.",
        "Романова Е.С.",
        "Белова О.М.",
        "Громова И.А."
    ],
    "Музыка": [
        "Иванова Л.Н.",
        "Смирнова С.Ю.",
        "Попова Т.Д.",
        "Кузнецова Е.В.",
        "Васильева Н.О."
    ],
    "Труд": [
        "Макаров Д.С.",
        "Никитин А.И.",
        "Соколов П.М.",
        "Фёдоров С.В.",
        "Егоров Р.А."
    ],
    "Мировая художественная культура": [
        "Петрова Е.М.",
        "Соколова Т.Н.",
        "Михайлова И.В.",
        "Новикова С.Ю.",
        "Романова Е.С."
    ],
    "Основы духовно-нравственной культуры народов России": [
        "Иванова О.С.",
        "Смирнова А.П.",
        "Козлова И.П.",
        "Васильева Н.В.",
        "Попова Е.А."
    ],
    "Второй иностранный язык": [
        "Сидорова Е.О.",
        "Козлова В.С.",
        "Алексеева М.П.",
        "Егорова А.Р.",
        "Степанова Ю.К."
    ]
}


class AddLessonDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить урок")
        self.setFixedWidth(300)

        layout = QVBoxLayout(self)

        self.class_input = QComboBox()
        self.class_input.addItems(["1А", "1Б", "1В", "1Г", "1Д", "1Е",
                                   "2А", "2Б", "2В", "2Г", "2Д", "2Е",
                                   "3А", "3Б", "3В", "3Г", "3Д", "3Е",
                                   "4А", "4Б", "4В", "4Г", "4Д", "4Е",
                                   "5А", "5Б", "5В", "5Г", "5Д", "5Е",
                                   "6А", "6Б", "6В", "6Г", "6Д", "6Е",
                                   "7А", "7Б", "7В", "7Г", "7Д", "7Е",
                                   "8А", "8Б", "8В", "8Г", "8Д", "8Е",
                                   "9А", "9Б", "9В", "9Г", "9Д", "9Е",
                                   "10А", "10Б", "10В", "10Г", "10Д", "10Е",
                                   "11А", "11Б", "11В", "11Г", "11Д", "11Е"])
        self.subject_combo = QComboBox()
        self.subject_combo.addItems([
    "Русский язык",
    "Литература",
    "Математика",
    "Алгебра",
    "Геометрия",
    "Вероятность и статистика",
    "Информатика",
    "Английский язык",
    "Немецкий язык",
    "Французский язык",
    "Испанский язык",
    "История России",
    "Всеобщая история",
    "Обществознание",
    "География",
    "Биология",
    "Физика",
    "Химия",
    "Астрономия",
    "Экология",
    "Физическая культура",
    "Основы безопасности и защиты Родины",
    "Изобразительное искусство",
    "Музыка",
    "Труд",
    "Мировая художественная культура",
    "Основы духовно-нравственной культуры народов России",
    "Второй иностранный язык"
])
        self.teacher_combo = QComboBox()
        self.classroom_input = QComboBox()
        self.classroom_input.addItems([
            "101",
            "102",
            "103",
            "104",
            "105",
            "106",
            "201",
            "202",
            "203",
            "204",
            "205",
            "206",
            "301",
            "302",
            "303",
            "304",
            "305",
            "306",

        ])
        self.day_input = QComboBox()
        self.day_input.addItems([
            "Понедельник",
            "Вторник",
            "Среда",
            "Четверг",
            "Пятница",
            "Суббота",
        ])
        self.lesson_input = QLineEdit()

        fields = [
            ("Класс", self.class_input),
            ("Предмет", self.subject_combo),
            ("Учитель", self.teacher_combo),
            ("Кабинет", self.classroom_input),
            ("День недели", self.day_input),
            ("Номер урока", self.lesson_input),
        ]

        for text, widget in fields:
            layout.addWidget(QLabel(text))
            layout.addWidget(widget)

        btn_add = QPushButton("Добавить")
        btn_add.clicked.connect(self.accept)
        layout.addWidget(btn_add)

        self.subject_combo.currentTextChanged.connect(self.update_teacher_list)

        self.update_teacher_list(self.subject_combo.currentText())

    def update_teacher_list(self, subject):
        self.teacher_combo.clear()

        teachers = teachers_by_subject.get(subject.strip(), [])

        if teachers:
            self.teacher_combo.addItems(teachers)
        else:
            self.teacher_combo.addItem("— выберите или введите вручную —")

    def get_data(self):
        return (
            self.class_input.currentText().strip(),
            self.subject_combo.currentText().strip(),
            self.teacher_combo.currentText().strip(),
            self.classroom_input.currentText().strip(),
            self.day_input.currentText().strip(),
            self.lesson_input.text().strip()
        )


class Schedule(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Расписание")
        self.resize(900, 500)

        self.init_ui()
        self.init_db()
        self.load_data()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Класс", "Предмет", "Учитель", "Кабинет", "День", "Урок"]
        )
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        left_layout.addWidget(self.table)

        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.btn_add = QPushButton("Добавить урок")
        self.btn_add.setFixedSize(150, 40)
        self.btn_add.clicked.connect(self.add_lesson)

        self.btn_del = QPushButton("Удалить урок")
        self.btn_del.setFixedSize(150, 40)
        self.btn_del.clicked.connect(self.delete_lesson)

        self.btn_back = QPushButton("Назад")
        self.btn_back.setFixedSize(150, 40)

        right_layout.addWidget(self.btn_add)
        right_layout.addWidget(self.btn_back)
        right_layout.addWidget(self.btn_del)
        right_layout.addStretch()

        main_layout.addWidget(left_widget, stretch=4)
        main_layout.addWidget(right_widget, stretch=1)

    def delete_lesson(self):
        selected = self.table.selectedItems()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите урок для удаления")
            return

        row = selected[0].row()
        lesson_id_item = self.table.item(row, 0)

        if not lesson_id_item:
            QMessageBox.warning(self, "Ошибка", "Не удалось определить ID урока")
            return

        lesson_id = lesson_id_item.text()

        reply = QMessageBox.question(
            self,
            "Подтверждение удаления",
            f"Удалить урок с ID {lesson_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply != QMessageBox.StandardButton.Yes:
            return

        try:
            conn = sqlite3.connect(DB_NAME)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM schedule WHERE id = ?", (lesson_id,))
            conn.commit()
            conn.close()

            self.load_data()
            QMessageBox.information(self, "Успех", "Урок удалён")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка базы данных", str(e))


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


