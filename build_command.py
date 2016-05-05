from sublime_plugin import ApplicationCommand

class BuildNsCommand(ApplicationCommand):
    @property
    def command_name(self):
        return "Build-NS"

    def run(self):
        print("Attempting to run " + self.command_name)