# Loco Positioning System Tools [![Build Status](https://api.travis-ci.org/bitcraze/lps-tools.svg?branch=master)](https://api.travis-ci.org/bitcraze/lps-tools.svg?branch=master) [![Build status](https://ci.appveyor.com/api/projects/status/dnko8ka5owq07cul?svg=true)](https://ci.appveyor.com/project/bitcraze/lps-tools)

Tools to configure the Loco Positioning System

This tool is still very much work in progress

## Running instruction

This is a python package that requires python 3.4+ and pip. If you are running
in Linux use ```pip3``` instead of ```pip```. For windows and mac-OS any
distribution of Python 3.4 or later should work.

To install for development (will use the files in the repos folder):
```
pip3 install -e .[pyqt5]
```

On linux, if you have installed pyqt5 using some other package manager
```
pip3 install -e .
```

To run the GUI:
```
python3 -m lpstools
```

## Building for Windows

It is possible to build a windows executable of the tool. This allows to
distribute the LPS tool without requiring a python installation.

To build the windows executable, you should first have the LPS tool working
on Windows. The you can build:
```
pip install cx_freeze
python cx_setup.py build
```

The final result is in the folder ```build\exe.win32-3.6```.

## Building installer for Windows

Once the Windows executable is built, you can build the Windows installer.
Building the installer requires the [nsis installer](http://nsis.sourceforge.net/Main_Page).

To build the installer:
```
cd win32install
python generate_nsis.py
```

This will generate the file lpstools.nsi, it can be used to generate the
installer using the nsis compiler:
```
makensis lpstools.nsi
```

## The tooolbelt

If you do not want to install python tools natively you can use the toolbelt
instead. See the [github repository.](https://github.com/bitcraze/toolbelt)

## Coding style

We use tools to automatically check the code style on the build server
(travis). To see what we check for take a look in the .pre-commit-config.yaml
file, it contains a list of all plugins that are running.

To run all checks:

* with native tools
```
tox  # You can also run 'pre-commit run --all-files' to check without virtual environment
```

* with the toolbelt
```
tb verify
```

## Unit testing

* with native tools
```
tox
```

* with the toolbelt
```
tb test
```
