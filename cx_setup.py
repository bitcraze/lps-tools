import sys
from cx_Freeze import setup, Executable
from setup_common import setup_options

setup(**setup_options,
      executables = [Executable("lpstools/gui.py", base = "Win32GUI")])
