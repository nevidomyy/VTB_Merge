import sys
from PyQt5 import QtWidgets
from forms import UiMainWindow
from functions import fill_main_table


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    fill_main_table(ui)
    sys.exit(app.exec())

