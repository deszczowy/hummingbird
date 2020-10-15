from PyQt5.QtSql import (QSqlDatabase, QSqlQuery)

from hb_dir import Directory

class Database():

    def __init__(self):
        self.name = Directory().get_notes_dir() + "notebooks.db"

    def create(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN :CREATE")
            return False

        query = QSqlQuery()
        query.exec_(
            '''CREATE TABLE IF NOT EXISTS notebook (
                id INT PRIMARY KEY NOT NULL,
                content TEXT NOT NULL,
                version INT NOT NULL,
                save_time TEXT NOT NULL,
                main_page INT NOT NULL,
                archived INT NOT NULL
            );'''
        )

        query.exec_(
            '''CREATE TABLE IF NOT EXISTS defaults (
                id INT PRIMARY KEY NOT NULL,
                version INT NOT NULL
            );'''
        )

        query.exec_(
            '''INSERT INTO defaults (id, version) 
               SELECT 1, 1 
               WHERE NOT EXISTS(SELECT 1 FROM defaults WHERE id = 1);
            '''
        )

    def save_notebook(self, content, side):
        main_indicator = -1
        if side:
            self.archive_side_notebook()
            main_indicator = 0
        else:
            self.archive_main_notebook()
            main_indicator = 1

        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN :SAVE")
            return False

        query = QSqlQuery()
        query.prepare(
        """INSERT INTO notebook (id, content, version, save_time, main_page, archived) values (
            (SELECT IFNULL(MAX(id),0) +1 FROM notebook), 
            :content,
            (SELECT IFNULL(MAX(version),0) +1 FROM notebook WHERE main_page = :mpage),
            datetime('now','localtime'),
            :mpage, 0
        );""")
                    
        query.bindValue(":content", content)
        query.bindValue(":mpage", main_indicator)
        query.exec_()

    def archive_main_notebook(self):
        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN :ARCH M")
            return False

        QSqlQuery().exec_("UPDATE notebook SET archived = 1 WHERE main_page = 1")

    def archive_side_notebook(self):
        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN :ARCH S")
            return False

        QSqlQuery().exec_("UPDATE notebook SET archived = 1 WHERE main_page = 0")

    def get_main_content(self):
        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN :GET M")
            return False

        query = QSqlQuery()
        query.exec_("SELECT content FROM notebook WHERE main_page = 1 AND archived = 0")
        while query.next():
            return query.value(0)
        
    def get_side_content(self):
        db = QSqlDatabase.database()
        db.setDatabaseName(self.name)

        if not db.open():
            print("NOT OPEN :GET S")
            return False

        query = QSqlQuery()
        query.exec_("SELECT content FROM notebook WHERE main_page = 0 AND archived = 0")
        while query.next():
            return query.value(0)
        