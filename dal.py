import sqlite3


class DAL:
    def __init__(self):
        self.database_name = 'example.db'
        self.database_connection = sqlite3.connect(self.database_name)
        self.initalise_database()


    def initalise_database(self):
        self.create_main_table()

    def create_main_table(self):
        cursor = self.database_connection.cursor()

        cursor.execute('''CREATE TABLE if not exists todo_list
                      (date TIMESTAMP DEFAULT (datetime('now','localtime')),
                      title text,
                      priority int,
                      complete BOOLEAN NOT NULL CHECK (complete IN (0, 1)) DEFAULT (0)
                      )''')
        self.database_connection.commit()

    def get_cmdo_list(self):
        cursor = self.database_connection.cursor()
        cmdo_list = cursor.execute('SELECT rowid, date, title, priority, complete FROM todo_list')
        return cmdo_list

    def add_to_cmdo_list(self, message, priority=0):
        cursor = self.database_connection.cursor()
        print 'Added "'+message+'" to todo list with priority',priority
        cursor.execute("INSERT INTO todo_list (title, priority) VALUES (?,0 )", (message,))
        self.database_connection.commit()

    def remove_by_id(self, item_id):
        cursor = self.database_connection.cursor()
        cursor.execute("DELETE FROM todo_list WHERE rowid = ?", (item_id,))
        # Vacuum reorders the table, is this desired ?
        # User could try to do multiple deletes, maybe its better to add it on the getlist call
        # self.database_connection.execute("VACUUM")
        self.database_connection.commit()

    def mark_as_done(self, item_id):
        cursor = self.database_connection.cursor()
        cursor.execute("UPDATE todo_list SET complete = 1 WHERE rowid = ?", (item_id,))

        self.database_connection.commit()

    def dump_database(self):
        cursor = self.database_connection.cursor()
        cmdo_list = cursor.execute('SELECT * FROM todo_list')
        for row in cmdo_list:
            print row

    def close_connection(self):
        self.database_connection.close()

