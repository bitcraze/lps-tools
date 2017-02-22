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

        # Connect buttons
        self.browseButton.clicked.connect(self._browse_clicked)
        self.updateButton.clicked.connect(self._update_clicked)

        self.show()

    def _browse_clicked(self):
        dialog_type = "QFileDialog.getOpenFileName()"
        dialog_filter = "DFU Files (*.dfu);;All Files (*)"
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                            dialog_type,
                                                            "",
                                                            dialog_filter)
        self.dfufile_line.setText(filename)

    def _update_clicked(self):
        print("TODO: Flashing %s" % self.dfufile_line.text())
        self.dfu_progress.setValue(42)


def main():
    filepath = os.path.realpath(__file__)
    uipath = os.path.sep.join(filepath.split(os.path.sep)[:-1])
    uipath += os.path.sep + "assets" + os.path.sep

    app = QtWidgets.QApplication(sys.argv)
    window = LpsToolsGui(uipath)  # noqa
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
