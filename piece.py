from board import Board
class Piece():
    def __init__(self, color, name, pos):
        self._color = color
        self._name = name
        self._pos = pos
    
    def valid_moves(self, board: Board):
        pass