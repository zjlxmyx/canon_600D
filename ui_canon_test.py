# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'canon_test.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1084, 896)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton_camera = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_camera.setGeometry(QtCore.QRect(890, 280, 101, 61))
        self.pushButton_camera.setCheckable(True)
        self.pushButton_camera.setObjectName("pushButton_camera")
        self.pushButton_capture = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_capture.setGeometry(QtCore.QRect(890, 480, 101, 61))
        self.pushButton_capture.setCheckable(True)
        self.pushButton_capture.setObjectName("pushButton_capture")
        self.label_image_show = QtWidgets.QLabel(self.centralwidget)
        self.label_image_show.setGeometry(QtCore.QRect(80, 60, 751, 711))
        self.label_image_show.setObjectName("label_image_show")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1084, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_camera.setText(_translate("MainWindow", "camera"))
        self.pushButton_capture.setText(_translate("MainWindow", "capture"))
        self.label_image_show.setText(_translate("MainWindow", "TextLabel"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

