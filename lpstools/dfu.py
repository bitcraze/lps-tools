# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2017 Bitcraze AB
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.
"""
This class handle dfu update of the firmware
"""
import math

import usb.core
import usb.util

import dfuse


class dfu():
    TRANSFER_SIZE = 2048
    VID = 0x0483
    PID = 0xdf11
    CFG = 0
    INTF = 0
    ALT = 0

    def find_device(self):
        """
        :Try to find the DFU device and return it"""
        usbdev = usb.core.find(idVendor=self.VID, idProduct=self.PID)

        if usbdev is not None:

            dfuDev = dfuse.DfuDevice(usbdev)
            for _, alt in dfuDev.alternates():
                if alt.configuration == self.CFG and \
                        alt.bInterfaceNumber == self.INTF and \
                        alt.bAlternateSetting == self.ALT:
                    dfuDev.set_alternate(alt)
                    status = dfuDev.get_status()
                    if status[1] == dfuse.DfuState.DFU_ERROR:
                        dfuDev.clear_status()  # Clear left-over errors
                    return dfuDev
        raise ValueError('No DfuSe compatible device found')

    def wait_for_device_ready(self, dfuDev):
        status = dfuDev.wait_while_state(
            dfuse.DfuState.DFU_DOWNLOAD_BUSY)
        if status[1] != dfuse.DfuState.DFU_DOWNLOAD_IDLE:
            raise RuntimeError(
                "An error occured. Device Status: {}".format(status))

    def flash(self, filepath, callback):
        dfuDev = self.find_device()
        dfufile = dfuse.DfuFile(filepath)

        targets = [t for t in dfufile.targets if t[
            'alternate'] == dfuDev.intf.bAlternateSetting]

        if len(targets) == 0:
            raise ValueError("No file target matches the device")

        total_transfer_blocks = 0
        blocks_transfered = 0
        for t in targets:
            for idx, image in enumerate(t['elements']):
                total_transfer_blocks += math.ceil(
                    len(image['data']) / self.TRANSFER_SIZE)

        for t in targets:
            for idx, image in enumerate(t['elements']):

                callback("Flashing", 0)

                data = image['data']
                flash_addr = image['address']
                blocks = [data[i:i + self.TRANSFER_SIZE]
                          for i in range(0, len(data), self.TRANSFER_SIZE)]

                for blocknum, block in enumerate(blocks):
                    block_addr = flash_addr + blocknum * self.TRANSFER_SIZE
                    dfuDev.erase(block_addr)
                    self.wait_for_device_ready(dfuDev)

                    dfuDev.set_address(flash_addr)
                    self.wait_for_device_ready(dfuDev)

                    dfuDev.write(blocknum, block)
                    self.wait_for_device_ready(dfuDev)

                    blocks_transfered += 1
                    callback("Flashing", blocks_transfered /
                             total_transfer_blocks)

                dfuDev.leave()
                callback("Flashing", 1.0)
