from PyQt5.QtGui import (QStandardItemModel, QStandardItem, QFont, QPen, QBrush)

from PyQt5.QtCore import (Qt)

from PyQt5.QtWidgets import *

from hb_enums import Priority
import datetime

class FolderItem(QStandardItem):
    folder_id = 0

class ToDoItem(QStandardItem):
    id = 0
    priority = Priority.Medium
    date = datetime.datetime.now()
    label = ""

    def data(self, role):
        if role == Qt.DisplayRole:
            return self.get_icon() + " " + self.label
        return super().data(role)

    def get_icon(self):
        icons = {
            Priority.Low: "\U0001F817",
            Priority.Medium: "\u279E",
            Priority.High: "\U0001F815",
            Priority.Critical: "\u25B2"
        }

        return icons.get(self.priority, "")