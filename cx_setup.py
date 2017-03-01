from cx_Freeze import Executable
from cx_Freeze import setup

from setup_common import setup_options

setup(executables=[Executable("lpstools/gui.py", base="Win32GUI")],
      **setup_options)
