import os
import platform
import sys
import time

import serial
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox

from lpstools import dfu
from lpstools import nodeConfigurator


STATE_NO_FIRMWARE = "no firmware"
STATE_DFU = "dfu"
STATE_DFU_FLASHING = "dfu flashing"
STATE_DFU_DONE = "dfu done"

MODES = {
    0: nodeConfigurator.MODE_TWR_ANCOR,
    1: nodeConfigurator.MODE_TAG,
    2: nodeConfigurator.MODE_SNIFFER,
    3: nodeConfigurator.MODE_TDOA2_ANCOR,
    4: nodeConfigurator.MODE_TDOA3_ANCOR,
}


class LpsToolsGui(QtWidgets.QMainWindow):
    programming_error = pyqtSignal('QString')
    programming_done = pyqtSignal()
    programming_progress = pyqtSignal('QString', float)
    config_done = pyqtSignal()
    config_progress = pyqtSignal(float)

    def __init__(self, uipath):
        super(LpsToolsGui, self).__init__()
        uic.loadUi(uipath + 'gui.ui', self)

        self.dfu_progress.setValue(0)
        self.cfg_progress.setValue(0)
        self._style_for_platform()

        # Connect buttons
        self.browseButton.clicked.connect(self._browse_clicked)
        self.updateButton.clicked.connect(self._update_clicked)
        self.configureButton.clicked.connect(self._configure_clicked)

        self._uipath = uipath

        self._dfu = dfu.dfu()
        self._node_configurator = nodeConfigurator.NodeConfigurator()

        self._state = STATE_NO_FIRMWARE
        self._dfu_connected = False

        self._device_detector_timer = QtCore.QTimer(self)
        self._device_detector_timer.timeout.connect(self._dfu_present)
        self._device_detector_timer.start(100)

        self.programming_error.connect(self._show_error)
        self.programming_done.connect(self._programming_done)
        self.programming_progress.connect(self._programming_progress)

        self.config_done.connect(self._config_done)
        self.config_progress.connect(self._config_progress)

        self._node_device = None
        self._node_connected = False

        self._update_state()

        self.show()

    # Styling

    def _style_for_platform(self):
        if platform.system() == 'Darwin':
            (Version, _, machine) = platform.mac_ver()
            tVersion = tuple(map(int, (Version.split("."))))
            yosemite = (10, 10, 0)

            if tVersion >= yosemite:
                self.setStyleSheet(
                    'QProgressBar {border: 0px; '
                    'background-color: transparent; '
                    'text-align: center;}')

    # UI Events handling

    def _browse_clicked(self):
        dialog_type = "QFileDialog.getOpenFileName()"
        dialog_filter = "DFU Files (*.dfu);;All Files (*)"
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self,
                                                            dialog_type,
                                                            "",
                                                            dialog_filter)
        self.dfufile_line.setText(filename)

        self.state = STATE_DFU

    def _update_clicked(self):
        # Flashing in a thread to keep the UI alive
        self._flasher_thread = _DfuThread(self, self._dfu,
                                          self.dfufile_line.text(),
                                          self.programming_progress.emit)
        self._flasher_thread.start()

        self.state = STATE_DFU_FLASHING

    def _configure_clicked(self):
        # Flashing in a thread to keep the UI alive
        mode_index = self.configure_mode_combo.currentIndex()
        self._cfg_thread = _ConfigureThread(self, self._node_device,
                                            self.configure_id_line.value(),
                                            mode_index)
        self._cfg_thread.start()

    def _show_error(self, error):
        msgbox = QMessageBox(self)
        msgbox.setText(error)
        msgbox.setWindowTitle("Error")
        msgbox.setIcon(QMessageBox.Critical)
        msgbox.show()

        self.state = STATE_DFU

    def _programming_done(self):
        self.state = STATE_DFU_DONE

    def _programming_progress(self, str, progress):
        self.dfu_progress.setValue(int(progress * 100))

    def _config_done(self):
        self.cfg_progress.setValue(100)
        self.cfg_progress.setFormat("Success!")

    def _config_progress(self, progress):
        self.cfg_progress.setFormat("%p%")
        self.cfg_progress.setValue(int(progress * 100))

    # UI State handling

    def _display_help(self, helpfile):
        pixmap = QPixmap(self._uipath + helpfile)  # noqa
        w = self.infoLabel.width()
        h = self.infoLabel.height()
        self.infoLabel.setPixmap(pixmap.scaled(w, h, Qt.KeepAspectRatio))

    def _update_state(self):
        if self._node_connected:
            self._display_help('help_5.png')
            self.updateButton.setEnabled(False)
            self.configureButton.setEnabled(True)
        elif not self._dfu_connected:
            self._display_help('help_2.png')
            self.updateButton.setEnabled(False)
            self.configureButton.setEnabled(False)
        elif self._state == STATE_NO_FIRMWARE:
            self._display_help('help_1.png')
            self.updateButton.setEnabled(False)
            self.configureButton.setEnabled(False)
        elif self._state == STATE_DFU and self._dfu_connected:
            self._display_help('help_3.png')
            self.updateButton.setEnabled(True)
            self.dfu_progress.setValue(0)
            self.dfu_progress.setFormat("%p%")
            self.configureButton.setEnabled(False)
        elif self._state == STATE_DFU_FLASHING:
            self._display_help('help_3.png')
            self.updateButton.setEnabled(False)
            self.dfu_progress.setFormat("%p%")
            self.configureButton.setEnabled(False)
        elif self._state == STATE_DFU_DONE:
            self._display_help('help_4.png')
            self.updateButton.setEnabled(True)
            self.dfu_progress.setFormat("Success!")
            self.configureButton.setEnabled(False)

    # Timer functions

    def _dfu_present(self):
        if self.state != STATE_DFU_FLASHING:
            try:
                self._dfu.find_device()
                self.dfu_connected = True
            except Exception:
                self.dfu_connected = False
                if self.state != STATE_NO_FIRMWARE:
                    self.state = STATE_DFU

        self._node_device = self._node_configurator.find_node()
        self.node_connected = self._node_device is not None
        if not self._node_connected:
            self.cfg_progress.setValue(0)
            self.cfg_progress.setFormat("%p%")

    # Properties

    def _get_state(self):
        return self._state

    def _set_state(self, state):
        self._state = state
        self._update_state()

    state = property(_get_state, _set_state)

    def _get_dfu_connected(self):
        return self._dfu_connected

    def _set_dfu_connected(self, dfu_connected):
        self._dfu_connected = dfu_connected
        self._update_state()

    dfu_connected = property(_get_dfu_connected, _set_dfu_connected)

    def _get_node_connected(self):
        return self._node_connected

    def _set_node_connected(self, node_connected):
        self._node_connected = node_connected
        self._update_state()

    node_connected = property(_get_node_connected, _set_node_connected)


class _DfuThread(QtCore.QThread):

    def __init__(self, window, dfu, file, callback):
        QtCore.QThread.__init__(self)
        self._window = window
        self._file = file
        self._callback = callback
        self._dfu = dfu

    def run(self):
        try:
            self._dfu.flash(self._file, self._callback)
            self._window.programming_done.emit()
        except dfu.usb.USBError as e:
            self._window.programming_error.emit("USB Error, node" +
                                                " disconnected? (%s)" % str(e))
        except Exception as e:
            self._window.programming_error.emit("Error while programming: " +
                                                str(e))


class _ConfigureThread(QtCore.QThread):

    def __init__(self, window, node_device, id, mode):
        QtCore.QThread.__init__(self)
        self._window = window
        self._id = id
        self._mode = mode
        self._node_device = node_device
        self._node_configurator = nodeConfigurator.NodeConfigurator()

    def run(self):
        self._window.config_progress.emit(0)

        for timeout in range(20):
            try:
                self._node_configurator.set_id(self._node_device,
                                               self._id)
                newmode = MODES[self._mode]
                self._node_configurator.set_mode(self._node_device, newmode)
                self._window.config_done.emit()
                return
            except serial.serialutil.SerialException as e:
                if e.errno == 16:
                    self._window.config_progress.emit(timeout / 21)
                    time.sleep(1)
                else:
                    self._window.programming_error.emit("Error while " +
                                                        "configuring: " +
                                                        str(e))

                    self._window.config_progress.emit(0)
                    return

            except Exception as e:
                self._window.programming_error.emit("Error while " +
                                                    "configuring: " +
                                                    str(e))

                self._window.config_progress.emit(0)
                return

        self._window.programming_error.emit("Error while configuring: " +
                                            "Serial port busy")
        self._window.config_progress.emit(0)


def main():
    if getattr(sys, 'frozen', False):
        # frozen
        uipath = os.path.dirname(sys.executable)
    else:
        # unfrozen
        uipath = os.path.dirname(os.path.realpath(__file__))
    uipath += os.path.sep + "assets" + os.path.sep

    app = QtWidgets.QApplication(sys.argv)
    window = LpsToolsGui(uipath)  # noqa
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
