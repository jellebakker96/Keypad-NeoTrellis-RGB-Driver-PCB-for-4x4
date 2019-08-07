@echo off

title exe builder
echo Lets start building 

"C:\Python37\Scripts\pyinstaller.exe" --hidden-import pkg_resources --hidden-import infi.systray --noconsole --onefile --icon=ggzvs.ico "C:\Gedeeld\Private Projects\Keypad-V2\Windows Code\src\SystemTray.py"

pause