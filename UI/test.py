# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Business\UI\test.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setGeometry(QtCore.QRect(80, 30, 651, 441))
        self.stackedWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.stackedWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.stackedWidget.setLineWidth(1)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.stackedWidget.addWidget(self.page)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.pushButton = QtWidgets.QPushButton(self.page_3)
        self.pushButton.setGeometry(QtCore.QRect(120, 130, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.stackedWidget.addWidget(self.page_3)
        self.New = QtWidgets.QWidget()
        self.New.setObjectName("New")
        self.listWidget = QtWidgets.QListWidget(self.New)
        self.listWidget.setGeometry(QtCore.QRect(170, 160, 256, 192))
        self.listWidget.setObjectName("listWidget")
        self.stackedWidget.addWidget(self.New)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menunew = QtWidgets.QMenu(self.menubar)
        self.menunew.setObjectName("menunew")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action1 = QtWidgets.QAction(MainWindow)
        self.action1.setObjectName("action1")
        self.action2 = QtWidgets.QAction(MainWindow)
        self.action2.setObjectName("action2")
        self.action3 = QtWidgets.QAction(MainWindow)
        self.action3.setObjectName("action3")
        self.menunew.addAction(self.action1)
        self.menunew.addAction(self.action2)
        self.menunew.addAction(self.action3)
        self.menubar.addAction(self.menunew.menuAction())

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.action1.triggered.connect(self.showpage1)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "PushButton"))
        self.menunew.setTitle(_translate("MainWindow", "new"))
        self.action1.setText(_translate("MainWindow", "1"))
        self.action2.setText(_translate("MainWindow", "2"))
        self.action3.setText(_translate("MainWindow", "3"))


    def showpage1(self):
        self.page_3.show()
        self.New.hide()
        self.page.hide()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
