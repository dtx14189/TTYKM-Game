from move_command import MoveCommand
class Piece():
    """Represnet a piece."""

    def __init__(self, color: str, name: str, pos: tuple):
        """Initialize a piece with the given color, name, and pos."""
        self._color = color
        self._name = name
        self._pos = pos
    
    def copy(self):
        """Generate a deep copy of the piece."""
        return Piece(self._color, self._name, self._pos)

    def assign_board(self, board):
        """Assign the piece to a board."""
        self._board = board

    def enumerate_possible_moves(self, focus, game):
        """Enumerate all possible moves for a piece, given a focus."""
        valid_moves = []
        directions = ['n', 'e', 's', 'w', 'f', 'b']
        eras = [0, 1, 2]
        for direction1 in directions:
            if self._board.invalid_move(self, direction1):
                continue
            board_copy = self._board.copy()
            piece_copy = board_copy.get_piece_at_pos(self._pos)
            board_copy.update(piece_copy, direction1)
            for direction2 in directions:
                if board_copy.invalid_move(piece_copy, direction2):
                    direction2 = None
                for era in eras:
                    if era != focus:
                        new_move = MoveCommand(game, self, direction1, direction2, era)
                        if new_move not in valid_moves:
                            valid_moves.append(new_move)
        return valid_moves
    
    def get_color(self):
        """Get color of piece."""
        return self._color
    
    def get_name(self):
        """Get name of piece."""
        return self._name
    
    def get_pos(self):
        """Get pos of piece."""
        return self._pos
    
    def set_pos(self, new_pos):
        """Set pos of piece."""
        self._pos = new_pos

    def get_era(self):
        """Get era of piece."""
        return self._pos[2]
     
    def __str__(self):
        return f"{self._name}"
