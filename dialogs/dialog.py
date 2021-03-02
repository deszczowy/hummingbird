from PyQt5 import QtCore, QtGui

from PyQt5.QtGui import QKeySequence, QPixmap

from PyQt5.QtWidgets import (
    QWidget, QTabWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QGridLayout
)

from hb_enums import *
from dialogs.info.window import *

class Dialog(QWidget):

    def __init__(self, parent):
        super(Dialog, self).__init__(parent)

        self.root = parent
        #self.root.setStyleSheet("border: 1px solid red;")

        self.create_info_page()

        self.pages = QTabWidget()
        page2 = QWidget()
        self.pages.addTab(self.info, "Info")
        self.pages.addTab(page2, "Page2")

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
        info_obj = Info(self.info)

    def resize(self):
        width = 700
        height = 500

        left = int((self.root.parent().width() - width) /2) 
        top = int((self.root.parent().height() - height) /2)

        self.root.setGeometry(left, top, width, height)