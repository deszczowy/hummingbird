class Stylist():

    def get_style_sheet(self):
        return """
            QWidget {
                margin:0px; 
                padding:0px; 
                border:0px;
                background-color: white;
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
        """

    def get_side_notes_style_sheet(self):
        return """
            border-left: 1px dashed black;
        """

    def get_status_board_style_sheet(self):
        return """
            .QFrame {
                border-top: 1px dashed black; 
            }
        """