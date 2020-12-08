import sys
from PyQt5 import (QtCore, QtGui)
from PyQt5.QtGui import (QStandardItemModel, QStandardItem)

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame, QMessageBox,
    QHBoxLayout, QVBoxLayout, QGridLayout, QSpacerItem,
    QTextEdit, QPushButton, QLabel, QSpinBox, 
    QListView,
    QShortcut, QDesktopWidget, QSizePolicy
)

notebooks = [
   'Work',
   'Private',
   'Book concept'
]

def show_window(dlg):
   if dlg.isVisible():
      dlg.hide()
   else:
      dlg.show()

def on_item_changed(index):
   alert = QMessageBox()
   alert.setText(index.data())
   alert.exec_()

def window():
   # Setup
   app = QApplication(sys.argv)
   w = QWidget()
   w.setGeometry(0,0,500,300)
   w.setWindowTitle("Playground")

   # Testing area
   """ # grid layout test
   g = QGridLayout()

   a = QLabel(w)
   a.setText("Option one")

   b = QLabel(w)
   b.setText("Spinbox")
   
   c = QLabel(w)
   c.setText("Option two")

   d = QLabel(w)
   d.setText("Edit")

   
   g.addWidget(a, 0, 0)
   g.addWidget(b, 0, 1)
   g.addWidget(c, 1, 0)
   g.addWidget(d, 1, 1)

   g.setRowStretch(2, 1)
   g.setColumnStretch(2, 1)
   
   g.setColumnMinimumWidth(0, 100)

   w.setLayout(g)   
   """

   # test window with list
   btn = QPushButton("Show a non-modal window")
   layout = QVBoxLayout(w)
   layout.addWidget(btn)

   ### dialog-
   dlg = QWidget(w)
   dlgLayout = QVBoxLayout(dlg)
   lbl = QLabel("Within window...", dlg)
   dlgLayout.addWidget(lbl)
   dlg.setStyleSheet("background-color:red;")

   book_picker = QListView()
   book_model = QStandardItemModel(book_picker)
   for nbook in notebooks:
      item = QStandardItem(nbook)
      item.setSelectable(True)
      item.setEditable(False)
      book_model.appendRow(item)
   book_picker.clicked.connect(on_item_changed)
   book_picker.setModel(book_model)
   book_picker.setStyleSheet("QListView{ margin:0px; padding:0px; border:0px; selection-color :blue; selection-background-color: yellow;  } ::item { padding: 10px; } ")

   dlgLayout.addWidget(book_picker)

   margin = 20
   wi = w.width() - (2*margin) 
   he = w.height() - (2*margin)
   dlg.setGeometry(margin, margin, wi, he)
   dlg.hide()
   ### -dialog

   btn.clicked.connect(lambda: show_window(dlg))

   # Show window
   w.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   window()