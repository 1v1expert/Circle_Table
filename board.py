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
import collections
import socket
import re

logger = logging.getLogger(__name__)

system = platform.system()


def read_configuration():
    with open('config.json', 'rb') as jfile:
        data = jfile.read().decode("utf-8").replace("'", '"')
        jf_file = json.loads(data)
        data_restruct = collections.OrderedDict(jf_file)
        return data_restruct

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

    """Board class. For accessing to the scanner board"""

    def __init__(self, config, parent=None, serial_name='', baud_rate=250000):
        self.parent = parent
        self.serial_name = serial_name
        self.baud_rate = baud_rate
        self.unplug_callback = None
        self.is_serial = True
        self._serial_port = None
        self._is_connected = False
        self._motor_enabled = False
        self._motor_position = 0
        self._motor_speed = 750
        self._motor_acceleration = 0
        self._motor_direction = 1
        self._tries = 0  # Check if command fails
        self.configuration = config
        self.load_configuration()
        self.rate = 750
    
    def connect_serial(self):
        """Open serial port and perform handshake"""
        logger.info("Connecting board {0} {1}".format(self.serial_name, self.baud_rate))
        self._is_connected = False
        try:
            self._serial_port = serial.Serial(self.serial_name, self.baud_rate, timeout=2)
            if self._serial_port.isOpen():
                logger.info("Try openning serial port on {0}\n".format(system))
                version = self._serial_port.readlines()
                #version_msg = "Version: {}".format(version)
                logger.info(version)
                #time.sleep(2)
                #self.motor_enable()
                #info = self.read(False)
                self._serial_port.timeout = 0.05
                self._is_connected = True
                #time.sleep(2)
                #self.motor_move(step=0)
                #info = self.read(False)
                #print(info)
                self.init_load_conf()
            else:
                raise BoardNotConnected()
        except Exception as exception:
            logger.error("Error opening the port {0}\n".format(self.serial_name))
            self._serial_port = None
            return False  # raise exception
        if self._is_connected:
            logger.info("Init board done")
            return True
        else:
            logger.error("ERROR CONNECTING TO BOARD")
            return False  # else:  # return False  # raise WrongFirmware()
    
    def connect_socket(self):
        """Open socket port and perform handshake"""
        logger.info("Connecting board {0} {1}".format(self.serial_name, self.baud_rate))
        self._is_connected = False
        # Connect to socket if "port" is an IP, device if not
        #host_regexp = re.compile("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$|^(([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z0-9]|[A-Za-z0-9][A-Za-z0-9\-]*[A-Za-z0-9])$")
        self.printer_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.printer_tcp.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.timeout = 0.25
        self.printer_tcp.settimeout(1.0)
        try:
            self.printer_tcp.connect((self.serial_name, self.baud_rate))
            self.printer_tcp.settimeout(self.timeout)
            self.printer = self.printer_tcp.makefile()
            print(self.printer_tcp, "\n----\n", self.printer)
        except socket.error as e:
            if (e.strerror is None): e.strerror = ""
            logger.error(_("Could not connect to %s:%s:") % (self.serial_name, self.baud_rate) + "\n" + _(
                "Socket error %s:") % e.errno + "\n" + e.strerror)
            self.printer = None
            self.printer_tcp = None
            return

    def connect(self):
        if self.is_serial:
            return self.connect_serial()
        else:
            return self.connect_socket()
    
    def load_configuration(self):
        if self.configuration:
            try:
                #self.rotation_speeds = collections.OrderedDict(self.configuration['Rotational_speed'])
                #self.list_rates =
                self.list_rates = list()
                #print(lambda x: y.append(x)(for value in self.configuration['Rotational_speed']))
                for keys in self.configuration['Rotational_speed']:
                    for key in keys.keys():
                        self.list_rates.append(key)
                self.delay_before_start = self.configuration['Default_settings']['Delay_before_start']
                self.delay_between_turns = self.configuration['Default_settings']['Delay_between_turns']
                self.steps = self.configuration['Default_settings']['Steps']
                self.degrees = self.configuration['Default_settings']['Degrees']
                self.cmd_delay_sends = self.configuration['Delay_command']
                self.use_delay_command = self.configuration['Use_delay_command']
                self.ini_commands = self.configuration['Init_command']
                self.use_init_command = self.configuration['Use_init_command']
                #Size main window
                self.width_window = self.configuration['Width_window']
                self.height_window = self.configuration['Height_window']
                # Set command roatet
                self.command_of_rotate = self.configuration['Command_of_rotate']
                # Set host ip
                self.host_ip = self.configuration['Host_ip']
                # Set position coordinate
                self.coordinate_absolute = self.configuration['Coordinate_absolute']
                
            except:
                logging.error("No loaded configuration from file")
                self.def_settings()
        else:
            logging.error("No loaded configuration from file")
            self.def_settings()
            
    def def_settings(self):
        self.list_rates = ['медленно', 'средне', 'быстро']
        self.delay_before_start = 0
        self.delay_between_turns = 1
        self.steps = 1
        self.degrees = 10
        self.ini_commands = []
        self.cmd_delay_sends = "G4 S{0}"
        self.command_of_rotate = "G1X{0}F{1}"
        self.use_delay_command = False
        self.use_init_command = False
        # Size main window
        self.width_window = 550
        self.height_window = 500
        # Set host ip
        self.host_ip = "127.0.0.1"
        # Set position coordinate
        self.coordinate_absolute = False
        
    def init_load_conf(self):
        try:
            if len(self.ini_commands) > 0 and self.use_init_command:
                for cmd in self.ini_commands:
                    command = cmd['command'] # No sure there
                    self._send_command(command)
                    response = self._serial_port.readlines()
                    print(command, ' -Succes send init command, response: ', response)
            else:
                logger.info('No find configuration or not command for init command')
        except:
            logger.error('Error load init configuration commands')
            
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
            #if self._motor_speed != value:
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
    
    def delay_sends(self, sec=0):
        if self._is_connected and self.use_delay_command:
            self._send_command(self.cmd_delay_sends.format(sec))

    def motor_reset_origin(self):
        if self._is_connected:
            self._send_command("G50")
            self._motor_position = 0

    def motor_move(self, step=0, nonblocking=True, callback=True):
        if self._is_connected:
            self._motor_position += step * self._motor_direction
            print(self._motor_position)
            self.send_command("G1X{0}".format(self._motor_position), nonblocking, callback)
            #self.send_command("G1X{0}".format(self._motor_position), nonblocking, callback)
    
    def motor_move_exchange(self, step=0, rate=0, nonblocking=True, callback=True):
        if self._is_connected:
            self.set_attempt = step/rate * 60
            if self.coordinate_absolute:
                self._motor_position += step * self._motor_direction
                self.send_command(self.command_of_rotate.format(self._motor_position, rate), nonblocking, callback, False, self.set_attempt)
            else:
                self.send_command(self.command_of_rotate.format(step * self._motor_direction, rate), nonblocking, callback, False, self.set_attempt)

    def send_command(self, req, nonblocking=False, callback=None, read_lines=False, attempt=0.0):
        if nonblocking:
            threading.Thread(target=self._send_command,
                             args=(req, attempt, callback, read_lines)).start()
        else:
            self._send_command(req, attempt, callback, read_lines)

    def _send_command(self, req, set_attempt=0.0, callback=None, read_lines=False):
        """Sends the request and returns the response"""
        ret = ''
        req = req.encode('utf-8')
        if self._is_connected and req != '':
            if self._serial_port is not None and self._serial_port.isOpen():
                try:
                    self._serial_port.flushInput()
                    self._serial_port.flushOutput()
                    self._serial_port.write(req + "\n".encode('utf-8'))
                    attempt = 0
                    print('Set_attempt -', set_attempt/0.01)
                    while req != '~' and req != '!' and ret == '':
                        if ret =='': attempt += 1
                        #ret = self._serial_port.readlines()
                        ret = self.read(read_lines)
                        logmsg = 'Send command: {}, request post: {}'.format(req, ret)
                        logger.info(logmsg)
                        print('Attempt: ', attempt, ', ret = ', ret, ', req=', req)
                        time.sleep(0.01)
                        if set_attempt:
                            if attempt > set_attempt/0.01:
                                logger.error('Fail, no answer from board')
                                self._is_connected = False
                                break
                        else:
                            if attempt > 100:
                                logger.error('Fail, no answer from board')
                                self._is_connected = False
                                break
                    else:
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
