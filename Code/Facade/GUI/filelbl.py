from PyQt5 import QtCore as qtc
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QMessageBox


class FileLabel(QLabel):
    """
    Объект класса - надпись, содержащая функционал drag and drop.
    """
    def __init__(self):
        super().__init__()
        self.setAlignment(qtc.Qt.AlignCenter)
        self.setText("Перетащите файл\n\nпервая строка - вместительность рюкзака\n\n"
                     "далее одна строка - один предмет\n(вес и цена через пробел)\n\n"
                     "необходимое расширение - txt")
        self.setStyleSheet("font: oblique 13pt \"Umpush\";")
        self.setAcceptDrops(True)
        self.pathToFile = ''

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                self.pathToFile = url.path()
            event.acceptProposedAction()
        else:
            event.ignore()


class SecondWindow(QtWidgets.QMainWindow):
    """
    Объект класса - окно для загрузки пользователем файла.
    Установка параметров окна и отрисовка gui.
    """
    submitClicked = qtc.pyqtSignal(str)
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("FILES")
        self.setGeometry(300, 300, 900, 900)

        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.vbox = QtWidgets.QGridLayout(self.centralWidget)

        self.btnNext = QPushButton("далее", self)
        self.btnNext.setFixedSize(400, 80)
        self.btnNext.clicked.connect(self.sendSignal)

        self.fileGetter = FileLabel()
        self.vbox.addWidget(self.fileGetter)
        self.vbox.addWidget(self.btnNext)

    def sendSignal(self):
        """
        Обработчик нажатия кнопки ДАЛЕЕ.
        Отправляет путь к файлу родительскому окну.
        """
        if self.fileGetter.pathToFile and self.fileGetter.pathToFile.endswith(".txt"):
            self.submitClicked.emit(self.fileGetter.pathToFile)
            self.close()
        else:
            msg = QMessageBox()
            msg.setStyleSheet("color: rgb(244, 12, 12); font: 75 13pt \"Umpush\";")
            msg.setWindowTitle("неполадки...")
            msg.setText("Файл не обнаружен!")
            msg.exec_()