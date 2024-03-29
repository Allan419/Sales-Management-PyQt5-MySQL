import os
import sys
sys.path.append("E:\\Business\\SaleManagement\\Sales-Management-PyQt5-MySQL\\UI")
sys.path.append("E:\\Business\\SaleManagement\\Sales-Management-PyQt5-MySQL")

import json
from UI.Ui_new import Ui_mainWindow
from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
import mysql.connector
import numpy as np


location_file_path = "E:\\Business\\SaleManagement\\Sales-Management-PyQt5-MySQL\\location.json"


class customerData():
    # file_path = "E:\\Business\\SaleManagement\\Sales-Management-PyQt5-MySQL\\"
    def __init__(self):
        self.provinceList = []
        self.cityList = []

    @property
    def getProvince(self):

        try:
            with open(location_file_path, 'rb') as listChina:
                provinces = json.loads(listChina.read())
                for province in provinces:
                    self.provinceList.append(province['text'])
        except FileNotFoundError:
            print(f"{location_file_path} Not Found!")
        else:
            return self.provinceList

    @property
    def getCity(self):
        try:
            self.cityList = []
            with open(location_file_path, 'rb') as f:
                data = json.loads(f.read())
                ui.comboCity.clear()
                for city in data[self.provinceList.index(ui.comboProvince.currentText())]['children']:
                    self.cityList.append(city["text"])
        except Exception as err:
            print("getCity Error!", err)
        else:
            return self.cityList


class Database():
    queryResult = []
    rowCount = 0
    # model = QtGui.QStandardItemModel(8, 17)

    def __init__(self):
        try:
            self.connect = mysql.connector.connect(host="localhost",
                                                   user="root",
                                                   passwd="Zzl33221144",
                                                   database="account",
                                                   port=3306)
            self.cursor = self.connect.cursor(buffered=True)
        except Exception as err:
            ui.statusbar.showMessage("Database connection error: ", err)

    def query(self, colQuery, key):
        # ui.textResult.clear()
        try:
            if key == '':
                self.cursor.execute("SELECT * FROM customer")
            else:
                self.cursor.execute("SELECT * FROM customer WHERE %s = '%s'" % (colQuery, key))
        except Exception as err:
            ui.statusbar.showMessage(err)
        else:
            rows = self.cursor.fetchall()
            self.rowCount = len(rows)
            self.queryResult = []
            if rows == []:
                ui.statusbar.showMessage("No Records found!")
            else:
                ui.statusbar.showMessage(f"{self.rowCount} Records found!")
                for row in rows:
                    self.queryResult.append(row)

    def report(self):
        try:
            pass
        except:
            pass
        else:
            pass

    def insert_customer(self, name, customerID, province, city, address, zip, phone, comment):
        try:
            self.cursor.execute(f"INSERT INTO `account`.`customer` (`personID`, `name`, `province`, `city`, `address`, `zip`, `phone`, `comment`) VALUES ('{customerID}','{name}','{province}','{city}','{address}','{zip}','{phone}', '{comment}');")
        except Exception as err:
            ui.statusbar.showMessage(f"Error occured during iserting data! {err}")
        else:
            self.connect.commit()
            ui.statusbar.showMessage("Successfully inserted one record.")

    def delete(self, personID):
        try:
            self.cursor.execute(f"DELETE FROM `account`.`customer` WHERE (`personID` = '{personID}');")
        except Exception as err:
            ui.statusbar.showMessage(f"Error occured while deleting record: {err}")
        else:
            self.connect.commit()
            ui.statusbar.showMessage("Successfully deleted 1 record")

    def update(self, personID, name, province, city, address, zip, phone, comment):
        # UPDATE `account`.`customer` SET `name` = '张三1', `province` = '湖南1' WHERE (`personID` = '200000000000000000');
        try:
            self.cursor.execute(f"UPDATE `account`.`customer` SET `name` = '{name}', `province` = '{province}', `city` = '{city}', `address` = '{address}', `zip` = '{zip}', `phone` = '{phone}', `comment` = '{comment}' WHERE (`personID` = '{personID}')")
        except Exception as err:
            ui.statusbar.showMessage(f"Error occured while updating record: {err}")
        else:
            self.connect.commit()
            ui.statusbar.showMessage("Successfully updated 1 record")


class myWindow(Ui_mainWindow, QtWidgets.QWidget):

    comboQueryList = ['ID', 'Name', 'Province', 'City', 'Address', 'Zip', 'Phone', 'Comment']
    comboItemList = ['商品1', '商品2', '商品3']
    comboQuantityList = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', ]

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.db = Database()
        self.cusInfo = customerData()

    def setupUi(self, MainWindow):
        Ui_mainWindow.setupUi(self, MainWindow)
        MainWindow.setWindowOpacity(0.97)
        ###  UI STYLESHEET  ###
        css_file_name = "E:\\Business\\SaleManagement\\Sales-Management-PyQt5-MySQL\\UI\\sty.css"
        with open(css_file_name, "r") as sty:
            MainWindow.setStyleSheet(sty.read())
        ###  Validator   ###
        self.textCustomerID.setValidator(QtGui.QDoubleValidator(self))
        self.textCustomerID.setMaxLength(18)
        self.textZip.setValidator(QtGui.QIntValidator(self))
        self.textZip.setMaxLength(6)
        self.textPhone.setValidator(QtGui.QDoubleValidator(self))
        self.textPhone.setMaxLength(11)
        self.dateOrder.setDate(QtCore.QDate.currentDate())

        ###  事件调用功能  ###
        self.buttonSubmit.clicked.connect(self.submitToSQL)  # 首页Submit按钮
        self.buttonQuery.clicked.connect(self.query)  # 第二页查询Go按钮
        self.buttonDelete.clicked.connect(self.delete)  # 第二页Delete按钮
        self.buttonReport.clicked.connect(self.report)  # 第三页Report按钮
        self.comboProvince.addItems(self.cusInfo.getProvince)
        self.comboProvince.currentTextChanged.connect(lambda: self.comboCity.addItems(self.cusInfo.getCity))
        self.tableWidgetResult.cellClicked.connect(self.cellClicked)
        self.tableWidgetResult.cellDoubleClicked.connect(self.editCellDialog)
        ###
        self.comboItem.addItems(self.comboItemList)
        self.comboQuantity.addItems(self.comboQuantityList)
        self.comboQuery.addItems(self.comboQueryList)
        ###   CheckBoxes   ###
        self.checkBoxSelectAll.stateChanged.connect(lambda: self.selectAll())

    def report(self):
        print("report")

    def selectAll(self):
        self.checkBoxID.setChecked(self.checkBoxSelectAll.isChecked())
        self.checkBoxName.setChecked(self.checkBoxSelectAll.isChecked())
        self.checkBoxProvince.setChecked(self.checkBoxSelectAll.isChecked())
        self.checkBoxCity.setChecked(self.checkBoxSelectAll.isChecked())
        self.checkBoxAdress.setChecked(self.checkBoxSelectAll.isChecked())
        self.checkBoxZip.setChecked(self.checkBoxSelectAll.isChecked())
        self.checkBoxPhone.setChecked(self.checkBoxSelectAll.isChecked())
        self.checkBoxComment.setChecked(self.checkBoxSelectAll.isChecked())

    def display(self):
        self.tableWidgetResult.setColumnCount(8)
        self.tableWidgetResult.setRowCount(self.db.rowCount)
        self.tableWidgetResult.setHorizontalHeaderLabels(['ID', 'Name', 'Province', 'City', 'Address', 'Zip', 'Phone', 'Comment'])
        ### 设置列宽 ###
        self.tableWidgetResult.setColumnWidth(0, 170)
        self.tableWidgetResult.setColumnWidth(1, 70)
        self.tableWidgetResult.setColumnWidth(2, 80)
        self.tableWidgetResult.setColumnWidth(3, 90)
        self.tableWidgetResult.setColumnWidth(4, 220)
        self.tableWidgetResult.setColumnWidth(5, 70)
        self.tableWidgetResult.setColumnWidth(6, 120)
        self.tableWidgetResult.setColumnWidth(7, 200)
        self.tableWidgetResult.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)  # 整行选中
        self.tableWidgetResult.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # 禁止编辑
        # self.tableWidgetResult.resizeColumnsToContents()#自动根据内容调整列宽
        # self.tableWidgetResult.resizeRowsToContents()#自动根据内容调整行高

        for row in range(self.db.rowCount):
            for col in range(8):
                self.tableWidgetResult.setItem(row, col, QtWidgets.QTableWidgetItem(self.db.queryResult[row][col]))

    def query(self):
        self.db.query(self.comboQuery.currentText(), self.textKeyWord.text())
        self.lcdRowCount.display(self.db.rowCount)
        self.display()

    def cellClicked(self, row, column):
        self.clickedRow = row
        self.clickedColumn = column

    def editCellDialog(self, row, column):
        self.statusbar.showMessage("Editing record!")
        self.doubleClickedRow = row
        self.doubleClickedColumn = column
        # print(row, column)
        self.editDialog = QtWidgets.QDialog()
        self.editDialog.resize(600, 150)
        self.editDialog.setWindowTitle('Modify the record')
        self.tableWidgetModify = QtWidgets.QTableWidget()
        self.tableWidgetModify.setColumnCount(8)
        self.tableWidgetModify.setRowCount(1)
        self.tableWidgetModify.setHorizontalHeaderLabels(['ID', 'Name', 'Province', 'City', 'Address', 'Zip', 'Phone', 'Comment'])
        # print("CURRENT ITEM",self.tableWidgetModify.currentItem())
        self.buttonModifyYes = QtWidgets.QPushButton()
        self.buttonModifyNo = QtWidgets.QPushButton()
        self.buttonModifyYes.setText('Update')
        self.buttonModifyNo.setText('Cancel')
        self.buttonModifyYes.clicked.connect(self.update)
        self.buttonModifyNo.clicked.connect(self.editDialog.close)
        buttons = QtWidgets.QHBoxLayout()
        buttons.addWidget(self.buttonModifyYes)
        buttons.addWidget(self.buttonModifyNo)
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.tableWidgetModify)
        layout.addLayout(buttons)
        self.editDialog.setLayout(layout)
        for i in range(8):
            temp = self.tableWidgetResult.item(row, i).text()
            self.tableWidgetModify.setItem(0, i, QtWidgets.QTableWidgetItem(temp))
        self.tableWidgetModify.setVerticalHeaderLabels([f'{row + 1}'])
        self.editDialog.exec()

    def update(self):
        updateInfo = QtWidgets.QMessageBox.information(self, 'Update', 'Are you sure to update the record?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if updateInfo == QtWidgets.QMessageBox.Yes:
            # print(self.tableWidgetModify.item(0, 1).text())
            self.db.update(self.tableWidgetModify.item(0, 0).text(),
                           self.tableWidgetModify.item(0, 1).text(),
                           self.tableWidgetModify.item(0, 2).text(),
                           self.tableWidgetModify.item(0, 3).text(),
                           self.tableWidgetModify.item(0, 4).text(),
                           self.tableWidgetModify.item(0, 5).text(),
                           self.tableWidgetModify.item(0, 6).text(),
                           self.tableWidgetModify.item(0, 7).text())
            self.editDialog.close()
            if self.textKeyWord.text() != "" and self.tableWidgetModify.item(0, self.comboQuery.currentIndex()).text() != self.tableWidgetResult.item(self.doubleClickedRow, self.comboQuery.currentIndex()).text():
                self.textKeyWord.setText(self.tableWidgetModify.item(0, self.comboQuery.currentIndex()).text())
            self.query()
            self.statusbar.showMessage('Successfully updated one record!')
        else:
            self.statusbar.showMessage('Abort Updating!')

    def delete(self):
        self.statusbar.showMessage("Warning: You are about to delete a record from the database!")
        delWarning = QtWidgets.QMessageBox.warning(self, 'Warning', 'Are you sure to delete the record?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if delWarning == QtWidgets.QMessageBox.Yes:
            self.db.delete(self.tableWidgetResult.item(self.clickedRow, self.clickedColumn).text())
            self.query()
            self.statusbar.showMessage("Successfully deleted one record")
        else:
            self.statusbar.showMessage("Abort deleting")

    def submitToSQL(self):
        if self.textName.text() == "":
            self.statusbar.showMessage("Please fill out the name!")
        elif self.textCustomerID.text() == "":
            self.statusbar.showMessage("Please fill out the customer ID!")
        elif self.comboProvince.currentText() == "":
            self.statusbar.showMessage("Please fill out the Province name!")
        elif self.comboCity.currentText() == "":
            self.statusbar.showMessage("Please fill out the City name!")
        elif self.textAddress.toPlainText() == "":
            self.statusbar.showMessage("Please fill out the Address!")
        elif self.textZip.text() == "":
            self.statusbar.showMessage("Please fill out the Zip code!")
        elif self.textPhone.text() == "":
            self.statusbar.showMessage("Please fill out the Phone number!")
        else:
            self.db.insert_customer(self.textName.text(), self.textCustomerID.text(), self.comboProvince.currentText(), self.comboCity.currentText(), self.textAddress.toPlainText(), self.textZip.text(), self.textPhone.text(), self.textCustomerComment.toPlainText())

    def retranslateUi(self, MainWindow):
        Ui_mainWindow.retranslateUi(self, MainWindow)
        _translate = QtCore.QCoreApplication.translate


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = myWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
