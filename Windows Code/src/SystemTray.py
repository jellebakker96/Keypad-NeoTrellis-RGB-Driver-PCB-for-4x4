from infi.systray import SysTrayIcon
from Settings import *
from LogHandler import Logger
import time
import sys
import webbrowser


def check_shutdown():
    """Check if the system tray is closed and if so close the main tread."""

    # Check if the system tray is closed.
    if system_tray_closed:
        sys.exit(0)

def check_apply_settings():
    """Check the state of the apply_settings variable."""

    global apply_settings
    return apply_settings

def update_apply_settings():
    """Update the state of the apply_settings variable."""

    global apply_settings
    apply_settings = False

def open_file(input1):
    """Open files."""

    webbrowser.open(input1)


def show_log(systrayicon):
    """This function is called when the show log button in the system tray is pressed."""

    # Open the log file.
    open_file(Filename_Logger)


def show_documentation(systrayicon):
    """This function is called when the documentation button in the system tray is pressed."""

    # Open the documentation file.
    open_file(Filename_documentation)


def show_config_keypress_file(systrayicon):
    """This function is called when the show config button in the system tray is pressed."""

    # Open the configuration file.
    open_file(Filename_Config_keypress)


def show_config_debugging_file(systrayicon):
    """This function is called when the debugging button in the system tray is pressed."""

    # Open the debugging configuration file.
    open_file(Filename_Config_debugging)


def close_program(systrayicon):
    """Create the flag in the system tray tread that is used to see if the system should quit."""

    # Declare global variable.
    global system_tray_closed
    system_tray_closed = True

def apply_settings_fun(systrayicon):
    """Create the flag in the system tray tread that is used to see if the system should update the settings and
    collors."""

    # Declare global variable.
    global apply_settings
    apply_settings = True

def setup_system_tray():
    """This function initializes the system tray tread."""

    # This text is seen when the mouse hovers over the tray icon.
    hover_text = "Keypad"
    # These meanu options are available for the system tray.
    menu_options = (('Documentation', 'documentation.ico', show_documentation),
                    ('Settings', 'settings.ico', show_config_keypress_file),
                    ('Apply Settings', 'applysettings.ico', apply_settings_fun),
                    ('Log', 'log.ico', show_log),
                    ('Debugging', "debugging.ico", show_config_debugging_file)
                    )
    # Setup the system tray.
    systrayicon = SysTrayIcon("ggzvs.ico", hover_text, menu_options, on_quit=close_program, default_menu_index=1)
    # Start the system tray icon tread.
    systrayicon.start()


def main():
    """SystemTray.py test."""

    # Initialize the logger object.
    l = Logger(Filename_Logger)
    # Start the system tray tread.
    setup_system_tray()
    # Check if the program should shutdown.
    while True:
        print('test')
        time.sleep(2)
        check_shutdown()


if __name__ == '__main__':
    main()
