from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import (
    QVBoxLayout, QWidget, QTextEdit
)

#from hb_dir import Directory

from hb_notes import Notes
from hb_enums import *

class Editor(QWidget):
    def __init__(self, parent, component_def):
        super(Editor, self).__init__(parent)
        self.component = component_def
        self.editor = QTextEdit()
        self.layout = QVBoxLayout()
        self.stack()
        self.font_size_pt = 1

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
        self.set_font_size(self.font_size_pt) #ugh... todo
        
    
    def setup(self, font_size):
        self.set_font_size(font_size)

    def set_font_size(self, size): #todo
        self.font_size_pt = size
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
        self.margin_width = 0
        self.current_mode = EditorMode.Normal

    def setup_mode(self, context):
        self.current_mode = context.editor_mode
        
        if self.current_mode == EditorMode.Focus:
            self.set_focus_mode_margins()
        else: # normal
            self.editor.setViewportMargins(0, 0, 0, 0)
            self.margin_width = 0
            #self.set_editor_theme()

    def set_focus_mode_margins(self):
        margin = self.parent().parent().width() - 300 - 750
        margin = round(margin / 2)

        if margin < 0:
            margin = 0
        if margin != self.margin_width:
            self.editor.setViewportMargins(margin, 20, margin, 20)
            self.margin_width = margin
    
    def refresh(self):
        if self.current_mode == EditorMode.Focus:
            self.set_focus_mode_margins()
    