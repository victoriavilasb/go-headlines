import unittest

from unittest.mock import MagicMock
from ttrack.repository.database.command import Command
from ttrack.repository.database.models import Project, ProjectStatus, Task

class TestCommand(unittest.TestCase):

    def setUp(self):
        self.session = MagicMock()
        self.command = Command(self.session)

    def test_create_project(self):
        self.command.create_project('fake-project-name')
        
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()

    def test_archive_project(self):
        self.command.archive_project('fake-project-name')

        self.session.update.return_value.where.return_value.values.assert_called_with(status = ProjectStatus.archived)
        self.session.commit.assert_called_once()

    def test_create_task(self):
        project = Project(name='fake-project-name')

        self.command.create_task('fake-task-name')

        self.session.query.return_value.filter.return_value.one.return_value(project)
        self.session.add.assert_called_once()
        self.session.commit.assert_called_once()

        






