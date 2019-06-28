import os
import sys
sys.path.append("E:\\Business\\SaleManagement\\Sales-Management-PyQt5-MySQL\\UI")
sys.path.append("E:\\Business\\SaleManagement\\Sales-Management-PyQt5-MySQL")
    
import json
from Ui_untitled import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
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
        if key == '':
            self.cur.execute("SELECT * FROM customer")
        else:
            self.cur.execute("SELECT * FROM customer WHERE %s = '%s'" % (colQuery, key))
        cols = self.cur.fetchall()
        for col in cols:
            ui.textResult.append(col[0] +'  '+ col[1] +'  '+ col[2])

    def insert_customer(self, name, customerID, province, city, address, zip, phone, comment = "Null"):
        try:
            self.cur.execute(f"INSERT INTO `account`.`customer` (`personID`, `name`, `province`, `city`, `address`, `zip`, `phone`, `comment`) VALUES ('{customerID}','{name}','{province}','{city}','{address}','{zip}','{phone}', '{comment}');")
        except Exception as err:
            ui.statusbar.showMessage(f"Error occured during iserting data! {err}")
        else:
            self.connection.commit()
            ui.statusbar.showMessage("Successfully inserted one record.") 

class myWindow(Ui_MainWindow):
    def __init__(self):
        self.mydb = dbConnect("localhost", "root", "Zzl33221144", "account", 3306)
        self.conn = self.mydb.con()
        self.ins = dbOperate(self.conn)
        self.cusInfo = customerData()
     
    def setupUi(self, MainWindow):
        Ui_MainWindow.setupUi(self, MainWindow)
        MainWindow.setWindowOpacity(0.97)

        ###  UI STYLESHEET  ###
        # css_file_name = "sty.css"
        # with open(css_file_name, "r") as sty:
        #     MainWindow.setStyleSheet(sty.read())
        ###  INPUT MASK  ###
        self.textCustomerID.setMaxLength(18)
        self.textZip.setMaxLength(6)
        self.textPhone.setMaxLength(11)
        # self.textCustomerID.setInputMask('000000000000000000;')
        # self.textZip.setInputMask('000000;')
        # self.textPhone.setInputMask('00000000000;')

        ###  事件调用功能  ###
        self.buttonSubmit.clicked.connect(self.submitToSQL) #首页Submit按钮
        self.buttonQuery.clicked.connect(self.query) #第二页查询Go按钮
        self.comboProvince.addItems(self.cusInfo.getProvince())
        self.comboProvince.currentTextChanged.connect(lambda: self.comboCity.addItems(self.cusInfo.getCity()))
        
    def query(self):
        # ins = dbOperate(self.conn)
        self.ins.query(self.comboQuery.currentText(), self.textKeyWord.text())

    def retranslateUi(self, MainWindow):
        Ui_MainWindow.retranslateUi(self, MainWindow)
        _translate = QtCore.QCoreApplication.translate
    
    ### BUTTON FUNCTIONS ###
    def submitToSQL(self):
        self.ins.insert_customer(self.textName.text() , self.textCustomerID.text(), self.comboProvince.currentText(), self.comboCity.currentText() ,self.textAddress.toPlainText(), self.textZip.text(), self.textPhone.text(), self.textCustomerComment.toPlainText())
            

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = myWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())