import tkinter as tk # Tkinter -> tkinter in Python3
from functools import partial
from Buttons import Button
from Settings import *
from tkinter import filedialog

class App(object):
    def __init__(self, root):
    # changing the title and icon of our master frame
        self.root = root
        self.root.title("ggzvs")
        self.root.iconbitmap('ggzvs.ico')
    # create a Frame for the Text and Scrollbar
        self.frm = tk.Frame(self.root, width=700, height=500)
        self.frm.grid_rowconfigure(0, weight=1)
        self.frm.grid_columnconfigure(0, weight=1)
        self.frm.grid(row=1, column=0, columnspan=4, sticky=tk.N+tk.S+tk.E+tk.W)

    # create buttons to set the program path
        self.btn_dict = {}
        self.col = 0
        self.words = ["1", "2", "3", "4"]
        for number in self.words:
            self.action = lambda x=number: self.but_pres(x)
            # create the buttons and assign to number:button-object dict pair
            self.btn_dict[number] = tk.Button(self.root, text="Selecteer app "+number, command=self.action)
            self.btn_dict[number].grid_rowconfigure(0, weight=1)
            self.btn_dict[number].grid_columnconfigure(self.col, weight=1)
            self.btn_dict[number].grid(row=0, column=self.col, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
            self.root.columnconfigure(self.col, weight=1)
            self.col += 1
        self.root.rowconfigure(1, weight=1)

    # create button to enter text
        button = tk.Button(self.root, text='Enter', command=partial(self.clicked, event="some input is needed here"))
        button.grid(row=2, column=0, columnspan=4, sticky=tk.N+tk.S+tk.E+tk.W)
        self.root.bind("<Return>", self.clicked)  # handle the enter key event of your keyboard
        self.root.columnconfigure(0, weight=1)

    # create a Text widget
        self.txt = tk.Text(self.frm, borderwidth=3, relief="sunken")
        self.txt.grid_rowconfigure(0, weight=1)
        self.txt.grid_columnconfigure(0, weight=1)
        self.txt.grid(row=0, column=0, sticky=tk.N + tk.S + tk.E + tk.W, padx=2, pady=2)
        self.txt.config(font=("consolas", 12), undo=True, wrap='word',state=tk.DISABLED)

    # create a entry widget
        self.entry_id = tk.StringVar()
        self.txt2 = tk.Entry(self.frm, textvariable=self.entry_id)
        self.txt2.grid_rowconfigure(1, weight=1)
        self.txt2.grid_columnconfigure(0, weight=1)
        self.txt2.grid(row=1, column=0, sticky=tk.N + tk.S + tk.E + tk.W, padx=2, pady=2)
        self.txt2.config(font=("consolas", 12))

    # create a Scrollbar and associate it with txt
        self.scrollb = tk.Scrollbar(self.frm, command=self.txt.yview)
        self.scrollb.grid_rowconfigure(0, weight=1)
        self.scrollb.grid_columnconfigure(1, weight=1)
        self.scrollb.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        self.txt['yscrollcommand'] = self.scrollb.set

    # Initialize the buttens to open the programs
        self.setup()

    # Make the program check the keyboard for inputs
        self.root.after(0, self.Check_Serial)

    def setup(self):
        counter = 0
        self.but_objs = list()

        try:
            f = open("Programmapad.txt", "r")
        except FileNotFoundError:
            f = open("programmapad.txt", "a")
            for path in prog_path_default:
                f.write(path + "\n")
            f = open("Programmapad.txt", "r")

        for x in f:
            self.but_objs.append(Button(str(counter), str(counter + 1), x.rstrip()))
            counter = counter + 2
            self.text_update(x.rstrip())

        self.max_but = len(self.but_objs) * 2

    def but_contr(self, button):
        try:
            int(button)
        except ValueError:
            self.text_update("Dit was niet een nummer")
            return False

        if (int(button) % 2 == 0 and int(button) <= self.max_but - 1):
            for but_obj in self.but_objs:
                x = but_obj.open(button)
                if x != False: self.text_update(str(x))
        elif (int(button) % 2 == 1 and int(button) <= self.max_but - 1):
            for but_obj in self.but_objs:
                x = but_obj.close(button)
                if x != False: self.text_update(str(x))
        elif (int(button) == self.max_but):
            self.text_update("De volgende opties zijn beschikbaar:")
            for but_obj in self.but_objs:
                self.text_update(but_obj.but_num_1 + ": Open " + but_obj.but_path)
                self.text_update(but_obj.but_num_2 + ": Sluit " + but_obj.but_path)
        else:
            self.text_update("Onbekende knop is gedrukt")
            return False
        return True

    def but_pres(self, input):
        fname = filedialog.askopenfilename(filetypes=(("Program FIles", "*.exe"), ("All files", "*")))
        print(fname)
        self.text_update("Button "+input+" pressed" + " and you selected:")
        self.text_update(fname)
        self.update_path(input,fname)


    def text_update(self, input):
        self.txt.config(state=tk.NORMAL)
        self.txt.insert(tk.END, input+"\n")
        self.txt.see("end")
        self.txt.config(state=tk.DISABLED)

    def Check_Serial(self):
        self.root.after(5000, self.Check_Serial)
        self.text_update("Check keyboard was called and returned")

    def clicked(self, event):
        text = self.entry_id.get()  # get the text from entry
        self.text_update("User entered: " + text)
        self.txt2.delete(0, 'end')
        self.but_contr(text)

    def update_path(self, button, path):
        try:
            int(button)
        except ValueError:
            self.text_update("Dit was niet een nummer")
            return False
        if int(button)<=(self.max_but/2):
            for but_obj in self.but_objs:
                but_obj.update_path(button,path)
        else:
            self.text_update("Onbekende knop is gedrukt")
            return False
        return True


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()

if __name__ == '__main__':
    main()