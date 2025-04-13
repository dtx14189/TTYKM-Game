class MoveCommand():
    def __init__(self, game, piece, move_direction1, move_direction2, new_focus_era):
        self._game = game
        self._piece = piece
        self._move_direction1 = move_direction1
        self._move_direction2 = move_direction2
        self._new_focus_era = new_focus_era
    
    def copy_move(self, game):
        piece_consistent_with_game = game.search_piece(self._piece.get_name())
        return MoveCommand(game, piece_consistent_with_game, self._move_direction1, self._move_direction2, self._new_focus_era)
    
    def execute(self):
        self._game.update(self._piece, self._move_direction1, self._move_direction2, self._new_focus_era)

    def get_num_moves(self):
        if self._move_direction2:
            return 2
        if self._move_direction1:
            return 1
        return 0
    
    def directions_match(self, directions, move_number):
        if move_number == 1:
            return self._move_direction1 == directions[0]
        else: # move_number = 0 or 2
            return self._move_direction1 == directions[0] and self._move_direction2 == directions[1]
    
    def focus_era_match(self, focus_era):
        return self._new_focus_era == focus_era
    
    def __eq__(self, other: 'MoveCommand'):
        return (
            self._piece == other._piece and 
            self._move_direction1 == other._move_direction1 and 
            self._move_direction2 == other._move_direction2 and 
            self._new_focus_era == other._new_focus_era
        )
    
    def __str__(self):
        return f"{self._piece},{self._move_direction1},{self._move_direction2},{self._new_focus_era}"