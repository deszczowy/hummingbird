from enum import Enum

class ActivePanel(Enum):
    Nothing = 0
    Options = 1
    Info = 2

class EditorMode(Enum):
    Normal = 0
    Focus = 1