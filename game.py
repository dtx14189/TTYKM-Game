from board import Board
from enum_eras import Era
from player import Player
class Game():
    def __init__(self):
        self._current_player: Player = Player(self, "white")
        self._other_player: Player = Player(self, "black")
        self._turn = 1
        self._board = Board(4)
        self._white_focus = Era.PAST
        self._black_focus = Era.FUTURE

    def update(self, piece, move_direction1, move_direction2, new_focus_era):
        pass
            

    @staticmethod 
    def direction_to_shift(pos, direction):
        row, col, era = pos[0], pos[1], pos[2]
        if direction == 'n':
            return (row - 1, col, era)
        elif direction == 'e':
            return (row, col + 1, era)
        elif direction == 's':
            return (row + 1, col, era)
        elif direction == 'w':
            return (row, col - 1, era)
        elif direction == 'f':
            return (row, col, era + 1)
        elif direction == 'b':
            return (row, col, era - 1)
    
    def _swap_players(self):
        temp = self._current_player
        self._current_player = self._other_player
        self._other_player = temp

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
        turn_player = f"Turn: {self._turn}, Current player: {self._current_player.get_color()}\n"
        result = black_focus + str(self._board) + white_focus + turn_player
        return result



    