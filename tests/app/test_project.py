import unittest

from unittest.mock import patch
from ttrack.repository.storage import Storage
from ttrack.app.project import ProjectApplication

class TestProject(unittest.TestCase):

    def setUp(self):
        self.storage = Storage()
        self.project_name = 'project-name'

    @patch.object(Storage, 'create_project')
    def test_start(self, create_project):
        project = ProjectApplication(self.storage, self.project_name)

        project.start()

        create_project.assert_called_with(self.project_name)

    @patch.object(Storage, 'update_project_status')
    def test_archive(self, update_project_status):
        project = ProjectApplication(self.storage, self.project_name)

        project.archive()

        update_project_status.assert_called_with(self.project_name, 'ARCHIVED')

