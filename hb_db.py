from PyQt5.QtSql import (QSqlDatabase, QSqlQuery)

from hb_dir import Directory
from hb_sql import Sql
from hb_version import VersionInfo

from classes.items.folder import *

class Database():

    def __init__(self):
        self.name = Directory().get_notes_dir() + "notebooks.db"

    def create(self): # todo
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
    
    def get_text(self, folder, sleeve):
        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN :GET M")
            return False

        query = QSqlQuery()
        query.prepare("SELECT content FROM notebook WHERE sleeve = :sleeve AND archived = 0 AND folder = :folder")
        query.bindValue(":folder", int(folder))
        query.bindValue(":sleeve", int(sleeve))
        query.exec_()
        while query.next():
            return query.value(0)
        return ""


#dragons 

    def save_text(self, folder, sleeve, content):

        return False
        
        sleeve_id = int(sleeve)

        query_text = """
        INSERT INTO notebook (
            id, 
            folder, 
            content, 
            version, 
            save_time, 
            sleeve, 
            archived
        ) values (
            (SELECT IFNULL(MAX(id),0) +1 FROM notebook), 
            :folder,
            :content,
            (SELECT IFNULL(MAX(version),0) +1 FROM notebook WHERE sleeve = :sleeve AND folder = :folder),
            datetime('now','localtime'),
            :sleeve, 
            0
        );"""

        #archive sleeve

        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN :SAVE NOTEBOOK")
            return False

        query = QSqlQuery()
        query.prepare(query_text)

        query.bindValue(":folder", folder)   
        query.bindValue(":content", content)
        query.bindValue(":sleeve", sleeve)
        query.exec_()

        # self.remove_old_versions(sleeve, folder_id)

    

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
            item = FolderItem(query.value(1))
            item.setSelectable(True)
            item.setEditable(False)
            item.folder_id = query.value(0)
            model.appendRow(item)

        return model

    def get_task_model(self, folder):
        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN :GET TASK")
            return False

        query = QSqlQuery()
        query.prepare("SELECT id, label, priority, stamp FROM task WHERE folder = :folder AND done = 0 ORDER BY priority DESC, stamp DESC")
        query.bindValue(":folder", folder)
        query.exec()

        model = QStandardItemModel()
        while query.next():
            item = ToDoItem()
            item.setSelectable(True)
            item.setEditable(False)
            item.setCheckable(True)
            item.id = int(query.value(0))
            item.label = query.value(1)
            item.priority = Priority(int(query.value(2)))
            item.date = datetime.datetime.strptime(query.value(3),"%Y%m%d%H%M%S")
            model.appendRow(item)
        
        return model

    def insert_folder(self, folder_name):
        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN :INS FOLDER")
            return False

        query = QSqlQuery()
        query.prepare(
        """INSERT INTO folder (id, label) values (
            (SELECT IFNULL(MAX(id),0) +1 FROM folder), :label
        );""")
                    
        query.bindValue(":label", folder_name)
        query.exec_()

    def update_folder(self, folder_id, new_name):
        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN :UPD FOLDER")
            return False

        query = QSqlQuery()
        query.prepare("UPDATE folder SET label = :label WHERE id = :folder;")
        query.bindValue(":label", new_name)
        query.bindValue(":folder", folder_id)
        query.exec_()

    def insert_task(self, folder, item):
        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN :I TASK")
            return False

        query = QSqlQuery()
        query.prepare("""
            INSERT INTO task (
                id, folder, label, priority, stamp, done
            ) VALUES (
                (SELECT IFNULL(MAX(id),0) +1 FROM task),
                :folder,
                :label,
                :priority,
                :stamp,
                0
            )
        """)
        query,bindValue(":folder", folder)
        query.bindValue(":label", item.text())
        query.bindValue(":date", item.date)
        query.bindValue(":priority", int(item.priority))
        query.exec_()