from unittest import TestCase
from unittest.mock import MagicMock, patch
from sys import modules


class TestDeploy(TestCase):
    @patch('nativescript-plugin.deploy_command.DeployNsCommand.on_finished', side_effect=lambda succeded: None)
    def test_deploy_command_when_project_is_none_should_return_none(self, on_finished):
        deploy_command = modules["nativescript-plugin.deploy_command"].DeployNsCommand()
        self.assertIsNone(deploy_command.execute(None, {}))

    @patch('nativescript-plugin.deploy_command.DeployNsCommand.on_finished', side_effect=lambda succeded: None)
    def test_deploy_command_when_device_is_none_should_return_none(self, on_finished):
        deploy_command = modules["nativescript-plugin.deploy_command"].DeployNsCommand()
        self.assertIsNone(deploy_command.execute("some_project_path", None))

    def test_deploy_command_should_pass_correct_parameters(self):
        device_mock = {"platform": "Android", "identifier": "192.168.56.101:5555"}
        project_path = "some_project_path"
        deploy_command = modules["nativescript-plugin.deploy_command"].DeployNsCommand()
        deploy_command.run_command = MagicMock()
        deploy_command.execute(project_path, device_mock)
        deploy_command.run_command.assert_called_with(["deploy",
                                                       device_mock["platform"],
                                                       "--justlaunch",
                                                       "--path", project_path,
                                                       "--device",
                                                       device_mock["identifier"]],
                                                      True,
                                                      "Deploying",
                                                      "Deployment succeeded",
                                                      "Deployment failed")

if __name__ == '__main__':
    unittest.main()
