import subprocess
import os
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

hiddenimports = collect_submodules('tensorflow_core')
datas = collect_data_files('tensorflow_core', subdir=None, include_py_files=True)


add_data = "--add-data=config.cfg;. "
add_data += "--add-data=../models/*;. "
add_data += "--add-data=../video/*;. "



command = r"PyInstaller -F --noupx main.py --additional-hooks-dir=hooks --name ALPR "+add_data+" --icon icons/app_icon.ico"

subprocess.call(command, 
				cwd=".")	