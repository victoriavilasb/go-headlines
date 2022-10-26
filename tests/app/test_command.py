import unittest

from unittest.mock import MagicMock
from ttrack.repository.database.command import Command
from ttrack.repository.database.models import Project

class TestCommand(unittest.TestCase):

    def test_create_project(self):
        session = MagicMock()
        command = Command(session)

        command.create_project('fake-project-name')
        
        session.add.assert_called_once()
        session.commit.assert_called_once()







