from .base_commands import NativeScriptCommand
from .commands_helper import select_project_and_device


class LiveSyncNsCommand(NativeScriptCommand):
    @property
    def command_name(self):
        return "Sync-NS"

    def on_started(self):
        select_project_and_device(self, self.execute)

    def execute(self, project_path, device):
        """
        LiveSyncs NativeScript project on device.
        """
        if project_path is None or device is None:
            self.on_finished(False)
            return None

        command = ["livesync", device["platform"],
                   "--justlaunch", "--path", project_path,
                   "--device", device["identifier"]]
        self.run_command(command, True,
                         "LiveSync in progress", "LiveSync succeeded",
                         "LiveSync failed")
