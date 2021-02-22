from PyQt5 import QtCore, QtGui

from PyQt5.QtGui import QKeySequence, QPixmap

from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QWidget, QPushButton
)

from hb_db import Database
from hb_dir import Directory

class SettingsView(QWidget):

    def __init__(self, settings_window_widget):

        super(SettingsView, self).__init__(settings_window_widget)

        self.main = settings_window_widget

        self.main.setStyleSheet("QWidget{background-color: #f5f5f5;}")

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)

        icon = QLabel()
        icon.setFixedWidth(80)
        
        myPixmap = QtGui.QPixmap(Directory().get_resource_dir() + 'icon.png')
        myScaledPixmap = myPixmap.scaled(icon.size(), QtCore.Qt.KeepAspectRatio)
        icon.setPixmap(myScaledPixmap)

        # buttons

        buttons = QWidget()
        buttons_layout = QHBoxLayout()
        buttons.setLayout(buttons_layout)
        button = QPushButton("OK")
        button.clicked.connect(self.close)
        buttons_layout.addStretch()
        buttons_layout.addWidget(button)

        # sides

        page = QWidget()
        page_layout = QHBoxLayout()
        page.setLayout(page_layout)

        column_left = QVBoxLayout()
        column_right = QVBoxLayout()

        page_layout.addLayout(column_left)
        page_layout.addLayout(column_right)

        # controls
        # todo: read from context

        self.font_size_label = QLabel()
        self.font_size_label.setText("Font size")
        self.font_size_label.setAlignment(QtCore.Qt.AlignLeft)
        column_left.addWidget(self.font_size_label)

        self.font_size_value = QLineEdit()
        self.font_size_value.setText(Database().get_value("text_size", "13"))
        self.font_size_value.setInputMask("D9")
        self.font_size_value.textChanged.connect(self.apply_font_size)
        column_left.addWidget(self.font_size_value)

        self.label = QLabel("Right side")
        column_right.addWidget(self.label)

        # fill the gaps

        column_left.addStretch()
        column_right.addStretch()

        # finalization

        main_layout.addWidget(icon)
        main_layout.addWidget(page)
        main_layout.addWidget(buttons)

        self.main.setLayout(main_layout)
        self.main.hide()

    def apply_font_size(self):
        size = self.font_size_value.text()
        if size == "" or size =="0":
            pt = 1
        else:
            pt = int(size)

        Database().store_value("text_size", pt) # todo: remove. context only. save on quit or on schedule
        self.main.parent().update_font_size()
    
    def close(self):
        self.main.hide()