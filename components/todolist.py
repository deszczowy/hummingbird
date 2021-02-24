from PyQt5 import QtCore, QtGui

from PyQt5.QtGui import (QStandardItemModel, QStandardItem)

from PyQt5.QtCore import QModelIndex

from PyQt5.QtWidgets import (
    QVBoxLayout, QWidget, QListView
)

from hb_enums import Component
from classes.items.folder import ToDoItem

class ToDoList(QWidget):
    def __init__(self, parent, component_def):
        super(ToDoList, self).__init__(parent)
        self.component = component_def
        self.layout = QVBoxLayout()
        self.list = QListView()
        self.stack()

    def stack(self):
        self.layout.addWidget(self.list)
        self.setLayout(self.layout)
        self.prepare()

    def prepare(self):
        item1 = ToDoItem("Entry 1")
        item1.setCheckable(True)
        item2 = ToDoItem("Entry 2")
        item2.setCheckable(True)
        model = QStandardItemModel()
        model.appendRow(item1)
        model.appendRow(item2)
        self.list.setModel(model)
        self.list.clicked[QModelIndex].connect(self.item_check)

    def item_check(self, index):
        item = self.list.model().itemFromIndex(index)
        if item.checkState() == QtCore.Qt.Checked:
            print(item.date)
            print(item.priority)
