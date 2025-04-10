from move import Move

class Board:
    def __init__(self, size: int):
        self.squares = [[([None] * size) for _ in range(size)] for _ in range(3)]

    def update(self, next_move: Move):
        pass

    def __str__(self):
        pass