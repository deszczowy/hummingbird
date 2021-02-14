from PyQt5 import QtCore, QtGui

from PyQt5.QtGui import QKeySequence, QPixmap

from PyQt5.QtWidgets import (
    QVBoxLayout, QLabel, QWidget, QHBoxLayout, QPushButton
)

from hb_dir import Directory

class FolderSwitch:

    def __init__(self, main_widget):

        main_widget.setStyleSheet("QWidget{background-color: #f5f5f5;}")
        switchLayout = QVBoxLayout()
        switchLayout.setContentsMargins(20, 20, 20, 20)
        
        icon = QLabel()
        icon.setFixedWidth(80)
        
        myPixmap = QtGui.QPixmap(Directory().get_resource_dir() + 'icon.png')
        myScaledPixmap = myPixmap.scaled(icon.size(), QtCore.Qt.KeepAspectRatio)
        icon.setPixmap(myScaledPixmap)

        header = QLabel()
        header.setText("Select notebook:")

        buttons = QWidget()
        buttons_layout = QHBoxLayout()
        button_ok = QPushButton("OK")
        button_add = QPushButton("Add")
        button_cancel = QPushButton("Cancel")
        buttons_layout.addWidget(button_add)
        buttons_layout.addStretch()
        buttons_layout.addWidget(button_ok)
        buttons_layout.addWidget(button_cancel)
        buttons.setLayout(buttons_layout)

        # stack

        switchLayout.addWidget(icon)
        switchLayout.addWidget(header)
        switchLayout.addStretch()
        switchLayout.addWidget(buttons)

        main_widget.setLayout(switchLayout)
        main_widget.hide()
    