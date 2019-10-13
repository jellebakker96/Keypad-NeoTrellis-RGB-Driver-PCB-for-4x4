from SystemTray import *
from ButtonHandler import *
from ComHandler import *
import time
import copy


def main():
    """The main file"""

    # Assign the settings.
    l = Logger(Filename_Logger, max_prints=max_prints)
    # Setup the system tray in the taskbar.
    setup_system_tray()
    # Initialize the key configuration.
    c = ConfigFileHandler(Filename_Config_keypress, l, config_key_sections_check, config_key_items_check,
                          config_key_items_data)
    # Initialize the debugging configuration.
    d = ConfigFileHandler(Filename_Config_debugging, l, config_debugging_sections_check, config_debugging_items_check,
                          config_debugging_items_data)
    # Make copy of initial leds settings which can be changed without changing the debugging file.
    leds_on = [d.settings[0][3]]
    # Initialize the Arduino communications.
    a = ArduinoCommunication(c.settings, d.settings, leds_on, c.changed_color, l)
    # Initialize the exit function.
    atexit.register(close_port, a)
    # Initialize the button objects.
    buttons = list()
    for i in range(16):
        buttons.append(Button(i, c.settings[i], leds_on, l))  # initialize button objects
    counter = 2
    while True:
        # Get the port and update the port if one is found.
        a.get_arduino_port()
        # Check if the program should shutdown.
        check_shutdown()
        if counter >= update_settings_counter:
            # Update the found port.
            a.update_arduino_port()
            # Check if the settings should be updated:
            # There are 3 times this should be done
            # 1) At start up
            # 2) When the apply settings button is pressed in the system tray
            # 3) When the port has been changed
            for i in range(16):
                if buttons[i].apply_settings: # check if the collor should be updated
                    buttons[i].update_apply_settings()
                    apply_settings = True
            if check_apply_settings() or a.apply_settings:
                apply_settings = True
            if apply_settings:
                # Check the config file for correctness.
                c.check_config_file()
                # Check the debugging file for correctness.
                d.check_config_file()
                # The config file is correct so update the settings.
                c.update_settings()
                # The debugging file is correct so update the settings.
                d.update_settings()
                # Update the keypad colors.
                a.update_color()
                # Settings have been applied so reset all the apply settings
                apply_settings = False
                update_apply_settings()
                a.update_apply_settings()
            counter = 0
        # Read message.
        message = a.read_arduino()
        # Open/close/simulate keypress depending on the settings.
        if message:
            for i in message:
                print(i)
                buttons[i].state_machine()
        # Increment counter.
        counter = counter + 1
        # Sleep.
        time.sleep(sleep_time)


if __name__ == '__main__':
    main()
