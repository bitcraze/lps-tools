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
import serial
from serial.tools.list_ports import comports

MODE_TWR_ANCOR = 0
MODE_TAG = 1
MODE_SNIFFER = 2
MODE_TDOA2_ANCOR = 3
MODE_TDOA3_ANCOR = 4


class NodeConfigurator:
    VID = 0x0483
    PID = 0x5740

    modes = {
        MODE_TWR_ANCOR:     ['m', '0'],
        MODE_TAG:           ['t'],
        MODE_SNIFFER:       ['s'],
        MODE_TDOA2_ANCOR:    ['m', '3'],
        MODE_TDOA3_ANCOR:    ['m', '4']
    }

    def find_node(self):
        ports = comports()

        for port in ports:
            if port.vid == self.VID and port.pid == self.PID:
                return port.device

    def set_id(self, device, id):
        if id < 10:
            ser = serial.Serial(device)
            ser.write(str(id).encode('utf-8'))
            ser.close()
        else:
            ser = serial.Serial(device)
            ser.write("i".encode('utf-8'))
            ser.write(str(id).encode('utf-8'))
            ser.write("\n".encode('utf-8'))
            ser.close()

    def set_mode(self, device, mode):
        ser = serial.Serial(device)
        try:
            for token in self.modes[mode]:
                ser.write(token.encode('utf-8'))
        except KeyError as e:
            ser.close()
            raise e
        ser.close()
