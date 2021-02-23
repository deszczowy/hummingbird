from PyQt5 import QtCore, QtGui

from PyQt5.QtGui import QKeySequence, QPixmap

from PyQt5.QtCore import QModelIndex

from PyQt5.QtWidgets import (
    QVBoxLayout, QLabel, QWidget, QHBoxLayout, QPushButton, QListView, QInputDialog
)

from hb_dir import Directory
from hb_db import Database

class FolderSwitch(QWidget):

    def __init__(self, main_widget):

        super(FolderSwitch, self).__init__(main_widget)

        self.selected_folder = 0

        self.main = main_widget

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
        self.button_edit = QPushButton("Change name")
        buttons_layout.addWidget(self.button_add)
        buttons_layout.addWidget(self.button_edit)
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.button_ok)
        buttons_layout.addWidget(self.button_cancel)
        buttons.setLayout(buttons_layout)

        self.button_cancel.clicked.connect(self.cancel)
        self.button_ok.clicked.connect(self.ok)
        self.button_add.clicked.connect(self.add)
        self.button_edit.clicked.connect(self.edit)

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
        self.selected_folder = item.folder_id

    def cancel(self):
        self.main.hide()

    def ok(self):
        self.main.parent().load_folder(self.selected_folder)
        self.main.hide()

    def add(self):
        new_folder, ok = QInputDialog.getText(self, 'Hummingbird', 'New notebook name:')
        if ok:
            db = Database()
            db.insert_folder(str(new_folder))
            self.folders.setModel(db.get_folder_model())

    def edit(self):
        new_name, ok = QInputDialog.getText(self, 'Hummingbird', 'New notebook name:')
        if ok:
            db = Database()
            db.update_folder(self.selected_folder, str(new_name))
            self.folders.setModel(db.get_folder_model())
        