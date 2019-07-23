from infi.systray import SysTrayIcon
from Settings import *
from LogHandler import Logger
import time
import sys
import webbrowser


def check_debugging(log):
    global debugging_state_old
    l = log
    if debugging_state_old != debugging_state:
        debugging_state_old = debugging_state
        if debugging_state:
            l.write_to_log('\n\nDebugging staat aan:')
        else:
            l.write_to_log('\n\nDebugging staat uit:')


def check_shutdown():
    if system_tray_closed:
        sys.exit(0)


def open_file(input1):
    webbrowser.open(input1)


def debugging_on(systrayicon):
    global debugging_state  # Create the flag in the system tray tread that is used to enable the debugger
    debugging_state = True


def debugging_off(systrayicon):
    global debugging_state  # Create the flag in the system tray tread that is used to enable the debugger
    debugging_state = False


def show_log(systrayicon):
    open_file(Filename_Logger)

def show_log(systrayicon):
    open_file(Filename_Manual)

def show_config_file(systrayicon):
    open_file(Filename_Config)


def close_program(systrayicon):
    global system_tray_closed  # Create the flag in the system tray tread that is used to see if the system should quit
    system_tray_closed = True


def setup_system_tray():
    hover_text = "Keypad"
    menu_options = (('Show log', 'log.ico', show_log),
                    ('Show manual', 'log.ico', show_manual),
                    ('Settings', 'settings.ico', show_config_file),
                    ('debugging', "debugging.ico", (('debugging on', "debugging_on.ico", debugging_on),
                                                    ('debugging off', "debugging_off.ico", debugging_off)))
                    )
    systrayicon = SysTrayIcon("ggzvs.ico", hover_text, menu_options, on_quit=close_program, default_menu_index=1)
    systrayicon.start()


def main():
    l = Logger(Filename_Logger)
    setup_system_tray()
    while True:
        print('test')
        time.sleep(2)
        check_shutdown()
        check_debugging(l)


if __name__ == '__main__':
    main()
