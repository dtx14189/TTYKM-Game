from board import Board
from move_command import MoveCommand
from enum_eras import Era
class Player():
    def __init__(self, color: str, board: Board):
        self._color = color
        if color == "black":
            self._focus = Era.FUTURE
        elif color == "white":
            self._focus = Era.PAST
        self._board = board

    def get_color(self):
        return self._color
    
    def get_move(self):
        raise NotImplementedError()
    
    def change_focus_era(self, new_focus_era):
        self._focus = new_focus_era

    def _enumerate_possible_moves(self):
        return self._board.valid_moves(self._color)
    
    @staticmethod
    def _indent_focus(focus):
        if focus == Era.PAST:
            return ' ' * 2
        elif focus == Era.PRESENT:
            return ' ' * 14
        elif focus == Era.FUTURE:
            return ' ' * 26
        
    def __str__(self):
        return Player._indent_focus(self._focus) + self._color + "\n"
   
class Human(Player):
    def get_move(self):
        piece_to_move = input("Select a copy to move\n")
        
        # if piece_to_move._valid_moves

    def _is_valid_move(self):
        pass

class Random_AI(Player):
    pass

class Heuristic_AI(Player):
    pass
