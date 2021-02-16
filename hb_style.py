from hb_enums import (EditorTheme)

class Stylist():

    def get_style_sheet(self, theme):
        if theme == EditorTheme.Dark:
            return self.get_style_sheet_dark()
        else:
            return self.get_style_sheet_light()

    def get_style_sheet_dark(self):
        return """
            QWidget {
                margin:0px; 
                padding:0px; 
                border:0px;
                background-color: black;
            } 

            QLineEdit {
                border: 1px dotted #353535;
            }

            QPushButton {
                font-size:12px; 
                color: #353535;
            }

            QScrollBar:vertical
            {
                    border: 0;
                    background-color: #000;
                    width:7px;
                    margin: 0;
            }

            QScrollBar::handle:vertical
            {
                min-height: 0px;
                background-color: #353535;
                border-radius: 3px;
            }

            QScrollBar::add-line:vertical
            {
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }

            QScrollBar::sub-line:vertical
            {
                height: 0 px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
            {
                background: none;
            }
        """
    def get_style_sheet_light(self):
        return """
            QWidget {
                margin:0px; 
                padding:0px; 
                border:0px;
                background-color: white;
            } 

            QLineEdit {
                border: 1px dotted silver;
            }

            QPushButton {
                font-size:12px; 
                color: silver;
            }

            QScrollBar:vertical
            {
                    border: 0;
                    background-color: #ffffff;
                    width:7px;
                    margin: 0;
            }

            QScrollBar::handle:vertical
            {
                min-height: 0px;
                background-color: silver;
                border-radius: 3px;
            }

            QScrollBar::add-line:vertical
            {
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }

            QScrollBar::sub-line:vertical
            {
                height: 0 px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }

            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical
            {
                background: none;
            }
            
            .info_class
            {
                line-height:0px; 
                font-size:10px; 
                font-family:mono; 
                width:100%; 
                text-align:center; 
                color:silver;
            }
        """



    def get_side_notes_style_sheet(self, theme):
        if theme == EditorTheme.Dark:
            return self.get_side_notes_style_sheet_dark()
        else:
            return self.get_side_notes_style_sheet_light()

    def get_side_notes_style_sheet_dark(self):
        return """
            border-left: 1px dashed #353535;
        """
    def get_side_notes_style_sheet_light(self):
        return """
            border-left: 1px dashed black;
        """
    def get_side_notes_style_focus(self, theme):
        if theme == EditorTheme.Dark:
            return "border:0px; color: #252525;"
        else:
            return "border:0px; color: silver;"



    def get_status_board_style_sheet(self, theme):
        if theme == EditorTheme.Dark:
            return self.get_status_board_style_sheet_dark()
        else:
            return self.get_status_board_style_sheet_light()

    def get_status_board_style_sheet_dark(self):
        return """
            .QFrame {
                border-top: 1px dashed #353535; 
            }
        """
    def get_status_board_style_sheet_light(self):
        return """
            .QFrame {
                border-top: 1px dashed black; 
            }
        """
    def get_status_board_style_focus(self, theme):
        if theme == EditorTheme.Dark:
            return ".QFrame {border:0px;} QPushButton {color: #252525;}"
        else:
            return ".QFrame {border:0px;} QPushButton {color: silver;}"
