import sys
from PyQt5 import QtGui

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame, QMessageBox,
    QHBoxLayout, QVBoxLayout, QGridLayout, QSpacerItem,
    QTextEdit, QPushButton, QLabel, QSpinBox,
    QShortcut, QDesktopWidget, QSizePolicy
)

def window():
   # Setup
   app = QApplication(sys.argv)
   w = QWidget()
   w.setGeometry(0,0,500,300)
   w.setWindowTitle("Playground")

   # Testing area
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

   # Show window
   w.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   window()