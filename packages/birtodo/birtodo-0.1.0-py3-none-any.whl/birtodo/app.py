from datetime import datetime
from pathlib import Path
from typing import NamedTuple

from birtodo.database import Database
from birtodo.exceptions import NoTodo


class EntryBody(NamedTuple):
    id: int
    content: str


class TodoBody(EntryBody):
    date_added: datetime


def separate_number(argument: str) -> EntryBody:
    """Used to separate number and content from the given arguments.

    Parameters
    ----------
    argument : str
        sys.argv aka arguments passed into command-line.

    Returns
    -------
    namedtuple
        The entry body namedtuple.
    """
    arr = argument.split()
    return EntryBody(arr[0], ' '.join(arr[1:]))


class Todo:
    def __init__(self, database_cls: Database) -> None:
        self.connection = database_cls.connection
        self.cursor = database_cls.cursor

    def add(self, content: str) -> None:
        """Add a to-do into your list.

        Parameters
        ----------
        content : str
            The content of to-do.
        """
        query = 'INSERT INTO todos(content, date_added) VALUES(?, ?);'
        values = (content, datetime.now())

        self.cursor.execute(query, values)
        self.connection.commit()

        added = self.cursor.execute(
            'SELECT id, content FROM todos WHERE content = ?;', (content,)
        ).fetchone()
        print(f'✅ Added todo:\n{added[0]}. {added[1]}')

    def remove(self, todo_id: int) -> None:
        """Remove a specific to-do from your list.

        Parameters
        ----------
        todo_id : int
            The ID of a to-do to get removed.
        """
        todo = self.cursor.execute(
            'SELECT * FROM todos WHERE id = ?;', todo_id
        ).fetchone()

        self.cursor.execute('DELETE FROM todos WHERE id = ?;', todo_id)
        self.connection.commit()

        print(f'✅ Removed todo:\n{todo[0]}. {todo[1]}')

    def edit(self, content: str) -> None:
        """Edit a specific to-do inside your list.

        Parameters
        ----------
        content : str
            To-do content with its ID specified at the beginning.
        """
        separated = separate_number(content)
        todo_id = separated.id
        cnt = separated.content

        todo = self.cursor.execute(
            'SELECT id, content FROM todos WHERE id = ?', todo_id
        ).fetchone()

        self.cursor.execute('UPDATE todos SET content = ? WHERE id = ?', (cnt, todo_id))
        self.connection.commit()

        print(f'✅ Edited your to-do:\n{todo_id}. {todo[1]}\n\t↓\n{todo_id}. {cnt}')

    def info(self, todo_id: int) -> None:
        """Get information about a specific to-do: id, content and added date.

        Parameters
        ----------
        todo_id : int
            The ID of a to-do to get info for.

        Raises
        ------
        NoTodo
            If no to-do with given ID was found.
        """
        row = self.cursor.execute('SELECT * FROM todos WHERE id = ?;', todo_id).fetchone()
        if row is None:  # None == does not exist in the DB.
            raise NoTodo(todo_id)

        data = TodoBody(*row)
        print(f'ID: {data.id}\nContent: {data.content}\nDate Added: {data.date_added}')

    def show(self) -> None:
        """See your to-do list.

        Raises
        ------
        RuntimeError
            If you don't have any to-dos yet.
        """
        if not (rows := self.cursor.execute('SELECT * FROM todos;').fetchall()):
            raise RuntimeError('No to-dos were found in your list :(')

        cnt = len(rows)
        todo_list = '\n'.join(f'{e[0]}. {e[1]}' for e in rows)

        print(f'✅ Your current to-do list ({cnt} entr{"y" if cnt == 1 else "ies"}):\n{todo_list}')

    def export(self) -> None:
        """Export your to-do list into a .txt file!"""
        rows = self.cursor.execute('SELECT * FROM todos;').fetchall()
        todo_list = '\n'.join(f'{e[0]}. {e[1]}' for e in rows)

        path = Path().absolute() / 'todos.txt'
        with open(path, 'w') as f:
            f.write(todo_list)

        print('✅ Successfully exported all your to-dos! Check your Desktop folder.')
