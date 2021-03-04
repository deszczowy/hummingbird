class Sql():

    separator = chr(1)

    @staticmethod
    def create_db(sep):
        return """
            CREATE TABLE IF NOT EXISTS "notebook" (
                "id"	INT NOT NULL,
                "folder"	INT NOT NULL,
                "sleeve"	INT NOT NULL,
                "content"	TEXT NOT NULL,
                "save_time"	TEXT NOT NULL,
                "version"	INT NOT NULL,
                "archived"	INT NOT NULL,
                PRIMARY KEY("id")
            );
        """ + sep + """
            CREATE TABLE IF NOT EXISTS dictionary (
                key TEXT PRIMARY KEY NOT NULL,
                entry TEXT NOT NULL
            )
        """ + sep + """
            CREATE TABLE IF NOT EXISTS folder (
                id INT PRIMARY KEY NOT NULL,
                label TEXT NOT NULL
            )
        """ + sep + """
            INSERT INTO dictionary (key, entry) 
               SELECT 'db_version', '5'
               WHERE NOT EXISTS(SELECT 1 FROM dictionary WHERE key = 'db_version');
        """ + sep + """
            INSERT INTO folder (id, label)
                SELECT 1, 'default'
                WHERE NOT EXISTS(SELECT 1 FROM folder WHERE id = 1);
        """ + sep + """
            CREATE TABLE IF NOT EXISTS task (
                id INT PRIMARY KEY NOT NULL,
                folder INT NOT NULL,
                label TEXT NOT NULL,
                priority INT NOT NULL,
                stamp TEXT NOT NULL,
                done INT NOT NULL
            );
        """

    @staticmethod
    def update_to_2(sep):
        return """ """ + sep + """ """

    @staticmethod
    def update_to_3(sep):
        return """
        ALTER TABLE notebook RENAME TO notebookOLD;
        """ + sep + """
        CREATE TABLE IF NOT EXISTS notebook (
            id INT PRIMARY KEY NOT NULL,
            folder INT NOT NULL,
            content TEXT NOT NULL,
            version INT NOT NULL,
            save_time TEXT NOT NULL,
            main_page INT NOT NULL,
            archived INT NOT NULL
        );
        """ + sep + """
        INSERT INTO notebook (id, folder, content, version, save_time, main_page, archived) SELECT id, 1, content, version, save_time, main_page, archived FROM notebookOLD;
        """ + sep + """
        DROP TABLE notebookOLD;
        """ + sep + """
        UPDATE dictionary SET entry = '3' WHERE key = 'db_version';
        """

    @staticmethod
    def update_to_4(sep):
        return """
        CREATE TABLE IF NOT EXISTS folder (
            id INT PRIMARY KEY NOT NULL,
            label TEXT NOT NULL
        );
        """ + sep + """
        INSERT INTO folder (id, label)
            SELECT 1, 'default'
            WHERE NOT EXISTS(SELECT 1 FROM folder WHERE id = 1);
        """ + sep + """
        INSERT OR REPLACE INTO dictionary(key, entry) VALUES('folder_source', 'LOCAL');
        """ + sep + """
        INSERT OR REPLACE INTO dictionary(key, entry) VALUES('folder_opened', '1');
        """ + sep + """
        INSERT OR REPLACE INTO dictionary(key, entry) VALUES('folder_path', '');
        """ + sep + """
        UPDATE dictionary SET entry = '4' WHERE key = 'db_version';
        """

    @staticmethod
    def update_to_5(sep):
        return """
        ALTER TABLE notebook RENAME TO notebookOLD;
        """ + sep + """
        CREATE TABLE "notebook" (
            "id"	INT NOT NULL,
            "folder"	INT NOT NULL,
            "sleeve"	INT NOT NULL,
            "content"	TEXT NOT NULL,
            "save_time"	TEXT NOT NULL,
            "version"	INT NOT NULL,
            "archived"	INT NOT NULL,
            PRIMARY KEY("id")
        );
        """ + sep + """
        INSERT INTO notebook (id, folder, sleeve, content, save_time, version, archived) 
        SELECT id, folder, 
        CASE WHEN main_page = 1 THEN 0 ELSE 1 END,
        content, save_time, version, archived FROM notebookOLD;
        """ + sep + """
        DROP TABLE notebookOLD;
        """ + sep + """
        UPDATE dictionary SET entry = '5' WHERE key = 'db_version';
        """ + sep + """
        CREATE TABLE "task" (
            "id"	INTEGER,
            "folder"	INTEGER NOT NULL,
            "label"	TEXT NOT NULL,
            "priority"	INTEGER NOT NULL,
            "stamp"	TEXT NOT NULL,
            "done"	INTEGER NOT NULL,
            PRIMARY KEY("id")
        );
        """ + sep + """
        DROP TABLE defaults;
        """