from PyQt5.QtSql import (QSqlDatabase, QSqlQuery)
from PyQt5.QtGui import (QStandardItem, QStandardItemModel)

from hb_dir import Directory
from hb_sql import Sql
from hb_version import VersionInfo

from classes.items.folder import *

class Database():

    def __init__(self):
        self.name = Directory().get_notes_dir() + "notebooks.db"

    def create(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN :CREATE")
            return False

        queries = Sql.create_db(Sql.separator).split(Sql.separator)
        sqlQuery = QSqlQuery()

        for query in queries:
            sqlQuery.exec_(query)

        self.update()

    def save_notebook(self, content, side, folder_id):
        main_indicator = -1
        if side:
            self.archive_side_notebook(folder_id)
            main_indicator = 0
        else:
            self.archive_main_notebook(folder_id)
            main_indicator = 1

        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN :SAVE")
            return False

        query = QSqlQuery()
        query.prepare(
        """INSERT INTO notebook (id, folder, content, version, save_time, main_page, archived) values (
            (SELECT IFNULL(MAX(id),0) +1 FROM notebook), 
            :folder,
            :content,
            (SELECT IFNULL(MAX(version),0) +1 FROM notebook WHERE main_page = :mpage AND folder = :folder),
            datetime('now','localtime'),
            :mpage, 0
        );""")

        query.bindValue(":folder", folder_id)   
        query.bindValue(":content", content)
        query.bindValue(":mpage", main_indicator)
        query.exec_()

        self.remove_old_versions(main_indicator, folder_id)

    def remove_old_versions(self, side, folder_id):
        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN: REMO")
            return False
        
        query = QSqlQuery()
        query.prepare("DELETE FROM notebook WHERE folder = :folder AND main_page = :side AND version <= (SELECT max(version) FROM notebook WHERE main_page = :side AND folder = :folder) -40;")
        query.bindValue(":folder", folder_id)
        query.bindValue(":side", side)
        query.exec_()

    def archive_main_notebook(self, folder_id):
        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN :ARCH M")
            return False

        query = QSqlQuery()
        query.prepare("UPDATE notebook SET archived = 1 WHERE main_page = 1 AND folder = :folder")
        query.bindValue(":folder", folder_id)
        query.exec_()

    def archive_side_notebook(self, folder_id):
        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN :ARCH S")
            return False

        query = QSqlQuery()
        query.prepare("UPDATE notebook SET archived = 1 WHERE main_page = 0 AND folder = :folder")
        query.bindValue(":folder", folder_id)
        query.exec_()
        

    def get_main_content(self, folder_id):
        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN :GET M")
            return False

        query = QSqlQuery()
        query.prepare("SELECT content FROM notebook WHERE main_page = 1 AND archived = 0 AND folder = :folder")
        query.bindValue(":folder", folder_id)
        query.exec_()
        while query.next():
            return query.value(0)
        return ""
        
    def get_side_content(self, folder_id):
        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN :GET S")
            return False

        query = QSqlQuery()
        query.prepare("SELECT content FROM notebook WHERE main_page = 0 AND archived = 0 AND folder = :folder")
        query.bindValue(":folder", folder_id)
        query.exec_()
        while query.next():
            return query.value(0)
        return ""

    def get_database_version(self):
        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN :GET DBV")
            return False
        
        return int(self.get_value("db_version", "1"))
        
    def update(self):
        local_version = self.get_database_version()
        current_version = VersionInfo.dbVersion
        difference = current_version - local_version

        separator = Sql.separator

        updaters = {
            1: Sql.update_to_2(separator),
            2: Sql.update_to_3(separator),
            3: Sql.update_to_4(separator)
        }

        if difference == 1:
            func = updaters.get(local_version)
            self.execute(func)
        else:
            for version in range(local_version, current_version):
                func = updaters.get(version)
                self.execute(func)

    def execute(self, script):
        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not script == "":

            if not db.open():
                print("NOT OPEN :EXECUTE")
                return False

            queries = (script).split(Sql.separator)
            sqlQuery = QSqlQuery()

            for query in queries:
                sqlQuery.exec_(query)

    def store_value(self, key, value):
        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN: STORE")
            return False
        
        query = QSqlQuery()
        query.prepare("INSERT OR REPLACE INTO dictionary(key, entry) VALUES(:key, :value);")
        query.bindValue(":key", key)
        query.bindValue(":value", value)
        query.exec_()

    def get_value(self, key, default_value):
        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN :GET VALUE")
            return False
        
        query = QSqlQuery()
        query.prepare(
        """WITH list(key) AS (
               VALUES (:key)
           )
           SELECT IFNULL(entry, :def) AS value
           FROM list
           LEFT JOIN dictionary USING (key);
        """
        )
        query.bindValue(":key", key)
        query.bindValue(":def", default_value)
        query.exec_()

        result = ""
        while query.next():
            res = query.value(0)
            if res == "":
                res = default_value

        return res

    def get_folder_model(self):
        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN :GET FOLDER")
            return False
        
        query = QSqlQuery()
        query.exec_("SELECT id, label FROM folder")

        model = QStandardItemModel()
        while query.next():
            item = QStandardItem(query.value(1))
            item.folder_id = query.value(0)
            model.appendRow(item)

        return model

    def insert_folder(self, folder_name):
        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN :SAVE")
            return False

        query = QSqlQuery()
        query.prepare(
        """INSERT INTO folder (id, label) values (
            (SELECT IFNULL(MAX(id),0) +1 FROM folder), :label
        );""")
                    
        query.bindValue(":label", folder_name)
        query.exec_()