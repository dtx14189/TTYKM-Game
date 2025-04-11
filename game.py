from board import Board
from enum_eras import Era
class Game():
    def __init__(self):
        self.board = Board(4)
        self._turn = 1
        self._white_focus = Era.PAST
        self._black_focus = Era.FUTURE

    def __str__(self):
        print("board")
        return f"Turn: {self._turn}, Current player: "


    