import glob
import os
import shutil
import sys
from os import path

from cx_Freeze import Executable
from cx_Freeze import setup

from setup_common import setup_options

files_to_copy = [
    ('lpstools\\assets\\*', 'assets\\')
]

setup(executables=[Executable("lpstools/gui.py", target_name="lpstool.exe",
                              base="Win32GUI", icon="bitcraze.ico")],
      **setup_options)

print()
print("Custom copy:")
if len(sys.argv) > 1 and sys.argv[1] == "build":
    for instr in files_to_copy:
        destpath = "build\\exe.win-amd64-3.11\\" + instr[1]
        print("Making folder {}".format(destpath))
        os.makedirs(destpath, exist_ok=True)
        for filepath in glob.glob(instr[0]):
            filename = path.sep.split(filepath)[-1]
            print("Copying {} to {}".format(filepath, destpath))
            shutil.copy(filepath, destpath)
