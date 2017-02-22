import os
import sys

from PyQt5 import QtWidgets
from PyQt5 import uic


class LpsToolsGui(QtWidgets.QWidget):

    def __init__(self, uipath):
        super(LpsToolsGui, self).__init__()
        uic.loadUi(uipath + os.path.sep + 'gui.ui', self)
        self.show()


def main():
    filepath = os.path.realpath(__file__)
    uipath = os.path.sep.join(filepath.split(os.path.sep)[:-1])

    app = QtWidgets.QApplication(sys.argv)
    window = LpsToolsGui(uipath)  # noqa
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
