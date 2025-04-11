from board import Board
from enum_eras import Era
class Game():
    def __init__(self):
        self._board = Board(4)
        self._white_focus = Era.PAST
        self._black_focus = Era.FUTURE

    @staticmethod
    def _indent_focus(focus):
        if focus == Era.PAST:
            return ' ' * 2
        elif focus == Era.PRESENT:
            return ' ' * 14
        elif focus == Era.FUTURE:
            return ' ' * 26
        
    def __str__(self):
        black_focus = Game._indent_focus(self._black_focus) + "black\n"
        white_focus = Game._indent_focus(self._white_focus) + "white\n"
        result = black_focus + str(self._board) + white_focus
        return result



    