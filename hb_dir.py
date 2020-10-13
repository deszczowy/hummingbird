import os

from pathlib import Path

class Directory():

    def __init__(self):
        self.root = os.path.dirname(os.path.realpath(__file__))
        self.notes = "storage"
        self.resource = "res"

    def get_notes_dir(self):
        notesDir = self.root + os.path.sep + self.notes
        Path(notesDir).mkdir(parents=True, exist_ok=True)
        return notesDir + os.path.sep

    def get_resource_dir(self):
        return self.root + os.path.sep + self.resource + os.path.sep

    def get_file_content(self, path):
        content = ""
        with open(path, 'a+') as _file:
            _file.seek(0)
            content = _file.read() 
        return content