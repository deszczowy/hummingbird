stylesheet_light = """

    /* Base components setup */

    QWidget
    {
        margin:0px; 
        padding:0px; 
        border:0px;
        background-color: #D4D4D4;
        color: #1E1E1E;
        font-size: 14px;
    }

    QLineEdit
    {
        border: 0px;
        border-bottom: 1px solid #8C8C8C;
        color: #1E1E1E;
    }

    QTextEdit
    {
        border: 0px;
        margin: 0px;
        padding: 0px;
        color: #1E1E1E;
    }

    QPushButton
    {
        font-size:12px;
        border: 0px; 
        min-width: 70px; 
        min-height: 30px; 
        padding: 5px; 
        background-color: #8C8C8C; 
        color: #D4D4D4;
    }

    /* List */

    QListView
    {
        background-color: #D4D4D4;
        margin:0px; 
        padding:0px;
        border:0px;
        selection-color: #1E1E1E;
        selection-background-color: #8C8C8C;
    }

    QListView::item
    {
        padding: 7px;
        background-color: #D4D4D4;
        color: #1E1E1E;
    }

    QListView::item:hover
    {
        background-color: #8C8C8C;
    }

    /* Scrollbar */

    QScrollBar:vertical
    {
        border: 0;
        background-color: #D4D4D4;
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
        background-color: #D4D4D4;
        color: #1E1E1E;
    }

    QTabWidget::tab-bar 
    {
        border: 0px;
        background-color: #8C8C8C;
        color: #1E1E1E;
        width: 300px;
    }

    QTabBar::tab {
    
        border: 0px;
        min-width: 70px;
        padding: 4px;
        background: white;
    }

    QTabBar::tab:selected {
        background-color: #D4D4D4;
        color: #1E1E1E;
    }

    QTabBar::tab:!selected {
        background: #8C8C8C;
        color: #D4D4D4;
    }

    QTabBar::tab:hover {
        font-weight: bold;
    }

    /* Select */

    QComboBox
    {
        background-color: #D4D4D4;
        border:0px;
    }

    QComboBox::item 
    {
        border: 0px;
        height: 20px;
        padding: 0px;
        margin: 0px;
        background-color: #D4D4D4;
        color: #1E1E1E;
    }

    QComboBox::item:selected {
        border: 0px;
        padding: 0px;
        margin: 0px;
        background-color: #8C8C8C;
        color: #D4D4D4;
    }

    #StatusBar
    {
        font-size: 10px;
        color: #8C8C8C;
        padding: 5px;
        font-family: mono;
    }

    #MessageBoard 
    {
        font-size: 10px;
        color: #8C8C8C;
        padding: 5px;
        font-family: mono;
    }
"""
