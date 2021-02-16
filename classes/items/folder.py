from PyQt5.QtGui import (QStandardItemModel, QStandardItem)

from PyQt5.QtCore import Qt

class BasicItemModel(QStandardItemModel):
    def flags(self, index):
        return Qt.ItemIsSelectable and Qt.ItemIsEnabled

class FolderItem(QStandardItem):
    folder_id = 0