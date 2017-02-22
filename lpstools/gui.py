import os
import sys

from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


class LpsToolsGui(QtWidgets.QMainWindow):

    def __init__(self, uipath):
        super(LpsToolsGui, self).__init__()
        uic.loadUi(uipath + os.path.sep + 'gui.ui', self)

        # Loading infographics
        pixmap = QPixmap(uipath + 'InfoGraphic_updateNode_step-1.png')
        w = self.infoLabel.width()
        h = self.infoLabel.height()
        self.infoLabel.setPixmap(pixmap.scaled(w, h, Qt.KeepAspectRatio))

        self.show()


def main():
    filepath = os.path.realpath(__file__)
    uipath = os.path.sep.join(filepath.split(os.path.sep)[:-1])
    uipath += os.path.sep + "assets" + os.path.sep

    app = QtWidgets.QApplication(sys.argv)
    window = LpsToolsGui(uipath)  # noqa
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
