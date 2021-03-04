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
        self.list.setWordWrap(True)
        self.list.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.list.verticalScrollBar().setSingleStep(5)

        self.form = QVBoxLayout()
        self.buttons = QHBoxLayout()

        self.add = QPushButton("Add")
        self.add.clicked.connect(self.action_add)

        self.label = QLineEdit()
        self.label.setPlaceholderText("new task name")
        self.label.returnPressed.connect(self.add.click)

        self.priority = QComboBox()
        self.priority.insertItem(0, "Low")
        self.priority.insertItem(1, "Medium")
        self.priority.insertItem(2, "High")
        self.priority.insertItem(3, "Critical")
        self.priority.setCurrentIndex(1)

        self.stack()

    def stack(self):
        self.layout.addWidget(self.list)
        self.form.addWidget(self.label)
        self.buttons.addWidget(self.priority)
        self.buttons.addWidget(self.add)
        self.form.addLayout(self.buttons)
        self.layout.addLayout(self.form)
        self.setLayout(self.layout)

    def load(self, folder):
        model = Database().get_task_model(folder)
        self.list.setModel(model)
        #self.list.clicked[QModelIndex].connect(self.item_check)

    #def item_check(self, index):
    #    item = self.list.model().itemFromIndex(index)
    #    if item.checkState() == QtCore.Qt.Checked:

    def action_add(self):
        if self.label.text() != "":
            item = ToDoItem()
            item.label = self.label.text()
            item.date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            item.priority = Priority(self.priority.currentIndex())
            item.setSelectable(True)
            item.setEditable(False)
            item.setCheckable(True)
            idx = self.get_index_of_priority_to_insert(item.priority)
            self.list.model().insertRow(idx, item)
            self.label.setText("")

    def get_index_of_priority_to_insert(self, priority):
        p = int(priority)
        c = self.list.model().rowCount()

        # print("inserted priority = %d" % p)

        for idx in range(0, c):
            item = self.list.model().item(idx)
            if int(item.priority) <= p:
                return idx
        return c

    def save(self, folder):
        model = self.list.model()
        result = False

        for index in range(model.rowCount()):
            item = model.item(index)
            if item.id == 0:
                item.id = Database().insert_task(folder, item)
                result = True
            else:
                if item.checkState() == QtCore.Qt.Checked:
                    Database().check_task(item.id) 
                    result = True

        self.tidy_up()

        return result

    def tidy_up(self):
        go_on = self.list.model().rowCount() > 0
        i = 0

        while go_on:
            if self.list.model().item(i).checkState() == QtCore.Qt.Checked:
                self.list.model().removeRow(i)
            else:
                i += 1
            go_on = i < self.list.model().rowCount()

    def focus(self):
        self.list.setFocus()