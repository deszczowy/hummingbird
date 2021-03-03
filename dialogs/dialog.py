from PyQt5 import QtCore, QtGui

from PyQt5.QtGui import QKeySequence, QPixmap

from PyQt5.QtWidgets import (
    QWidget, QTabWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QGridLayout
)

from hb_enums import *
from dialogs.info.window import *
from dialogs.settings.window import * # todo: do something with those imports...

class Dialog(QWidget):

    def __init__(self, parent):
        super(Dialog, self).__init__(parent)

        self.root = parent
        self.active = ActivePanel.Info

        #self.root.setStyleSheet("border: 1px solid red;")

        self.create_info_page()
        self.create_settings_page()

        self.pages = QTabWidget()
        self.pages.addTab(self.info, "Info")
        self.pages.addTab(self.settings, "Settings")

        layout = QVBoxLayout()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.pages)
        self.root.setLayout(layout)

        self.resize()
        self.root.hide()

    def show_dialog(self, page):
        if page == ActivePanel.Info:
            self.pages.setCurrentIndex(0)
        if page == ActivePanel.Options:
            self.pages.setCurrentIndex(1)
        self.root.show()

    def create_info_page(self):
        self.info = QWidget(self)
        self.info_obj = Info(self.info)

    def create_settings_page(self):
        self.settings = QWidget(self)
        self.settings_obj = Settings(self.settings)

    def resize(self):
        width = 700
        height = 500

        left = int((self.root.parent().width() - width) /2) 
        top = int((self.root.parent().height() - height) /2)

        self.root.setGeometry(left, top, width, height)

    def setup(self, context):
        self.settings_obj.setup(context)

    def hide_dialog(self):
        self.root.hide()