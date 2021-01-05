# -*- coding: utf-8 -*-
import os
from subprocess import PIPE
from subprocess import Popen

import jinja2

DIST_PATH = "..\\build\\exe.win32-3.7"
EXCLUDED_FILES = ["Qt5WebEngineCore.dll", "qtwebengine_devtools_resources.pak"]

# Get list of files and directory to install/uninstall
INSTALL_FILES = []
INSTALL_DIRS = []

os.chdir(os.path.join(os.path.dirname(__file__), DIST_PATH))
for root, dirs, files in os.walk("."):
    for f in files:
        if len(list(filter(lambda e: e in f, EXCLUDED_FILES))) != 0:
            print("Ignoring excluded file {}".format(f))
            continue
        INSTALL_FILES += [os.path.join(root[2:], f)]
    INSTALL_DIRS += [root[2:]]

print("Found {} files in {} folders to install.".format(len(INSTALL_FILES),
                                                        len(INSTALL_DIRS)))


# Get git tag or VERSION
try:
    process = Popen(["git", "describe", "--tags"], stdout=PIPE)
    (output, err) = process.communicate()
    exit_code = process.wait()
except OSError:
    raise Exception("Cannot run git: Git is required to generate installer!")

VERSION = output.strip().decode("utf-8")

print("Lps-tools version {}".format(VERSION))

os.chdir("..\\..\\win32install")

with open("lps-tools.nsi.tmpl", "r") as template_file:
    TEMPLATE = template_file.read()

TMPL = jinja2.Template(TEMPLATE)

with open("lpstools.nsi", "w") as out_file:
    out_file.write(TMPL.render(files=INSTALL_FILES,
                               dirs=INSTALL_DIRS,
                               version=VERSION))
