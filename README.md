# Keypad-NeoTrellis-RGB-Driver-PCB-for-4x4
This software offers a stand alone solution which allows the user to control the NeoTrellis RGB Driver PCB for 4x4 keypad using an arduino. The following directrories are pressent:

The installation process is simple.

1) Download \Keypad-V2\Windows Code\MakeSetup\dist\Keypad_setup.exe

2) install Keypad_setup.exe

2) Connect the "NeoTrellis RGB Driver PCB for 4x4 keypad" to an arduino (leonardo was used during dev) :"https://learn.adafruit.com/adafruit-neotrellis/arduino-code"
 
3) Connect the arduino to the PC using the USB connection from the arduino

4) start Keypad.exe

A more detailed explanation is given in \Keypad-V2\Documentation\Keypad_Documentatie.pdf. This explanation is written in Dutch.



The following folders can be found in this git repository:

1) Arduino Code - The arduino programmes used for testing and controlling the arduino.
  
1) ArduinoController - This is the final program to control the arduino.

2) KeyPadCheck - Used to check if the NeoTrellis driver PCB is working.

3) PingPong - Used to check if the serial communications are working by first reading from the serial port and then writing the read message.


2) Documentation - Contains the Python and arduino libraries, the used programs and all other documentation.


3) Windows Code - The Python code used to make the kepad program.

3.1) icons - The .ico files.

3.2) MakeEXE - The .bat files used by pyinstaller to make the .exe files.

3.2.1) build - Pyinstaller build files.

3.2.2) dist - Pyinstaller output folder for the .exe files.

3.3) Old Keypad - Previous version of the keypad program.


4) 3D Files - All the files that are used for the 3D housing of the keypad module.

4.1) 3D Housing - All the Solidworks and STL files.

4.2) Paper Table - The paper table template for the keypad module.

4.3) Reference Images - The reference images used for the creation of the keypad module housing.

There are three possible action which can be performed when a button press is detected. 

1) Open a program

2) Close a program

3) Simulate a keyboard button

