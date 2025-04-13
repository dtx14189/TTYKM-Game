class MoveCommand():
    def __init__(self, game, piece, move_direction1, move_direction2, new_focus_era):
        self._game = game
        self._piece = piece
        self._move_direction1 = move_direction1
        self._move_direction2 = move_direction2
        self._new_focus_era = new_focus_era
    
    def execute(self):
        self._game.update(self._piece, self._move_direction1, self._move_direction2, self._new_focus_era)

    def get_num_moves(self):
        if self._move_direction2:
            return 2
        if self._move_direction1:
            return 1
        return 0
    
    def directions_match(self, directions):
        return self._move_direction1 == directions[0] and self._move_direction2 == directions[1]
    
    def focus_era_match(self, focus_era):
        return self._new_focus_era == focus_era
    
    def __str__(self):
        return f"{self._piece},{self._move_direction1},{self._move_direction2},{self._new_focus_era}"