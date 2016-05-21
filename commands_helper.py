from .projects_space import select_project
from .devices_space import select_device


def select_project_and_device(nativescript_command, callback):
    select_project(nativescript_command,
                   lambda selected_project:
                   select_device(nativescript_command,
                                 lambda selected_device:
                                 callback(selected_project, selected_device))
                   if selected_project is not None
                   else callback(None, None))
