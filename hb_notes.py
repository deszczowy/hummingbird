import os.path

from hb_db import Database

class Notes():
    
    ## new
    def save_text(self, folder, sleeve, content):
        return Database().save_text(folder, sleeve, content)
    
    def get_text(self, folder, sleeve):
        return Database().get_text(folder, sleeve)
