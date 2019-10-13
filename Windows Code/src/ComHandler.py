from ConfigHandler import *
from functools import partial
import serial.tools.list_ports
import serial
import atexit
import signal


class ArduinoCommunication:
    def __init__(self, settings, debugging, leds_on, changed_color, log):
        """This class handles the communications with the Arduino."""

        # Assign the settings.
        self.settings = settings
        # Debugging variable.
        self.debugging = debugging[0][0]
        # Manual ID of the Aruidno.
        self.debugging_vid = debugging[0][1]
        self.debugging_pid = debugging[0][2]
        # Should the leds be on or off the first time you start the program
        self.leds_on = leds_on
        # Changed color variable.
        self.changed_color = changed_color
        # Assign log object.
        self.l = log
        # Keep track if the Arduino is going through its setup correctly.
        self.start_counter_state = False
        # Variable used to count the Arduino setup time, if it is to long a message will be printed.
        self.start_ctr = 0
        # Variable to store the port connected to an Arduino.
        self.port = []
        # Old port variable to check if it has changed.
        self.port_old = []
        self.port_old2 = []
        # Used to see if a port was found.
        self.port_found = False
        # Used to see if a port has changed.
        self.port_changed = False
        # Check if an Arduino is connected and if so get the corresponding port.
        self.get_arduino_port()
        # Initialize serial communication
        self.initialize_ser()
        # Initialize the apply_settings variable
        self.apply_settings = False

    def initialize_ser(self):
        """Initialize serial communications with the Aruidno"""

        # Check if a port has been found.
        if self.port_found:
            # Iterate through each port.
            for num, port in enumerate(self.port):
                # Try to connect to the Arduino.
                try:
                    self.ser = serial.Serial(port, baudrate, timeout=0, parity=serial.PARITY_EVEN, rtscts=1)
                    self.l.logger('connected to {}'.format(port), self.debugging)
                    break
                # Exception for if the port is occupied.
                except serial.serialutil.SerialException:
                    self.l.logger('tried to connect to {} but attempted failed'.format(port), self.debugging)
                    if num >= len(self.port) - 1:
                        self.connection_error_detected('Het lijkt er op dat je dit progamma for de tweede keer probeerd'
                                                       ' te starten,\n Dit wordt niet ondersteunt.\n Het kan ook zijn'
                                                       ' dat er een ander programa is dat verbinding maakt met de '
                                                       'aruino.')

    def get_arduino_port(self):
        """Get all USB ports connected to an Arduino."""

        # Save the current Arduino ports.
        self.port_old2 = copy.deepcopy(self.port_old)
        self.port_old = copy.deepcopy(self.port)
        print(self.port_old)
        # Clear the port list.
        self.port.clear()
        # Reset the port_found variable
        self.port_found = False
        # List all ports.
        ports = list(serial.tools.list_ports.comports())
        # Iterate through each port.
        for num, p in enumerate(ports):
            # Print the port info.
            self.print_arduino_info(num, p)
            if self.debugging:
                self.print_arduino_info(num, p)
            # Check if 'Arduino' occurs in the description or if the vid and pid codes are in the default arduino list
            # found in the settings.
            if ("Arduino" in p[1]) or ((p.vid in arduino_vid) and (p.pid in arduino_pid)):
                self.port.append(p[0])
                # An Arduino port has been found.
                self.port_found = True
                # An new Arduino port has been found.
                if self.port_old != self.port:
                    self.port_changed = True
            # Make sure that the custom vid/pid variables exist.
            elif self.debugging_vid or self.debugging_pid:
                # The vid/pid variables exist now check if they are the same as the vid/pid codes of the currently
                # connected devices.
                if (p.vid == self.debugging_vid) and (p.pid == self.debugging_pid):
                    self.port.append(p[0])
                    self.port_found = True
                    if self.port_old != self.port:
                        self.port_changed = True
        # Check if a port has been.
        if self.port_found:
            self.l.logger(
                'Er zijn {} arduinos gevonden. Er wordt verbinding gemaakt met de eerste arduino of de eene die '
                'een open port heeft\nDe volgende porten zijn gevonden {}'.format(len(self.port), self.port),
                self.debugging)

    def update_arduino_port(self):
        """Update the arduino port if it has moved."""

        # Check if the Arduino port has changed and if it has been found.
        if self.port_changed and self.port_found:
            # The port get updated so reset the "self.port_changed" variable.
            self.port_changed = False
            # This variable is used to update the collors
            self.apply_settings = True
            # This makes sure that you can first start the program and then connect the keypad.
            print(self.port_old)
            if not self.port_old:
                self.initialize_ser()
            # A new Arduino has been connected, a connection will be made with the new Arduino.
            else:
                for port in self.port:
                    if port in self.port:
                        self.ser.port = port

    def update_apply_settings(self):
        self.apply_settings = False

    def write_arduino(self, inp):
        """Write to the Arduino."""

        # Check if a port was found and if you can connect to it.
        if self.port_found:
            # Encode to 'utf-8' and add "\n".
            inp_byte = (inp + "\n").encode('utf-8')
            # Try to write to the Arduino
            try:
                self.ser.write(inp_byte)
            except serial.serialutil.SerialException:
                return
            # Wait to make sure everything has been send, currently this has been set to 0s.
            time.sleep(wait_write)

    def read_arduino(self):
        """Read from the Arduino."""
        # TODO figure out what the cause of the ser.read errors is.

        # Variable used to store the message.
        message_int = []
        # Check if a port was found and if you can connect to it.
        if self.port_found:
            # Read up to one hundred bytes or as much is in the buffer.
            try:
                message = self.ser.read(100)
            except serial.serialutil.SerialException:
                return False
            except AttributeError:
                return False
            # Decode bytes.
            msg_dec = message.decode('utf-8')
            # Split the message based on '\n'.
            msg_split = msg_dec.split('\n')
            # Needed for if you want to switch to an other usb port. The data becomes corrupted.
            try:
                # Clean message.
                msg_split.remove('')
            except ValueError:
                return False
            # Strip the message.
            msg_clean = [i.strip() for i in msg_split]
            # A start and done message is expected from the Arduino within a certain time period.
            # A start message was send and a port was found.
            if self.start_counter_state and self.port_found:
                # The
                self.start_ctr += 1
            # The Arduino took to long to send the done message
            if self.start_ctr > 10 and self.port_found:
                self.start_counter_state = False  # the arduino setup failed
                self.connection_error_detected('De arduino kan geen verbinding maken met de knoppen, kijk of alle '
                                               'draaden goed zijn verbonden')
                return False
            # Check if there was a message.
            if not msg_clean:
                return False
            # Check if the start message was send
            if msg_clean[0] == 'start':
                self.start_counter_state = True
                # It is possible that the 'done' message is read immediately.
                if len(msg_clean) > 1:
                    if msg_clean[1] == 'done':
                        self.start_counter_state = False
                return False
            # Check if the done message is send.
            elif msg_clean[0] == 'done':
                self.start_counter_state = False
                self.start_ctr = 0
                return False
            # Convert to integers to represent buttons.
            try:
                for mes in msg_clean:
                    message_int.append(int(mes))
                return message_int
            except ValueError:
                self.l.logger('Arduino geeft geen correct getal, arduino output is:\n{}'.format(message))
                return False
        return False

    def update_color(self):
        """Update the colors"""

        if self.leds_on[0]:
            self.turn_leds_on()
        else:
            self.turn_leds_off()

    def turn_leds_on(self):
        """Turn the leds on."""

        if self.port_found:
            for i in range(16):
                self.write_arduino(str(i).zfill(2) + str(self.settings[i][4]).zfill(3))

    def turn_leds_off(self):
        """Turn the leds off."""

        list_of_zeros = [0] * 16
        for i in range(16):
            self.write_arduino(str(i).zfill(2) + str(list_of_zeros[i]).zfill(3))

    def connection_error_detected(self, inp):
        """Terminate the program if an error was detected."""

        self.l.logger(inp)
        self.l.logger('\nHet programma wordt afgesloten.\nJe kunt 4 dingen doen.'
                      '\n\t1) Installeer het programma opnieuw om een nieuwe config file te maken.'
                      '\n\t2) Verbind de 9 toetsen eerst voordat je het programma start'
                      '\n\t3) Zorg er voor dat maar 1 toetsenbord (die 9 knopen) is verbonden.'
                      '\n\t4) Check of het toetsenbord kapot is door een ander toetsenbord te gebruiken'
                      '\n Als je klaar bent met de veranderingen moet je het programma in de system tray afsluiten'
                      '\n vervolgens kun je het programma opnieuw opstarten.')
        self.l.open_log()
        sys.exit(0)

    def print_arduino_info(self, num, p):
        """Print the info from the devices that are connected to the PC."""

        temp = ('This is port {}\n'.format(num))
        temp += ('\t device = {}\n'.format(p.device))
        temp += ('\t name = {}\n'.format(p.name))
        temp += ('\t description = {}\n'.format(p.description))
        temp += ('\t hwid = {}\n'.format(p.hwid))
        temp += ('\t vid = {}\n'.format(p.vid))
        temp += ('\t pid = {}\n'.format(p.pid))
        temp += ('\t serial_number = {}\n'.format(p.serial_number))
        temp += ('\t location = {}\n'.format(p.location))
        temp += ('\t manufacturer = {}\n'.format(p.manufacturer))
        temp += ('\t product = {}\n'.format(p.product))
        temp += ('\t interface = {}\n'.format(p.interface))
        self.l.logger(temp, self.debugging)

def close_port(a):
    """Normal shutdown"""

    a.turn_leds_off()
    a.ser.close()
    a.l.logger('port is closed', a.debugging)


def main():
    """ComHandler test."""

    # Initialize the logger object.
    l = Logger(Filename_Logger)
    # Initialize the key configuration.
    c = ConfigFileHandler(Filename_Config_keypress, l, config_key_sections_check, config_key_items_check,
                          config_key_items_data)
    # Initialize the debugging configuration.
    d = ConfigFileHandler(Filename_Config_debugging, l, config_debugging_sections_check, config_debugging_items_check,
                          config_debugging_items_data)
    # Initialize the Arduino communications.
    a = ArduinoCommunication(c.settings, d.settings, c.changed_color, l)
    # Initialize the exit function.
    atexit.register(close_port, a)
    # Set counter.
    counter = 2
    while True:
        # Get the port and update the port if one is found.
        a.get_arduino_port()
        if counter >= update_settings_counter:
            # Update the found port.
            a.update_arduino_port()
            # Update the keypad colors.
            a.update_color()
            # Check the config file for correctness.
            c.check_config_file()
            # Check the config file for correctness.
            d.check_config_file()
            # The config file is correct so update the settings.
            c.update_settings()
            # The config file is correct so update the settings.
            d.update_settings()
            # Counter set to 0.
            counter = 0
        # Read the messages.
        message = a.read_arduino()
        print('test 1')
        if message:
            for i in message:
                print(i)
        counter = counter + 1
        time.sleep(sleep_time)


if __name__ == '__main__':
    main()
