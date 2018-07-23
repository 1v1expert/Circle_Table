# -*- coding: utf-8 -*-

#
#
# Created by: VLADDOS
#
#

import main
import sys
from PyQt5.QtWidgets import QApplication

if __name__=='__main__':
    app = QApplication(sys.argv)
    ui = main.Ui_MainWindow()
    sys.exit(app.exec_())
