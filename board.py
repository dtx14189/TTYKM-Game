from piece import Piece
class Board():
    def __init__(self, size: int):
        self._size = size
        self._squares = [[([None] * 3) for _ in range(size)] for _ in range(size)]
        self._setup()

    def _setup(self):
        for i in range(3):
            self._squares[0][0][i] = Piece('b', f'{i+1}', (0, 0, i))
        for i in range(3):
            letter = chr(ord('A') + i)
            self._squares[3][3][i] = Piece('w', f'{letter}', (3, 3, i))

    def get_neighbors(self, pos) -> list:
        neighbors = []
        directions = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0) (0, 0, 1), (0, 0, -1))
        for direction in directions:
            new_pos = (pos[0] + direction[0], pos[1] + direction[1], pos[2] + direction[2])
            if self._valid_pos(new_pos):
                neighbors.append(new_pos)
        return neighbors

    def _valid_pos(self, pos) -> bool:
        if pos[0] < 0 or pos[0] >= self._size:
            return False
        if pos[1] < 0 or pos[1] >= self._size:
            return False
        if pos[2] < 0 or pos[2] >= 2:
            return False
        return True

    def __str__(self):
        return "test"