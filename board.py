from move_command import MoveCommand

class Board:
    def __init__(self, size: int):
        self.squares = [[([None] * size) for _ in range(size)] for _ in range(3)]
        self._size = size

    def update(self):
        pass

    def __str__(self):
        return "test"