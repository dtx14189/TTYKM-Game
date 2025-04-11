class Piece():
    def __init__(self, color: str, name: str, pos: tuple):
        self._color = color
        self._name = name
        self._pos = pos
    
    def valid_moves(self, board):
        pass

    def __str__(self):
        return f"{self._name}"