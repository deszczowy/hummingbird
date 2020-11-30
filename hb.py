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
    QHBoxLayout, QVBoxLayout,
    QTextEdit, QPushButton, QLabel, QSpinBox,
    QShortcut, QDesktopWidget
)

from hb_notes import Notes
from hb_version import VersionInfo
from hb_enums import (ActivePanel, EditorMode)

from hb_dir import Directory

from hb_db import Database
from hb_style import Stylist

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.hMainWindow = QFrame()
        self.marginWidth = 0
        self.editorMode = EditorMode.Normal
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
        self.toggleSettingsButton = QPushButton()
        self.toggleAppInfoButton = QPushButton()
        # settings
        self.switchBoard = QFrame()
        self.switchLayout = QVBoxLayout()
        # - settings board
        self.optionsBoard = QFrame()
        self.fontSizeLabel = QLabel()
        self.fontSizeValue = QSpinBox()
        self.optionsLayout = QHBoxLayout()
        # - info board
        self.infoBoard = QFrame()
        self.infoLayout = QHBoxLayout()
        self.aboutLabel = QLabel()
        self.iconLabel = QLabel()
        # keys
        self.shortcutSave = QShortcut(QKeySequence("Ctrl+S"), self)
        self.shortcutInfo = QShortcut(QKeySequence("F1"), self)
        self.shortcutMain = QShortcut(QKeySequence("F2"), self)
        self.shortcutSide = QShortcut(QKeySequence("F3"), self)
        self.shortcutNormal = QShortcut(QKeySequence("F7"), self)
        self.shortcutFocus = QShortcut(QKeySequence("F8"), self)
        self.shortcutSetup = QShortcut(QKeySequence("F9"), self)
        self.shortcutExit = QShortcut(QKeySequence("F10"), self)
        self.shortcutHide = QShortcut(QKeySequence("Esc"), self)
        # go!
        self.init_ui()
        #print("Start")

    # editor modes {
    def switch_editor_mode_to_focus(self):
        self.editorMode = EditorMode.Focus
        self.set_focus_mode_margins()
    
    def switch_editor_mode_to_normal(self):
        self.editorMode = EditorMode.Normal
        self.mainPage.setViewportMargins(0, 0, 0, 0)
        self.marginWidth = 0

    def set_focus_mode_margins(self):
        margin = self.width() - self.sideNotes.width() - 750
        margin = round(margin / 2)

        if margin < 0:
            margin = 0
        if margin != self.marginWidth:
            self.mainPage.setViewportMargins(margin, 20, margin, 20)
            self.marginWidth = margin
    # }

    def resizeEvent(self, event):
        if self.editorMode == EditorMode.Focus:
            self.set_focus_mode_margins()


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
            self.notes.save_main_notes_to_db(self.mainPage.toPlainText())
            self.mainPage.document().setModified(False)
            saved = True

        if self.sideNotes.document().isModified():
            self.notes.save_side_notes_to_db(self.sideNotes.toPlainText())
            self.sideNotes.document().setModified(False)
            saved = True
        
        if saved:
            self.action_publish_message("Saved!")
            self.tic = 5

    def action_publish_message(self, message):
        self.messageBoard.setText(message + " ") # with margin
    
    def action_toggle_options_panel(self, sender):
        if sender == self.activePanel:
            self.activePanel = ActivePanel.Nothing
        else:
            self.activePanel = sender

        self.hide_all_panels()

        if self.activePanel != ActivePanel.Nothing:
            self.switchBoard.setFixedHeight(60)

        if sender == ActivePanel.Info:
            self.infoBoard.setFixedHeight(60)
        elif sender == ActivePanel.Options:
            self.optionsBoard.setFixedHeight(60)

    def action_focus_main(self):
        self.mainPage.setFocus()

    def action_focus_side(self):
        self.sideNotes.setFocus()

    def action_terminate(self):
        self.action_save()
        self.close()
    # }




    # events {
    def closeEvent(self, event):
        self.action_save()
        event.accept()
    # }


    
    
    # book {
    def prepare_book(self):
        self.set_book_margins()
        self.stack_book_elements()
        self.load_notes_contents()

    def set_book_margins(self):
        self.mainPage.setContentsMargins(0, 0, 0, 0)
        self.sideNotes.setContentsMargins(0, 0, 0, 0)
        self.sideNotes.setFixedWidth(300)
        self.sideNotes.setStyleSheet(self.stylist.get_side_notes_style_sheet())
        self.desktop.setContentsMargins(0, 0, 0, 0)
        self.binding.setContentsMargins(0, 0, 0, 0)
        self.binding.setSpacing(0)
    
    def stack_book_elements(self):
        self.mainPage.setFontPointSize(13)
        self.sideNotes.setFontPointSize(13)
        self.binding.addWidget(self.mainPage)
        self.binding.addWidget(self.sideNotes)
        self.desktop.setLayout(self.binding)
    
    def load_notes_contents(self):
        self.mainPage.setPlainText(self.notes.get_main_notes_from_db())
        self.sideNotes.setPlainText(self.notes.get_side_notes_from_db())
    # }




    # status {
    def prepare_status_board(self):
        self.setup_switch_buttons()
        self.set_status_margins()
        self.stack_status_elements()
    
    def set_status_margins(self):
        self.statusLayout.setSpacing(0)

    def stack_status_elements(self):
        self.statusLayout.addWidget(self.toggleSettingsButton)
        self.statusLayout.addWidget(self.toggleAppInfoButton)
        self.statusLayout.addWidget(self.messageBoard)
        self.statusLayout.setContentsMargins(0, 0, 0, 0)
        self.statusLayout.addSpacing(0)
        self.statusBoard.setLayout(self.statusLayout)
        self.statusBoard.setStyleSheet(self.stylist.get_status_board_style_sheet())

    # status slots
    def setup_switch_buttons(self):
        self.toggleSettingsButton.setText('\u25B3' + "Options" ) # + '\u25BD'
        self.toggleSettingsButton.setFixedWidth(70)
        self.toggleSettingsButton.clicked.connect(self.on_settings_toggle)

        self.toggleAppInfoButton.setText('\u25B3' + "Info" )
        self.toggleAppInfoButton.setFixedWidth(70)
        self.toggleAppInfoButton.clicked.connect(self.on_info_toggle)

        self.messageBoard.setAlignment(QtCore.Qt.AlignRight)

    def on_settings_toggle(self):
        self.action_toggle_options_panel(ActivePanel.Options)
    
    def on_info_toggle(self):
        self.action_toggle_options_panel(ActivePanel.Info)
        #alert = QMessageBox()
        #alert.setText('You clicked info button!')
        #alert.exec_()
    # }




    # settings {
    def prepare_settings_board(self):
        self.set_settings_margins()
        self.set_info_panel()
        self.set_settings_panel()
        self.stack_settings_elements()

    def set_settings_margins(self):
        self.switchLayout.setContentsMargins(0, 0, 0, 0)
        self.switchLayout.setSpacing(0)

    def set_info_panel(self):
        self.iconLabel.setFixedWidth(50)
        
        myPixmap = QtGui.QPixmap(self.directory.get_resource_dir() + 'icon.png')
        myScaledPixmap = myPixmap.scaled(self.iconLabel.size(), QtCore.Qt.KeepAspectRatio)
        self.iconLabel.setPixmap(myScaledPixmap)

        self.aboutLabel.setText("""
        This little notetaking app is created by <a href=\"https://github.com/deszczowy\">Deszczowy</a><br />
        Fabolous Hummingbird icon is made by <a href=\"https://www.flaticon.com/authors/freepik\">Freepik</a> from <a href=\"http://www.flaticon.com\">www.flaticon.com</a>
        """
        )        
        self.aboutLabel.setOpenExternalLinks(True)
        self.aboutLabel.setWordWrap(True)
        self.infoLayout.addWidget(self.iconLabel)
        self.infoLayout.addWidget(self.aboutLabel)
        self.infoBoard.setLayout(self.infoLayout)

    def set_settings_panel(self):
        self.fontSizeLabel.setText("Font size")
        self.fontSizeLabel.setAlignment(QtCore.Qt.AlignRight)
        self.fontSizeLabel.setFixedHeight(20)
        self.fontSizeLabel.setFixedWidth(100)

        self.fontSizeValue.setMinimum(6)
        self.fontSizeValue.setMaximum(100)
        self.fontSizeValue.setValue(13)
        self.fontSizeValue.setFixedHeight(30)
        self.fontSizeValue.setFixedWidth(70)
        self.fontSizeValue.valueChanged.connect(self.on_font_size_change)

        self.optionsLayout.addWidget(self.fontSizeLabel)
        self.optionsLayout.addWidget(self.fontSizeValue)
        self.optionsBoard.setLayout(self.optionsLayout)

    def on_font_size_change(self):
        mainPageTextCursor = self.mainPage.textCursor()
        sideNoteTextCursor = self.sideNotes.textCursor()
        mainPageModified = self.mainPage.document().isModified()
        sideNoteModified = self.sideNotes.document().isModified()
        self.mainPage.selectAll()
        self.mainPage.setFontPointSize(self.fontSizeValue.value())
        self.mainPage.setTextCursor(mainPageTextCursor)
        self.mainPage.document().setModified(mainPageModified)
        self.sideNotes.selectAll()
        self.sideNotes.setFontPointSize(self.fontSizeValue.value())
        self.sideNotes.setTextCursor(sideNoteTextCursor)
        self.sideNotes.document().setModified(sideNoteModified)

    def stack_settings_elements(self):
        self.switchLayout.addWidget(self.optionsBoard)
        self.switchLayout.addWidget(self.infoBoard)
        self.switchBoard.setLayout(self.switchLayout)
        self.hide_all_panels()

    def hide_all_panels(self):
        self.optionsBoard.setFixedHeight(0)
        self.infoBoard.setFixedHeight(0)
        self.switchBoard.setFixedHeight(0)
    # }




    # app {
    def stack_gui_elements(self):
        self.stack_book_elements()
        self.stack_status_elements()
        self.stack_settings_elements()

        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.appLayout.setSpacing(0)
        self.appLayout.addWidget(self.desktop)
        self.appLayout.addWidget(self.statusBoard)
        self.appLayout.addWidget(self.switchBoard)
        self.hMainWindow.setLayout(self.appLayout)

    def setup_app(self):
        self.setup_icon()
        self.bind_shortcuts()
        self.setup_window_geometry()
        self.setWindowTitle(self.version.app_name())

    def setup_window_geometry(self):
        screen = QDesktopWidget().screenGeometry(-1)
        w = (screen.width() / 3) *2
        h = (screen.height() / 3) *2
        if w < 800: 
            w = 800
        if h < 600:
            h = 600        
        self.setGeometry(0, 0, int(w), int(h))
        print(w)
        print(h)

    def setup_icon(self):
        self.setWindowIcon(QtGui.QIcon(self.directory.get_resource_dir() + 'icon.png'))

    def bind_shortcuts(self):
        self.shortcutSave.activated.connect(self.action_save)
        self.shortcutMain.activated.connect(self.action_focus_main)
        self.shortcutSide.activated.connect(self.action_focus_side)
        self.shortcutInfo.activated.connect(self.on_info_toggle)
        self.shortcutSetup.activated.connect(self.on_settings_toggle)
        self.shortcutHide.activated.connect(self.hide_all_panels)
        self.shortcutExit.activated.connect(self.action_terminate)
        self.shortcutNormal.activated.connect(self.switch_editor_mode_to_normal)
        self.shortcutFocus.activated.connect(self.switch_editor_mode_to_focus)

    def center(self):
        geometry = self.frameGeometry()
        screen = QApplication.desktop().screenNumber(QApplication.desktop().cursor().pos())
        centerPoint = QApplication.desktop().screenGeometry(screen).center()
        geometry.moveCenter(centerPoint)
        self.move(geometry.topLeft())

    def init_ui(self):
        self.prepare_book()
        self.prepare_status_board()
        self.prepare_settings_board()
        self.stack_gui_elements()
        self.setup_app()
        self.prepare_timers()
        self.center()
        self.setCentralWidget(self.hMainWindow)
    # }

def main():
    Database().create()
    app = QApplication(sys.argv)
    app.setStyleSheet(Stylist().get_style_sheet())
    w = MainWindow()
    w.show()
    app.exec()

    #gui = HummingBirdGui()
    

    #sys.exit(app.exec_())

if __name__ == '__main__':
    main()
