from PyQt5.QtWidgets import QLabel, QRadioButton, QPushButton, QButtonGroup


class Page1RadioButtons:
    """
    Отрисовка gui первой страницы (выбор опций пользователем).
    """
    def __init__(self, window):
        self.window = window

        self.group1, self.group2, self.group3 = QButtonGroup(self.window), QButtonGroup(self.window), QButtonGroup(self.window)

        self.mainText1 = QLabel("Способ задания входных данных:", self.window)

        self.rdbtn1 = QRadioButton("через GUI", self.window)
        self.rdbtn2 = QRadioButton("чтение из файла", self.window)
        self.rdbtn3 = QRadioButton("генерация случайных данных", self.window)

        self.mainText2 = QLabel("Параметры алгоритма:", self.window)

        self.rdbtn4 = QRadioButton("задать самостоятельно", self.window)
        self.rdbtn5 = QRadioButton("значения по умолчанию", self.window)

        self.mainText3 = QLabel("Визуализация поиска решения:", self.window)

        self.rdbtn6 = QRadioButton("пошаговая", self.window)
        self.rdbtn7 = QRadioButton("сразу перейти к решению", self.window)

        self.radioButtons = [self.rdbtn1, self.rdbtn2, self.rdbtn3, self.rdbtn4, self.rdbtn5,
                             self.rdbtn6, self.rdbtn7]
        mainTexts = [self.mainText1, self.mainText2, self.mainText2, self.mainText3]
        for item in self.radioButtons:
            item.setStyleSheet("font: 25 12pt \"Umpush\";")
        for item in mainTexts:
            item.setStyleSheet("font: oblique 14pt \"Umpush\";")

        self.btnNext = QPushButton("далее", window)
        self.btnNext.setFixedSize(400, 80)
        self.btnNext.clicked.connect(self.window.choseTypeOfInput)

        for i in range(2):
            self.group1.addButton(self.radioButtons[i])
            self.group2.addButton(self.radioButtons[i + 3])
            self.group3.addButton(self.radioButtons[i + 5])
        self.group1.addButton(self.radioButtons[2])

        self.group1.buttonClicked.connect(self.window.group1Response)
        self.group2.buttonClicked.connect(self.window.group2Response)
        self.group3.buttonClicked.connect(self.window.group3Response)

        window.vbox.addWidget(self.mainText1)
        window.vbox.addWidget(self.rdbtn1)
        window.vbox.addWidget(self.rdbtn2)
        window.vbox.addWidget(self.rdbtn3)
        window.vbox.addWidget(self.mainText2)
        window.vbox.addWidget(self.rdbtn4)
        window.vbox.addWidget(self.rdbtn5)
        window.vbox.addWidget(self.mainText3)
        window.vbox.addWidget(self.rdbtn6)
        window.vbox.addWidget(self.rdbtn7)
        window.vbox.addWidget(self.btnNext)