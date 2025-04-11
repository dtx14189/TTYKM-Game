from piece import Piece
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
            self._squares[3][3][i] = Piece("white", f'{letter}', (3, 3, i))

    def get_neighbors(self, pos) -> list:
        neighbors = []
        directions = ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))
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

    def _get_piece(self, row, col, era):
        return self._squares[row][col][era]

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
                    piece = self._get_piece(row, j // 2, i)
                    if piece == None:
                        result.append(" ")
                    else:
                        result.append(str(piece))
            if i < 2:
                result.append("   ")
        result.append("\n")
        
