@echo off

title exe builder
echo Lets start building the entire project

"C:\Python37\Scripts\pyinstaller.exe" --hidden-import pkg_resources --hidden-import infi.systray --noconsole --onefile --icon=ggzvs.ico "C:\Gedeeld\Private Projects\Keypad-V2\Windows Code\src\Keypad.py"

"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" "C:\Gedeeld\Private Projects\Keypad-V2\Windows Code\MakeEXE\Make_setup.iss"

pause