from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def update(self):
        self.label.adjustSize()

    def StartClicked(self):
        self.label.setText("you pressed the button")
        self.update()

    def initUI(self):
        self.setGeometry(450, 200, 500, 300)  # set the windows x, y, width, height
        self.setWindowTitle("~Motion To Sound~")  # set the window title

        self.label = QtWidgets.QLabel(self)
        self.label.setText("my first label")
        self.label.move(50, 50)  # x, y from top left hand corner of the window

        self.startButton = QtWidgets.QPushButton(self)
        self.startButton.setText("Start Recording")
        self.startButton.move(100, 100)  # x, y from top left hand corner of the window
        self.startButton.clicked.connect(self.StartClicked)


def window():
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


window()
