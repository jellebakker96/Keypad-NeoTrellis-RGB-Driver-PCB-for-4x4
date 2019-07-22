from Settings import *
from functools import partial
import serial.tools.list_ports
import serial
import atexit
import signal
import time

class PingPong:
    def __init__(self):
        self.port = ''
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "Arduino" in p[1]:
                self.port = p[0]
        print(self.port)
        self.ser = serial.Serial(self.port, baudrate, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)

    def write_arduino(self,inp):
        self.ser.write(inp.encode('utf-8'))

    def read_arduino(self):
        message = self.ser.read(100)
        return message

def close_port(p): # normal shutdown
    p.ser.close()
    print('port is closed 1')


def close_port_interrupt(p, signal, frame): # interrupt shutdown
    p.ser.close()
    print('port is closed 2')


def main():
    p = PingPong()
    atexit.register(close_port,p)
    signal.signal(signal.SIGINT, partial(close_port_interrupt,p))

    counter = 2
    while True:
        p.write_arduino('12345\n')
        message = p.read_arduino()
        if message:
            print(message)
        time.sleep(sleep_time)


if __name__ == '__main__':
    main()
