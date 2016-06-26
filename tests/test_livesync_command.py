from unittest import TestCase
from unittest.mock import MagicMock, patch
from sys import modules


class TestLiveSync(TestCase):
    @patch('nativescript-plugin.livesync_command.LiveSyncNsCommand.on_finished', side_effect=lambda succeded: None)
    def test_livesync_command_when_project_is_none_should_return_none(self, on_finished):
        livesync_command = modules["nativescript-plugin.livesync_command"].LiveSyncNsCommand()
        self.assertIsNone(livesync_command.execute(None, {}))

    @patch('nativescript-plugin.livesync_command.LiveSyncNsCommand.on_finished', side_effect=lambda succeded: None)
    def test_livesync_command_when_device_is_none_should_return_none(self, on_finished):
        livesync_command = modules["nativescript-plugin.livesync_command"].LiveSyncNsCommand()
        self.assertIsNone(livesync_command.execute("some_project_path", None))

    def test_livesync_command_should_pass_correct_parameters(self):
        device_mock = {"platform": "Android", "identifier": "192.168.56.101:5555"}
        project_path = "some_project_path"
        livesync_command = modules["nativescript-plugin.livesync_command"].LiveSyncNsCommand()
        livesync_command.run_command = MagicMock()
        livesync_command.execute(project_path, device_mock)
        livesync_command.run_command.assert_called_with(["livesync",
                                                         device_mock["platform"],
                                                         "--justlaunch",
                                                         "--path", project_path,
                                                         "--device",
                                                         device_mock["identifier"]],
                                                        True,
                                                        "LiveSync in progress",
                                                        "LiveSync succeeded",
                                                        "LiveSync failed")

if __name__ == '__main__':
    unittest.main()
