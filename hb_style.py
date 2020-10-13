class Stylist():

    def get_style_sheet(self):
        sheet = ""
        with open("./style.css", 'r') as _file:
            sheet = _file.read() 
        return sheet

    def get_side_notes_style_sheet(self):
        return """
            border-left: .05em dashed silver;
        """

    def get_status_board_style_sheet(self):
        return """
            .QFrame {
                border-top: .05em dashed silver; 
            }
        """