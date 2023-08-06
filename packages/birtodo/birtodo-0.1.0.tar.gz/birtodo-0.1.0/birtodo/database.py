import sqlite3

from birtodo.exceptions import SetupScriptError


class Database:
    def __init__(self, db_path: str = None) -> None:
        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()
        try:
            self.cursor.execute('SELECT 1 FROM todos;')
        except sqlite3.OperationalError:  # The table does not exist yet.
            self.setup()

    def setup(self) -> None:
        """The method for setting up the database tables."""
        with open('data/schema.sql', 'r') as fp:
            query = fp.read()

        try:
            self.cursor.execute(query)
        except sqlite3.OperationalError as e:
            raise SetupScriptError('There was a problem on executing the SQL script.') from e
