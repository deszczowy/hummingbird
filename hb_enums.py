from enum import (Enum, IntEnum)

class ActivePanel(Enum):
    Nothing = 0
    Options = 1
    Info = 2

class EditorMode(Enum):
    Normal = 0
    Focus = 1

class EditorTheme(Enum):
    Light = 0
    Dark = 1

class Component(IntEnum):
    Notepad = 0
    SideNotes = 1
    ToDoList = 2
    StatusBar = 3

class Priority(IntEnum):
    Low = 0
    Medium = 1
    High = 2
    Critical = 3