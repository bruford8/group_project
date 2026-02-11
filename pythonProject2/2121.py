class AddLessonDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить урок")
        self.setFixedWidth(300)

        layout = QVBoxLayout(self)

        self.class_input = QLineEdit()
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
        self.subject_combo.setEditable(True)
        self.teacher_combo = QComboBox()
        self.teacher_combo.setEditable(True)
        self.classroom_input = QLineEdit()
        self.day_input = QLineEdit()
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
        """Обновляет список учителей в зависимости от выбранного предмета"""
        self.teacher_combo.clear()

        teachers = teachers_by_subject.get(subject.strip(), [])

        if teachers:
            self.teacher_combo.addItems(teachers)
        else:
            self.teacher_combo.addItem("— выберите или введите вручную —")

    def get_data(self):
        return (
            self.class_input.text().strip(),
            self.subject_combo.currentText().strip(),
            self.teacher_combo.currentText().strip(),
            self.classroom_input.text().strip(),
            self.day_input.text().strip(),
            self.lesson_input.text().strip(),
        )