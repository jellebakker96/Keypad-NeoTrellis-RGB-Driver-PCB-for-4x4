from Settings import *
import os
import webbrowser

class Logger:
    def __init__(self, filename, debug = False):
        self.filename = filename          # give filename
        self.temp = os.path.isfile(self.filename)   # check if there is already a log file
        self.first_message = 'Deze text file is gemaakt door het programma "Keypad". Dit programma kan waarschijnlijk ' \
                             'worden gevonden in de folder "C:\\Program Files (x86)\\Keypad"'
        if self.temp:
            with open(self.filename, 'w') as f:     # overwrite previous content
                f.write(self.first_message+'\n\n')
                self.temp = False
        else:
            with open(self.filename, 'a') as f:     # append previous content
                f.write(self.first_message+'\n\n')


    def logger(self, input, debug=True):
        if debug:
            self.write_to_log(input)


    def write_to_log(self,input):
        with open(self.filename, 'a') as f:     # append previous content
            f.write(input+'\n')

    def open_log(self):
        webbrowser.open(self.filename)


def main():
    l = Logger(Filename_Logger)
    l.logger('Hello world')
    l.logger('Hello world2',False)
    l.open_log()


if __name__ == '__main__':
    main()