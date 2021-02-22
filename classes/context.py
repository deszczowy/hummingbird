from hb_db import *
from hb_enums import *

class Context:

    color_theme = EditorTheme.Light
    
    text_size = 13

    is_source_local = False
    source_folder = 1
    source_path = ""
    
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
            self.color_theme = EditorTheme.Dark
        else:
            self.color_theme = EditorTheme.Light

    def read_text_properties(self):
        self.text_size = int(Database().get_value("text_size", "13"))

    def read_notes_params(self):
        db = Database()
        self.is_source_local = db.get_value("folder_source", "LOCAL") == "LOCAL"
        self.source_folder = int(db.get_value("folder_opened", "1"))
        self.source_path = db.get_value("folder_path", "")

    def read_window_params(self):
        db = Database()
        self.window_left = int(db.get_value("window_left", "-1"))
        self.window_top = int(db.get_value("window_top", "-1"))
        self.window_width = int(db.get_value("window_width", "-1"))
        self.window_height = int(db.get_value("window_height", "-1"))
        self.windows_maximized = int(db.get_value("window_max", "0")) == 1

    def store(self):
        db = Database()
        db.store_value("text_size", self.text_size)

        value = "D" if self.color_theme == EditorTheme.Dark else "L"
        db.store_value("theme", value)

        value = "LOCAL" if self.is_source_local else "PATH"
        db.store_value("folder_source", value)
        db.store_value("folder_opened", self.source_folder)
        db.store_value("folder_path", self.source_path)

        value = "1" if self.window_maximized else "0"
        db.store_value("window_max", value)
        db.store_value("window_left", self.window_left)
        db.store_value("window_top", self.window_top)
        db.store_value("window_width", self.window_width)
        db.store_value("window_height", self.window_height)
        