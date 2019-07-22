# File names
Filename_Logger = 'log.txt'
Filename_Config = 'config.txt'

# Config file
config_items_check = ['programma_knop', 'progamma_pad', 'open_progamma', 'knop_functie', 'kleur']
config_items_data = ['boolean', 'path', 'boolean', 'string', 'int']
config_keypress_options = ['alt', 'backspace', 'caps_lock', 'cmd', 'ctrl', 'delete', 'enter', 'esc', 'num_lock',
                           'pause', 'print_screen']

# Timing
sleep_time = 0.25  # total time that the program sleeps in seconds
update_settings_counter = 16  # the settings are updated every sleep_time*update_settings_counter seconds

# System Tray
system_tray_closed = False
debugging_state = False
debugging_state_old = False

# Arduino Communication
baudrate = 115200
wait_write = 0.0  # make sure the write buffer is empty (not really needed)
