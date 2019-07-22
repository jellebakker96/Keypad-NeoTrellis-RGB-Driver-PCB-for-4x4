# Keypad-NeoTrellis-RGB-Driver-PCB-for-4x4
This software offers a stand alone solution which allows the user to control the NeoTrellis RGB Driver PCB for 4x4 keypad using an arduino. The following directrories are pressent:

(1) Arduino Code - The arduino programmes used for testing and controlling the arduino.
  
(1.1) ArduinoController - This is the final program to control the arduino

(1.2) KeyPadCheck - Used to check if the NeoTrellis driver PCB is working

(1.3) PingPong - Used to check if the serial communications are working by first reading from the serial port and then writing the read message.


(2) Documentation - Contains the Python and arduino libraries and the used programs


(3) Windows Code - The Python code used to make the .exe

(3.1) icons - the .ico files

(3.2) MakeEXE - the .bat files used by pyinstaller to make the .exe files

(3.2.1) build - pyinstaller build files

(3.2.2) dist - pyinstaller output folder for the .exe files

(3.3) Old Keypad - privious version of the keypad program


There are three possible action which can be performed when a button press is detected. 

(1) Open a program

(2) Close a program

(3) Simulate a keyboard button

