# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QHBoxLayout)
from PyQt5.QtGui import QPixmap
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(474, 425)

        #hbox = QHBoxLayout(self)
        

        #hbox.addWidget(lbl)
        
        MainWindow.setMaximumSize(QtCore.QSize(474, 425))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 281, 391))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 30, 131, 16))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(160, 30, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 70, 131, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 110, 131, 16))
        self.label_3.setObjectName("label_3")
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(160, 110, 111, 22))
        self.comboBox.setCurrentText("")
        self.comboBox.setMaxVisibleItems(12)
        self.comboBox.setObjectName("comboBox")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 70, 113, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(10, 150, 131, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(10, 190, 161, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 230, 131, 16))
        self.label_6.setObjectName("label_6")
        self.comboBox_2 = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_2.setGeometry(QtCore.QRect(160, 230, 111, 22))
        self.comboBox_2.setCurrentText("")
        self.comboBox_2.setMaxVisibleItems(12)
        self.comboBox_2.setObjectName("comboBox_2")
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(290, 10, 181, 351))
        self.graphicsView.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.graphicsView.setMouseTracking(False)
        self.graphicsView.setAutoFillBackground(False)
        self.graphicsView.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.graphicsView.setObjectName("graphicsView")
        #MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 474, 23))
        self.menubar.setObjectName("menubar")
        #MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        #MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBox.setTitle(_translate("MainWindow", "Управление"))
        self.label.setText(_translate("MainWindow", "Угол поворотного стол:"))
        self.lineEdit.setInputMask(_translate("MainWindow", "99999"))
        self.label_2.setText(_translate("MainWindow", "Количество шагов:"))
        self.label_3.setText(_translate("MainWindow", "Скорость вращения:"))
        self.lineEdit_2.setInputMask(_translate("MainWindow", "99999"))
        self.label_4.setText(_translate("MainWindow", "Задержка перед стартом:"))
        self.label_5.setText(_translate("MainWindow", "Задержка между поворотами:"))
        self.label_6.setText(_translate("MainWindow", "Направление вращения:"))

#app = QApplication(sys.argv)
#ex = Example()
#sys.exit(app.exec_())
app = QApplication(sys.argv)
window = QWidget()
ui = Ui_MainWindow()
ui.setupUi(window)
#QtCore.QObject.connect(ui.butQuit, QtCore.SIGNAL("clicked()"), QtGui.qApp.quit)
window.show()
sys.exit(app.exec_())