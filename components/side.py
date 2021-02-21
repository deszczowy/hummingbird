from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import (
    QVBoxLayout, QWidget, QTextEdit
)

#from hb_dir import Directory

from hb_notes import Notes
from hb_enums import Component

class Editor(QWidget):
    def __init__(self, parent, component_def):
        super(Editor, self).__init__(parent)
        self.component = component_def
        self.editor = QTextEdit()
        self.layout = QVBoxLayout()
        self.stack()

    def stack(self):
        self.layout.addWidget(self.editor)
        self.setLayout(self.layout)
        self.prepare()

    def prepare(self):
        self.editor.setContentsMargins(0, 0, 0, 0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

    def save(self, folder):

        if self.editor.document().isModified():
            Notes().save_text(
                folder,
                self.component, 
                self.editor.toPlainText()
            )
            self.editor.document().setModified(False)
            return True
        return False

    def load(self, folder):
        self.editor.setPlainText(
            Notes().get_text(
                folder, self.component
            ))
    
    def setup(self, font_size):
        self.set_font_size(font_size)

    def set_font_size(self, size):
        currentTextCursor = self.editor.textCursor()
        isModified = self.editor.document().isModified()
        self.editor.selectAll()
        self.editor.setFontPointSize(size)
        self.editor.setTextCursor(currentTextCursor)
        self.editor.document().setModified(isModified)

    def focus(self):
        self.editor.setFocus()
        

class SideNotes(Editor):

    def __init__(self, parent):
        super(SideNotes, self).__init__(parent, Component.SideNotes)

class Notepad(Editor):

    def __init__(self, parent):
        super(Notepad, self).__init__(parent, Component.Notepad)

    
    
    