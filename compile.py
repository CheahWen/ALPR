import subprocess
import os

add_data = "--add-data config.cfg;. "
add_data += "--add-data layout.kv;. "
add_data += "--add-data icons/*;icons "
add_data += "--add-data models/*;models "

command = r"PyInstaller -F --noupx main.py --name UCSI_Carplate_App --noconsole --windowed --additional-hooks-dir=hooks "+add_data+" --icon icons/app_icon.ico"

subprocess.call(command, 
				cwd=".")	

# pyinstaller.py --windowed --noconsole --clean --onefile AppStart\AppStart.spec
