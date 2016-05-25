from .project import Project
from .notifier import log_info


def select_project(nativescript_command, on_project_selected):
    projects = set()
    working_dir = nativescript_command.get_working_dir()
    project_dir = Project.get_project_dir(working_dir)
    if bool(project_dir):
        projects.add(project_dir)

    for folder in nativescript_command.get_window().folders():
        project_dir = Project.get_project_dir(folder)
        if bool(project_dir):
            projects.add(project_dir)

    projectsCount = len(projects)
    projects = list(projects)
    if projectsCount == 1:
        on_project_selected(projects[0])
    elif projectsCount > 1:
        nativescript_command.get_window().show_quick_panel(
            projects,
            lambda project_index:
            on_project_selected(projects[project_index])
            if project_index >= 0 else on_project_selected(None))
    else:
        log_info("There are no projects in your currently opened folders")
        on_project_selected(None)
