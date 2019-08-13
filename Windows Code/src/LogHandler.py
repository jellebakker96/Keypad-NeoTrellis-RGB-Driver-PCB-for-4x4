from Settings import *
import os
import webbrowser
import datetime


class Logger:
    def __init__(self, filename, debug=False, max_prints=None):
        """This class handles log."""

        # Assign Filename of the log.
        self.filename = filename
        # Check if the log file exist.
        self.temp = os.path.isfile(self.filename)
        # Write the first message.
        self.first_message = 'Deze text file is gemaakt door het programma "Keypad". Dit programma kan waarschijnlijk ' \
                             'worden gevonden in de folder "C:\\Program Files (x86)\\Keypad"'
        # Assign a max limit to the amount of log messages
        self.max_prints = max_prints
        # Start the message counter.
        self.prints_ctr = 0
        # Overwrite previous content.
        if self.temp:
            with open(self.filename, 'w') as f:
                f.write(self.first_message + '\n\n')
                self.temp = False
        # Append previous content.
        else:
            with open(self.filename, 'a') as f:
                f.write(self.first_message + '\n\n')

    def logger(self, input, debug=True):
        """This function handles writing to the log file."""

        # Check if there is a max msg limit.
        if self.max_prints:
            # If there is a maximum msg limit if it has been reached and if debugging is true.
            if debug and self.prints_ctr < self.max_prints:
                self.prints_ctr += 1
                self.write_to_log(input)
            # There is no maximum msg limit so only check if debugging is true.
        else:
            if debug:
                self.write_to_log(input)

    def write_to_log(self, input):
        """Write to the log file."""

        # Append previous content.
        with open(self.filename, 'a') as f:
            f.write('[{date:%Y-%m-%d %H:%M:%S}] '.format(date=datetime.datetime.now()))
            f.write(input + '\n')

    def open_log(self):
        """Open the log file."""

        webbrowser.open(self.filename)


def main():
    """Test LogHandler.py"""

    # Initialize the log object.
    l = Logger(Filename_Logger, max_prints=max_prints)
    # Print to the log.
    l.logger('Hello world')
    l.logger('Hello world2', True)
    l.logger('Hello world3', False)
    l.logger('Hello world4', True)
    l.open_log()


if __name__ == '__main__':
    main()
