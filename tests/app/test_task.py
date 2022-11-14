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

    @patch.object(Storage, 'update_task_status')
    def test_finish_task(self, update_task_status):
        task = TaskApplication(self.storage, self.task_name, None)
        
        task.finish()

        update_task_status.assert_called_with(self.task_name, 'FINISHED')

    @patch.object(Storage, 'update_task_status')
    @patch.object(Storage, 'find_task', return_value={'status': 'RUNNING'})
    def test_pause_task_when_task_is_not_finished(self, find_task, update_task_status):
        task = TaskApplication(self.storage, self.task_name, None)
        
        task.pause()

        find_task.assert_called_with(self.task_name)

        update_task_status.assert_called_with(self.task_name, 'PAUSED')

    @patch.object(Storage, 'find_task', return_value={'status': 'FINISHED'})
    def test_pause_task_when_task_is_finished(self, find_task):
        task = TaskApplication(self.storage, self.task_name, None)
        
        with self.assertRaises(SystemExit):
            task.pause()

        find_task.assert_called_with(self.task_name)

    @patch.object(Storage, 'find_task', return_value={'name': 'task_name'})
    @patch.object(Storage, 'find_tag', return_value={})
    @patch.object(Storage, 'create_tag')
    def test_add_tag_to_task_when_tag_does_not_exist_and_task_exists(self, create_tag, find_tag, find_task):
        task = TaskApplication(self.storage, self.task_name, None)
        
        task.add_tag_to_task('fake-tag-name')

        find_tag.assert_called_with('fake-tag-name')

        create_tag.assert_called_with('fake-tag-name')

        find_task.assert_called_with(self.task_name)

    @patch.object(Storage, 'find_task', return_value={'name': 'task_name'})
    @patch.object(Storage, 'find_tag', return_value={'name': 'fake-tag-name'})
    def test_add_tag_to_task_when_tag_exists_and_task_exists(self, find_tag, find_task):
        task = TaskApplication(self.storage, self.task_name, None)
        
        task.add_tag_to_task('fake-tag-name')

        find_tag.assert_called_with('fake-tag-name')

        find_task.assert_called_with(self.task_name)

    @patch.object(Storage, 'find_task', return_value={})
    @patch.object(Storage, 'find_tag', return_value={'name': 'fake-tag-name'})
    def test_add_tag_to_task_when_tag_exists_and_task_does_not_exists(self, find_tag, find_task):
        task = TaskApplication(self.storage, self.task_name, None)
        
        with self.assertRaises(SystemExit):
            task.add_tag_to_task('fake-tag-name')

        find_tag.assert_called_with('fake-tag-name')

        find_task.assert_called_with(self.task_name)

    @patch.object(Storage, 'list_tasks', return_value=[{'name': 'task-name'}])
    def test_resume_task_running_task_exist(self, list_tasks):
        task = TaskApplication(self.storage, self.task_name, None)
        
        with self.assertRaises(SystemExit):
            task.resume()

        list_tasks.assert_called_with(status='RUNNING')

    @patch.object(Storage, 'list_tasks', return_value=[])
    @patch.object(Storage, 'update_task_status', return_value={'name': 'fake-tag-name'})
    def test_resume_task_when_no_running_task_exist(self, update_task_status, list_tasks):
        task = TaskApplication(self.storage, self.task_name, None)
        
        task.resume()

        list_tasks.assert_called_with(status='RUNNING')

        update_task_status.assert_called_with(self.task_name, 'RUNNING')

        