from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import (
    QVBoxLayout, QWidget, QLabel
)

from hb_enums import Component

class ToDoList(QWidget):
    def __init__(self, parent, component_def):
        super(ToDoList, self).__init__(parent)
        self.component = component_def
        self.layout = QVBoxLayout()
        self.label = QLabel()
        self.stack()

    def stack(self):
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.prepare()

    def prepare(self):
        self.label.setText("ToDoList")