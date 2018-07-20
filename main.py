# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'apps.form2.ui'
#
# Created by: VLADDOS
#
#

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, QAction, qApp, QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QHBoxLayout)
import sys
import comscanner

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
    
    def onChanged(self, text):
        self.lineEdit.setText(text)
        self.lineEdit.adjustSize()
    def find_ports(self):
        comscanner.find_ports()
    def Init_board(self):
        comscanner.get_start()

    def show_modal_window(self):
        global modalWindow
        # Parts 11.
        modalWindow = QWidget(self, QtCore.Qt.Window)
        modalWindow.setWindowTitle("Настройки")
        modalWindow.resize(300, 150)
        modalWindow.setMinimumSize(QtCore.QSize(300, 150))
        modalWindow.setMaximumSize(QtCore.QSize(300, 150))
        # modalWindow.setWindowModality(QtCore.Qt.WindowModal)
        #-- central widget
        centralwidget = QtWidgets.QWidget(modalWindow)
        centralwidget.setObjectName("centralwidget")
        #-- group box
        groupBox = QtWidgets.QGroupBox(centralwidget)
        groupBox.setGeometry(QtCore.QRect(5, 10, 290, 130))
        groupBox.setObjectName("groupBox")
        
        modalWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        modalWindow.move(self.geometry().center() - modalWindow.rect().center() - QtCore.QPoint(100, 50))
        modalWindow.show()
        
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 500)
        MainWindow.setMinimumSize(QtCore.QSize(550, 500))
        MainWindow.setMaximumSize(QtCore.QSize(550, 500))
        #MainWindow.setWindowOpacity(0.0)
        MainWindow.setAutoFillBackground(True)
        MainWindow.setToolButtonStyle(QtCore.Qt.ToolButtonIconOnly)
        MainWindow.setDocumentMode(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 20, 311, 411))
        self.groupBox.setObjectName("groupBox")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 50, 111, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        self.spinBox = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox.setRange(0, 100)
        self.spinBox.setValue(10)
        self.spinBox.setSingleStep(5)
        #self.spinBox.setPrefix("текст до (")
        self.spinBox.setSuffix(" градусов")
        self.spinBox.setGeometry(QtCore.QRect(190, 60, 113, 20))
        #self.spinBox.valueChanged[int].connect(on_value_changed1)
        #self.spinBox.valueChanged[str].connect(on_value_changed2)
        
        #self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        #self.lineEdit.setGeometry(QtCore.QRect(190, 60, 113, 20))
        #self.lineEdit.setObjectName("lineEdit")
        
        #self.lineEdit.textChanged[str].connect(self.onChanged)
        #---
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 100, 131, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 140, 141, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        #print('sadsa')
        self.label_3.setFont(font)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.comboBox = QtWidgets.QComboBox(self.groupBox)
        self.comboBox.setGeometry(QtCore.QRect(190, 140, 111, 22))
        self.comboBox.setCurrentText("")
        self.comboBox.setMaxVisibleItems(12)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItems(["Медленная", "Средняя", "Высокая"])
        ## ---
        self.lineEdit_2 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(190, 100, 113, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(10, 190, 131, 31))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(10, 230, 131, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.label_5.setFont(font)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 270, 131, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.comboBox_2 = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_2.setGeometry(QtCore.QRect(190, 280, 111, 22))
        self.comboBox_2.setCurrentText("")
        self.comboBox_2.setMaxVisibleItems(12)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItems(["Прямо", "Инверс"])
        self.lineEdit_3 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_3.setGeometry(QtCore.QRect(190, 240, 113, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_4.setGeometry(QtCore.QRect(190, 190, 113, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")

        self.pushButton2 = QtWidgets.QPushButton(self.groupBox)
        self.pushButton2.setGeometry(QtCore.QRect(150, 340, 121, 51))
        self.pushButton2.setCheckable(False)
        self.pushButton2.setObjectName("pushButton2")
        
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(30, 340, 121, 51))
        self.pushButton.setCheckable(False)
        self.pushButton.setObjectName("pushButton")
        
        #----- MAin button
        self.pushButton.clicked.connect(self.Init_board)
        #self.pushButton.clicked.connect(self.show_modal_window)
        self.pushButton2.clicked.connect(self.show_modal_window)
        #self.pushButton.clicked.connect(self.find_ports)
        #self.pushButton.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(360, 40, 181, 191))
        self.label_7.setSizeIncrement(QtCore.QSize(0, 0))
        self.label_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_7.setText("")
        self.label_7.setTextFormat(QtCore.Qt.AutoText)
        self.label_7.setPixmap(QtGui.QPixmap("img/logo.png"))
        self.label_7.setScaledContents(True)
        self.label_7.setObjectName("label_7")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 500, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Завершение приложения')
        exitAction.triggered.connect(qApp.quit)

        #exitAction2 = QAction(QIcon('exit2.png'), '&Exit', self)
        #exitAction2.setShortcut('Ctrl+R')
        #exitAction2.setStatusTip('Вызов настроек')
        #exitAction2.triggered.connect(self.show_modal_window)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Файл')
        fileMenu.addAction(exitAction)
        #fileMenu.addAction(exitAction2)
        

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Круглый стол')

        self.statusBar().showMessage('Ready')
        
        self.show()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Круглый стол"))
        self.groupBox.setTitle(_translate("MainWindow", "Управление"))
        self.label.setText(_translate("MainWindow", "Шаг (°)"))
        #self.lineEdit.setInputMask(_translate("MainWindow", "99999"))
        self.label_2.setText(_translate("MainWindow", "Количество шагов:"))
        self.label_3.setText(_translate("MainWindow", "Скорость вращения:"))
        self.lineEdit_2.setInputMask(_translate("MainWindow", "99999"))
        self.label_4.setText(_translate("MainWindow", "Задержка перед стартом:"))
        self.label_5.setText(_translate("MainWindow", "Задержка между поворотами:"))
        self.label_6.setText(_translate("MainWindow", "Направление вращения:"))
        self.lineEdit_3.setInputMask(_translate("MainWindow", "99999"))
        self.lineEdit_4.setInputMask(_translate("MainWindow", "99999"))
        self.pushButton.setText(_translate("MainWindow", "Полетели !"))
        self.pushButton.setShortcut(_translate("MainWindow", "Return"))

        self.pushButton2.setText(_translate("MainWindow", "Настройки"))
        self.pushButton2.setShortcut(_translate("MainWindow", "Return"))
        
class myWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

if __name__=="__main__":
    app = QApplication(sys.argv)
    
    
    #window = QMainWindow()
    #ss = myWin()
    #window.show()
    
    ui = Ui_MainWindow()
    #ui.setupUi(window)
    #window.show()
    sys.exit(app.exec_())
    
    
    #app = QtWidgets.QApplication(sys.argv)
    #myapp = myWin()
    #myapp.show()
    #sys.exit(app.exec_())

#app = QApplication(sys.argv)
#window = QtGui()
#ui = Ui_MainWindow()
#ui.setupUi(window)
#QtCore.QObject.connect(ui.butQuit, QtCore.SIGNAL("clicked()"), QtGui.qApp.quit)
#window.show()
#sys.exit(app.exec_())
