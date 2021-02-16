import os.path

from hb_db import Database

class Notes():
    
    def save_main_notes_to_db(self, content, folder_id):
        Database().save_notebook(content, False, folder_id)
    
    def save_side_notes_to_db(self, content, folder_id):
        Database().save_notebook(content, True, folder_id)

    def get_side_notes_from_db(self, folder_id):
        return Database().get_side_content(folder_id)

    def get_main_notes_from_db(self, folder_id):
        return Database().get_main_content(folder_id)
