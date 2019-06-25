import os
import sys
import json
from account import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector

provinceList = []
with open("E:\\Business\\UI\\location.json", 'rb') as listChina:
    provinces = json.loads(listChina.read())
    for province in provinces:
        provinceList.append(province['text'])
listChina.close()

print(provinceList)

class dbConnect:
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

class dbOperate:
    def __init__(self, connection, colQuery, key):
        self.connection = connection
        self.cur = self.connection.cursor()
        self.colQuery = colQuery
        self.key = key

    def query(self):
        #ui.textResult.setText("")
        print("SELECT * FROM customer WHERE %s = %s" % (self.colQuery, self.key))
        self.cur.execute("SELECT * FROM customer WHERE %s = '%s'" % (self.colQuery, self.key))
        cols = self.cur.fetchall()
        for col in cols:
            pass
            ui.tableResult.append(col[0] +'  '+ col[1] +'  '+ col[2])

    def insert(self):
        pass
        #self.cur.execute()

class myWindow(Ui_MainWindow):
    def __init__(self):
        self.mydb = dbConnect("localhost", "root", "Zzl33221144", "account", 3306)
        self.conn = self.mydb.con()
     
    def setupUi(self, MainWindow):
        Ui_MainWindow.setupUi(self, MainWindow)

        MainWindow.setWindowOpacity(0.97)
        path = os.path.abspath('account.py')
        print(path)
        #try:
        
        #except:
        #    print("Error!")
        ###  UI STYLESHEET  ###
        with open("E:\\Business\\UI\\sty.css", "r") as sty:
            MainWindow.setStyleSheet(sty.read())
            print("Alles klar")
        sty.close()
        #MainWindow.setStyleSheet(open("E:\\Business\\UI\\newsty.css", "r").read())
        ###  INPUT MASK  ###
        #self.textCustomerID.setInputMask('000000000000000000;')
        #self.textZip.setInputMask('000000;')
        #self.textPhone.setInputMask('00000000000;')

        ###  事件调用功能  ###
        self.ButtonSubmit.clicked.connect(self.submitToSQL) #首页Submit按钮
        self.ButtonQuery.clicked.connect(self.query) #第二页查询Go按钮
        self.actionNewRecord.triggered.connect(self.pageNewRecord)
        self.actionQuery.triggered.connect(self.pageQuery)
                #===  调用Calendar  ==#
        self.calendarWidget.hide() #默认隐藏
        self.textDate.mousePressEvent = self.showCalendar #鼠标点击TextEdit显示Calendar
        self.calendarWidget.clicked.connect(self.showDate) #鼠标点击Calendar在TextEdit显示所选日期
        self.textDate.textChanged.connect(self.hideCalendar) #日期输入TextEdit隐藏Calendar
        #print(self.comboQuery.currentText())

        self.tableResult.setShowGrid(True)
        #self.comboProvince.mousePressEvent = self.loadprovince()
        self.comboProvince.addItems(provinceList)

        
        #print(self.comboProvince.currentTextChanged)

    def loadcity(self):
        print(provinceList.index(self.comboProvince.currentText()))
        

    def query(self):
        ins = dbOperate(self.conn, self.comboQuery.currentText(), self.TextKeyWord.text())
        ins.query()
        

    def retranslateUi(self, MainWindow):
        Ui_MainWindow.retranslateUi(self, MainWindow)
        _translate = QtCore.QCoreApplication.translate


    ### 调用Calendar函数  ###
    def showCalendar(self,QMouseEvent):
	    self.calendarWidget.show()

    def showDate(self):
    	self.calendarWidget.dateTextFormat
    	self.textDate.setText(self.calendarWidget.selectedDate().toString("yyyy-MM-dd"))
	
    def hideCalendar(self):
        self.calendarWidget.hide()

    ###  页面切换  ###
    def pageQuery(self):
        self.pageEntry.hide()
        self.pageResult.show()

    def pageNewRecord(self):
        self.pageResult.hide()
        self.pageEntry.show()
    
    ### BUTTON FUNCTIONS ###
    def submitToSQL(self):
        textName = self.textName.text() #姓名
        textCustomerID = self.textCustomerID.text() #身份证号
        textProvince = self.comboProvince.currentText() #省份
        textCity = self.comboCity.currentText() #城市
        textAddress = self.textAddress.toPlainText() #地址
        textZip = self.textZip.text() #邮编
        textPhone = self.textPhone.text() #手机

        print(textName + "\n" 
                + textCustomerID + "\n"
                + textProvince + "\n"
                + textCity + "\n"
                + textAddress + "\n"
                + textZip + "\n"
                + textPhone + "\n")
        
        self.pageEntry.hide()
        self.pageResult.show()               


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = myWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    #print(help(myWindow))
    sys.exit(app.exec_())