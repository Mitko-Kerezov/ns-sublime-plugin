from unittest import TestCase
from unittest.mock import MagicMock, patch
from sys import modules


class TestLiveSync(TestCase):
    @patch('nativescript-plugin.toggle_livesync_command.ToggleLiveSyncNsCommand.on_finished', side_effect=lambda succeded: None)
    def test_toggle_livesync_command_when_project_is_none_should_return_none(self, on_finished):
        toggle_livesync_command = modules["nativescript-plugin.toggle_livesync_command"].ToggleLiveSyncNsCommand()
        self.assertIsNone(toggle_livesync_command.execute(None, {}))

    @patch('nativescript-plugin.toggle_livesync_command.ToggleLiveSyncNsCommand.on_finished', side_effect=lambda succeded: None)
    def test_toggle_livesync_command_when_device_is_none_should_return_none(self, on_finished):
        toggle_livesync_command = modules["nativescript-plugin.toggle_livesync_command"].ToggleLiveSyncNsCommand()
        self.assertIsNone(toggle_livesync_command.execute("some_project_path", None))

    def test_toggle_livesync_command_should_pass_correct_parameters(self):
        device_mock = {"platform": "Android", "identifier": "192.168.56.101:5555"}
        project_path = "some_project_path"
        toggle_livesync_command = modules["nativescript-plugin.toggle_livesync_command"].ToggleLiveSyncNsCommand()
        toggle_livesync_command.run_command = MagicMock()
        toggle_livesync_command.execute(project_path, device_mock)
        toggle_livesync_command.run_command.assert_called_with(["livesync",
                                                                device_mock["platform"],
                                                                "--watch",
                                                                "--path", project_path,
                                                                "--device",
                                                                device_mock["identifier"]],
                                                               False)

    def test_toggle_livesync_command_when_called_for_second_time_should_terminate_process(self):
        device_mock = {"platform": "Android", "identifier": "192.168.56.101:5555"}
        project_path = "some_project_path"
        toggle_livesync_command = modules["nativescript-plugin.toggle_livesync_command"].ToggleLiveSyncNsCommand()
        terminate_called = False

        class MockThread():
            def terminate(self):
                nonlocal terminate_called
                terminate_called = True

        mock_thread = MockThread()
        toggle_livesync_command.run_command = MagicMock(return_value=MockThread())
        toggle_livesync_command.execute(project_path, device_mock)
        toggle_livesync_command.run_command.assert_called_with(["livesync",
                                                                device_mock["platform"],
                                                                "--watch",
                                                                "--path", project_path,
                                                                "--device",
                                                                device_mock["identifier"]],
                                                               False)
        toggle_livesync_command.execute(project_path, device_mock)
        self.assertTrue(terminate_called)

if __name__ == '__main__':
    unittest.main()
