import unittest

from unittest.mock import patch
from ttrack.repository.storage import Storage
from ttrack.app.task import TaskApplication

class TestTask(unittest.TestCase):
    
    def setUp(self):
        self.storage = Storage()
        self.task_name = 'task-name'

    @patch.object(Storage, 'find_project', return_value={'name': 'project-name'})
    @patch.object(Storage, 'list_tasks', return_value=[])
    @patch.object(Storage, 'create_task')
    def test_start_when_project_is_given(self, create_task, list_tasks, find_project):
        project = 'project-name'

        task = TaskApplication(self.storage, self.task_name, project)

        task.start(force=False)

        find_project.assert_called_with(project)
        list_tasks.assert_called_with(status='RUNNING')
        create_task.assert_called_with(self.task_name, project)

    @patch.object(Storage, 'list_tasks', return_value=[])
    @patch.object(Storage, 'create_task')
    def test_start_when_project_is_not_given(self, create_task, list_tasks):
        task = TaskApplication(self.storage, self.task_name, None)

        task.start(force=False)

        list_tasks.assert_called_with(status='RUNNING')
        create_task.assert_called_with(self.task_name, None)

    @patch.object(Storage, 'find_project', return_value={})
    def test_start_when_project_is_given_and_does_not_exists(self, find_project):
        project = 'project-name'

        task = TaskApplication(self.storage, self.task_name, project)

        with self.assertRaises(SystemExit):
            task.start(force=False)

        find_project.assert_called_with(project)

    @patch.object(Storage, 'list_tasks', return_value=[{'name': 'running_task', 'status': 'RUNNING'}])
    def test_start_when_a_running_task_exists_and_force_false(self, list_tasks):
        task = TaskApplication(self.storage, self.task_name, None)
        
        with self.assertRaises(SystemExit):
            task.start(force=False)

        list_tasks.assert_called_with(status='RUNNING')

    @patch.object(Storage, 'list_tasks', return_value=[{'name': 'running-task', 'status': 'RUNNING'}])
    @patch.object(Storage, 'create_task')
    @patch.object(Storage, 'update_task_status')
    def test_start_when_a_running_task_exists_and_force_true(self, update_task_status, create_task, list_tasks):
        task = TaskApplication(self.storage, self.task_name, None)
        
        task.start(force=True)

        list_tasks.assert_called_with(status='RUNNING')
        update_task_status.assert_called_with('running-task', 'PAUSED')
        create_task.assert_called_with(self.task_name, None)


