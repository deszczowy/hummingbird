from hb_enums import (EditorTheme)
from style.dark import *

class Stylist():

    def get_style_sheet(self, theme):
        if theme == EditorTheme.Dark:
            return stylesheet_dark
        else:
            return self.get_style_sheet_light()

# info_window_widget.setStyleSheet("QWidget{background-color: #efefef;}")
# self.main.setStyleSheet("QWidget{background-color: #f5f5f5;}")
# self.main.setStyleSheet("QWidget{background-color: #f5f5f5;}")
#         header.setStyleSheet("font-size: 20px;")

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

            QPushButton
            {
                font-size:12px;
                border: 1px solid silver; 
                min-width: 70px; 
                min-height: 30px; 
                padding: 5px; 
                background-color: #fff; 
                color: black;
            }
        """