import sys

from birtodo.app import Todo
from birtodo.database import Database
from birtodo.exceptions import WrongCommand


def main() -> None:
    """The core of this CLI.

    Raises
    ------
    WrongCommand
        If the wrong command was given.
    """
    db = Database('data/todos.db')
    todo = Todo(db)
    first_arg = sys.argv[1]

    try:
        command = getattr(todo, first_arg)
    except AttributeError:
        raise WrongCommand(first_arg)

    if not (content := ' '.join(sys.argv[2:])):
        return command()

    return command(content)


if __name__ == '__main__':
    main()
