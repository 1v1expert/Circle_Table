# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'apps.form2.ui'
#
# This file is part of the 3DCircle Project

__author__ = 'Sazonov Vladislav Sergeevich <1v1expert@gmail.com>'
__copyright__ = 'Copyright (C) 2018 VLADDOS'
__license__ = 'GNU General Public License v2 http://www.gnu.org/licenses/gpl2.html'

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, QAction, qApp, QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QHBoxLayout)
import sys
import comscanner
import board
import time

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        self.std_speeds = ['250000', '115200', '57600', '38400', '19200', '9600', '4800',
                      '2400', '1200', '600', '300', '150', '100', '75', '50']  # Скорость COM порта
        self.degrees = 10
        self.steps = 1
        self.rate = 750
        self.delay_before_start = 0
        self.delay_between_turns = 1
        self.invert = False
        
        try:
            self.configuration = board.read_configuration(self)
            self.list_rates = self.configuration['Rotational_speed'].keys()
            #print(list(self.configuration['Rotational_speed'].keys()))
            #self.list_rates = [x.popitem()[0] for x in self.configuration['Rotational_speed']]
        except:
            self.list_rates = ['медленно', 'средне', 'быстро']
        #print( ll )
        
        super().__init__()
        self.setupUi(self)
        self.board = board.Board()
        
        
        
    def motor_invert(self, choos):
        if choos == 'Инверс':
            self.board.motor_invert(True)
        else:
            self.board.motor_invert(False)
            
    def ChangeRate_motor(self, rate):
        speed = 750
        try:
            speed = self.configuration['Rotational_speed'][rate]
        except:
            if rate == "медленно": speed = 750
            elif rate == "средне": speed = 3750
            elif rate == "быстро": speed = 7500
            #self.board._motor_speed = speed
        self.board.motor_speed(speed)

        
    def onChanged(self, text):
        self.lineEdit.setText(text)
        self.lineEdit.adjustSize()
        
    def find_ports(self):
        comscanner.find_ports()
        
    def Init_board(self):
        comscanner.get_start()

    def onSetSerial(self, serial_name):
        self.board.serial_name = serial_name
        
    def onSetSerialSpeeds(self, speed):
        self.board.baud_rate = int(speed)
    
    def onConnectBoard(self):
        f_rot = True
        if not self.board.serial_name:
            if (len(self.board.get_serial_list())):
                self.board.serial_name = self.board.get_serial_list()[0]
            else:
                f_rot = False
                self.statusBar().showMessage('Нет доступного порта')
                
        if self.board.connect() and f_rot:
            self.statusBar().showMessage('Подключено')
        else:
            self.statusBar().showMessage('Не удалось подключиться')
        self.modalWindow.close()
    
    def changeDegrees(self, degree):
        self.degrees = degree
        
    def changeSteps(self, step):
        self.steps = step
    
    def ChangeDelay_before_start(self, sec):
        self.delay_before_start = sec
    
    def Changedelay_between_turns(self, sec):
        self.delay_between_turns = sec
        
    def Rotate(self):
        if self.board._is_connected:
            print('Start rotate')
            #self.board.motor_enable()
            time.sleep(self.delay_before_start)
            print('motor speed = ', self.board._motor_speed, " steps = ", self.degrees)
            
            for rt in range(self.steps):
                sec = float(self.degrees / self.board._motor_speed)
                print("sec = ", 10 * sec * 6, " sleep = ", sec + self.delay_between_turns)
                self.board.motor_move(step=self.degrees)
                time.sleep(60 * sec + self.delay_between_turns)
            
        else:
            self.statusBar().showMessage('Ошибка! Нет подключения')
            self.show_modal_window()
            
    def show_modal_window(self):
        global modalWindow
        _translate = QtCore.QCoreApplication.translate
        # Parts 11.
        self.modalWindow = QWidget(self, QtCore.Qt.Window)
        self.modalWindow.setWindowTitle("Настройки")
        self.modalWindow.resize(450, 150)
        self.modalWindow.setMinimumSize(QtCore.QSize(450, 150))
        self.modalWindow.setMaximumSize(QtCore.QSize(450, 150))

        #-- central widget
        self.centralwidget = QtWidgets.QWidget(self.modalWindow)
        self.centralwidget.setObjectName("centralwidget")
        #-- group box
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(5, 10, 440, 130))
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setTitle(_translate("MainWindow", "Настройка подключения"))

        self.comboBox_SerialPorts = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_SerialPorts.setGeometry(QtCore.QRect(5, 25, 231, 22))
        self.comboBox_SerialPorts.setCurrentText("")
        self.comboBox_SerialPorts.setMaxVisibleItems(12)
        self.comboBox_SerialPorts.setObjectName("comboBox_SerialPorts")
        if (len(self.board.get_serial_list())):
            self.comboBox_SerialPorts.addItems(self.board.get_serial_list())
        else:
            self.comboBox_SerialPorts.addItems(['Устройства не найдены'])
        self.comboBox_SerialPorts.activated[str].connect(self.onSetSerial)

        self.comboBox_Std_speeds = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_Std_speeds.setGeometry(QtCore.QRect(300, 25, 120, 22))
        self.comboBox_Std_speeds.setCurrentText("")
        self.comboBox_Std_speeds.setMaxVisibleItems(12)
        self.comboBox_Std_speeds.setObjectName("comboBox_Std_speeds")
        #if (len(self.board.get_serial_list())):
        #    self.comboBox_SerialPorts.addItems(self.board.get_serial_list())
        #else:
        self.comboBox_Std_speeds.addItems(self.std_speeds)
        self.comboBox_Std_speeds.activated[str].connect(self.onSetSerialSpeeds)
        
        self.ConnectButton = QtWidgets.QPushButton(self.groupBox)
        self.ConnectButton.setGeometry(QtCore.QRect(90, 80, 221, 51))
        self.ConnectButton.setCheckable(False)
        self.ConnectButton.setObjectName("pushButton")
        
        self.ConnectButton.setText(_translate("MainWindow", "подключить"))
        self.ConnectButton.clicked.connect(self.onConnectBoard)
        
        #self.statusBar().showMessage('подключено')
        
        self.modalWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        self.modalWindow.move(self.geometry().center() - self.modalWindow.rect().center() - QtCore.QPoint(100, 50))
        self.modalWindow.show()
        
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

        self.DegreesSpinBox = QtWidgets.QSpinBox(self.groupBox)
        self.DegreesSpinBox.setRange(0, 1000)
        self.DegreesSpinBox.setValue(self.degrees)
        self.DegreesSpinBox.setSingleStep(5)
        #self.spinBox.setPrefix("текст до (")
        self.DegreesSpinBox.setSuffix(" градусов")
        self.DegreesSpinBox.setGeometry(QtCore.QRect(190, 60, 113, 20))
        self.DegreesSpinBox.valueChanged[int].connect(self.changeDegrees)
        
        #---
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 100, 131, 16))

        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 140, 141, 20))

        self.label_3.setFont(font)
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.RateComboBox = QtWidgets.QComboBox(self.groupBox)
        self.RateComboBox.setGeometry(QtCore.QRect(190, 140, 113, 22))
        self.RateComboBox.setCurrentText("")
        self.RateComboBox.setMaxVisibleItems(12)
        self.RateComboBox.setObjectName("comboBox")
        self.RateComboBox.addItems(self.list_rates)
        self.RateComboBox.activated[str].connect(self.ChangeRate_motor)
        ## ---

        self.ValueStepsSpinBox = QtWidgets.QSpinBox(self.groupBox)
        self.ValueStepsSpinBox.setRange(0, 100)
        self.ValueStepsSpinBox.setValue(1)
        self.ValueStepsSpinBox.setSingleStep(self.steps)
        # self.spinBox.setPrefix("текст до (")
        self.ValueStepsSpinBox.setSuffix(" шаг(-а, -ов)")
        self.ValueStepsSpinBox.setGeometry(QtCore.QRect(190, 100, 113, 20))
        self.ValueStepsSpinBox.valueChanged[int].connect(self.changeSteps)
        
        
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(10, 190, 131, 31))

        self.label_4.setFont(font)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(10, 230, 131, 41))

        font.setKerning(True)
        self.label_5.setFont(font)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 270, 131, 41))

        self.label_6.setFont(font)
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        
        self.motor_invers_comboBox = QtWidgets.QComboBox(self.groupBox)
        self.motor_invers_comboBox.setGeometry(QtCore.QRect(190, 280, 111, 22))
        self.motor_invers_comboBox.setCurrentText("")
        self.motor_invers_comboBox.setMaxVisibleItems(12)
        self.motor_invers_comboBox.setObjectName("comboBox_2")
        self.motor_invers_comboBox.addItems(["Прямо", "Инверс"])
        self.motor_invers_comboBox.activated[str].connect(self.motor_invert)

        self.Delay_between_turns = QtWidgets.QSpinBox(self.groupBox)
        self.Delay_between_turns.setRange(0, 1000)
        self.Delay_between_turns.setValue(self.delay_between_turns)
        self.Delay_between_turns.setSingleStep(10)
        self.Delay_between_turns.setSuffix(" c")
        self.Delay_between_turns.setGeometry(QtCore.QRect(190, 240, 113, 20))
        self.Delay_between_turns.valueChanged[int].connect(self.Changedelay_between_turns)
        

        self.Delay_before_start = QtWidgets.QSpinBox(self.groupBox)
        self.Delay_before_start.setRange(0, 1000)
        self.Delay_before_start.setValue(self.delay_before_start)
        self.Delay_before_start.setSingleStep(10)
        self.Delay_before_start.setSuffix(" c")
        self.Delay_before_start.setGeometry(QtCore.QRect(190, 190, 113, 20))
        self.Delay_before_start.valueChanged[int].connect(self.ChangeDelay_before_start)


        self.OpenSettings = QtWidgets.QPushButton(self.groupBox)
        self.OpenSettings.setGeometry(QtCore.QRect(150, 340, 121, 51))
        self.OpenSettings.setCheckable(False)
        self.OpenSettings.setObjectName("OpenSettings")
        
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(30, 340, 121, 51))
        self.pushButton.setCheckable(False)
        self.pushButton.setObjectName("pushButton")
        
        #----- MAin button
        self.pushButton.clicked.connect(self.Rotate)
        #self.pushButton.clicked.connect(self.Init_board)
        #self.pushButton.clicked.connect(self.show_modal_window)
        self.OpenSettings.clicked.connect(self.show_modal_window)
        #self.pushButton.clicked.connect(self.find_ports)
        #self.pushButton.clicked.connect(QtCore.QCoreApplication.instance().quit)
        
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(330, 30, 215, 390))
        self.label_7.setSizeIncrement(QtCore.QSize(0, 0))
        self.label_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.label_7.setText("")
        self.label_7.setTextFormat(QtCore.Qt.AutoText)
        self.label_7.setPixmap(QtGui.QPixmap("img/logo_vert.png"))
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
        exitAction = QAction(QIcon('img/exit.png'), '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Завершение приложения')
        exitAction.triggered.connect(qApp.quit)

        settingsAction = QAction(QIcon('img/settings.png'), '&Settings', self)
        settingsAction.setShortcut('Ctrl+S')
        settingsAction.setStatusTip('Настройки')
        settingsAction.triggered.connect(self.show_modal_window)
        #exitAction2 = QAction(QIcon('exit2.png'), '&Exit', self)
        #exitAction2.setShortcut('Ctrl+R')
        #exitAction2.setStatusTip('Вызов настроек')
        #exitAction2.triggered.connect(self.show_modal_window)

        #self.centralwidget.setStyleSheet("""
        #            color: white;
        #            background-image: url(img/TmpSVG1.jpg);
        #            background-attachment: scroll;
        #        """)

        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&Файл')
        fileMenu.addAction(exitAction)
        fileMenu.addAction(settingsAction)
        

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('3DQ Rotate')

        self.statusBar().showMessage('Не подключено')
        
        self.show()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Круглый стол"))
        self.groupBox.setTitle(_translate("MainWindow", "Управление"))
        self.label.setText(_translate("MainWindow", "Шаг (°)"))
        #self.lineEdit.setInputMask(_translate("MainWindow", "99999"))
        self.label_2.setText(_translate("MainWindow", "Количество шагов:"))
        self.label_3.setText(_translate("MainWindow", "Скорость вращения:"))
        #self.lineEdit_2.setInputMask(_translate("MainWindow", "99999"))
        self.label_4.setText(_translate("MainWindow", "Задержка перед стартом:"))
        self.label_5.setText(_translate("MainWindow", "Задержка между поворотами:"))
        self.label_6.setText(_translate("MainWindow", "Направление вращения:"))
        #self.lineEdit_3.setInputMask(_translate("MainWindow", "99999"))
        #self.lineEdit_4.setInputMask(_translate("MainWindow", "99999"))
        self.pushButton.setText(_translate("MainWindow", "Старт"))
        self.pushButton.setShortcut(_translate("MainWindow", "Return"))

        self.OpenSettings.setText(_translate("MainWindow", "Настройки"))
        self.OpenSettings.setShortcut(_translate("MainWindow", "Return"))
        
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
