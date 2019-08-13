from LogHandler import Logger
from Settings import *
import configparser
import time
import sys
import os
import copy


class ConfigFileHandler:
    """This class handles config files, so the keypad config file which tells what the buttons should do and a
    debugging config file that is used when something goes wrong."""

    def __init__(self, config_filename, log, config_sections, config_items, config_items_data_type):
        """Constructor of the ConfigFileHandler class."""

        # pass the logger object
        self.l = log
        # assign filename
        self.filename = config_filename
        # Assign the expected sections of the config file, for exampl ['knop_0', 'knop_1', 'knop_2', 'knop_3'].
        self.config_sections = config_sections
        # Assign the expected sections of the config file, for example ['programma_knop', 'progamma_pad',
        # 'open_progamma', 'knop_functie', 'kleur'].
        self.config_items = config_items
        # assign the expected item data types of the config file, for example ['boolean', 'path', 'boolean',
        # 'keypress string', 'int'].
        self.config_items_data_type = config_items_data_type
        # Check if there is a config file.
        self.temp = os.path.isfile(self.filename)
        if self.temp == False:
            self.config_error_detected('Er is geen {} file gevonden.'.format(self.filename), close_program=True)
        # Create the configparser object.
        self.config = configparser.ConfigParser()
        # Create the settings list that will be called by rest of the program.
        self.settings = []
        for num, sec in enumerate(self.config_sections):
            self.settings.append([0] * len(self.config_items[num]))
        # Create the settings list that holds the previous settings, used to see if the settings have changed.
        self.settings_old = []
        for num, sec in enumerate(self.config_sections):
            self.settings_old.append([0] * len(self.config_items[num]))
        # List that is used to see if the general settings have changed.
        self.changed_key = []
        # List that is used to see if the color settings have changed. If 'kleur' is part of the config items.
        if 'kleur' in self.config_items[0]:
            self.changed_color = []
            self.check_color = True
        else:
            self.check_color = False
        # Check the config file for correctness.
        self.check_config_file()
        # The config file is correct so update the settings.
        self.update_settings()

    def check_config_file(self):
        """Check if the config file is written correctly, most errors are caught"""
        # TODO When a section is removed after starting the program it is not caught the same is true for removing a
        # TODO item

        # Read the config file.
        self.config.read(self.filename)
        # Extract the sections from the config file.
        self.configsections = self.config.sections()
        # Check if there are the correct amount of sections.
        if len(self.configsections) != len(self.config_sections):
            self.config_error_detected('Er zijn te veel of the weinig secties of een sectie naam is verandered terwijl '
                                       'het programma aan stond. \nEr waren {} secties verwacht een sectie is bijv. '
                                       '[knop_1] of [debugging_knop]'.format(len(self.config_sections)),
                                       close_program=True)
        # Check if all sections and items are correct.
        for num1, section in enumerate(self.config._sections):
            if section != self.config_sections[num1]:
                self.config_error_detected('Een sectie naam is incorrect.\nDe secties moeten {} '
                                           'heten.'.format(self.config_sections), close_program=True)
            for num2, item in enumerate(self.config._sections[section]):
                if item != self.config_items[num1][num2]:
                    self.config_error_detected('Een optie naam is incorrect.\nDe opties moeten in de volgende '
                                               'volgorde staan ' + str(self.config_items), close_program=True)

    def update_settings(self):
        """Update the settings."""

        # Make a deep copy of the settings list.
        self.settings_old = copy.deepcopy(self.settings)
        # Read the config file.
        self.config.read(self.filename)
        # Check the values of the config file
        for num1, section in enumerate(self.config_sections):
            for num2, item in enumerate(self.config_items[num1]):
                # Check if the setting is empty.
                if self.config._sections[section][item] == "":
                    if item == 4:  # check if it the color option
                        self.settings[num1][num2] = 0  # 0 is off
                    else:
                        self.settings[num1][num2] = None  # Not Used
                # Check if the setting data types are correct.
                elif self.config_items_data_type[num1][num2] == 'boolean':
                    self.settings[num1][num2] = self.check_boolean(self.config._sections[section][item])
                elif self.config_items_data_type[num1][num2] == 'path':
                    self.settings[num1][num2] = self.check_path(self.config._sections[section][item])
                elif self.config_items_data_type[num1][num2] == 'keypress string':
                    self.settings[num1][num2] = self.check_key(self.config._sections[section][item])
                elif self.config_items_data_type[num1][num2] == 'string':
                    self.settings[num1][num2] = self.check_string(self.config._sections[section][item])
                elif self.config_items_data_type[num1][num2] == 'int':
                    self.settings[num1][num2] = self.check_int(self.config._sections[section][item])
        # Check if a setting has changed.
        self.check_config_change()

    def check_boolean(self, inp):
        """Boolean data type check."""

        if inp == ('True' or 'TRUE' or 'true' or '1' or 'Waar' or 'Waar' or 'WAAR' or 'Ja' or 'JA' or 'ja' or
                   'Correct' or 'CORRECT' or 'correct'):  # Check voor True
            return True
        elif inp == ('False' or 'FALSE' or 'false' or '0' or 'Niet Waar' or 'NIET WAAR' or 'Niet waar' or 'Nee' or
                     'NEE' or 'nee' or 'Incorrect' or 'INCORRECT' or 'incorrect' or 'Niet Correct' or
                     'Niet correct' or 'niet correct'):  # Check voor False
            return False
        return self.config_error_detected('Er is een boolean waarde incorrect gebruikt:\n{}\nJe moet True '
                                          'of False gebruiken.'.format(inp), close_program=True)

    def check_path(self, inp):
        """Check a path."""

        self.check_string(inp)
        if os.path.exists(inp):  # check if it is a correct path
            return inp
        return self.config_error_detected('Er is een incorrect programma pad gevonden:\n' + str(inp),
                                          close_program=True)

    def check_key(self, inp):
        """Check a key."""

        self.check_string(inp)
        if inp in config_keypress_options:
            return inp
        return self.config_error_detected('Er is een incorrecte optie ingevuld "' + str(inp) + '"\nDe mogelijke '
                                                                                               'opties zijn:\n{}'.format(
            config_keypress_options), close_program=True)

    def check_string(self, inp):
        """Check if a variable is a string."""

        if isinstance(inp, str):
            return inp
        return self.config_error_detected('Er is een vreemd symbol gevonden dat geen string is:\n{}'.format(inp),
                                          close_program=True)

    def check_int(self, inp):
        """Check if a variable is an integer"""

        if inp.isdigit():
            output = int(inp)
            return output
        else:
            return self.config_error_detected('De kleur/vid/pid hoort een nummer te zijn', close_program=True)

    def config_error_detected(self, inp, close_program=False):
        """An error is detected"""

        # Print the message and open the log
        if self.changed_key or close_program or print_msg:
            self.l.logger(inp)
            self.l.logger('Er is een error gevonden in de config file.\nJe kunt drie dingen doen.'
                          '\n\t1) Installeer het programma opnieuw om een nieuwe config file te maken.'
                          '\n\t2) Lees de documentatie om te zien hoe de config file er uit moet zien.'
                          '\n De config files kunnen worden gevonden in "C:\Program Files (x86)\Keypad\TextFiles"')
            self.l.open_log()
        # In some cases it is better to close the program.
        if close_program:
            self.l.logger('Als je klaar bent met de veranderingen moet je het programma in de system tray afsluiten'
                          '\n vervolgens kun je het programma opnieuw opstarten.')
            sys.exit(0)
        return None

    def check_config_change(self):
        """Check if the settings have changed."""

        # Clear the previous changed key variable.
        self.changed_key.clear()
        # Check if the file contains a color.
        if self.check_color:
            self.changed_color.clear()
        # Check if settings is different than the old settings
        for num, key in enumerate(self.settings):
            if self.settings_old[num] != self.settings[num]:
                self.changed_key.append(num)
                if self.check_color:
                    if self.settings_old[num][4] != self.settings[num][4]:
                        self.changed_color.append(num)


def main():
    """ConfigHandler test."""

    # Initialize the logger object.
    l = Logger(Filename_Logger)
    # Initialize the key configuration.
    c = ConfigFileHandler(Filename_Config_keypress, l, config_key_sections_check, config_key_items_check,
                          config_key_items_data)
    # Initialize the debugging configuration.
    d = ConfigFileHandler(Filename_Config_debugging, l, config_debugging_sections_check, config_debugging_items_check,
                          config_debugging_items_data)
    # Set the counter to 2
    counter = 2;
    # Continuously run the following code.
    while True:
        # Check if the config file has to be updated.
        if counter >= update_settings_counter:
            # Check the config file for correctness.
            c.check_config_file()
            # Check the config file for correctness.
            d.check_config_file()
            # The config file is correct so update the settings.
            c.update_settings()
            # The config file is correct so update the settings.
            d.update_settings()
            # Set the counter to 0.
            counter = 0
            # Print the settings.
            print(c.settings)
            print(c.changed_key)
            print(c.changed_color)
            print(d.settings)
            print(d.changed_key)
        # Increment the counter and sleep.
        counter = counter + 1
        time.sleep(sleep_time)


if __name__ == '__main__':
    main()
