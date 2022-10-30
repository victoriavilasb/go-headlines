import unittest

from unittest.mock import patch
from ttrack.repository.storage import Storage
from ttrack.app.task import TaskApplication

class TestTask(unittest.TestCase):

    @patch.object(Storage, 'create_task')
    def test_start_with_project(self, mock_method):
        storage = Storage('fake-session')
        task = TaskApplication(storage)

        task.start('fake-task-name', 'fake-project-name')

        mock_method.assert_called_with('fake-task-name', 'fake-project-name')

    @patch.object(Storage, 'create_task')
    def test_start_with_no_project(self, mock_method):
        storage = Storage('fake-session')
        task = TaskApplication(storage)

        task.start('fake-task-name')

        mock_method.assert_called_with('fake-task-name', None)
