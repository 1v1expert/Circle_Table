# -*- coding: utf-8 -*-
# This file is part of the 3DCircle Project

__author__ = 'Sazonov Vladislav Sergeevich <1v1expert@gmail.com>'
__copyright__ = 'Copyright (C) 2018 VLADDOS'
__license__ = 'GNU General Public License v2 http://www.gnu.org/licenses/gpl2.html'

import main
import sys
from PyQt5.QtWidgets import QApplication
import logging

logging.basicConfig(filename='3dcircle.log', level=logging.INFO)

if __name__=='__main__':
    app = QApplication(sys.argv)
    ui = main.Ui_MainWindow()
    logging.info('Success start APP')
    sys.exit(app.exec_())
