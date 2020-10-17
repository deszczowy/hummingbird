class Sql():

    separator = chr(1)

    @staticmethod
    def create_db(sep):
        return """
            CREATE TABLE IF NOT EXISTS notebook (
                id INT PRIMARY KEY NOT NULL,
                content TEXT NOT NULL,
                version INT NOT NULL,
                save_time TEXT NOT NULL,
                main_page INT NOT NULL,
                archived INT NOT NULL,
                topic INT NULL
            );
        """ + sep + """
            CREATE TABLE IF NOT EXISTS defaults (
                id INT PRIMARY KEY NOT NULL,
                version INT NOT NULL
            );
        """ + sep + """
            CREATE TABLE IF NOT EXISTS dictionary (
                key TEXT PRIMARY KEY NOT NULL,
                entry TEXT NOT NULL
            )
        """ + sep + """
            INSERT INTO defaults (id, version) 
               SELECT 1, 1 
               WHERE NOT EXISTS(SELECT 1 FROM defaults WHERE id = 1);
        """ + sep + """
            INSERT INTO dictionary (key, entry) 
               SELECT 'db_version', '3'
               WHERE NOT EXISTS(SELECT 1 FROM dictionary WHERE key = 'db_version');
        """

    @staticmethod
    def update_to_2(sep):
        return """ """ + sep + """ """

    @staticmethod
    def update_to_3(sep):
        return """
        ALTER TABLE notebook ADD COLUMN topic INT NULL;
        """ + sep + """
        UPDATE notebook SET topic = 2;
        """ + sep + """
        UPDATE dictionary SET entry = '3' WHERE key = 'db_version';
        """

    @staticmethod
    def update_to_4(sep):
        return """ """ + sep + """ """