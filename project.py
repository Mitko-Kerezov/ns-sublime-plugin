from os import path
from json import load
from codecs import open


class Project:
    PROJECT_FILE_NAME = "package.json"
    PROJECT_KEY = "nativescript"

    @staticmethod
    def get_project_dir(project_path):
        if path.isdir(project_path):
            pair = (project_path, True)
            while bool(pair[1]):
                if Project._has_valid_project_file(pair[0]):
                    return pair[0]
                else:
                    pair = path.split(pair[0])

    @staticmethod
    def _has_valid_project_file(project_path):
        file_name = path.join(project_path, Project.PROJECT_FILE_NAME)
        if path.isfile(file_name):
            try:
                json_data = open(file_name, "r", "utf-8")
                return Project.PROJECT_KEY in load(json_data)
            except UnicodeError:
                return False
