import subprocess
import uuid
import unittest

class TestTtrackE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config_environment()

    def setUp(self):
        self.task_name = 'task_{}'.format(uuid.uuid4())
        self.project_name = 'project_{}'.format(uuid.uuid4())
        
        self._start_project()
        self._start_task()
   
    def test_check_if_task_exists(self):
        output = self._get_task_by_status("RUNNING")
        self.assertIn(self.task_name, output)

    def test_check_if_task_is_running(self):
        output = self._get_task_by_status("RUNNING")
        self.assertIn(self.task_name, output)

    def test_finish_task(self):
        self._finish_task()

        output = self._get_task_by_status("FINISHED")
        self.assertIn(self.task_name, output)

    def test_check_project(self):
        output = self._get_project_by_status("ACTIVE")
        self.assertIn(self.project_name, output)

    def test_archive_project(self):
        self._archive_project()
        output = self._get_project_by_status("ARCHIVED")
        self.assertIn(self.project_name, output)

    def _start_task(self):
        subprocess.call([
            "python3",
            "-m",
            "ttrack",
            "start",
            "task",
            self.task_name,
            "--project",
            self.project_name,
            "--force"
        ])

    def _start_project(self):
        subprocess.run([
            "python3",
            "-m",
            "ttrack",
            "start",
            "project",
            self.project_name,
        ])

    def _finish_task(self):
        subprocess.run([
            "python3",
            "-m",
            "ttrack",
            "finish",
            "--task",
            self.task_name,
        ])

    def _get_task_by_status(self, status):
        ps = subprocess.run([
            "python3",
            "-m",
            "ttrack",
            "list",
            "--tasks"
        ],  capture_output=True)

        out = subprocess.run(["grep", status], input=ps.stdout, capture_output=True)

        return str(out.stdout.decode('utf-8').strip())

    def _get_project_by_status(self, status):
        ps = subprocess.run([
            "python3",
            "-m",
            "ttrack",
            "list",
            "--projects"
        ],  capture_output=True)

        out = subprocess.run(["grep", status], input=ps.stdout, capture_output=True)

        return str(out.stdout.decode('utf-8').strip())

    def _archive_project(self):
        subprocess.run([
            "python3",
            "-m",
            "ttrack",
            "archive",
            "--project",
            self.project_name,
        ])

def config_environment():
    # configure ttrack
    subprocess.run([
        "python3",
        "-m",
        "ttrack",
        "config",
        "--storage",
        "database",
        "--uri",
        "postgresql://postgres:postgres@0.0.0.0:5432/ttrack"
    ])

    # run database migrations
    subprocess.run(["alembic", "upgrade", "head"])