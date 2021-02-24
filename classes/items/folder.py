from PyQt5.QtGui import (QStandardItemModel, QStandardItem)

from PyQt5.QtCore import Qt

from hb_enums import Priority
import datetime

class FolderItem(QStandardItem):
    folder_id = 0

class ToDoItem(QStandardItem):
    id = 0
    priority = Priority.Medium
    date = datetime.datetime.now()