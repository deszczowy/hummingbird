#1E1E1E active background
#1A1A1A inactive background
#8C8C8C visible background elements (bottom lines, scrollbars, etc.)
#D4D4D4 main text
#4D4D4D clickable areas (buttons, items)

#252526 dialog background

#474747 separators, unused in palette

stylesheet_dark = """

    /* Base components setup */

    QWidget
    {
        margin:0px; 
        padding:0px; 
        border:0px;
        background-color: #1E1E1E;
        color: #D4D4D4;
    }

    QLineEdit
    {
        border: 0px;
        border-bottom: 1px solid #8C8C8C;
        color: #D4D4D4;
    }

    QTextEdit
    {
        border: 0px;
        margin: 0px;
        padding: 0px;
        color: #D4D4D4;
    }

    QPushButton
    {
        font-size:12px;
        border: 0px; 
        min-width: 70px; 
        min-height: 30px; 
        padding: 5px; 
        background-color: #4D4D4D; 
        color: #D4D4D4;
    }

    /* List */

    QListView
    {
        background-color: #1E1E1E;
        margin:0px; 
        padding:0px;
        border:0px;
        selection-color: #D4D4D4;
        selection-background-color: #4D4D4D;
    }

    QListView::item
    {
        padding: 7px;
        background-color: #1E1E1E;
        color: #D4D4D4;
    }

    QListView::item:hover
    {
        background-color: #4D4D4D;
    }

    /* Scrollbar */

    QScrollBar:vertical
    {
        border: 0;
        background-color: #1E1E1E;
        width:7px;
        margin: 0;
    }

    QScrollBar::handle:vertical
    {
        min-height: 0px;
        background-color: #8C8C8C;
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

    /* Tabs */

    QTabWidget::pane
    {
        border: 0px solid red;
        padding: 0px;
        margin: 0px;
        background-color: #1E1E1E;
        color: #D4D4D4;
    }

    QTabWidget::tab-bar 
    {
        border: 0px;
        background-color: #1E1E1E;
        color: #D4D4D4;
        width: 300px;
    }

    QTabBar::tab {
    
        border: 0px;
        min-width: 70px;
        padding: 4px;
        background: black;
    }

    QTabBar::tab:selected {
        background-color: #1E1E1E;
        color: #D4D4D4;
    }

    QTabBar::tab:!selected {
        background: #1A1A1A;
        color: #4D4D4D;
    }

    QTabBar::tab:hover {
        font-weight: bold;
    }

    /* Select */

    QComboBox
    {
        background-color: #1E1E1E;
        border:0px;
    }

    QComboBox::item 
    {
        border: 0px;
        height: 20px;
        padding: 0px;
        margin: 0px;
        background-color: #1E1E1E;
        color: #D4D4D4;
    }

    QComboBox::item:selected {
        border: 0px;
        padding: 0px;
        margin: 0px;
        background-color: #4D4D4D;
        color: #D4D4D4;
    }

"""