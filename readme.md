# Loco Positioning System Tools [![Build Status](https://api.travis-ci.org/bitcraze/lps-tools.svg?branch=master)](https://api.travis-ci.org/bitcraze/lps-tools.svg?branch=master)

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
tox
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
