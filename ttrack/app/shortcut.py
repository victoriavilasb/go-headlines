import subprocess
import shutil
import webbrowser

from os import environ
from ttrack.repository.yaml import Yaml

SC_PATH = "{}/.ttrack/shortcuts".format(environ['HOME'])

class Shortcut:
    
    def __init__(self, name: str, repo: Yaml):
        self.name = name
        self.path = self._mount_shortcut_path()
        self.repo = repo

    def create(self, pages, programs):
        shortcut = {
            "name": self.name,
            "pages": pages.split(","),
            "programs": []
        }

        for program_name in programs.split(","):
            shortcut["programs"].append({
                "name": program_name,
                "path": self._find_program_path(program_name)
            })

        self.repo.write_file(self.path, shortcut)

    def open(self):
        shortcut = self.repo.read_file(self.path)

        self._open_programs(shortcut["programs"])
        self._open_web_pages(shortcut["pages"])

    def edit(self):
        subprocess.call(["vim", self._mount_shortcut_path()])


    def _find_program_path(self, name):
        path = shutil.which(name)
        if len(path) == 0:
            print("WARNING: couldn't find {}.".format(path))

        return path

    def _open_web_pages(self, pages): 
        for page in pages:
            webbrowser.open(page, new=0, autoraise=True) 


    def _open_programs(self, programs):
        to_open = [program["path"] for program in programs if len(program["path"]) > 0]
        subprocess.call(to_open)

    def _mount_shortcut_path(self):
        return SC_PATH+"/{}.yaml".format(self.name)
