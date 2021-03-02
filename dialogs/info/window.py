from PyQt5 import QtCore, QtGui

from PyQt5.QtGui import QKeySequence, QPixmap

from PyQt5.QtWidgets import (
    QVBoxLayout, QLabel
)

from hb_dir import Directory
from dialogs.info.content import *

class Info:

    def __init__(self, info_window_widget):
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

        infoLayout.addWidget(icon)
        infoLayout.addWidget(about)
        infoLayout.addWidget(shortcuts)
        infoLayout.addStretch()

        info_window_widget.setLayout(infoLayout)
    