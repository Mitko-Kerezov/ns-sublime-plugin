from .base_commands import NativeScriptCommand
from .commands_helper import select_project_and_device


class ToggleLiveSyncNsCommand(NativeScriptCommand):
    def __init__(self):
        super().__init__()
        self._is_checked = False
        self._command_thread = None

    @property
    def command_name(self):
        return "Toggle LiveSync-NS"

    def run(self):
        self.on_started()

    def on_finished(self, succeded):
        pass

    def on_started(self):
        select_project_and_device(self, self.execute)

    def execute(self, project_path, device):
        if not self._is_checked:
            if project_path is None or device is None:
                self.on_finished(False)
                return None

            command = ["livesync", device["platform"],
                       "--watch", "--path", project_path,
                       "--device", device["identifier"]]
            self._command_thread = self.run_command(command, False)
        else:
            self._command_thread.terminate()

        self._is_checked = not self._is_checked

    def is_checked(self):
        return self._is_checked
