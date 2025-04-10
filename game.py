from board import Board
class Game:
    def __init__(self):
        self._current_player = None
        self._other_player = None
        self.board = Board()
        self._turn = 1
        self._white_focus = None
        self._black_focus = None


    