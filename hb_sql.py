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
                archived INT NOT NULL
            );
        """ + sep + """
            CREATE TABLE IF NOT EXISTS defaults (
                id INT PRIMARY KEY NOT NULL,
                version INT NOT NULL
            );
        """ + sep + """
            INSERT INTO defaults (id, version) 
               SELECT 1, 1 
               WHERE NOT EXISTS(SELECT 1 FROM defaults WHERE id = 1);
        """