import os
import csv
import datetime
import fileinput
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QSettings
from serializers import RegistryFactory
    
# Main Functions
def select_filesdir(ui: QtWidgets) -> None:
    ui.path = QtWidgets.QFileDialog.getExistingDirectory(None, "Выберите папку с реестрами", ui.line_path.text(), 
                                                         QtWidgets.QFileDialog.ShowDirsOnly)
    if ui.path:
        ui.path = QtCore.QDir.toNativeSeparators(ui.path)
        ui.line_path.setText(ui.path)
        ui.tableWidget.setRowCount(0)
        ui.line_count.setText('')
        ui.line_summ.setText('')
        fill_main_table(ui)


def fill_main_table(ui: QtWidgets):
    """
    This method fill main table
    """
    save_settings(ui)
    if not ui.line_path.text():
        show_error(ui, "Папка для проверки реестров не указана! Хотите указать сейчас?")
        return
    fill_table(ui, get_registry_info(ui, ui.line_path.text()))
    ui.statusbar.showMessage('Информация загружена!')


def get_registry_info(ui: QtWidgets, path: str) -> tuple | None:
    files_info = list()
    try:
        for file in os.listdir(path):
            file_obj = RegistryFactory(os.path.join(path, file))
            if file_obj.get_info() is not None:
                files_info.append(file_obj.get_info())
    except Exception as error:
        ui.statusbar.showMessage('Ошибка получения информации: %s' %error )
    if len(files_info) == 0:
        show_error(ui, "В указанной папке реестры не найдены! Хотите выбрать другую папку?")
        return

    return tuple(files_info)


def fill_table(ui: QtWidgets, files: tuple):
    if files is None:
        return
    ui.tableWidget.setRowCount(len(files))
    # Disable editing in table
    ui.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    total_summ = float()
    total_lines = int()
    for index, file in enumerate(files):
        ui.tableWidget.setItem(index, 0, QtWidgets.QTableWidgetItem(file.get('filename')))
        ui.tableWidget.setItem(index, 1, QtWidgets.QTableWidgetItem(file.get('bank_name')))
        ui.tableWidget.setItem(index, 2, QtWidgets.QTableWidgetItem(str(file.get('line_count'))))
        ui.tableWidget.setItem(index, 3, QtWidgets.QTableWidgetItem(str(format(file.get('summ'), ',').replace(',', ' '))))
        total_summ += file.get('summ')
        total_lines += file.get('line_count')
    ui.line_summ.setText(str(format(round(total_summ, 2), ',').replace(',', ' ')))
    ui.line_count.setText(str(total_lines))


def merge(ui: QtWidgets):
    save_id(ui)
    filecount = ui.tableWidget.rowCount()

    if filecount <= 1:
        show_merge_error('Недостаточно реестров для объединения!')
        return

    if not ui.line_number.text():
        show_merge_error('Не введен номер для реестра!')
        return

    if not ui.line_company_name.text():
        show_merge_error('Не введено название организации!')
        return

    if not ui.line_company_id.text():
        show_merge_error('Не введен код организации!')
        return
        
    merge_path =  QtWidgets.QFileDialog.getExistingDirectory(None, 'Выберите папку для сохранения реестра', '', 
                                                             QtWidgets.QFileDialog.ShowDirsOnly)
    if not merge_path:
        return
        
    registry_number = "{:03d}".format(int(ui.line_number.text()))
    registry_name ='Z_' + ui.line_company_id.text()+ '_' + get_date() + '_' + registry_number + '_01.txt' 
    if registry_name in os.listdir(merge_path):
        show_merge_error('Невозможно сохранить файл в указанный каталог! Укажите другой номер '
                         'для реестра либо выберите другой путь для сохранения!')
        ui.statusbar.showMessage('Файл не выгружен! Попробуйте снова!')
        return

    outputfile = os.path.join(merge_path, registry_name)
    for row in range(filecount):
        file_obj = RegistryFactory(os.path.join(ui.line_path.text(), ui.tableWidget.item(row, 0).text()))
        try:
            file_obj.merge(output_file=outputfile, filenumber=row,
                           filecount=filecount,
                           registry_number=registry_number,
                           company_name=ui.line_company_name.text(),
                           line_count=ui.line_count.text(),
                           summ=ui.line_summ.text().replace(' ', '').replace('.', ',')
                        )
            ui.statusbar.showMessage("Файл успешно выгружен") 
        except Exception as error:
            ui.statusbar.showMessage("Ошибка слияния: %s" % error) 


def show_error(ui: QtWidgets, text: str):
    error = QtWidgets.QMessageBox()
    error.setWindowTitle("Ошибка проверки реестров")
    error.setText(text)
    error.setIcon(QtWidgets.QMessageBox.Warning)
    error.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)

    error.exec()

    # If clicked ok - started select_filesdir
    button = error.clickedButton()
    sb = error.standardButton(button)
    if sb == QtWidgets.QMessageBox.Yes:
        select_filesdir(ui)
    if sb == QtWidgets.QMessageBox.No:
        return


def show_merge_error(text: str):
    error = QtWidgets.QMessageBox()
    error.setWindowTitle("Предупреждение!")
    error.setText(text)
    error.setIcon(QtWidgets.QMessageBox.Warning)
    error.exec()


def get_date() -> str:
    date = datetime.datetime.now()
    month, day, year = date.strftime("%m"), date.strftime("%d"), date.strftime("%Y")
    return year + month + day


def save_settings(ui: QtWidgets):
    settings = QSettings(ui.CONFIG_FILE_NAME, QSettings.IniFormat)
    settings.setValue("path", ui.line_path.text())
    settings.setValue("company_name", ui.line_company_name.text())
    settings.setValue("company_id", ui.line_company_id.text())


def save_id(ui: QtWidgets):
    settings = QSettings(ui.CONFIG_FILE_NAME, QSettings.IniFormat)
    settings.setValue("company_name", ui.line_company_name.text())
    settings.setValue("company_id", ui.line_company_id.text())

def load_settings(ui: QtWidgets):
    settings = QSettings(ui.CONFIG_FILE_NAME, QSettings.IniFormat)
    ui.line_path.setText(settings.value("path"))
    ui.line_company_name.setText(settings.value("company_name"))
    ui.line_company_id.setText(settings.value("company_id"))

