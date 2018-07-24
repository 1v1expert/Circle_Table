# -*- coding: utf-8 -*-
# This file is part of the 3DCircle Project

__author__ = 'Sazonov Vladislav Sergeevich <1v1expert@gmail.com>'
__copyright__ = 'Copyright (C) 2018 VLADDOS'
__license__ = 'GNU General Public License v2 http://www.gnu.org/licenses/gpl2.html'

import sys, glob, time, serial, os, struct, subprocess, threading, struct

std_speeds = ['1843200', '921600', '460800', '230400', '115200', '57600', '38400', '19200', '9600', '4800', '2400',
              '1200', '600', '300', '150', '100', '75', '50']  # Скорость COM порта
paritys = ['N', 'E', 'O']  # Бит четности
stopbitss = [1, 2]  # Количество стоп-бит
bite_size = 8  # Биты данных
t_out = 1  # Таймаут в секундах, должен быть больше 1с
flag1 = 0  # Флаг для остановки программы, устанавливается в 1, если найдена сигнатура
reading_bytes = 10  # Количество байт для чтения после открытия порта
keyword = b'\x00\x00\x00'  # !Сигнатура для поиска
cmd = b'\x00\x34\x65'  # !Команда перед началом приема
ser = serial.Serial()
import logging
logger = logging.getLogger(__name__)

################# Поиск доступных портов windows, linux, cygwin, darwin
def serial_ports():
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        print('Unsupported platform')
        raise EnvironmentError('Unsupported platform')
    
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


##################################
def find_ports():
    std_speeds = ['1843200', '921600', '460800', '230400', '115200', '57600', '38400', '19200', '9600', '4800', '2400',
                  '1200', '600', '300', '150', '100', '75', '50']  # Скорость COM порта
    paritys = ['N', 'E', 'O']  # Бит четности
    stopbitss = [1, 2]  # Количество стоп-бит
    bite_size = 8  # Биты данных
    t_out = 1  # Таймаут в секундах, должен быть больше 1с
    flag1 = 0  # Флаг для остановки программы, устанавливается в 1, если найдена сигнатура
    reading_bytes = 10  # Количество байт для чтения после открытия порта
    keyword = b'\x00\x00\x00'  # !Сигнатура для поиска
    cmd = b'\x00\x34\x65'  # !Команда перед началом приема
    ser = serial.Serial()
    
    print('Сигнатура для поиска ', end='')
    print(keyword)

    ports = serial_ports()
    print('PORTS - ', ports)
    if ports:
        print('Доступные порты:')
        print(ports)
        if len(ports) > 1:
            ser.port = input('Введите адрес COM порта ')
        else:
            ser.port = ports[0]
            print('Работаем с портом ' + ser.port)
    else:
        print('\nНет доступных COM портов, проверьте подключние.\n')
        sys.exit()

    try:
        for stop_bit in stopbitss:
            for parit in paritys:
                for com_speed in std_speeds:
                    ser.close()
                    ser.baudrate = com_speed
                    ser.timeout = t_out
                    ser.bytesize = bite_size
                    ser.parity = parit
                    ser.stopbits = stop_bit
                    ser.open()
                    # ser.write(cmd)                                       #!Раскомментировать при необходимости отправки команды в устройство для инициализации связи
                    message_b = ser.read(reading_bytes)
                    if flag1 == 1:
                        break
                    if message_b:
                        print('\nRAW data on ' + ser.port + ', ' + com_speed + ', ' + str(
                            ser.bytesize) + ', ' + ser.parity + ', ' + str(ser.stopbits) + ':')
                        print('---------------------')
                        print(message_b)
                        print('---------------------')
                        try:
                            if keyword in message_b:
                                print('\n\033[0;33mСигнатура ', end='')  # желтый цвет текста
                                print(keyword, end='')
                                print(' найдена при следующих настройках: \n' + ser.port + ', ' + com_speed + ', ' + str(
                                    ser.bytesize) + ', ' + ser.parity + ', ' + str(ser.stopbits))
                                print('\x1b[0m')
                                ser.close()
                                flag1 = 1
                                break
                            else:
                                ser.close()
                        except:
                            print('error decode')
                            print('---------------------')
                            ser.close()
                    else:
                        print('timeout on ' + ser.port + ', ' + com_speed + ', ' + str(
                            ser.bytesize) + ', ' + ser.parity + ', ' + str(ser.stopbits))
                        print('---------------------')
                        ser.close()
        if flag1 == 0:
            print('Поиск завершен, сигнатура не найдена')
    except serial.SerialException:
        print('Ошибка при открытии порта ' + ser.port)
        sys.exit()

    sys.exit()
    
def start_platform():
    cmd_init = "M17"
    cmd = "G1X-10"
    t_out = 1
    bite_size = 8
    ports = serial_ports()
    print('PORTS - ', ports)

    ser = serial.Serial()
    ser.port = input('Введите адрес COM порта ')
    
    ser.close()
    ser.baudrate = '115200'
    #ser.timeout = t_out
    #ser.bytesize = bite_size
    ser.open()
    print(cmd)
    ser.write(cmd_init.encode('utf-8'))
    message_b = ser.read(reading_bytes)
    print(message_b)
    time.sleep(1)
    ser.write(cmd.encode('utf-8'))
    message_b = ser.read(reading_bytes)
    print(message_b)
    ser.close()

def get_start(serial_name = '/dev/tty.wchusbserial1410', baud_rate = '115200'):
    serial_port = serial.Serial(serial_name, baud_rate, timeout=2)
    is_connected = False
    def motor_reset_origin():
        _send_command("G50")
    def _send_command(req):
        ret = ''
        read_lines = False
        serial_port.flushInput()
        serial_port.flushOutput()
        serial_port.write(req.encode('utf-8') + "\r\n".encode('utf-8'))
        while req != '~' and req != '!' and ret == '':
            ret = serial_port.read(read_lines)
            time.sleep(0.01)
            print(ret)
        print('Vax')
    def OldFirmware():
        print('Old Firmware')
    def motor_speed(value):
        motor_speed = value
        _send_command("G1F{0}".format(value))
        
    def reset():
        serial_port.flushInput()
        serial_port.flushOutput()
        cmd = "\x18\r\n"
        serial_port.write(cmd.encode('utf-8'))  # Ctrl-x
        serial_port.readline()
        
    if serial_port.isOpen():
        print('Port open')
        reset()
        version = serial_port.readline()
        if "Horus 0.1 ['$' for help]" in version.decode('utf-8'):
            raise OldFirmware()
        elif "Horus 0.2 ['$' for help]" in version.decode('utf-8'):
            motor_speed(100)
            serial_port.timeout = 0.05
            is_connected = True
            motor_reset_origin()
            logger.info(" Done")
            _send_command("G1X150")
        serial_port.close()
    else: print('Port closed')

if __name__=='__main__':
    get_start()
    #start_platform()