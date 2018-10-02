# -*- coding: utf-8 -*-
# This file is part of the 3DCircle Project

__author__ = 'Sazonov Vladislav Sergeevich <1v1expert@gmail.com>'
__copyright__ = 'Copyright (C) 2018 VLADDOS'
__license__ = 'GNU General Public License v2 http://www.gnu.org/licenses/gpl2.html'

import main, board
import sys
from PyQt5.QtWidgets import QApplication
import logging

logging.basicConfig(filename='3dcircle.log',
                    format = u'%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)

if __name__=='__main__':
    app = QApplication(sys.argv)
    try:
        configuration = board.read_configuration()
        logging.info('Success read configuration')
    except:
        configuration = {}
        logging.error('Error read configuration')
    #-- Socket connection --
    #board = board.Board(config=configuration, serial_name="192.168.1.124", baud_rate=22)
    #board.is_serial = False
    #board.connect()
    #--- Start princore
    #p = printcore.printcore("192.168.1.124:22", 250000)
    #p.connect(port="192.168.1.124:22", baud=250000)
    #p.disconnect()
    
    ui = main.Ui_MainWindow(configuration)
    sys.exit(app.exec_())
