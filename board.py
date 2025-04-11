from piece import Piece
from memento import Snapshot
from copy import deepcopy
class Board():
    def __init__(self, size: int):
        self._size = size
        self._squares = [[([None] * 3) for _ in range(size)] for _ in range(size)]
        self._setup()

    def _setup(self):
        for i in range(3):
            self._squares[0][0][i] = Piece("black", f'{i+1}', (0, 0, i))
        for i in range(3):
            letter = chr(ord('A') + i)
            self._squares[self._size-1][self._size-1][i] = Piece("white", f'{letter}', (self._size-1, self._size-1, i))

    def get_neighbors(self, pos) -> list:
        neighbors = []
        directions = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
        for direction in directions:
            row, col, era = pos[0] + direction[0], pos[1] + direction[1], pos[2] + direction[2]
            if self._valid_pos(row, col, era):
                neighbors.append(self._squares[row, col, era])
        return neighbors

    def _valid_pos(self, row, col, era) -> bool:
        if row < 0 or row >= self._size:
            return False
        if col < 0 or col >= self._size:
            return False
        if era < 0 or era >= 2:
            return False
        return True
    
    def save(self):
        return Snapshot(self._zip_state())
    
    def restore(self, snapshot: Snapshot):
        self._unzip_state(snapshot.get_state())

    def _zip_state(self) -> tuple:
        return (self._size, deepcopy(self._squares))
    
    def _unzip_state(self, state):
        self._size = state[0]
        self._squares = state[1]

    def __str__(self):
        result = []
        for i in range(2 * self._size + 1):
            if i % 2 == 0:
                self._print_plus_minus(result)
            else:
                self._print_board_row(result, i // 2)
        return f"{''.join(result)}"

    def _print_plus_minus(self, result: list):
        for i in range(3):
            for j in range(2 * self._size + 1):
                if j % 2 == 0:
                    result.append('+')
                else:
                    result.append('-')
            if i < 2:
                result.append("   ")
        result.append('\n')

    def _print_board_row(self, result: list, row):
        for i in range(3):
            for j in range(2 * self._size + 1):
                if j % 2 == 0:
                    result.append('|')
                else:
                    piece = self._squares(row, j // 2, i)
                    if piece == None:
                        result.append(" ")
                    else:
                        result.append(str(piece))
            if i < 2:
                result.append("   ")
        result.append("\n")
        
