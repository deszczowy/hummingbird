from PyQt5 import QtCore, QtGui

from PyQt5.QtWidgets import (
    QHBoxLayout, QWidget, QLabel
)

#from hb_dir import Directory

from hb_enums import Component

class StatusBar(QWidget):

    def __init__(self, parent, component_def):
        super(StatusBar, self).__init__(parent)
        self.component = component_def
        self.layout = QHBoxLayout()
        self.messages = QLabel()
        self.info = QLabel()

        self.build()

    def build(self):
        self.prepare()
        self.layout.addWidget(self.info)
        self.layout.addWidget(self.messages)
        self.setLayout(self.layout)

    def prepare(self):
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(0, 0, 0, 0)
        self.layout.addSpacing(0)
        self.info.setText(self.get_info())
        self.info.setAlignment(QtCore.Qt.AlignLeft)
        self.messages.setAlignment(QtCore.Qt.AlignRight)

    def get_info(self):
        return "F1:Info   F4:Switch notebooks   F9:Settings"

    def publish(self, message):
        self.messages.setText(message + " ") # with margin

    def clear(self):
        self.messages.setText("")