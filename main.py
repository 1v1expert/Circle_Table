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
import board
import time
import logging


logger = logging.getLogger(__name__)

class Ui_MainWindow(QMainWindow):
    def __init__(self, config):
        self.invert = False
        self.configuration = config
        self.is_socket = False
        self.board = board.Board(config=self.configuration)
        self.std_speeds = self.board.baudrate # Скорость COM порта
        self.online = False
        #self.check_open_ports()
        #self.configuration = board.read_configuration(self)
        #print(self.configuration['Rotational_speed'].keys())
        #.encode('cp1251')
        super().__init__()
        self.setupUi(self)
        self.testApp()
        
        logging.info('Success init app')
        
    def check_open_ports(self):
        self.is_open_port = True
        if not self.board.serial_name:
            if (len(self.board.serial_list)):
                self.board.serial_name = self.board.serial_list[0]
            else:
                self.is_open_port = False
                self.statusBar().showMessage('Нет доступного порта')

    def motor_invert(self, choose):
        if choose == 'Инверс':
            self.board.motor_invert(True)
        else:
            self.board.motor_invert(False)
    
    def testApp(self):
        print('Rate - {0}, Steps - {1}, Degrees - {2}'.format(self.board.rate, self.board.steps, self.board.degrees))
        
    def ChangeRate_motor(self, rate):
        try:
            for key in self.configuration['Rotational_speed']:
                if key.get(rate): self.board.rate = key.get(rate)
        except:
            if rate == "медленно": self.board.rate = 750
            elif rate == "средне": self.board.rate = 3750
            elif rate == "быстро": self.board.rate = 7500
            #self.board._motor_speed = speed
        #self.board.motor_speed(self.board.rate)

    def onChanged(self, text):
        self.lineEdit.setText(text)
        self.lineEdit.adjustSize()

    def onSetSerial(self, serial_name):
        self.board.serial_name = serial_name
        
    def onSetSerialSpeeds(self, speed):
        self.board.baud_rate = int(speed)
    
    def onConnectBoardTelnet(self):
        """ Connect device to telnet protocol """
        #tn = telnetlib.Telnet("192.168.1.124", "22")
        #tn.write(b"STATUS\n\n")
        #request = tn.read_all()
        text = self.port_connection.text()
        #text_after = ""
        #for char in text:
        #    try: a_char = int(char)
        #    except: a_char = char
        #    if isinstance(a_char, int):
        #        text_after += str(a_char)
        if self.comboBox_SerialPorts.lineEdit():
            print('LINEEDIT-', self.comboBox_SerialPorts.currentText())
        ports = [port for port in text.split() if port.isdigit()]
        self.dest = self.address_connection.text() + ":" + ports[0]
        # --- Start princore\
        print(self.dest)
    def triggerConnect(self):
        _translate = QtCore.QCoreApplication.translate
        self.online = not self.online
        if self.online:
            #self.ConnectButtonSerial.destroy()
            self.ConnectButtonSerial.setText("отключить")
            self.statusBar().showMessage('Подключено')
            self.modalWindow.close()
        else:
            self.statusBar().showMessage('Отключено')
            self.ConnectButtonSerial.setText("подключить")
            self.modalWindow.close()
        
    def onConnectBoard(self):
        self.serialPort = self.comboBox_SerialPorts.currentText()
        if self.online:
            self.board.disconnect()
            self.triggerConnect()
        else:
            if self.serialPort:
                self.board.serial_name = self.serialPort
                if self.board.connect():
                    self.triggerConnect()
                else:
                    self.statusBar().showMessage('Не удалось подключиться')
                    self.modalWindow.close()
            else:
                self.statusBar().showMessage('Нет доступного порта')
                self.modalWindow.close()
                time.sleep(0.7)
                self.show_modal_window()
    
    def changeDegrees(self, degree):
        self.board.degrees = degree
        
    def changeSteps(self, step):
        self.board.steps = step
    
    def ChangeDelay_before_start(self, sec):
        self.board.delay_before_start = sec
    
    def Changedelay_between_turns(self, sec):
        self.board.delay_between_turns = sec
        
    def Rotate(self):
        if not self.board._is_connected:
            if self.online:
                self.triggerConnect()
        if self.board._is_connected:
            try:
                if self.board.is_serial:
                    time.sleep(self.board.delay_before_start)
                    self.board.delay_sends(sec=self.board.delay_before_start) #Should me rewrite
                    self.testApp()
                    for rt in range(self.board.steps):
                        self.board.motor_move_exchange(step=self.board.degrees, rate=self.board.rate)
                        if rt == self.board.steps or self.board.steps == 1:
                            pass
                        else:
                            self.board.delay_sends(sec=self.board.delay_between_turns)
                    logger.info('-----FINISH ROTATE----')
                else:
                    time.sleep(self.board.delay_before_start)
                    self.board.delay_sends(sec=self.board.delay_before_start)
                    for rt in range(self.board.steps):
                        self.board.motor_move_exchange(step=self.board.degrees, rate=self.board.rate)
                        if rt == self.board.steps or self.board.steps == 1:
                            pass
                        else:
                            self.board.delay_sends(sec=self.board.delay_between_turns)
            except:
                self.triggerConnect()
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
        self.comboBox_SerialPorts.setEditable(True)
        if (len(self.board.serial_list)):
            self.comboBox_SerialPorts.addItems(self.board.serial_list)
        else:
            self.comboBox_SerialPorts.addItems(['Устройства не найдены'])
        self.comboBox_SerialPorts.activated[str].connect(self.onSetSerial)

        self.comboBox_Std_speeds_board = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_Std_speeds_board.setGeometry(QtCore.QRect(300, 25, 120, 22))
        self.comboBox_Std_speeds_board.setCurrentText("")
        self.comboBox_Std_speeds_board.setMaxVisibleItems(12)
        self.comboBox_Std_speeds_board.setObjectName("comboBox_Std_speeds")
        #self.comboBox_Std_speeds_board.setEditable(True)
        self.comboBox_Std_speeds_board.addItems(self.std_speeds)
        self.comboBox_Std_speeds_board.activated[str].connect(self.onSetSerialSpeeds)
        
        #self.address_connection = QtWidgets.QLineEdit(self.groupBox)
        #self.address_connection.setInputMask('090.090.090.090')
        #self.address_connection.setText(self.board.host_ip)
        #self.address_connection.setGeometry(QtCore.QRect(65, 55, 131, 22))
        #self.port_connection.valueChanged[int].connect(self.Changedelay_between_turns)
        #self.address_connection.setVisible(True)
        
        #self.port_connection = QtWidgets.QSpinBox(self.groupBox)
        #self.port_connection.setRange(0, 99999)
        #self.port_connection.setValue(22)
        #self.port_connection.setSingleStep(1)
        #self.port_connection.setSuffix(" порт")
        #self.port_connection.setGeometry(QtCore.QRect(310, 55, 80, 22))
        #self.port_connection.valueChanged[int].connect(self.Changedelay_between_turns)
        #self.port_connection.setVisible(True)

        #self.flo = QtWidgets.QFormLayout()
        #self.flo.addRow("integer validator", self.port_connection)

        #self.ConnectButtonTelnet = QtWidgets.QPushButton(self.groupBox)
        #self.ConnectButtonTelnet.setGeometry(QtCore.QRect(10, 80, 180, 51))
        #self.ConnectButtonTelnet.setCheckable(False)
        #self.ConnectButtonTelnet.setObjectName("pushButton")
        #self.ConnectButtonTelnet.setText(_translate("MainWindow", "Telnet"))
        #self.ConnectButtonTelnet.clicked.connect(self.onConnectBoardTelnet)
        
        self.ConnectButtonSerial = QtWidgets.QPushButton(self.groupBox)
        self.ConnectButtonSerial.setGeometry(QtCore.QRect(120, 65, 180, 51))
        self.ConnectButtonSerial.setCheckable(True)
        self.ConnectButtonSerial.setObjectName("ConnectButtonSerial")
        if self.online:
            self.ConnectButtonSerial.setText("отключить")
        else:
            self.ConnectButtonSerial.setText("подключить")
        self.ConnectButtonSerial.clicked.connect(self.onConnectBoard)
        
        self.modalWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
        #self.modalWindow.setLayout(self.flo)
        self.modalWindow.move(self.geometry().center() - self.modalWindow.rect().center() - QtCore.QPoint(100, 50))
        
        self.modalWindow.show()
        
    def setupUi(self, MainWindow):
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.board.width_window, self.board.height_window)
        MainWindow.setMinimumSize(QtCore.QSize(self.board.width_window, self.board.height_window))
        MainWindow.setMaximumSize(QtCore.QSize(self.board.width_window, self.board.height_window))
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
        #-- Set Font --
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        
        self.label.setFont(font)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")

        self.DegreesSpinBox = QtWidgets.QSpinBox(self.groupBox)
        self.DegreesSpinBox.setRange(0, 1000)
        self.DegreesSpinBox.setValue(self.board.degrees)
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
        self.RateComboBox.addItems(self.board.list_rates)
        self.RateComboBox.activated[str].connect(self.ChangeRate_motor)
        ## ---
        # -- Choose steps degrees --
        self.ValueStepsSpinBox = QtWidgets.QSpinBox(self.groupBox)
        self.ValueStepsSpinBox.setRange(0, 100)
        self.ValueStepsSpinBox.setValue(self.board.steps)
        self.ValueStepsSpinBox.setSingleStep(1)
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
        self.Delay_between_turns.setValue(self.board.delay_between_turns)
        self.Delay_between_turns.setSingleStep(10)
        self.Delay_between_turns.setSuffix(" c")
        self.Delay_between_turns.setGeometry(QtCore.QRect(190, 240, 113, 20))
        self.Delay_between_turns.valueChanged[int].connect(self.Changedelay_between_turns)
        

        self.Delay_before_start = QtWidgets.QSpinBox(self.groupBox)
        self.Delay_before_start.setRange(0, 1000)
        self.Delay_before_start.setValue(self.board.delay_before_start)
        self.Delay_before_start.setSingleStep(10)
        self.Delay_before_start.setSuffix(" c")
        self.Delay_before_start.setGeometry(QtCore.QRect(190, 190, 113, 20))
        self.Delay_before_start.valueChanged[int].connect(self.ChangeDelay_before_start)


        self.OpenSettings = QtWidgets.QPushButton(self.groupBox)
        self.OpenSettings.setGeometry(QtCore.QRect(150, 340, 121, 51))
        self.OpenSettings.setCheckable(True)
        self.OpenSettings.setObjectName("OpenSettings")
        
        self.pushButton = QtWidgets.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(30, 340, 121, 51))
        self.pushButton.setCheckable(True)
        self.pushButton.setObjectName("pushButton")
        
        #----- MAin button
        self.pushButton.clicked.connect(self.Rotate)
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
        self.label_4.setText(_translate("MainWindow", "Задержка перед стартом:"))
        self.label_5.setText(_translate("MainWindow", "Задержка между поворотами:"))
        self.label_6.setText(_translate("MainWindow", "Направление вращения:"))
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
    ui = Ui_MainWindow()
    sys.exit(app.exec_())
