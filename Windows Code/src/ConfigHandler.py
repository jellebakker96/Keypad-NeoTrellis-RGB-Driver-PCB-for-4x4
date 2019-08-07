from LogHandler import Logger
from Settings import *
import configparser
import time
import sys
import os
import copy


class ConfigFileHandler:
    def __init__(self, config_filename, log, config_sections, config_items, config_items_data_type):
        self.l = log
        self.filename = config_filename  # give config filename
        self.config_sections = config_sections  # for exampl ['knop_0', 'knop_1', 'knop_2', 'knop_3', 'knop_4',
        # 'knop_5', 'knop_6', 'knop_7', 'knop_8', 'knop_9', 'knop_10', 'knop_11', 'knop_12', 'knop_13', 'knop_14',
        #  'knop_15']
        self.config_items = config_items  # for example ['programma_knop', 'progamma_pad', 'open_progamma',
        # 'knop_functie', 'kleur']
        self.config_items_data_type = config_items_data_type  # for example ['boolean', 'path', 'boolean',
        # 'keypress string', 'int']
        self.temp = os.path.isfile(self.filename)  # check if there is a config file
        if self.temp == False:
            self.config_error_detected('Er is geen config.txt file gevonden.')
        self.config = configparser.ConfigParser()  # create the configparser
        self.settings = [[0] * len(self.config_items) for i in range(len(self.config_sections))]  # create the settings
        # list that will be called by rest of the program
        self.settings_old = [[0] * len(self.config_items) for i in range(len(self.config_sections))]  # create the
        # settings list that holds the previous settings
        self.changed_key = []  # list to that is used to see if settings have changed
        self.changed_color = []
        if 'kleur' in self.config_items:
            self.check_color = True
        else:
            self.check_color = False

        self.check_config_file()  # check the config file for correctness
        self.update_settings()  # the config file is correct so update the settings

    def check_config_file(self):
        self.config.read(self.filename)  # read the config file
        self.configsections = self.config.sections()

        if len(self.configsections) > len(self.config_sections):  # check if there are not to many option available
            self.config_error_detected('Er zijn te veel secties. \nEr worden maximaal {} secties ondersteund'
                                       ' een sectie is bijv. [knop_1] of [debugging_knop]'.format(
                len(self.config_sections)))

        for num, section in enumerate(self.configsections):
            if (self.config_sections[num] in self.configsections) == False:  # check if all sections are named correctly
                self.config_error_detected('Een sectie naam is incorrect.\nDe secties moeten {} '
                                           'heten.'.format(self.config_sections))
            for num2, item in enumerate(self.config_items):
                try:
                    self.config._sections[section][item]  # check if each option can be found
                except KeyError:
                    self.config_error_detected('Een optie naam is incorrect.\nDe opties moeten in de volgende '
                                               'volgorde staan ' + str(self.config_items))

    def update_settings(self):
        self.settings_old = copy.deepcopy(self.settings)
        self.config.read(self.filename)  # read the config file
        self.configsections = self.config.sections()
        for num, section in enumerate(self.configsections):
            for num2, item in enumerate(self.config_items):
                if self.config._sections[section][item] == "":  # Check if the setting is empty
                    if item == 4:  # check if it the color option
                        self.settings[num][num2] = 0  # 0 is off
                    else:
                        self.settings[num][num2] = 'NU'  # Not Used
                elif self.config_items_data_type[num2] == 'boolean':
                    self.settings[num][num2] = self.check_boolean(self.config._sections[section][item])
                elif self.config_items_data_type[num2] == 'path':
                    self.settings[num][num2] = self.check_path(self.config._sections[section][item])
                elif self.config_items_data_type[num2] == 'keypress string':
                    self.settings[num][num2] = self.check_key(self.config._sections[section][item])
                elif self.config_items_data_type[num2] == 'string':
                    self.settings[num][num2] = self.check_string(self.config._sections[section][item])
                elif self.config_items_data_type[num2] == 'int':
                    self.settings[num][num2] = self.check_int(self.config._sections[section][item])
        self.check_config_change()

    def check_boolean(self, inp):
        if inp == ('True' or 'TRUE' or 'true' or '1' or 'Waar' or 'Waar' or 'WAAR' or 'Ja' or 'JA' or 'ja' or
                   'Correct' or 'CORRECT' or 'correct'):  # Check voor True
            return True
        elif inp == ('False' or 'FALSE' or 'false' or '0' or 'Niet Waar' or 'NIET WAAR' or 'Niet waar' or 'Nee' or
                     'NEE' or 'nee' or 'Incorrect' or 'INCORRECT' or 'incorrect' or 'Niet Correct' or
                     'Niet correct' or 'niet correct'):  # Check voor False
            return False
        self.config_error_detected('Er is een boolean waarde incorrect gebruikt:\n{}\nJe moet True '
                                   'of False gebruiken.'.format(inp))

    def check_path(self, inp):
        self.check_string(inp)
        if os.path.exists(inp):  # check if it is a correct path
            return inp
        self.config_error_detected('Er is een incorrect programma pad gevonden:\n' + str(inp))

    def check_key(self, inp):
        self.check_string(inp)
        if inp in config_keypress_options:
            return inp
        self.config_error_detected('Er is een incorrecte optie ingevuld "' + str(inp) + '"\nDe mogelijke '
                                                                                        'opties zijn:\n{}'.format(
            config_keypress_options))

    def check_string(self, inp):
        if isinstance(inp, str):
            return inp
        self.config_error_detected('Er is een vreemd symbol gevonden dat geen string is:\n{}'.format(inp))

    def check_int(self, inp):
        try:
            output = int(inp)
            return output
        except ValueError:
            self.config_error_detected('De kleur hoort een nummer te zijn')

    def config_error_detected(self, inp):
        self.l.logger(inp)
        self.l.logger('\nHet programma wordt afgesloten.\nJe kunt twee dingen doen.'
                      '\n1) Installeer het programma opnieuw om een nieuwe config file te maken.'
                      '\n2) Lees de documentatie om te zien hoe de config file er uit moet zien.')
        self.l.open_log()
        sys.exit(0)

    def check_config_change(self):
        self.changed_key.clear()
        self.changed_color.clear()
        for num, key in enumerate(self.settings):
            if self.settings_old[num] != self.settings[num]:
                self.changed_key.append(num)
                if self.check_color:
                    if self.settings_old[num][4] != self.settings[num][4]:
                        self.changed_color.append(num)


def main():
    l = Logger(Filename_Logger)
    c = ConfigFileHandler(Filename_Config_keypress, l, config_key_sections_check, config_key_items_check,
                          config_key_items_data)  # key configuration
    d = ConfigFileHandler(Filename_Config_debugging, l, config_debugging_sections_check, config_debugging_items_check,
                          config_debugging_items_data)  # debugging configuration
    counter = 2;
    while True:
        if counter >= update_settings_counter:
            c.check_config_file()  # check the config file for correctness
            d.check_config_file()  # check the config file for correctness
            c.update_settings()  # the config file is correct so update the settings
            d.update_settings()  # the config file is correct so update the settings
            counter = 0
            print(c.settings)
            print(c.changed_key)
            print(c.changed_color)
            print(d.settings)
            print(d.changed_key)
            print(d.changed_color)
        counter = counter + 1
        time.sleep(sleep_time)


if __name__ == '__main__':
    main()
