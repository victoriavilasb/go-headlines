import unittest

from unittest.mock import patch
from ttrack.repository.database.command import Command
from ttrack.repository.database.query import Query
from ttrack.app.task import TaskApplication

class TestTask(unittest.TestCase):

    @patch.object(Command, 'create_task')
    def test_start_with_project(self, mock_method):
        command = Command('fake-session')
        query = Query('fake-session')
        task = TaskApplication(command, query)

        task.start('fake-task-name', 'fake-project-name')

        mock_method.assert_called_with('fake-task-name', 'fake-project-name')

    @patch.object(Command, 'create_task')
    def test_start_with_no_project(self, mock_method):
        command = Command('fake-session')
        query = Query('fake-session')
        task = TaskApplication(command, query)

        task.start('fake-task-name')

        mock_method.assert_called_with('fake-task-name', None)


