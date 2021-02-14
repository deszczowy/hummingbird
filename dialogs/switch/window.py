from PyQt5 import QtCore, QtGui

from PyQt5.QtGui import QKeySequence, QPixmap

from PyQt5.QtCore import QModelIndex

from PyQt5.QtWidgets import (
    QVBoxLayout, QLabel, QWidget, QHBoxLayout, QPushButton, QListView
)

from hb_dir import Directory
from hb_db import Database

class FolderSwitch(QWidget):

    def __init__(self, main_widget):

        super(FolderSwitch, self).__init__(main_widget)

        self.main = main_widget

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

        self.folders = QListView()
        self.folders.setModel(Database().get_folder_model())
        self.folders.clicked[QModelIndex].connect(self.select_folder)

        buttons = QWidget()
        buttons_layout = QHBoxLayout()
        self.button_ok = QPushButton("OK")
        self.button_add = QPushButton("Add")
        self.button_cancel = QPushButton("Cancel")
        buttons_layout.addWidget(self.button_add)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.button_ok)
        buttons_layout.addWidget(self.button_cancel)
        buttons.setLayout(buttons_layout)

        self.button_cancel.clicked.connect(self.cancel)

        # stack

        switchLayout.addWidget(icon)
        switchLayout.addWidget(header)
        switchLayout.addWidget(self.folders)
        switchLayout.addStretch()
        switchLayout.addWidget(buttons)

        main_widget.setLayout(switchLayout)
        main_widget.hide()
    
    def select_folder(self, index):
        item = self.folders.model().itemFromIndex(index)
        print(item.folder_id)

    def cancel(self):
        self.main.hide()