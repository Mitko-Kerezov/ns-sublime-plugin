from unittest import TestCase
from unittest.mock import MagicMock, patch
from sys import modules
from json import loads

package_jsons_data = ["""
                      {
                          "name": "first-project",
                          "nativescript": {
                          }
                      }
                      """,
                      """
                      {
                         "name": "second-project",
                          "nativescript": {
                          }
                      }
                      """]


class TestProjects(TestCase):
    def test_select_project_when_no_project_should_return_none(self):
        callback_called = False
        projects_space = modules["nativescript-plugin.projects_space"]

        def _callback(device):
            self.assertIsNone(device)
            nonlocal callback_called
            callback_called = True

        class MockWindow:
            def folders(self):
                return []

        class MockNSCommand:
            def get_working_dir():
                return ""

            def get_window():
                return MockWindow()

        projects_space.select_project(MockNSCommand, _callback)
        self.assertTrue(callback_called)

    @patch('nativescript-plugin.project.path.isdir', side_effect=lambda project_path: True)
    @patch('nativescript-plugin.project.path.isfile', side_effect=lambda file_path: True)
    @patch('nativescript-plugin.project.open', side_effect=lambda file, mode, buffering: package_jsons_data[0])
    @patch('nativescript-plugin.project.load', side_effect=lambda file: loads(file))
    def test_select_project_when_one_project_should_return_project_dir(self, isdir, isfile, open, load):
        callback_called = False
        projects_space = modules["nativescript-plugin.projects_space"]
        working_dir = "working-dir"

        def _callback(project_dir):
            self.assertEqual(project_dir, working_dir)
            nonlocal callback_called
            callback_called = True

        class MockWindow:
            def folders(self):
                return []

        class MockNSCommand:
            def get_working_dir():
                return working_dir

            def get_window():
                return MockWindow()

        projects_space.select_project(MockNSCommand, _callback)
        self.assertTrue(callback_called)

    @patch('nativescript-plugin.project.path.isdir', side_effect=lambda project_path: True)
    @patch('nativescript-plugin.project.path.isfile', side_effect=lambda file_path: True)
    @patch('nativescript-plugin.project.open', side_effect=lambda file, mode, buffering: package_jsons_data[0])
    @patch('nativescript-plugin.project.load', side_effect=lambda file: loads(file))
    def test_select_project_when_multiple_projects_should_prompt_user(self, isdir, isfile, open, load):
        projects_space = modules["nativescript-plugin.projects_space"]
        working_dir = "working-dir"
        sub_dir = "sub-dir"

        class MockWindow:
            def folders(self):
                return [sub_dir]

            def show_quick_panel(ns_command, actual_projects, panel_callback):
                assert [sub_dir, working_dir] == actual_projects

        class MockNSCommand:
            def get_working_dir():
                return working_dir

            def get_window():
                return MockWindow()

        projects_space.select_project(MockNSCommand, None)

    @patch('nativescript-plugin.project.path.isdir', side_effect=lambda project_path: True)
    @patch('nativescript-plugin.project.path.isfile', side_effect=lambda file_path: True)
    @patch('nativescript-plugin.project.open', side_effect=lambda file, mode, buffering: package_jsons_data[0])
    @patch('nativescript-plugin.project.load', side_effect=lambda file: loads(file))
    def test_select_project_when_multiple_projects_when_user_cancels_should_return_none(self, isdir, isfile, open, load):
        callback_called = False
        projects_space = modules["nativescript-plugin.projects_space"]
        working_dir = "working-dir"
        sub_dir = "sub-dir"

        def _callback(project_dir):
            self.assertIsNone(project_dir)
            nonlocal callback_called
            callback_called = True

        class MockWindow:
            def folders(self):
                return [sub_dir]

            def show_quick_panel(ns_command, actual_projects, panel_callback):
                assert [sub_dir, working_dir] == actual_projects
                panel_callback(-1)

        class MockNSCommand:
            def get_working_dir():
                return working_dir

            def get_window():
                return MockWindow()

        projects_space.select_project(MockNSCommand, _callback)
        self.assertTrue(callback_called)

    @patch('nativescript-plugin.project.path.isdir', side_effect=lambda project_path: True)
    @patch('nativescript-plugin.project.path.isfile', side_effect=lambda file_path: True)
    @patch('nativescript-plugin.project.open', side_effect=lambda file, mode, buffering: package_jsons_data[0])
    @patch('nativescript-plugin.project.load', side_effect=lambda file: loads(file))
    def test_select_project_when_multiple_projects_when_user_selects_should_return_project_dir(self, isdir, isfile, open, load):
        callback_called = False
        projects_space = modules["nativescript-plugin.projects_space"]
        working_dir = "working-dir"
        sub_dir = "sub-dir"
        expected_projects = [sub_dir, working_dir]
        index = 1

        def _callback(project_dir):
            self.assertEqual(project_dir, expected_projects[index])
            nonlocal callback_called
            callback_called = True

        class MockWindow:
            def folders(self):
                return [sub_dir]

            def show_quick_panel(ns_command, actual_projects, panel_callback):
                assert expected_projects == actual_projects
                panel_callback(index)

        class MockNSCommand:
            def get_working_dir():
                return working_dir

            def get_window():
                return MockWindow()

        projects_space.select_project(MockNSCommand, _callback)
        self.assertTrue(callback_called)


if __name__ == '__main__':
    unittest.main()
