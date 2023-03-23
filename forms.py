import os
from PyQt5 import QtCore, QtGui, QtWidgets
from functions import fill_main_table, load_settings, select_filesdir, merge


class UiMainWindow(object):
    def __init__(self):
        # Config path and filename
        self.BASE_DIR = os.path.dirname(__file__)
        self.CONFIG_FILE_NAME = os.path.join(self.BASE_DIR, "config.ini")

    def setup_ui(self, MainWindow):
        # Create main window
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(880, 475)
        MainWindow.setFixedSize(880, 475)
        MainWindow.setWindowIcon(QtGui.QIcon(os.path.join(self.BASE_DIR, "icon.ico")))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget") 

        # Create path line
        self.line_path = QtWidgets.QLineEdit(self.centralwidget)
        self.line_path.setGeometry(QtCore.QRect(10, 2, 591, 31))
        self.line_path.setObjectName("line_path")
        self.line_path.setReadOnly(True)

        # Create company_name line
        self.line_company_name = QtWidgets.QLineEdit(self.centralwidget)
        self.line_company_name.setGeometry(QtCore.QRect(10, 40, 350, 31))
        self.line_company_name.setObjectName("line_company_name")
        self.line_company_name.setPlaceholderText('Введите название организации')

        # Create company_id line 
        self.line_company_id = QtWidgets.QLineEdit(self.centralwidget)
        self.line_company_id.setGeometry(QtCore.QRect(360, 40, 241, 31))
        self.line_company_id.setObjectName("line_company_id")
        self.line_company_id_validator = QtGui.QRegExpValidator(QtCore.QRegExp('\d{0,10}'), self.centralwidget)
        self.line_company_id.setValidator(self.line_company_id_validator)
        self.line_company_id.setPlaceholderText('Введите код организации: 0001234567')

        # Create opendialog button
        self.btn_open = QtWidgets.QPushButton(self.centralwidget)
        self.btn_open.setGeometry(QtCore.QRect(610, 2, 111, 31))
        self.btn_open.setObjectName("btn_open")
        
        # Create reread button
        self.btn_reread = QtWidgets.QPushButton(self.centralwidget)
        self.btn_reread.setGeometry(QtCore.QRect(610, 39, 111, 31))
        self.btn_reread.setObjectName("btn_reread")  
       
        # Create summ label
        self.summ_label = QtWidgets.QLabel(self.centralwidget)
        self.summ_label.setText("Итого сумма: ")
        self.summ_label.setGeometry(QtCore.QRect(600, 386 ,100, 30))
        
        # Create summ line
        self.line_summ = QtWidgets.QLineEdit(self.centralwidget)
        self.line_summ.setGeometry(QtCore.QRect(700, 386, 150, 30))
        self.line_summ.setObjectName("line_status")
        self.line_summ.setReadOnly(True)

        # Create line_count label
        self.line_count_label = QtWidgets.QLabel(self.centralwidget)
        self.line_count_label.setText("Итого строк: ")
        self.line_count_label.setGeometry(QtCore.QRect(600, 420, 100, 30))

        #Create line_count edit form
        self.line_count = QtWidgets.QLineEdit(self.centralwidget)
        self.line_count.setGeometry(QtCore.QRect(700, 420, 150, 30))
        self.line_count.setObjectName("line_count")
        self.line_count.setReadOnly(True)

        #Create merge button
        self.btn_merge = QtWidgets.QPushButton(self.centralwidget)
        self.btn_merge.setGeometry(QtCore.QRect(20, 405, 180, 30))
        self.btn_merge.setObjectName("btn_merge")

        # Create LineNumber
        self.line_number = QtWidgets.QLineEdit(self.centralwidget)
        self.line_number.setGeometry(QtCore.QRect(205, 405, 120, 30))
        self.line_number.setObjectName("line_number")
        self.line_number_validator = QtGui.QRegExpValidator(QtCore.QRegExp('\d{1,3}'), self.centralwidget)
        self.line_number.setValidator(self.line_number_validator)
        self.line_number.setPlaceholderText('Номер реестра')

        # Create table   
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setGeometry(QtCore.QRect(0, 90, 880, 291))
        self.tableWidget.setObjectName("tableView")
        self.tableWidget.setHorizontalHeaderLabels(["Файл реестра: ", "Банк: ", "Найдено строк: ", "Сумма: "])
        

        # Initial Resize model for table
        # Resize header in full widht!
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        # Resize table column in content widht
        self.tableWidget.resizeColumnsToContents()

        # Create other elements for main window
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        #self.statusbar.showMessage("Готов")

        self.translate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
       
        #Execute connect functions!
        self.add_functions()
        
        # Load setting
        load_settings(self)

    def translate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "Объединение реестров для ВТБ"))
        self.btn_open.setText(_translate("MainWindow", "Выбор папки"))
        self.btn_reread.setText(_translate("MainWindow", "Перечитать"))
        self.btn_merge.setText(_translate("MainWindow", "Объединить реестры"))

    # All connect functions
    def add_functions(self):
        self.btn_open.clicked.connect(self.click_select_dir)
        self.btn_reread.clicked.connect(self.click_reread)
        self.btn_merge.clicked.connect(self.click_merge)
        
    def click_select_dir(self) -> None:
        select_filesdir(self)
        
    def click_reread(self) -> None:
        fill_main_table(self)
        
    def click_merge(self) -> None:
        merge(self)
        
