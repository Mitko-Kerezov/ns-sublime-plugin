from sublime import active_window
from sublime_plugin import ApplicationCommand
from abc import abstractmethod
from os import path

from .notifier import log_info, log_error
from .command_executor import run_command


class NativeScriptCommand(ApplicationCommand):
    def __init__(self):
        super().__init__()
        self._is_running = False

    @abstractmethod
    def on_started(self):
        pass

    @abstractmethod
    def command_name(self):
        pass

    def active_view(self):
        return self.get_window().active_view()

    def get_window(self):
        return active_window()

    def is_enabled(self):
        return not self._is_running

    def get_working_dir(self):
        file_name = self._active_file_name()
        if file_name:
            return path.realpath(path.dirname(file_name))
        else:
            try:
                return self.get_window().folders()[0]
            except IndexError:
                return ''

    def run(self):
        self._is_running = True
        self.on_started()

    def on_data(self, data):
        log_info(data)

    def on_finished(self, succeded):
        self._is_running = False
        if succeded:
            log_info("%s finished successfully" % self.command_name)
        else:
            log_error("%s failed" % self.command_name)

    def run_command(self, command, show_progress=False,
                    in_progress_message="", success_message="",
                    failure_message=""):
        return run_command(command, self.on_data, self.on_finished,
                           show_progress, in_progress_message,
                           success_message, failure_message)

    def _active_file_name(self):
        view = self.active_view()
        if view and view.file_name() and len(view.file_name()) > 0:
            return view.file_name()
