
from maincontrol import Ui_MainWindow
from PyQt5.QtWidgets import QApplication, QMainWindow, QButtonGroup
from PyQt5.QtGui import QIcon
import sys

class Gooey(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Gooey, self).__init__(parent)
        self.setupUi(self)
        self.Start_pushButton.clicked.connect(self.function__name)

    def function_name(self):
        pass

def main():
    app = QApplication(sys.argv)
    form = Gooey()
    form.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
