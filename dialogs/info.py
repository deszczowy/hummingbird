from PyQt5 import QtCore, QtGui

from PyQt5.QtGui import QKeySequence, QPixmap

from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton
)

from hb_dir import Directory
from dialogs.info_content import *

class Info:

    def __init__(self, info_window_widget):

        self.main = info_window_widget

        infoLayout = QVBoxLayout()
        infoLayout.setContentsMargins(20, 20, 20, 20)
        
        icon = QLabel()
        icon.setFixedWidth(80)
        
        myPixmap = QtGui.QPixmap(Directory().get_resource_dir() + 'icon.png')
        myScaledPixmap = myPixmap.scaled(icon.size(), QtCore.Qt.KeepAspectRatio)
        icon.setPixmap(myScaledPixmap)

        about = QLabel()
        about.setText(header_information)
        about.setOpenExternalLinks(True)
        about.setWordWrap(True)

        shortcuts = QLabel()
        shortcuts.setText(shortcuts_information)

        # buttons

        buttons_layout = QHBoxLayout()
        button = QPushButton("Ok")
        button.clicked.connect(self.close)
        buttons_layout.addStretch()
        buttons_layout.addWidget(button)

        infoLayout.addWidget(icon)
        infoLayout.addWidget(about)
        infoLayout.addWidget(shortcuts)
        infoLayout.addStretch()
        infoLayout.addLayout(buttons_layout)

        self.main.setLayout(infoLayout)

    def close(self):
        self.main.parent().parent().parent().hide()
    