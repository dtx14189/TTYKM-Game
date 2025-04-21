class MoveCommand():
    """Represent a move in ttykm."""

    def __init__(self, game, piece, move_direction1, move_direction2, new_focus_era):
        """Initailize a move, which stores all the input arguments."""
        self._game = game
        self._piece = piece
        self._move_direction1 = move_direction1
        self._move_direction2 = move_direction2
        self._new_focus_era = new_focus_era
    
    def generate_version(self, game):
        """Generate a deep copy of the move that matches the inputted game."""
        if self._piece is not None: # Move(A, west, north, future)
            piece_consistent_with_game = game.search_piece(self._piece.get_name())
        else: # Move(None, None, None, future)
            piece_consistent_with_game = None
        
        return MoveCommand(game, piece_consistent_with_game, self._move_direction1, self._move_direction2, self._new_focus_era)
    
    def execute(self):
        """Execute the move on the game."""
        self._game.update(self._piece, self._move_direction1, self._move_direction2, self._new_focus_era)

    def get_num_moves(self):
        """Get number of non-None move directions."""
        if self._move_direction2:
            return 2
        if self._move_direction1:
            return 1
        return 0
    
    def directions_match(self, directions, move_number):
        """Check if inputted directions match with move."""
        if move_number == 1:
            return self._move_direction1 == directions[0]
        else: # move_number = 0 or 2
            return self._move_direction1 == directions[0] and self._move_direction2 == directions[1]
    
    def focus_era_match(self, focus_era):
        """Check if focus_eras match."""
        return self._new_focus_era == focus_era
    
    def __eq__(self, other: 'MoveCommand'):
        return (
            self._piece == other._piece and 
            self._move_direction1 == other._move_direction1 and 
            self._move_direction2 == other._move_direction2 and 
            self._new_focus_era == other._new_focus_era
        )
    
    def __str__(self):
        if self._new_focus_era == 0:
            new_focus_era_str = "past"
        elif self._new_focus_era == 1:
            new_focus_era_str = "present"
        elif self._new_focus_era == 2:
            new_focus_era_str = "future"
        return f"{self._piece},{self._move_direction1},{self._move_direction2},{new_focus_era_str}"