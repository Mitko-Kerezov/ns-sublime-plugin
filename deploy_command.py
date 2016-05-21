from .base_commands import NativeScriptCommand
from .commands_helper import select_project_and_device


class DeployNsCommand(NativeScriptCommand):
    @property
    def command_name(self):
        return "Deploy-NS"

    def on_started(self):
        select_project_and_device(self, self.execute)

    def execute(self, project_path, device):
        if project_path is None or device is None:
            self.on_finished(False)
            return None

        command = ["deploy", device["platform"],
                   "--justlaunch", "--path", project_path,
                   "--device", device["identifier"]]
        self.run_command(command, True,
                         "Deploying", "Deployment succeeded",
                         "Deployment failed")
