from SystemTray import *
from ButtonHandler import *
from ComHandler import *
import time


def main():
    l = Logger(Filename_Logger)
    setup_system_tray()  # setup the system tray in the taskbar
    c = ConfigFileHandler(Filename_Config_keypress, l, config_key_sections_check, config_key_items_check,
                          config_key_items_data) # key configuration
    d = ConfigFileHandler(Filename_Config_debugging, l, config_debugging_sections_check, config_debugging_items_check,
                          config_debugging_items_data) # debugging configuration
    a = ArduinoCommunication(c.settings, d.settings, c.changed_color, l)
    atexit.register(close_port, a)

    buttons = list()
    for i in range(16):
        buttons.append(Button(i, c.settings[i], l))  # initialize button objects
    counter = 2
    while True:
        a.get_arduino_port()  # get the port and update the port if one is found
        check_shutdown() # check if the program should shutdown
        if counter >= update_settings_counter:
            a.update_arduino_port() # update the found port
            a.update_color() # update the keypad colors
            c.check_config_file()  # check the config file for correctness
            d.check_config_file()  # check the debugging file for correctness
            c.update_settings()  # the config file is correct so update the settings
            d.update_settings()  # the debugging file is correct so update the settings
            counter = 0
            print('test')

        message = a.read_arduino()
        if message:
            for i in message:
                print(i)
                buttons[i].state_machine()  # open/close/simulate keypress depending on the settings

        counter = counter + 1
        time.sleep(sleep_time)


if __name__ == '__main__':
    main()
