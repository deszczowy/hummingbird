from hb_db import *
from hb_enums import *

class Context:

    color_theme = EditorTheme.Light
    
    text_size = 13

    is_source_local = False
    source_folder = 1
    
    window_left = 0
    window_top = 0
    window_width = 0
    window_height = 0
    window_maximized = False

    #def __init__(self):

    def load(self):
        self.read_theme_from_db()
        self.read_text_properties()
        self.read_notes_params()
        self.read_window_params()

    def read_theme_from_db(self):
        theme = Database().get_value("theme", "L")
        if theme == "D":
            self.editorTheme = EditorTheme.Dark
        else:
            self.editorTheme = EditorTheme.Light

    def read_text_properties(self):
        self.text_size = int(Database().get_value("text_size", "13"))

    def read_notes_params(self):
        self.is_source_local = Database().get_value("folder_source", "LOCAL") == "LOCAL"
        self.source_folder = int(Database().get_value("folder_opened", "1"))

    def read_window_params(self):
        self.window_left = int(Database().get_value("window_left", "-1"))
        self.window_top = int(Database().get_value("window_top", "-1"))
        self.window_width = int(Database().get_value("window_width", "-1"))
        self.window_height = int(Database().get_value("window_height", "-1"))
        self.windows_maximized = int(Database().get_value("window_max", "0")) == 1

    def store_context(self):
        db = Database()
        #db.store_value("text_size", self.)