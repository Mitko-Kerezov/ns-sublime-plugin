from os import path, pathsep, environ
from subprocess import Popen, PIPE
from platform import system
from functools import lru_cache

from .config import get_config
from .thread_progress import run_progress_indicator
from .command_thread import CommandThread


def run_command(command, on_data=None, on_done=None, show_progress=True,
                in_progress_message="Loading", success_message="",
                failure_message=""):
    nativescript_path = _get_nativescript_path()
    if nativescript_path is None:
        on_done(False)
        return None

    command = nativescript_path + command
    thread = CommandThread(command, on_data, on_done)
    thread.start()

    if show_progress:
        run_progress_indicator(thread, in_progress_message,
                               success_message, failure_message)

    return thread


def show_quick_panel(window, items, on_done):
    window.show_quick_panel(items, on_done)


@lru_cache(maxsize=1)
def _get_nativescript_path():
    _nativescript_path = []
    system_name = system()
    if system_name == "Windows":
        _nativescript_path.append(_find_win_node_path())
        _nativescript_path.append(_find_win_nativescript_path())
    elif system_name == "Darwin":
        osx_node_path = get_config("osx_node_path")
        osx_nativescript_path = get_config("osx_nativescript_path")
        if path.isfile(osx_node_path) and path.isfile(osx_nativescript_path):
            _nativescript_path.append(osx_node_path)
            _nativescript_path.append(osx_nativescript_path)
        else:
            return None
    elif system_name == "Linux":
        linux_node_path = get_config("linux_node_path")
        linux_nativescript_path = get_config("linux_nativescript_path")

        if linux_node_path == "":
            linux_node_path = _get_output(['/bin/bash', '-i',
                                           '-c', 'which node'])

        if linux_nativescript_path == "":
            linux_nativescript_path = _get_output(['/bin/bash', '-i',
                                                   '-c', "which nativescript"])

        if path.isfile(linux_node_path) and path.isfile(linux_nativescript_path):
            _nativescript_path.append(linux_node_path)
            _nativescript_path.append(linux_nativescript_path)
        else:
            return None

    return _nativescript_path


def _get_output(command):
    command_output_raw = Popen(command, stdout=PIPE).communicate()[0]
    return str(command_output_raw.decode("utf-8")).strip()


def _find_win_node_path():
    paths = _get_paths()
    for environ_path in paths:
        try:
            node_path = path.join(environ_path, get_config("win_node_name"))
            proc = Popen([node_path])
            proc.terminate()
            return node_path
        except WindowsError:
            pass
    return get_config("win_node_name")


def _find_win_nativescript_path():
    paths = _get_paths()
    for environ_path in paths:
        try:
            nativescript_path = path.join(environ_path,
                                          get_config("win_nativescript_name"))
            proc = Popen([nativescript_path + ".cmd"])
            proc.terminate()
            if "npm" in environ_path:
                return path.join(environ_path,
                                 "node_modules", "nativescript", "bin",
                                 get_config("win_nativescript_name") + ".js")
            else:
                return path.join(environ_path,
                                 get_config("win_nativescript_name") + ".js")
        except WindowsError:
            pass
    return get_config("win_nativescript_name")


def _get_paths():
    return environ["PATH"].split(pathsep)
