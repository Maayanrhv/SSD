import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDialog
from PyQt5.QtGui import QIcon


class Example(QWidget):

    def __init__(self):
        super().__init__()
        self.win = QDialog()
        self.initUI()

    def initUI(self):
        self.win.setGeometry(300, 300, 300, 220)
        self.win.setWindowTitle('Icon')
        self.win.setWindowIcon(QIcon('icon.png'))

        self.win.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())