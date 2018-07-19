# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
import sys

def on_clicked():
    print(spinBox.text())
    print(spinBox.prefix())
    print(spinBox.suffix())
    print(spinBox.value(), type(spinBox.value()))
    print(spinBox.cleanText(), type(spinBox.cleanText()))


def on_value_changed1(x):
    print("on_value_changed1", x)


def on_value_changed2(s):
    print("on_value_changed2", s)


app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.setWindowTitle("Класс QSpinBox")
window.resize(300, 70)
spinBox = QtWidgets.QSpinBox()
spinBox.setRange(0, 100)
spinBox.setValue(10)
spinBox.setSingleStep(5)
spinBox.setPrefix("текст до (")
spinBox.setSuffix(") текст после")
spinBox.valueChanged[int].connect(on_value_changed1)
spinBox.valueChanged[str].connect(on_value_changed2)
button = QtWidgets.QPushButton("Получить значение")
button.clicked.connect(on_clicked)
box = QtWidgets.QVBoxLayout()
box.addWidget(spinBox)
box.addWidget(button)
window.setLayout(box)
window.show()
sys.exit(app.exec_())

