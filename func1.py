import os
import sys
sys.path.append("E:\\Business\\SaleManagement\\Sales-Management-PyQt5-MySQL\\UI")
sys.path.append("E:\\Business\\SaleManagement\\Sales-Management-PyQt5-MySQL")
    
import json
from Ui_untitled import Ui_mainWindow
from PyQt5 import QtCore, QtGui, QtWidgets, QtSql
import mysql.connector

#provinceList = []
location_file_path = "E:\\Business\\SaleManagement\\Sales-Management-PyQt5-MySQL\\location.json"
# try:
#     with open(location_file_path, 'rb') as listChina:
#         provinces = json.loads(listChina.read())
#         for province in provinces:
#             provinceList.append(province['text'])
# except FileNotFoundError:
#     print(f"{location_file_path} Not Found!")

class customerData():
    # file_path = "E:\\Business\\SaleManagement\\Sales-Management-PyQt5-MySQL\\"
    def __init__(self):
        self.provinceList = []
        self.cityList = []
    
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
        
    def getCity(self):
        try:
            self.cityList = []
            with open(location_file_path, 'rb') as f:
                data = json.loads(f.read())
                ui.comboCity.clear()
                for city in data[self.provinceList.index(ui.comboProvince.currentText())]['children']:
                    self.cityList.append(city["text"])
        except Exception:
            print("getCity() Error!")
        else:
            return self.cityList

class dbConnect():
    def __init__(self, dhost, duser, dpasswd, ddatabase, dport):
        self.host = dhost
        self.user = duser
        self.passwd = dpasswd
        self.database = ddatabase
        self.port = dport
        #self.conn = mysql.connector.connect(host, user, passwd, database, port)

    def con(self):
        return mysql.connector.connect(host = self.host, 
                                       user = self.user, 
                                       passwd = self.passwd, 
                                       database = self.database,  
                                       port = self.port) 

    def close(self):
        #print(self.con)
        print("Hey")

class dbOperate():
    def __init__(self, connection):
        self.connection = connection
        self.cur = self.connection.cursor()
        # self.colQuery = colQuery
        # self.key = key

    def query(self, colQuery, key):
        ui.textResult.clear()
        try:
            if key == '':
                self.cur.execute("SELECT * FROM customer")
            else:
                self.cur.execute("SELECT * FROM customer WHERE %s = '%s'" % (colQuery, key))
        except Exception as err:
            ui.statusbar.showMessage(err)
        else:
            cols = self.cur.fetchall()
            if cols == []:
                ui.statusbar.showMessage("No Records found!")
            else:
                ui.statusbar.showMessage(f"{len(cols)} Records found!")
                for col in cols:
                    ui.textResult.append(col[0] +'  '+ col[1] +'  '+ col[2])

    def insert_customer(self, name, customerID, province, city, address, zip, phone, comment):
        try:
            self.cur.execute(f"INSERT INTO `account`.`customer` (`personID`, `name`, `province`, `city`, `address`, `zip`, `phone`, `comment`) VALUES ('{customerID}','{name}','{province}','{city}','{address}','{zip}','{phone}', '{comment}');")
        except Exception as err:
            ui.statusbar.showMessage(f"Error occured during iserting data! {err}")
        else:
            self.connection.commit()
            ui.statusbar.showMessage("Successfully inserted one record.") 
            
    def getRowCount(self):
        try:
            self.cur.execute("SELECT COUNT(*) FROM account.customer")
            rowCount = self.cur.fetchall()
        except Exception as err:
            ui.statusbar.showMessage(err)
        else:
            return rowCount[0][0]

class data():
    def __init__(self):
        
        self.model = QtGui.QStandardItemModel(8,2)#ui.ins.getRowCount())
        self.model.setHorizontalHeaderLabels(['ID', 'Name', 'Province', 'City','Address', 'Zip', 'Phone', 'Comment'])
        # self.tableView = QtWidgets.QTableView()
        # #关联QTableView空间和Model
        # self.tableView.setModel(self.model)
        
        
class myWindow(Ui_mainWindow, QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.mydb = dbConnect("localhost", "root", "Zzl33221144", "account", 3306)
        self.conn = self.mydb.con()
        self.ins = dbOperate(self.conn)
        self.cusInfo = customerData()
        #self.model = data()
        
    def setupUi(self, MainWindow):
        Ui_mainWindow.setupUi(self, MainWindow)
        MainWindow.setWindowOpacity(0.97)

        ###  UI STYLESHEET  ###
        # css_file_name = "sty.css"
        # with open(css_file_name, "r") as sty:
        #     MainWindow.setStyleSheet(sty.read())
        ###  Validator   ### 
        # customerIDValidator = QtGui.QIntValidator(self)
        # zipValidator = QtGui.QIntValidator(self)
        # phoneValidator = QtGui.QIntValidator(self)
        self.textCustomerID.setValidator(QtGui.QDoubleValidator(self))
        self.textZip.setValidator(QtGui.QIntValidator(self))
        self.textPhone.setValidator(QtGui.QDoubleValidator(self))
        ###  INPUT MASK  ###
        self.textCustomerID.setMaxLength(18)
        self.textZip.setMaxLength(6)
        self.textPhone.setMaxLength(11)
        # self.textCustomerID.setInputMask('000000000000000000;')
        # self.textZip.setInputMask('000000;')
        # self.textPhone.setInputMask('00000000000;')
        self.dateOrder.setDate(QtCore.QDate.currentDate())

        ###  事件调用功能  ###
        self.buttonSubmit.clicked.connect(self.submitToSQL) #首页Submit按钮
        self.buttonQuery.clicked.connect(self.query) #第二页查询Go按钮
        self.comboProvince.addItems(self.cusInfo.getProvince())
        self.comboProvince.currentTextChanged.connect(lambda: self.comboCity.addItems(self.cusInfo.getCity()))
        # if self.comboProvince.currentText() != "":
        #     print("OK1")
        #     getCity = QtCore.pyqtSignal()
        #     getCity.connect(lambda: self.comboCity.addItems(self.cusInfo.getCity()))
        #     getCity.emit()
        #self.tableViewResult.setModel(self.model)
        #QtSql.QSqlDatabase.addDatabase('Q')
        
    def query(self):
        # ins = dbOperate(self.conn)
        self.ins.query(self.comboQuery.currentText(), self.textKeyWord.text())

    def retranslateUi(self, MainWindow):
        Ui_mainWindow.retranslateUi(self, MainWindow)
        _translate = QtCore.QCoreApplication.translate
    
    ### BUTTON FUNCTIONS ###
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
            self.ins.insert_customer(self.textName.text() , self.textCustomerID.text(), self.comboProvince.currentText(), self.comboCity.currentText() ,self.textAddress.toPlainText(), self.textZip.text(), self.textPhone.text(), self.textCustomerComment.toPlainText())
           
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = myWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())