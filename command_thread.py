from threading import Thread
from subprocess import PIPE, STARTUPINFO, STARTF_USESTDHANDLES, \
    STARTF_USESHOWWINDOW, STDOUT, Popen
from os import name
from sublime import set_timeout
from functools import partial

from .notifier import log_error


def main_thread(callback, *args):
    set_timeout(partial(callback, *args), 0)


def _get_command_failed_message(exit_code):
    return "Command failed with exit code: {code}".format(code=exit_code)


class CommandThread(Thread):
    def __init__(self, command, on_data, on_done):
        super().__init__()
        self.command = command
        self.on_data = on_data
        self.on_done = on_done
        self.stdin = PIPE
        self.stdout = PIPE
        self.proc = None

    def run(self):
        if name == "nt":
            startupinfo = STARTUPINFO()
            startupinfo.dwFlags = STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW

        self.proc = Popen(self.command,
                          stdout=self.stdout, stderr=STDOUT,
                          stdin=self.stdin, universal_newlines=True,
                          startupinfo=startupinfo)

        if self.on_data:
            for line in iter(self.proc.stdout.readline, ""):
                main_thread(self.on_data, line)

        self.proc.wait()

        if self.proc.returncode:
            main_thread(log_error,
                        _get_command_failed_message(self.proc.returncode))

        self._on_finished(self.proc.returncode == 0)

    def success(self):
        return not self.is_alive() and self.proc and not self.proc.returncode

    def _on_finished(self, succeeded):
        if self.on_done:
            main_thread(self.on_done, succeeded)
