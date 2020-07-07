import sys
import os

from PyQt5 import QtCore, QtGui

from PyQt5.QtCore import (
    QSize, QTimer
)

from PyQt5.QtGui import QKeySequence

from PyQt5.QtWidgets import (
    QApplication, QWidget, QFrame, QMessageBox,
    QHBoxLayout, QVBoxLayout,
    QTextEdit, QPushButton, QLabel,
    QShortcut
)

from hb_notes import Notes
from hb_version import VersionInfo
from hb_enums import ActivePanel
from hb_style import Stylist

class HummingBirdGui(QWidget):

    def __init__(self):
        super().__init__()
        # timer
        self.tic = 0
        self.timer = QTimer(self)
        self.schedule = QTimer(self)
        # backend
        self.notes = Notes()
        self.version = VersionInfo()
        self.stylist = Stylist()
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
        # - info board
        self.infoBoard = QFrame()
        self.infoLayout = QVBoxLayout()
        self.aboutLabel = QLabel()
        # keys
        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        # go!
        self.init_ui()




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
            self.notes.saveMainNotes(self.mainPage.toPlainText())
            self.mainPage.document().setModified(False)
            saved = True

        if self.sideNotes.document().isModified():
            self.notes.saveSideNotes(self.sideNotes.toPlainText())
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
        self.binding.addWidget(self.mainPage)
        self.binding.addWidget(self.sideNotes)
        self.desktop.setLayout(self.binding)
    
    def load_notes_contents(self):
        self.mainPage.setPlainText(self.notes.getMainNotes())
        self.sideNotes.setPlainText(self.notes.getSideNotes())
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
        self.stack_settings_elements()

    def set_settings_margins(self):
        self.switchLayout.setContentsMargins(0, 0, 0, 0)
        self.switchLayout.setSpacing(0)

    def set_info_panel(self):
        self.aboutLabel.setText("About")
        self.infoLayout.addWidget(self.aboutLabel)
        self.infoBoard.setLayout(self.infoLayout)

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
        self.setLayout(self.appLayout)

    def setup_app(self):
        self.setup_icon()
        self.bind_shortcuts()
        self.setGeometry(300, 300, 800, 600)
        self.setWindowTitle(self.version.app_name())

    def setup_icon(self):
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'ico' + os.path.sep + 'icon.png'))

    def bind_shortcuts(self):
        self.save_shortcut.activated.connect(self.action_save)

    def init_ui(self):
        self.prepare_book()
        self.prepare_status_board()
        self.prepare_settings_board()
        self.stack_gui_elements()
        self.setup_app()
        self.prepare_timers()
    # }

def main():

    app = QApplication(sys.argv)
    app.setStyleSheet(Stylist().get_style_sheet())

    gui = HummingBirdGui()
    gui.show()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()