from unittest import TestCase
from unittest.mock import MagicMock, patch
from sys import modules
from json import loads

devices_data = ["""
                {"identifier":"192.168.56.101:5555",
                "displayName":"vbox86p",
                "model":"Nexus_6P_API_23",
                "version":"6.0",
                "vendor":"Android",
                "platform":"Android",
                "status":"Connected",
                "errorHelp":null,
                "isTablet":false,
                "type":"Emulator"}
                """,
                """
                {"identifier":"192.168.56.102:5555",
                "displayName":"vbox86p",
                "model":"Nexus_5_API_22",
                "version":"5.0",
                "vendor":"Android",
                "platform":"Android",
                "status":"Connected",
                "errorHelp":null,
                "isTablet":false,
                "type":"Emulator"}
                """]


def _assert_run_command_called_with_correct_parameters(command):
    assert command == ["device", "--json"]


def _run_command_false(command, on_data=None, on_done=None, show_progress=True,
                       in_progress_message="Loading", success_message="",
                       failure_message=""):
    _assert_run_command_called_with_correct_parameters(command)
    on_done(False)


def _run_command_no_devices(command, on_data=None, on_done=None, show_progress=True,
                            in_progress_message="Loading", success_message="",
                            failure_message=""):
    _assert_run_command_called_with_correct_parameters(command)
    on_done(True)


def _run_command_one_device(command, on_data=None, on_done=None, show_progress=True,
                            in_progress_message="Loading", success_message="",
                            failure_message=""):
    _assert_run_command_called_with_correct_parameters(command)
    on_data(devices_data[0])
    on_done(True)


def _run_command_multiple_devices(command, on_data=None, on_done=None, show_progress=True,
                                  in_progress_message="Loading", success_message="",
                                  failure_message=""):
    _assert_run_command_called_with_correct_parameters(command)
    for device_data in devices_data:
        on_data(device_data)
    on_done(True)


class TestDevices(TestCase):
    @patch('nativescript-plugin.devices_space.run_command', side_effect=_run_command_false)
    def test_select_device_when_unsuccessful_should_return_none(self, run_command):
        callback_called = False
        devices = modules["nativescript-plugin.devices_space"]

        def _callback(device):
            self.assertIsNone(device)
            nonlocal callback_called
            callback_called = True
        devices.select_device(None, _callback)
        self.assertTrue(callback_called)

    @patch('nativescript-plugin.devices_space.run_command', side_effect=_run_command_no_devices)
    def test_select_device_when_successful_when_no_devices_should_return_none(self, run_command):
        callback_called = False
        devices = modules["nativescript-plugin.devices_space"]

        def _callback(device):
            self.assertIsNone(device)
            nonlocal callback_called
            callback_called = True
        devices.select_device(None, _callback)
        self.assertTrue(callback_called)

    @patch('nativescript-plugin.devices_space.run_command', side_effect=_run_command_one_device)
    def test_select_device_when_successful_when_one_device_should_return_device(self, run_command):
        callback_called = False
        devices = modules["nativescript-plugin.devices_space"]

        def _callback(actual_device):
            self.assertEqual(actual_device, loads(devices_data[0]))
            nonlocal callback_called
            callback_called = True
        devices.select_device(None, _callback)
        self.assertTrue(callback_called)

    @patch('nativescript-plugin.devices_space.run_command', side_effect=_run_command_multiple_devices)
    def test_select_device_when_successful_when_multiple_devices_should_prompt_user(self, run_command):
        class MockWindow:
            def show_quick_panel(ns_command, actual_devices, callback):
                expected_devices = list(map(lambda device: modules["nativescript-plugin.helpers"].get_device_info(loads(device)), devices_data))
                assert expected_devices == actual_devices

        class MockNSCommand:
            def get_window():
                return MockWindow()

        devices = modules["nativescript-plugin.devices_space"]
        devices.select_device(MockNSCommand, None)

    @patch('nativescript-plugin.devices_space.run_command', side_effect=_run_command_multiple_devices)
    def test_select_device_when_successful_when_multiple_devices_when_user_cancels_should_return_none(self, run_command):
        class MockWindow:
            def show_quick_panel(ns_command, actual_devices, panel_callback):
                expected_devices = list(map(lambda device: modules["nativescript-plugin.helpers"].get_device_info(loads(device)), devices_data))
                assert expected_devices == actual_devices
                panel_callback(-1)

        class MockNSCommand:
            def get_window():
                return MockWindow()

        callback_called = False
        devices = modules["nativescript-plugin.devices_space"]

        def _callback(actual_device):
            self.assertIsNone(actual_device)
            nonlocal callback_called
            callback_called = True
        devices.select_device(MockNSCommand, _callback)

    @patch('nativescript-plugin.devices_space.run_command', side_effect=_run_command_multiple_devices)
    def test_select_device_when_successful_when_multiple_devices_when_user_selects_should_return_device(self, run_command):
        index = 1

        class MockWindow:
            def show_quick_panel(ns_command, actual_devices, panel_callback):
                expected_devices = list(map(lambda device: modules["nativescript-plugin.helpers"].get_device_info(loads(device)), devices_data))
                assert expected_devices == actual_devices
                panel_callback(index)

        class MockNSCommand:
            def get_window():
                return MockWindow()

        callback_called = False
        devices = modules["nativescript-plugin.devices_space"]

        def _callback(actual_device):
            self.assertEqual(actual_device, loads(devices_data[index]))
            nonlocal callback_called
            callback_called = True
        devices.select_device(MockNSCommand, _callback)


if __name__ == '__main__':
    unittest.main()
