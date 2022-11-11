import subprocess
import shutil
import webbrowser

from ttrack.repository.yaml import Yaml

class Shortcut:
    
    def __init__(self, name: str, path, repo: Yaml):
        self.name = name
        self.path = path
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

        self.open_programs(shortcut["programs"])
        self.open_web_pages(shortcut["pages"])


    def _find_program_path(self, name):
        path = shutil.which(name)
        if len(path) == 0:
            print("WARNING: couldn't find {}.".format(path))

        return path

    def open_web_pages(self, pages): 
        # i`m using brave and it isnt working, test with chrome
        for page in pages:
            webbrowser.open(page, new=0, autoraise=True) 


    def open_programs(self, programs):
        to_open = [program["path"] for program in programs if len(program["path"]) > 0]
        subprocess.call([to_open])
