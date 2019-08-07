from ConfigHandler import *
from functools import partial
import serial.tools.list_ports
import serial
import atexit
import signal


class ArduinoCommunication:
    def __init__(self, settings, debugging, changed_color, log):
        self.settings = settings
        self.debugging = debugging[0][0]
        self.changed_color = changed_color
        self.l = log
        self.start_counter_state = False  # keep track if the arduino is going through its setup correctly
        self.start_ctr = 0  # variable used to count the arduino setup time, if it is to long a message will be printed
        self.port = []  # variable to store the port connected to an arduino
        self.port_old = []  # ald port variable to check if it has changed
        self.port_found = False  # Used to see if a port was found
        self.get_arduino_port()
        self.initialize_ser()

    def initialize_ser(self):
        if self.port_found:
            for num, port in enumerate(self.port):
                try:
                    self.ser = serial.Serial(port, baudrate, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
                    self.l.logger('connected to {}'.format(port), self.debugging)
                    break
                except serial.serialutil.SerialException:
                    self.l.logger('tried to connect to {} but attempted failed'.format(port), self.debugging)
                    print(port)

                    if num >= len(self.port) - 1:
                        self.connection_error_detected('Het lijkt er op dat je dit progamma for de tweede keer probeerd'
                                                       ' te starten,\n Dit wordt niet ondersteunt.\n Het kan ook zijn'
                                                       ' dat er een ander programa is dat verbinding maakt met de '
                                                       'aruino.')

    def get_arduino_port(self):
        self.port_old = copy.deepcopy(self.port)
        self.port.clear()
        self.port_found = False
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if "Arduino" in p[1]:
                self.port.append(p[0])
                self.port_found = True
        if self.port_found:
            self.l.logger(
                'Er zijn {} arduinos gevonden. Er wordt verbinding gemaakt met de eerste arduino of de eene die '
                'een open port heeft\nDe volgende porten zijn gevonden {}'.format(len(self.port), self.port),
                self.debugging)

    def update_arduino_port(self):
        if (self.port_old != self.port) and self.port_found:
            if not self.port_old:  # this makes sure that you can fist start the program and then connect the keypad
                self.initialize_ser()
            else:  # a new arduino has been connected, a connection will be made with the new arduino
                for port in self.port:
                    if port in self.port:
                        self.ser.port = port

    def write_arduino(self, inp):  # check if a port was found and if you can connect to it
        if self.port_found:
            inp_byte = (inp + "\n").encode('utf-8')
            try:
                self.ser.write(inp_byte)
                # print('This is writen: {}'.format(inp_byte))
            except serial.serialutil.SerialException:
                return
            self.ser.flush()
            time.sleep(wait_write)  # wait to make sure everything has been send

    def read_arduino(self):
        message_int = []
        if self.port_found:  # check if a port was found and if you can connect to it
            try:
                message = self.ser.read(100)  # read up to one hundred bytes or as much is in the buffer
            except serial.serialutil.SerialException:
                return False
            mes_dec = message.decode('utf-8')  # decode bytes
            mes_split = mes_dec.split('\n')  # split message
            try:  # needed for if you want to switch to an other usb port. The data becomes corrupted
                mes_split.remove('')  # clean message
            except ValueError:
                return False

            mes_clean = [i.strip() for i in mes_split]
            if self.start_counter_state and self.port_found:
                self.start_ctr += 1
            if self.start_ctr > 10 and self.port_found:
                self.start_counter_state = False  # the arduino setup failed
                self.connection_error_detected('De arduino kan geen verbinding maken met de knoppen, kijk of alle '
                                               'draaden goed zijn verbonden')
                return False

            if not mes_clean:  # check if there was a message
                return False
            if mes_clean[0] == 'start':
                self.start_counter_state = True
                if len(mes_clean) > 1:  # it is possible that the 'done' message is read immediately
                    if mes_clean[1] == 'done':
                        self.start_counter_state = False
                return False
            elif mes_clean[0] == 'done':
                self.start_counter_state = False
                self.start_ctr = 0
                print('tests 2')
                return False

            try:  # convert to integers to represent buttons
                for mes in mes_clean:
                    message_int.append(int(mes))
                return message_int
            except ValueError:
                self.l.logger('Arduino geeft geen correct getal, arduino output is:\n{}'.format(message))
                return False
        return False

    def update_color(self):
        if self.port_found:
            for i in range(16):
                self.write_arduino(str(i).zfill(2) + str(self.settings[i][4]).zfill(3))

    def connection_error_detected(self, inp):
        self.l.logger(inp)
        self.l.logger('\nHet programma wordt afgesloten.\nJe kunt 4 dingen doen.'
                      '\n1) Installeer het programma opnieuw om een nieuwe config file te maken.'
                      '\n2) Verbind de 9 toetsen eerst voordat je het programma start'
                      '\n3) Zorg er voor dat maar 1 toetsenbord (die 9 knopen) is verbonden.'
                      '\n4) Check of het toetsenbord kapot is door een ander toetsenbord te gebruiken')
        self.l.open_log()
        sys.exit(0)


def close_port(a):  # normal shutdown
    a.ser.close()
    print('port is closed 1')


def close_port_interrupt(a, signal, frame):  # interrupt shutdown
    a.ser.close()
    print('port is closed 2')


def main():
    l = Logger(Filename_Logger)
    c = ConfigFileHandler(Filename_Config_keypress, l, config_key_sections_check, config_key_items_check,
                          config_key_items_data)  # key configuration
    d = ConfigFileHandler(Filename_Config_debugging, l, config_debugging_sections_check, config_debugging_items_check,
                          config_debugging_items_data)  # debugging configuration
    a = ArduinoCommunication(c.settings, d.settings, c.changed_color, l)
    atexit.register(close_port, a)
    signal.signal(signal.SIGINT, partial(close_port_interrupt, a))

    counter = 2
    while True:
        if counter >= update_settings_counter:
            a.get_arduino_port()  # get the port and update the port if one is found
            a.update_arduino_port()  # update the found port
            a.update_color()  # update the keypad colors
            c.check_config_file()  # check the config file for correctness
            d.check_config_file()  # check the config file for correctness
            c.update_settings()  # the config file is correct so update the settings
            d.update_settings()  # the config file is correct so update the settings
            counter = 0
        message = a.read_arduino()
        if message:
            for i in message:
                print(i)
        counter = counter + 1
        time.sleep(sleep_time)


if __name__ == '__main__':
    main()
