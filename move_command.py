from game import Game
from piece import Piece

class MoveCommand:
    def __init__(self, game: Game, piece: Piece, move_direction1, move_direction2, new_focus_era):
        self._game = game
        self._piece = piece
        self._move_direction1 = move_direction1
        self._move_direction2 = move_direction2
        self._new_focus_era = new_focus_era
    
    def execute(self):
        # self._game.update()
        pass

    def __str__(self):
        return f"{self._piece}, {self._move_direction1}, {self._move_direction2}, {self._new_focus_era}"