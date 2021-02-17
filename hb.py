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
    QShortcut, QDesktopWidget
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

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # local 
        self.context = Context()

        # external windows
        self.infoWindow = None
        self.settingsWindow = None
        self.folderSwitch = None

        #
        # code to reorganize
        self.hMainWindow = QFrame()
        self.marginWidth = 0
        self.editorMode = EditorMode.Normal
        self.editorTheme = EditorTheme.Dark
        self.wasMaximized = False
        # timer
        self.tic = 0
        self.timer = QTimer(self)
        self.schedule = QTimer(self)
        # backend
        self.notes = Notes()
        self.version = VersionInfo()
        self.stylist = Stylist()
        self.directory = Directory()
        self.activePanel = ActivePanel.Nothing
        # app
        self.appLayout = QVBoxLayout()
        # book
        self.desktop = QFrame()
        self.mainPage = QTextEdit()
        self.sideNotes = QTextEdit()
        self.binding = QHBoxLayout()
        # status board
        self.statusBoard = QFrame()
        self.statusLayout = QHBoxLayout()
        self.messageBoard = QLabel()
        self.infoBoard = QLabel()
        # keys
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
        # go!
        self.init_ui()
        #print("Start")

    def toggle_fullscreen(self):
        if self.isFullScreen():
            if self.wasMaximized:
                self.showNormal()
                self.showMaximized()
            else:
                self.showNormal()
        else:
            self.wasMaximized = self.isMaximized()
            self.showFullScreen()

    # editor themes {
    def read_theme_from_settings(self):
        theme = Database().get_value("theme", "L")
        if theme == "D":
            self.editorTheme = EditorTheme.Dark
        else :
            self.editorTheme = EditorTheme.Light

    def switch_editor_theme(self):
        if self.editorTheme == EditorTheme.Dark:
            self.editorTheme = EditorTheme.Light
        else:
            self.editorTheme = EditorTheme.Dark
        self.set_editor_theme()

    def set_editor_theme(self):
        self.sideNotes.setStyleSheet(self.stylist.get_side_notes_style_sheet(self.editorTheme))
        self.statusBoard.setStyleSheet(self.stylist.get_status_board_style_sheet(self.editorTheme))
        self.setStyleSheet(self.stylist.get_style_sheet(self.editorTheme))
    # }

    # editor modes {
    def switch_editor_mode(self):
        if self.editorMode == EditorMode.Focus:
            self.editorMode = EditorMode.Normal
        else:
            self.editorMode = EditorMode.Focus
        self.set_editor_mode()
    
    def set_editor_mode(self):
        if self.editorMode == EditorMode.Focus:
            self.set_focus_mode_margins()
            self.shortcutInfoLabel.hide()
            self.sideNotes.setStyleSheet(self.stylist.get_side_notes_style_focus(self.editorTheme))
            self.statusBoard.setStyleSheet(self.stylist.get_status_board_style_focus(self.editorTheme))
        else: # normal
            self.mainPage.setViewportMargins(0, 0, 0, 0)
            self.marginWidth = 0
            self.shortcutInfoLabel.show()
            self.set_editor_theme()
    
    def set_focus_mode_margins(self):
        margin = self.width() - self.sideNotes.width() - 750
        margin = round(margin / 2)

        if margin < 0:
            margin = 0
        if margin != self.marginWidth:
            self.mainPage.setViewportMargins(margin, 20, margin, 20)
            self.marginWidth = margin
    # }

    # timers {
    def prepare_timers(self):
        self.timer.timeout.connect(self.timer_tic)
        self.schedule.timeout.connect(self.schedule_tic)
        self.timer.start(1000)
        self.schedule.start(7000)
    
    def timer_tic(self):
        if self.tic > 0:
            self.tic -= 1
        if self.tic == 1:
            self.messageBoard.setText("")

    def schedule_tic(self):
        self.action_save()
    # }




    # actions {
    def action_save(self):
        saved = False

        if self.mainPage.document().isModified():
            self.notes.save_main_notes_to_db(self.mainPage.toPlainText(), self.context.active_folder)
            self.mainPage.document().setModified(False)
            saved = True

        if self.sideNotes.document().isModified():
            self.notes.save_side_notes_to_db(self.sideNotes.toPlainText(), self.context.active_folder)
            self.sideNotes.document().setModified(False)
            saved = True
        
        if saved:
            self.action_publish_message("Saved!")
            self.tic = 5

    def action_publish_message(self, message):
        self.messageBoard.setText(message + " ") # with margin
    
    def action_focus_main(self):
        self.mainPage.setFocus()

    def action_focus_side(self):
        self.sideNotes.setFocus()

    def action_terminate(self):
        self.save_window_position()
        self.action_save()
        self.close()
    # }




    # events {
    def closeEvent(self, event):
        self.save_window_position()
        self.action_save()
        event.accept()

    def resizeEvent(self, event):
        if self.editorMode == EditorMode.Focus:
            self.set_focus_mode_margins()
        if not (self.infoWindow is None):
            self.resize_info_panel()
        if not (self.settingsWindow is None):
            self.resize_settings_panel()
        if not (self.folderSwitch is None):
            self.resize_folder_switch()
    # }


    
    
    # book {
    def prepare_book(self):
        self.set_book_margins()
        self.stack_book_elements()
        self.load_context()
        self.load_notes_contents()

    def set_book_margins(self):
        self.mainPage.setContentsMargins(0, 0, 0, 0)
        self.sideNotes.setContentsMargins(0, 0, 0, 0)
        self.sideNotes.setFixedWidth(300)
        self.desktop.setContentsMargins(0, 0, 0, 0)
        self.binding.setContentsMargins(0, 0, 0, 0)
        self.binding.setSpacing(0)
    
    def stack_book_elements(self):
        text_size = int(Database().get_value("text_size", "13"))
        self.mainPage.setFontPointSize(text_size)
        self.sideNotes.setFontPointSize(text_size)
        self.binding.addWidget(self.mainPage)
        self.binding.addWidget(self.sideNotes)
        self.desktop.setLayout(self.binding)
    
    def load_context(self):
        source = Database().get_value("folder_source", "LOCAL")
        self.context.source_local = source == "LOCAL"
        self.context.active_folder = int(Database().get_value("folder_opened", "1"))

    def load_notes_contents(self):
        if self.context.source_local:
            self.mainPage.setPlainText(self.notes.get_main_notes_from_db(self.context.active_folder))
            self.sideNotes.setPlainText(self.notes.get_side_notes_from_db(self.context.active_folder))
    # }


    def load_folder(self, folder):
        if folder != self.context.active_folder:
            self.action_save()
            db = Database()
            db.store_value("folder_opened", folder)
            db.store_value("folder_source", "LOCAL")
            self.context.active_folder = folder
            self.load_notes_contents()

    # status {
    def prepare_status_board(self):
        self.setup_switch_buttons()
        self.set_status_margins()
        self.stack_status_elements()
    
    def set_status_margins(self):
        self.statusLayout.setSpacing(0)

    def stack_status_elements(self):
        
        self.statusLayout.addWidget(self.infoBoard)
        self.statusLayout.addWidget(self.messageBoard)
        self.statusLayout.setContentsMargins(0, 0, 0, 0)
        self.statusLayout.addSpacing(0)
        self.statusBoard.setLayout(self.statusLayout)

    # status slots
    def setup_switch_buttons(self):

        self.infoBoard.setText("F1 - Info   F4 - Switch notebooks")
        self.infoBoard.setStyleSheet("font-size:10px;")
        self.infoBoard.setAlignment(QtCore.Qt.AlignLeft)
        self.messageBoard.setAlignment(QtCore.Qt.AlignRight)

    def on_settings_toggle(self):
        if self.settingsWindow.isVisible():
            self.settingsWindow.hide()
        else:
            self.settingsWindow.show()
    
    def on_info_toggle(self):
        if self.infoWindow.isVisible():
            self.infoWindow.hide()
        else:
            self.infoWindow.show()

    def on_folder_switch(self):
        if self.folderSwitch.isVisible():
            self.folderSwitch.hide()
        else:
            self.folderSwitch.show()
    # }




    # settings {

    def update_font_size(self):
        pt = int(Database().get_value("text_size", "13"))

        mainPageTextCursor = self.mainPage.textCursor()
        sideNoteTextCursor = self.sideNotes.textCursor()
        mainPageModified = self.mainPage.document().isModified()
        sideNoteModified = self.sideNotes.document().isModified()
        self.mainPage.selectAll()
        self.mainPage.setFontPointSize(pt)
        self.mainPage.setTextCursor(mainPageTextCursor)
        self.mainPage.document().setModified(mainPageModified)
        self.sideNotes.selectAll()
        self.sideNotes.setFontPointSize(pt)
        self.sideNotes.setTextCursor(sideNoteTextCursor)
        self.sideNotes.document().setModified(sideNoteModified)
    # }

    # info dialog {
    def build_info_panel(self):
        self.infoWindow = QWidget(self)
        info = InfoWindow(self.infoWindow)
        self.resizeEvent(None)

    def resize_info_panel(self):
        max_width_ip = 700
        max_height_ip = 500

        left_shift = int((self.width() - max_width_ip) /2) 
        top_shift = int((self.height() - max_height_ip) /2)

        self.infoWindow.setGeometry(left_shift, top_shift, max_width_ip, max_height_ip)
    # }

    # settings dialog {
    def build_settings_dialog(self):
        self.settingsWindow = QWidget(self)
        settings = SettingsView(self.settingsWindow)
        self.resizeEvent(None)

    def resize_settings_panel(self):
        max_width_ip = 700
        max_height_ip = 500

        left_shift = int((self.width() - max_width_ip) /2) 
        top_shift = int((self.height() - max_height_ip) /2)

        self.settingsWindow.setGeometry(left_shift, top_shift, max_width_ip, max_height_ip)
    # }



    # switch folder {
    def build_folder_switch(self):
        self.folderSwitch = QWidget(self)
        switch = FolderSwitch(self.folderSwitch)
        self.resizeEvent(None)

    def resize_folder_switch(self):
        maxw = 700
        maxh = 500

        left_shift = int((self.width() - maxw) /2) 
        top_shift = int((self.height() - maxh) /2)

        self.folderSwitch.setGeometry(left_shift, top_shift, maxw, maxh)
    # }



    # app {
    def stack_gui_elements(self):
        self.stack_book_elements()
        self.stack_status_elements()

        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.appLayout.setSpacing(0)
        self.appLayout.addWidget(self.desktop)
        self.appLayout.addWidget(self.statusBoard)
        self.hMainWindow.setLayout(self.appLayout)
    
    def setup_app(self):
        self.read_theme_from_settings()
        self.set_editor_theme()
        self.setup_icon()
        self.bind_shortcuts()
        self.setWindowTitle(self.version.app_name())
        self.setup_window_geometry()
        if int(Database().get_value("window_max", "0")) == 1:
            self.showMaximized()
        else:
            self.showNormal()

    def setup_window_geometry(self):
        x = int(Database().get_value("window_left", "-1"))
        y = int(Database().get_value("window_top", "-1"))
        w = int(Database().get_value("window_width", "-1"))
        h = int(Database().get_value("window_height", "-1"))

        #print(x)
        #print(y)
        #print(w)
        #print(h)

        if x < 0 or y < 0:
            screen = QDesktopWidget().screenGeometry(-1)
            w = (screen.width() / 3) *2
            h = (screen.height() / 3) *2
            if w < 800: 
                w = 800
            if h < 600:
                h = 600
            self.setGeometry(0, 0, int(w), int(h))
            self.center()
        else:
            if w < 800: 
                w = 800
            if h < 600:
                h = 600
            self.setGeometry(x, y, int(w), int(h))
            self.move(x, y)


    def setup_icon(self):
        self.setWindowIcon(QtGui.QIcon(self.directory.get_resource_dir() + 'icon.png'))

    def bind_shortcuts(self):
        self.shortcutSave.activated.connect(self.action_save)
        self.shortcutMain.activated.connect(self.action_focus_main)
        self.shortcutSide.activated.connect(self.action_focus_side)
        self.shortcutSwitch.activated.connect(self.on_folder_switch)
        self.shortcutInfo.activated.connect(self.on_info_toggle)
        self.shortcutSetup.activated.connect(self.on_settings_toggle)
        self.shortcutExit.activated.connect(self.action_terminate)
        self.shortcutTheme.activated.connect(self.switch_editor_theme)
        self.shortcutMode.activated.connect(self.switch_editor_mode)
        self.shortcutFullscreen.activated.connect(self.toggle_fullscreen)

    def save_window_position(self):
        if not self.isMaximized():
            geometry = self.geometry()
            pos = self.pos()
            Database().store_value("window_left", pos.x())
            Database().store_value("window_top", pos.y())
            Database().store_value("window_width", geometry.width())
            Database().store_value("window_height", geometry.height())
        maximized = "1" if self.isMaximized() else "0"
        Database().store_value("window_max", maximized)
        theme = "D" if self.editorTheme == EditorTheme.Dark else "L"
        Database().store_value("theme", theme)

    def center(self):
        geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        geometry.moveCenter(centerPoint)
        self.move(geometry.topLeft())

    def init_ui(self):
        self.setMinimumSize(800, 600)
        self.prepare_book()
        self.prepare_status_board()
        self.stack_gui_elements()
        self.setup_app()
        self.prepare_timers()
        self.setCentralWidget(self.hMainWindow)
        self.build_info_panel()
        self.build_settings_dialog()
        self.build_folder_switch()
    # }

def main():
    Database().create()
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()

if __name__ == '__main__':
    main()
