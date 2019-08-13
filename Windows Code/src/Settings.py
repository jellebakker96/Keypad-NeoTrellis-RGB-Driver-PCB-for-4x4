# File names
Filename_Logger = 'TextFiles\log.txt'
Filename_Config_keypress = 'TextFiles\config.txt'
Filename_Config_debugging = 'TextFiles\debugging.txt'
Filename_documentation = 'Keypad_Documentatie.pdf'

# Config
config_keypress_options = ['alt', 'backspace', 'caps_lock', 'cmd', 'ctrl', 'delete', 'enter', 'esc', 'num_lock',
                           'pause', 'print_screen']

# Config file key options
config_key_sections_check = ['knop_0', 'knop_1', 'knop_2', 'knop_3', 'knop_4', 'knop_5', 'knop_6', 'knop_7', 'knop_8',
                             'knop_9', 'knop_10', 'knop_11', 'knop_12', 'knop_13', 'knop_14', 'knop_15']
key_items = ['programma_knop', 'progamma_pad', 'open_progamma', 'knop_functie', 'kleur']
config_key_items_check = [key_items] * len(config_key_sections_check)
key_items_data = ['boolean', 'path', 'boolean', 'keypress string', 'int']
config_key_items_data = [key_items_data] * len(config_key_sections_check)

# Config file debugging
config_debugging_sections_check = ['debugging_knop']
config_debugging_items_check = [['debugging', 'vid', 'pid']]
config_debugging_items_data = [['boolean', 'int', 'int']]

# Timing
sleep_time = 0.25  # total time that the program sleeps in seconds
update_settings_counter = 16  # the settings are updated every sleep_time*update_settings_counter seconds

# System Tray
system_tray_closed = False

# Arduino Communication
baudrate = 115200
wait_write = 0.0  # make sure the write buffer is empty (not really needed)
arduino_vid = [9025]  # serial devices with these vid numbers will also be seen as an arduino
arduino_pid = [32822]  # serial devices with these pid numbers will also be seen as an arduino

# Logger
max_prints = 100  # maximum number of messages that will be printed
