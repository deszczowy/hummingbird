from PyQt5 import QtCore, QtGui

from PyQt5.QtGui import (QStandardItemModel, QStandardItem)

from PyQt5.QtCore import QModelIndex

from PyQt5.QtWidgets import (
    QVBoxLayout, QHBoxLayout, 
    QWidget, QListView, QLineEdit, QComboBox, QPushButton
)

from hb_enums import Component
from classes.items.folder import *
from hb_db import Database

class ToDoList(QWidget):
    def __init__(self, parent, component_def):
        super(ToDoList, self).__init__(parent)
        self.component = component_def
        self.layout = QVBoxLayout()
        self.list = QListView()
        self.ids = []

        self.form = QVBoxLayout()
        self.buttons = QHBoxLayout()

        self.label = QLineEdit()
        self.label.setPlaceholderText("new task name")
        self.priority = QComboBox()
        self.priority.insertItem(0, "Low")
        self.priority.insertItem(1, "Medium")
        self.priority.insertItem(2, "High")
        self.priority.insertItem(3, "Critical")
        
        self.add = QPushButton("Add")
        self.add.clicked.connect(self.action_add)

        self.stack()

    def stack(self):
        self.layout.addWidget(self.list)
        self.form.addWidget(self.label)
        self.buttons.addWidget(self.priority)
        self.buttons.addWidget(self.add)
        self.form.addLayout(self.buttons)
        self.layout.addLayout(self.form)
        self.setLayout(self.layout)
        self.prepare()

    def prepare(self):
        model = Database().get_task_model(1)
        self.list.setModel(model)
        #self.list.clicked[QModelIndex].connect(self.item_check)

    #def item_check(self, index):
    #    item = self.list.model().itemFromIndex(index)
    #    if item.checkState() == QtCore.Qt.Checked:

    def action_add(self):
        item = ToDoItem()
        item.label = self.label.text()
        item.date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        item.priority = Priority(self.priority.currentIndex())
        item.setSelectable(True)
        item.setEditable(False)
        item.setCheckable(True)
        idx = self.get_index_of_priority_to_insert(item.priority)
        self.list.model().insertRow(idx, item)

    def get_index_of_priority_to_insert(self, priority):
        p = int(priority)
        for idx in range(0, self.list.model().rowCount()):
            item = self.list.model().item(idx)
            if int(item.priority) <= p:
                return idx
        return 0

    def do_count(self):
        self.ids.clear()

        model = self.list.model()
        for index in range(model.rowCount()):
            item = model.item(index)
            if item.checkState() == QtCore.Qt.Checked:
                self.ids.append(item.id)
        
        print(self.ids)