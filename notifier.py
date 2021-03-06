from sublime import set_timeout, active_window
from functools import partial

_INFO_LOG_LEVEL_NAME = "info"
_ERROR_LOG_LEVEL_NAME = "error"
_FAIL_LEVEL_NAME = "fail"


def log_error(message):
    _process_message(message, _ERROR_LOG_LEVEL_NAME)


def log_info(message):
    _process_message(message, _INFO_LOG_LEVEL_NAME)


def log_fail(message):
    _process_message(message, _FAIL_LEVEL_NAME)


def _process_message(message, level):
    window = active_window()
    if window:
        _log(message, level)
    else:
        set_timeout(
            partial(_process_message, message, level), 100
        )


def _log(message, level):
    if level == _INFO_LOG_LEVEL_NAME:
        _log_info(message)
    elif level == _ERROR_LOG_LEVEL_NAME:
        _log_error(message)
    elif level == _FAIL_LEVEL_NAME:
        _log_fail(message)


def _log_error(message):
    _show_panel()
    _log_info(message)


def _log_info(message):
    print(message)


def _log_fail(message):
    error_message(message)


def _show_panel():
    window = active_window()
    if window is None:
        set_timeout(_show_panel, 100)
    else:
        window.run_command("show_panel", {"panel": "console"})
