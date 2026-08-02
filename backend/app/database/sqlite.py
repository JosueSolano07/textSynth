from sqlite3 import connect


class Database:

    def __init__(self, path: str):

        self.path = path

        self.connection = None


    def connect(self):

        if self.connection is None:
            self.connection = connect(self.path)

        return self.connection


    def close(self):

        if self.connection:
            self.connection.close()
            self.connection = None