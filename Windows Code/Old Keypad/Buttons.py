import subprocess
import os
from Settings import *

class Button:
    def __init__(self, but_num_1, but_num_2, but_path):
        self.but_num_1 = but_num_1          # give the first button a number (used to open the program)
        self.but_num_2 = but_num_2          # give the second button a number (used to close the program)
        self.but_path = but_path            # give the initial path to the program that has to be opened
        self.prog = list()                  # initiate a list of opened programs
        self.prog_closed = False           # looks if a program has been opened that can be closed

    def open(self, button):
        if button == self.but_num_1:
            try:
                self.prog.append(subprocess.Popen([self.but_path]))
                return (self.but_num_1 + " is ingedrukt en zal openen: "+self.but_path)
            except FileNotFoundError:
                return (self.but_num_1 + " is ingedrukt maar het volgende programma kon niet worden gevonden: "+self.but_path+" je kunt het pad naar het programma aanpassen in programmapad.txt dit bestand zit in de zelfde folder als dit programma")
        return False

    def close(self, button):
            if button == self.but_num_2:
                for prog in self.prog:
                    try:
                        prog.kill()
                        self.prog_closed = True
                    except AttributeError:
                        self.prog_closed = False
                self.prog = list()
                if self.prog_closed:
                    return (self.but_num_2 + " is ingedrukt en zal sluiten: " + self.but_path)
                else:
                    return (self.but_num_2 + " is ingedrukt maar dit programma: "+ self.but_path + " is nog niet eerder opgestart")
            return False

    def update_path(self, button, path):
        if int(button)*2-1 == int(self.but_num_2):
            self.but_path=path
