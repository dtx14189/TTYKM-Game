class MoveCommand():
    def __init__(self, player, game, piece, move_direction1, move_direction2, new_focus_era):
        self._game = game
        self._player = player
        self._piece = piece
        self._move_direction1 = move_direction1
        self._move_direction2 = move_direction2
        self._new_focus_era = new_focus_era
    
    def execute(self):
        self._game.update(self._player, self._piece, self._move_direction1, self._move_direction2, self._new_focus_era)

    def __str__(self):
        return f"{self._piece}, {self._move_direction1}, {self._move_direction2}, {self._new_focus_era}"