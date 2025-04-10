from game import Game
from piece import Piece

class MoveCommand:
    def __init__(self, game: Game, piece: Piece, new_pos=None, new_focus_era=None):
        self._game = game
        self._piece = piece
        self._new_pos = new_pos
        self._new_focus_era = new_focus_era