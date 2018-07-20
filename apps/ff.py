# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from PyQt5.QtWidgets import (QMainWindow, QAction, qApp, QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QHBoxLayout)
from PyQt5.QtWidgets import (QWidget, QPushButton,
    QHBoxLayout, QVBoxLayout, QApplication)

def show_modal_window():
    global modalWindow
    #Часть 11. Создание оконных приложений
    modalWindow = QWidget(windowl, QtCore.Qt.Window)
    modalWindow.setWindowTitle("Moдaльнoe окно")
    modalWindow.resize(100, 50)
    #modalWindow.setWindowModality(QtCore.Qt.WindowModal)
    modalWindow.setAttribute(QtCore.Qt.WA_DeleteOnClose, True)
    modalWindow.move(windowl.geometry().center() - modalWindow.rect().center() - QtCore.QPoint(100, 50))
    modalWindow.show()
    
app = QApplication(sys.argv)
windowl = QWidget()
windowl.setWindowTitle("Moдaльнoe окно 2")
windowl.resize(300, 100)
button = QtWidgets.QPushButton( "Открьrгь модальное окно")
button.clicked.connect(show_modal_window)
#QtCore.QObject.connect(button, QtCore.SIGNAL("clicked()"), show_modal_window)
vbox = QVBoxLayout()
vbox.addWidget(button)
windowl.setLayout(vbox)
windowl.show ()
window2 = QWidget()
window2.setWindowTitle("Это окно не будет блокировано")
window2.resize(500, 100)
window2.show()
#sys.exit(app.exec_())
sys.exit(app.exec_())