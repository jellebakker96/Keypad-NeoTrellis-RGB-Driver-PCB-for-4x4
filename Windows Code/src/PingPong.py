from Settings import *
from functools import partial
import serial.tools.list_ports
import serial
import atexit
import signal
import time


class PingPong:
    def __init__(self):
        """This class is used to send a message and reads the send message."""

        # Initialize the port variable.
        self.port = ''
        # Get a list of ports.
        ports = list(serial.tools.list_ports.comports())
        # Check which port is for the Arduino.
        for p in ports:
            if "Arduino" in p[1]:
                self.port = p[0]
        print(self.port)
        # Start the serial communications.
        self.ser = serial.Serial(self.port, baudrate, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)

    def write_arduino(self, inp):
        """Handle writing."""

        # Write to the Arduino.
        self.ser.write(inp.encode('utf-8'))

    def read_arduino(self):
        """Handle reading."""

        # Read from the Arduino.
        message = self.ser.read(100)
        return message


def close_port(p):
    """normal shutdown."""

    # Close the port.
    p.ser.close()
    print('port is closed 1')


def close_port_interrupt(p, signal, frame):
    """Interrupt shutdown."""

    # Close the port.
    p.ser.close()
    print('port is closed 2')


def main():
    """PingPong.py test"""

    # Initialize pingpong object.
    p = PingPong()
    # Exit handlers.
    atexit.register(close_port, p)
    signal.signal(signal.SIGINT, partial(close_port_interrupt, p))

    counter = 2
    while True:
        # Write to the Arduino.
        p.write_arduino('12345\n')
        # Read the Arduino.
        message = p.read_arduino()
        # Print message.
        if message:
            print(message)
        # Sleep.
        time.sleep(sleep_time)


if __name__ == '__main__':
    main()
