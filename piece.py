from memento import Caretaker
from move_command import MoveCommand
class Piece():
    """Purely meant for storing attributes of a piece"""
    def __init__(self, color: str, name: str, pos: tuple, board):
        self._color = color
        self._name = name
        self._pos = pos
        self._board = board
    
    def enumerate_possible_moves(self, focus, game):
        valid_moves = []
        directions = ['n', 'e', 's', 'w', 'f', 'b']
        # eras = [Era.PAST, Era.PRESENT, Era.FUTURE]
        eras = [0, 1, 2]
        caretaker = Caretaker(self._board)
        for direction1 in directions:
            if self._board.invalid_move(self, direction1):
                continue
            caretaker.backup()
            self._board.update(self, direction1)
            for direction2 in directions:
                if self._board.invalid_move(self, direction2):
                    direction2 = None
                for era in eras:
                    if era != focus:
                        new_move = MoveCommand(game, self, direction1, direction2, era)
                        valid_moves.append(new_move)
            caretaker.undo()
        return valid_moves
    
    def get_color(self):
        return self._color
    
    def get_name(self):
        return self._name
    
    def get_pos(self):
        return self._pos
    
    def set_pos(self, new_pos):
        self._pos = new_pos

    def get_era(self):
        return self._pos[2]
        
    def __str__(self):
        return f"{self._name}"
