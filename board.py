# -*- coding: utf-8 -*-
# This file is part of the 3DCircle Project

__author__ = 'Sazonov Vladislav Sergeevich <1v1expert@gmail.com>'
__copyright__ = 'Copyright (C) 2018 VLADDOS'
__license__ = 'GNU General Public License v2 http://www.gnu.org/licenses/gpl2.html'

import time
import glob
import threading
import platform
import serial
import json
import logging

logger = logging.getLogger(__name__)

system = platform.system()


def read_configuration(self):
    with open('config.json') as jfile:
        jf_file = json.load(jfile)
        return jf_file

class WrongFirmware(Exception):

    def __init__(self):
        Exception.__init__(self, "Wrong Firmware")


class BoardNotConnected(Exception):

    def __init__(self):
        Exception.__init__(self, "Board Not Connected")


class OldFirmware(Exception):

    def __init__(self):
        Exception.__init__(self, "Old Firmware")


class Board(object):

    """Board class. For accessing to the scanner board

    Gcode commands:

        G1 Fnnn : feed rate
        G1 Xnnn : move motor
        G50     : reset origin position

    """

    def __init__(self, parent=None, serial_name='', baud_rate=250000):
        self.parent = parent
        self.serial_name = serial_name
        self.baud_rate = baud_rate
        self.unplug_callback = None

        self._serial_port = None
        self._is_connected = False
        self._motor_enabled = False
        self._motor_position = 0
        self._motor_speed = 750
        self._motor_acceleration = 0
        self._motor_direction = 1
        self._laser_number = 2
        self._laser_enabled = self._laser_number * [False]
        self._tries = 0  # Check if command fails
    
    def connect(self):
        """Open serial port and perform handshake"""
        logger.info("Connecting board {0} {1}".format(self.serial_name, self.baud_rate))
        self._is_connected = False
        try:
            self._serial_port = serial.Serial(self.serial_name, self.baud_rate, timeout=2)
            if self._serial_port.isOpen():
                logger.info("Try openning serial port on {0}\n".format(system))
                
                version = self._serial_port.readlines()
                logger.info(" Version: ", version)
                #if version:
                #    for ver in version:
                #        if "1.1.0-RC7_3DQ0.2" in ver.decode('utf-8'):
                #            print('SUCCESS INPLUG')
                #        else:
                #            logger.info(" Error connect, not found 1.1.0-RC7_3DQ0.2 in FIRMWARE")
                #            return False
                #    logger.info(version)
                #else:
                #    return False
                #info = self.read(True)
                #print(info)
                
                
                #self._serial_port.write("G1X10".encode('utf-8'))
                #G1F{0}
                #version = self._serial_port.readlines()
                #print(version)
                #self._serial_port.write("G1F5000".encode('utf-8'))
                #version = self._serial_port.readlines()
                #print(version)
                #self._serial_port.write("G1X100".encode('utf-8'))
                #while version != "b''":
                #    version = self._serial_port.readline()
                #    print(version)
                #if "Horus 0.1 ['$' for help]" in version.decode('utf-8'):
                #    raise OldFirmware()
                # elif "Horus 0.2 ['$' for help]" in version.decode('utf-8'):
                #if version.decode('utf-8'):
                #self._reset()  # Force Reset and flush
                #-----
                time.sleep(2)
                self.motor_enable()
                info = self.read(False)
                print(info)
                #------
                #time.sleep(2)
                #self.motor_move(20)
                #info = self.read(False)
                #print(info)
                #version = self._serial_port.readlines()
                #for ver in version:
                #    print(ver.decode('utf-8'))
                #version = self._serial_port.readline()
                #print(version)
                self._serial_port.timeout = 0.05
                self._is_connected = True
                time.sleep(2)
                self.motor_move(step=0)
                info = self.read(False)
                print(info)
                try:
                    jf_file = read_configuration()
                    for cmd in jf_file['Init_command']:
                        self._send_command(cmd['command'])
                        response = self._serial_port.readlines()
                        time.sleep(0.5)
                        print(response)
                    logger.info(" Success loaded config file")
                except:
                    logger.info(" Error loaded configuration file")
                #self._send_command("M92 X45.3")
                
                #self._send_command("G92 X0")

                #self._send_command("G91")
                #info = self.read(False)
                #print(info)
                # Set current position as origin
                #self.motor_reset_origin()
                logger.info(" Done")
                return True
                #else:
                    #return False
                    #raise WrongFirmware()
            else:
                raise BoardNotConnected()
        except Exception as exception:
            logger.error("Error opening the port {0}\n".format(self.serial_name))
            self._serial_port = None
            return False
            #raise exception

    def disconnect(self):
        """Close serial port"""
        if self._is_connected:
            logger.info("Disconnecting board {0}".format(self.serial_name))
            try:
                if self._serial_port is not None:
                    self.motor_disable()
                    self._is_connected = False
                    self._serial_port.close()
                    del self._serial_port
            except serial.SerialException:
                logger.error("Error closing the port {0}\n".format(self.serial_name))
            logger.info(" Done")

    def set_unplug_callback(self, value):
        self.unplug_callback = value

    def motor_invert(self, value):
        if value:
            self._motor_direction = -1
        else:
            self._motor_direction = +1

    def motor_speed(self, value):
        if self._is_connected:
            if self._motor_speed != value:
                self._motor_speed = value
                self._send_command("G1F{0}".format(value))

    def motor_acceleration(self, value):
        if self._is_connected:
            if self._motor_acceleration != value:
                self._motor_acceleration = value
                self._send_command("$120={0}".format(value))

    def motor_enable(self):
        if self._is_connected:
            if not self._motor_enabled:
                self._motor_enabled = True
                # Save current speed value
                speed = self._motor_speed
                self.motor_speed(1)
                # Enable stepper motor
                self._send_command("M17")
                time.sleep(1)
                # Restore speed value
                self.motor_speed(speed)

    def motor_disable(self):
        if self._is_connected:
            if self._motor_enabled:
                self._motor_enabled = False
                self._send_command("M18")

    def motor_reset_origin(self):
        if self._is_connected:
            self._send_command("G50")
            self._motor_position = 0

    def motor_move(self, step=0, nonblocking=True, callback=True):
        if self._is_connected:
            self._motor_position += step * self._motor_direction
            print(self._motor_position)
            self.send_command("G1X{0}".format(step), nonblocking, callback)
            #self.send_command("G1X{0}".format(self._motor_position), nonblocking, callback)


    def send_command(self, req, nonblocking=False, callback=None, read_lines=False):
        if nonblocking:
            threading.Thread(target=self._send_command,
                             args=(req, callback, read_lines)).start()
        else:
            self._send_command(req, callback, read_lines)

    def _send_command(self, req, callback=None, read_lines=False):
        """Sends the request and returns the response"""
        ret = ''
        req = req.encode('utf-8')
        if self._is_connected and req != '':
            if self._serial_port is not None and self._serial_port.isOpen():
                try:
                    self._serial_port.flushInput()
                    self._serial_port.flushOutput()
                    self._serial_port.write(req + "\n".encode('utf-8'))
                    while req != '~' and req != '!' and ret == '':
                        #ret = self._serial_port.readlines()
                        ret = self.read(read_lines)
                        #self._reset()
                        print('ret = ', ret, 'req=', req)
                        time.sleep(0.01)
                    self._success()
                    #ret = self.read(read_lines)
                    print('succes send command')
                except:
                    print("False send command")
                    if hasattr(self, '_serial_port'):
                        if callback is not None:
                            callback(ret)
                        self._fail()
        if callback is not None:
            print(ret)
            #callback(ret)
        return ret

    def read(self, read_lines=False):
        if read_lines:
            return ''.join(self._serial_port.readlines())
        else:
            return ''.join(self._serial_port.readline().decode('utf-8'))

    def _success(self):
        self._tries = 0

    def _fail(self):
        if self._is_connected:
            logger.debug("Board fail")
            self._tries += 1
            if self._tries >= 3:
                self._tries = 0
                if self.unplug_callback is not None and \
                   self.parent is not None and \
                   not self.parent.unplugged:
                    self.parent.unplugged = True
                    self.unplug_callback()

    def _reset(self):
        self._serial_port.flushInput()
        self._serial_port.flushOutput()
        self._serial_port.write("\x18\r\n".encode('utf-8'))  # Ctrl-x
        self._serial_port.readline()

    def get_serial_list(self):
        """Obtain list of serial devices"""
        baselist = []
        if system == 'Windows':
            import winreg
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_LOCAL_MACHINE, "HARDWARE\\DEVICEMAP\\SERIALCOMM")
                i = 0
                while True:
                    try:
                        values = winreg.EnumValue(key, i)
                    except:
                        return baselist
                    if 'USBSER' in values[0] or \
                       'VCP' in values[0] or \
                       '\Device\Serial' in values[0]:
                        baselist.append(values[1])
                    i += 1
            except:
                return baselist
        else:
            for device in ['/dev/ttyACM*', '/dev/ttyUSB*', '/dev/tty.usb*', '/dev/tty.wchusb*',
                           '/dev/cu.*', '/dev/rfcomm*']:
                baselist = baselist + glob.glob(device)
        return baselist
