
class TodoError(Exception):
    """The base exception class for all following child-errors."""


class WrongCommand(TodoError):
    """Raised when there was no such command in the CLI."""

    def __init__(self, command: str) -> None:
        super().__init__(f'There is no command "{command}".')


class NoTodo(TodoError):
    """Raised when there was no to-do for a given id."""

    def __init__(self, todo_id: int) -> None:
        super().__init__(f'Could not find the to-do with this id: {todo_id}.')


class SetupScriptError(TodoError):
    """Raised when the application gets failed on executing the SQL setup script."""
