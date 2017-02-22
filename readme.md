# Loco Positioning System Tools

Tools to configure the Loco Positioning System

This tool is still very much work in progress

## Running instruction

This is a python package that requires python 3.4+ and pip. If you are running
in Linux use ```pip3``` instead of ```pip```. For windows and mac-OS any
distribution of Python 3.4 or later should work.

To install for development (will use the files in the repos folder):
```
pip install -e .
```

To install in the system:
```
pip install .
```

To run the GUI:
```
python3 -m lpstools.gui
```

## Coding style

We use tools to automatically check the code style on the build server 
(travis). To see what we check for take a look in the .pre-commit-config.yaml 
file, it contains a list of all plugins that are running.
