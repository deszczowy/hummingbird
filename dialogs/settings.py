from PyQt5 import QtCore, QtGui

from PyQt5.QtGui import QKeySequence, QPixmap

from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QWidget, QPushButton, QComboBox, QGridLayout
)

from hb_db import Database
from hb_dir import Directory
from hb_enums import *

class Settings(QWidget):

    def __init__(self, settings_window_widget):

        super(Settings, self).__init__(settings_window_widget)

        self.main = settings_window_widget
        self.context = None

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)

        icon = QLabel()
        icon.setFixedWidth(80)
        
        myPixmap = QtGui.QPixmap(Directory().get_resource_dir() + 'icon.png')
        myScaledPixmap = myPixmap.scaled(icon.size(), QtCore.Qt.KeepAspectRatio)
        icon.setPixmap(myScaledPixmap)

        # buttons

        buttons_layout = QHBoxLayout()
        button = QPushButton("Ok")
        button.clicked.connect(self.close)
        buttons_layout.addStretch()
        buttons_layout.addWidget(button)

        # controls
        # todo: read from context

        page = QGridLayout()
        page.setColumnStretch(0, 1) # todo: columns id as consts
        page.setColumnStretch(1, 2)
        page.setColumnMinimumWidth(2, 20)
        page.setColumnStretch(3, 1)
        page.setColumnStretch(4, 2)

        # Font size
        self.font_size_label = QLabel()
        self.font_size_label.setText("Font size")
        self.font_size_label.setAlignment(QtCore.Qt.AlignLeft)

        self.font_size_value = QLineEdit()
        self.font_size_value.setInputMask("D9")
        page.addWidget(self.font_size_label, 0, 0)
        page.addWidget(self.font_size_value, 0, 1)

        # Color theme
        color_theme_label = QLabel("Color theme")
        color_theme_label.setAlignment(QtCore.Qt.AlignLeft)
        self.color_theme_picker = QComboBox()
        self.color_theme_picker.insertItem(0, "Light")
        self.color_theme_picker.insertItem(1, "Dark")
        page.addWidget(color_theme_label, 0, 3)
        page.addWidget(self.color_theme_picker, 0, 4)

        # Editor mode
        editor_mode_label = QLabel("Editor mode")
        editor_mode_label.setAlignment(QtCore.Qt.AlignLeft)
        self.editor_mode_picker = QComboBox()
        self.editor_mode_picker.insertItem(0, "Normal")
        self.editor_mode_picker.insertItem(1, "Focus")
        page.addWidget(editor_mode_label, 1, 3)
        page.addWidget(self.editor_mode_picker, 1, 4)

        # finalization
        page.setRowStretch(4, 1)
        
        main_layout.addWidget(icon)
        main_layout.addLayout(page)
        main_layout.addLayout(buttons_layout)

        self.main.setLayout(main_layout)
        #self.main.hide()

    def load_context_values(self):
        self.font_size_value.setText(str(self.context.text_size))

        if self.context.color_theme == EditorTheme.Light:
            self.color_theme_picker.setCurrentIndex(0)
        else:
            self.color_theme_picker.setCurrentIndex(1)

    def get_font_size(self):
        size = self.font_size_value.text()
        if size == "" or size =="0":
            pt = 1
        else:
            pt = int(size)
        return pt

    def get_color_theme(self):
        if self.color_theme_picker.currentIndex() == 0:
            return EditorTheme.Light
        else:
            return EditorTheme.Dark
    
    def close(self):
        self.update()
        self.main.parent().parent().parent().parent().update_params()
        self.main.parent().parent().parent().hide()

    def setup(self, local_context):
        self.context = local_context
        self.load_context_values()

    def update(self):
        self.context.text_size = self.get_font_size()
        self.context.color_theme = self.get_color_theme()