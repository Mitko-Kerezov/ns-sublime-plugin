from sublime import status_message, set_timeout

_ACCELERATION_VALUE = 1
_INDICATOR_SIZE = 8


def run_progress_indicator(thread, message, success_message, fail_message):
    model = CommandInProgressModel(thread, message,
                                   success_message, fail_message)

    _run(model, 0)


def _run(model, index):
    if model.is_running():
        status_message("%s %s" % (model.message,
                                  _get_busy_animation_part(index)))
        set_timeout(lambda: _run(model, index + _ACCELERATION_VALUE), 100)
    else:
        status_message(model.get_result_message())


def _get_busy_animation_part(index):
    before_count = index % _INDICATOR_SIZE
    after_count = _INDICATOR_SIZE - 1 - before_count
    return "[%s = %s]" % ("-" * before_count, "-" * after_count)


class CommandInProgressModel:
    def __init__(self, thread, message, success_message, fail_message):
        self.iterations_before_release = 20
        self.thread = thread
        self.message = message
        self.success_message = success_message
        self.fail_message = fail_message

    def is_running(self):
        return self.thread.is_alive()

    def get_result_message(self):
        if not self.thread.is_alive():
            if self.thread.success():
                return self.success_message
            else:
                return self.fail_message
        else:
            return ""
