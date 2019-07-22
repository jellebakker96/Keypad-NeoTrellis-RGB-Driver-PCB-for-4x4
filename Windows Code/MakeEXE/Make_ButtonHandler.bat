@echo off

title exe builder
echo Lets start building 

"C:\Python37\Scripts\pyinstaller.exe" --onefile --icon=ggzvs.ico "C:\Gedeeld\Private Projects\Keypad-V2\Windows Code\ButtonHandler.py"

pause