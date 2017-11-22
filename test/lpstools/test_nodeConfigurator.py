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
import unittest
from unittest.mock import call
from unittest.mock import MagicMock
from unittest.mock import patch

import serial
from serial.tools.list_ports_common import ListPortInfo

from lpstools import nodeConfigurator
from lpstools.nodeConfigurator import NodeConfigurator


class TestNodeConfigurator(unittest.TestCase):
    VID = 0x0483
    PID = 0x5740

    def setUp(self):
        self.sut = NodeConfigurator()

    @patch.object(nodeConfigurator, 'comports', auto_spec=True)
    def test_that_find_node_returns_the_first_matching_port(self,
                                                            comports_mock):
        # Fixture
        expected = '/dev/expected'
        comports_mock.return_value = [
            self._mock_port_info(self.VID, None, 'dev1'),
            self._mock_port_info(None, self.PID, 'dev2'),
            self._mock_port_info(None, None, None),
            self._mock_port_info(self.VID, self.PID, expected),
            self._mock_port_info(self.VID, self.PID, 'dev3')
        ]

        # Test
        actual = self.sut.find_node()

        # Assert
        self.assertEqual(expected, actual)

    @patch.object(nodeConfigurator, 'comports', auto_spec=True)
    def test_that_none_is_returned_if_no_node_is_found(self, comports_mock):
        # Fixture
        comports_mock.return_value = []

        # Test
        actual = self.sut.find_node()

        # Assert
        self.assertIsNone(actual)

    @patch.object(serial, 'Serial', autospec=True)
    def test_that_data_is_written_when_id_is_set(self, ctor_mock):
        # Fixture
        device = '/dev/the_device'
        serial_mock = MagicMock(spec=serial.Serial, autospec=True)
        ctor_mock.side_effect = lambda x: {device: serial_mock}[x]

        # Test
        self.sut.set_id(device, 3)

        # Assert
        serial_mock.write.assert_called_once_with(b'3')
        serial_mock.close.assert_called_once_with()

    @patch.object(serial, 'Serial', autospec=True)
    def test_that_data_is_written_when_mode_is_set(self, ctor_mock):
        # Fixture
        device = '/dev/the_device'
        serial_mock = MagicMock(spec=serial.Serial, autospec=True)
        ctor_mock.side_effect = lambda x: {device: serial_mock}[x]

        # Test
        self.sut.set_mode(device, nodeConfigurator.MODE_TWR_ANCOR)

        # Assert
        serial_mock.write.assert_has_calls([call(b'm'), call(b'0')])
        serial_mock.close.assert_called_once_with()

    @patch.object(serial, 'Serial', autospec=True)
    def test_that_exception_is_raised_when_mode_is_wrong(self, ctor_mock):
        # Fixture
        device = '/dev/the_device'
        serial_mock = MagicMock(spec=serial.Serial, autospec=True)
        ctor_mock.side_effect = lambda x: {device: serial_mock}[x]

        # Test & assert
        self.assertRaises(KeyError, lambda: self.sut.set_mode(device, 666))

        # Assert
        serial_mock.close.assert_called_once_with()

    def _mock_port_info(self, vid, pid, device):
        port_mock = MagicMock(spec=ListPortInfo, auto_spec=True)

        port_mock.vid = vid
        port_mock.pid = pid
        port_mock.device = device

        return port_mock
