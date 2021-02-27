#from PyQt5 import QtWidgets

import sys
import os

from PyQt5 import QtCore, QtGui

from PyQt5.QtCore import (
    QSize, QTimer
)

from PyQt5.QtGui import QKeySequence, QPixmap

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame, QMessageBox,
    QHBoxLayout, QVBoxLayout, QGridLayout,
    QTextEdit, QPushButton, QLabel, QLineEdit,
    QShortcut, QDesktopWidget, QTabWidget
)

from hb_notes import Notes
from hb_version import VersionInfo
from hb_enums import (ActivePanel, EditorMode, EditorTheme)

from hb_dir import Directory

from hb_db import Database
from hb_style import Stylist

from dialogs.info.window import InfoWindow
from dialogs.settings.window import SettingsView
from dialogs.switch.window import FolderSwitch
from classes.context import *
from classes.timer import *
from components.side import *
from components.todolist import *
from components.statusbar import *

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_flags()
        self.create_backend()
        self.create_shortcuts()
        self.build_ui()
        self.build_dialogs()
        self.window_setup()
        self.load_folder()
        self.show_window()

        #
        # code to reorganize
        
        self.marginWidth = 0

    # main app creators
    def create_main_components(self):
        # main window
        self.window = QFrame()
        self.layout = QVBoxLayout()

        # external windows
        self.infoWindow = None
        self.settingsWindow = None
        self.folderSwitch = None

    def create_context(self):
        self.context = Context()
        self.context.load()

    def create_shortcuts(self):
        self.shortcutSave = QShortcut(QKeySequence("Ctrl+S"), self)
        self.shortcutInfo = QShortcut(QKeySequence("F1"), self)
        self.shortcutMain = QShortcut(QKeySequence("F2"), self)
        self.shortcutSide = QShortcut(QKeySequence("F3"), self)
        self.shortcutSwitch = QShortcut(QKeySequence("F4"), self)
        self.shortcutTheme = QShortcut(QKeySequence("F7"), self)
        self.shortcutMode = QShortcut(QKeySequence("F8"), self)
        self.shortcutSetup = QShortcut(QKeySequence("F9"), self)
        self.shortcutExit = QShortcut(QKeySequence("F10"), self)
        self.shortcutFullscreen = QShortcut(QKeySequence("F11"), self)
        self.shortcutHide = QShortcut(QKeySequence("Esc"), self)
        self.bind_shortcuts()

    def create_flags(self):
        # enums
        self.editorMode = EditorMode.Normal
        self.activePanel = ActivePanel.Nothing
        # logic
        self.wasMaximized = False

    def create_backend(self):
        self.notes = Notes() ## do remove
        self.version = VersionInfo() ## to context
        self.stylist = Stylist()
        self.directory = Directory()
        self.timer = Timer(self)

    def create_side_components(self):
        self.sidenote = SideNotes(self)

    def create_notepad_components(self):
        self.notepad = Notepad(self)

    def create_todolist_components(self):
        self.todolist = ToDoList(self, Component.ToDoList)

    def create_status_bar(self):
        self.status_bar = StatusBar(self, Component.StatusBar)

    def build_ui(self):
        self.create_context()
        self.create_main_components()
        self.create_notepad_components()
        self.create_side_components()
        self.create_todolist_components()
        self.create_status_bar()

        desktop = QWidget()
        desktop_container = QHBoxLayout()

        side_tabs = QTabWidget()
        side_tabs.addTab(self.sidenote, "Side Notes")
        side_tabs.addTab(self.todolist, "To Do List")
        side_tabs.setFixedWidth(300)

        desktop_container.addWidget(self.notepad) # separate class
        desktop_container.addWidget(side_tabs)
        desktop.setLayout(desktop_container)
        
        desktop.setContentsMargins(0, 0, 0, 0)
        desktop_container.setContentsMargins(0, 0, 0, 0)
        desktop_container.setSpacing(0)

        self.layout.addWidget(desktop)
        self.layout.addWidget(self.status_bar)

        self.window.setLayout(self.layout)
        self.setCentralWidget(self.window)

    # shortcuts actions
    def bind_shortcuts(self):
        self.shortcutSave.activated.connect(self.action_save)
        self.shortcutFullscreen.activated.connect(self.action_toggle_fullscreen)
        self.shortcutExit.activated.connect(self.action_terminate)

        self.shortcutMain.activated.connect(self.action_focus_notepad)
        self.shortcutSide.activated.connect(self.action_focus_sidenote)

        self.shortcutSwitch.activated.connect(self.action_toggle_folder_switch)
        self.shortcutInfo.activated.connect(self.action_toggle_info_window)
        self.shortcutSetup.activated.connect(self.action_toggle_settings_window)

        self.shortcutTheme.activated.connect(self.action_switch_editor_theme)
        self.shortcutMode.activated.connect(self.action_switch_editor_mode)
        
    def action_save(self):
        print("save")
        saved = False
        saved = saved or self.notepad.save(self.context.source_folder)
        saved = saved or self.sidenote.save(self.context.source_folder)
        saved = saved or self.todolist.save(self.context.source_folder)
        
        if saved:
            self.status_bar.publish("Saved!")
            self.timer.setup()
    
    def action_toggle_fullscreen(self):
        if self.isFullScreen():
            if self.wasMaximized:
                self.showNormal()
                self.showMaximized()
            else:
                self.showNormal()
        else:
            self.wasMaximized = self.isMaximized()
            self.showFullScreen()

    def action_terminate(self):
        self.save_window_position()
        self.action_save()
        self.close()

    def action_focus_notepad(self):
        self.notepad.focus()
    
    def action_focus_sidenote(self):
        self.sidenote.focus()

    def action_toggle_folder_switch(self):
        if self.folderSwitch.isVisible():
            self.folderSwitch.hide()
        else:
            self.folderSwitch.show()
    
    def action_toggle_info_window(self):
        if self.infoWindow.isVisible():
            self.infoWindow.hide()
        else:
            self.infoWindow.show()

    def action_toggle_settings_window(self):
        if self.settingsWindow.isVisible():
            self.settingsWindow.hide()
        else:
            self.settingsWindow.show()

    def action_switch_editor_theme(self):
        if self.context.color_theme == EditorTheme.Dark:
            self.context.color_theme = EditorTheme.Light
        else:
            self.context.color_theme = EditorTheme.Dark
        self.set_editor_theme()

    def action_switch_editor_mode(self):
        if self.editorMode == EditorMode.Focus:
            self.editorMode = EditorMode.Normal
        else:
            self.editorMode = EditorMode.Focus
        self.set_editor_mode()

    # dialogs
    def build_dialogs(self):
        self.build_settings_dialog()
        self.build_info_dialog()
        self.build_folder_switch_dialog()

    def build_settings_dialog(self):
        self.settingsWindow = QWidget(self)
        settings = SettingsView(self.settingsWindow)
        self.resizeEvent(None)

    def build_info_dialog(self):
        self.infoWindow = QWidget(self)
        info = InfoWindow(self.infoWindow)
        self.resizeEvent(None)

    def build_folder_switch_dialog(self):
        self.folderSwitch = QWidget(self)
        switch = FolderSwitch(self.folderSwitch)
        self.resizeEvent(None)

    # main window settings
    def window_setup(self):
        self.setMinimumSize(800, 600)
        self.setWindowTitle(self.version.app_name())

        self.set_editor_theme()
        self.set_icon()
        self.set_geometry()

    def set_editor_theme(self):
        self.setStyleSheet(self.stylist.get_style_sheet(self.context.color_theme))

    def set_icon(self):
        self.setWindowIcon(QtGui.QIcon(self.directory.get_resource_dir() + 'icon.png'))

    def set_geometry(self):
        if self.context.window_left < 0 or self.context.window_top < 0:
            
            screen = QDesktopWidget().screenGeometry(-1)
            self.context.window_width = int(screen.width() / 3) * 2
            self.context.window_height = int(screen.height() / 3) * 2
            if self.context.window_width < 800:
                self.context.window_width = 800
            if self.context.window_height < 600:
                self.context.window_height = 600
            self.setGeometry(
                0, 0, 
                self.context.window_width,
                self.context.window_height
            )
            self.center_window()
        else:
            if self.context.window_width < 800:
                self.context.window_width = 800
            if self.context.window_height < 600:
                self.context.window_height = 600
            self.setGeometry(
                self.context.window_left, 
                self.context.window_top,
                self.context.window_width,
                self.context.window_height
            )
            self.move(
                self.context.window_left,
                self.context.window_top
            )

    def center_window(self):
        geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        geometry.moveCenter(centerPoint)
        self.move(geometry.topLeft())

    def show_window(self):
        if self.context.window_maximized == 1:
            self.showMaximized()
        else:
            self.showNormal()

    #
    def load_folder(self):
        if self.context.is_source_local:
            self.notepad.load(self.context.source_folder)
            self.sidenote.load(self.context.source_folder)
            self.todolist.load(self.context.source_folder)

    def clear_status(self):
        self.status_bar.clear()

    def save_window_params(self):
        if self.isMaximized():
            self.context.window_maximized = True
        else:
            self.context.window_maximized = False
            geometry = self.geometry()
            pos = self.pos()
            self.context.window_left = pos.x()
            self.context.window_top = pos.y()
            self.context.window_width = geometry.width()
            self.context.window_height = geometry.height()

    # events
    def resizeEvent(self, event):
        if self.editorMode == EditorMode.Focus:
            self.set_focus_mode_margins()
        if not (self.infoWindow is None):
            self.resize_info_panel()
        if not (self.settingsWindow is None):
            self.resize_settings_panel()
        if not (self.folderSwitch is None):
            self.resize_folder_switch()

    def closeEvent(self, event):
        self.save_window_params()
        self.context.store()
        self.action_save()
        event.accept()




    ## dragons below

   
    def set_editor_mode(self):
        if self.editorMode == EditorMode.Focus:
            self.set_focus_mode_margins()
        else: # normal
            self.mainPage.setViewportMargins(0, 0, 0, 0)
            self.marginWidth = 0
            self.set_editor_theme()
    
    def set_focus_mode_margins(self):
        margin = self.width() - self.sideTabs.width() - 750
        margin = round(margin / 2)

        if margin < 0:
            margin = 0
        if margin != self.marginWidth:
            self.mainPage.setViewportMargins(margin, 20, margin, 20)
            self.marginWidth = margin








    # events {
    


    # }

    #def load_folder(self, folder): # should be switch folder method
    #    if folder != self.context.source_folder:
    #        self.action_save()
    #        db = Database()
    #        db.store_value("folder_opened", folder)
    #        db.store_value("folder_source", "LOCAL")
    #        self.context.source_folder = folder
    #        self.load_notes_contents()

    # status {


    # settings {

    def update_font_size(self):
        pt = int(Database().get_value("text_size", "13"))

        self.notepad.setup(pt)
        self.sidenote.setup(pt)

    # }

    # info dialog {


    def resize_info_panel(self):
        max_width_ip = 700
        max_height_ip = 500

        left_shift = int((self.width() - max_width_ip) /2) 
        top_shift = int((self.height() - max_height_ip) /2)

        self.infoWindow.setGeometry(left_shift, top_shift, max_width_ip, max_height_ip)
    # }

    # settings dialog {


    def resize_settings_panel(self):
        max_width_ip = 700
        max_height_ip = 500

        left_shift = int((self.width() - max_width_ip) /2) 
        top_shift = int((self.height() - max_height_ip) /2)

        self.settingsWindow.setGeometry(left_shift, top_shift, max_width_ip, max_height_ip)
    # }



    # switch folder {

    def resize_folder_switch(self):
        maxw = 700
        maxh = 500

        left_shift = int((self.width() - maxw) /2) 
        top_shift = int((self.height() - maxh) /2)

        self.folderSwitch.setGeometry(left_shift, top_shift, maxw, maxh)
    # }


      
        
        


    









def main():
    Database().create()
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()

if __name__ == '__main__':
    main()
