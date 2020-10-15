import os.path

from hb_db import Database

class Notes():
    
    def save_main_notes_to_db(self, content):
        Database().save_notebook(content, False)
    
    def save_side_notes_to_db(self, content):
        Database().save_notebook(content, True)

    def get_side_notes_from_db(self):
        return Database().get_side_content()

    def get_main_notes_from_db(self):
        return Database().get_main_content()
