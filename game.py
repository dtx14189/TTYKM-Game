from board import Board
class Game:
    def __init__(self):
        self.board = Board(4)
        self._turn = 1
        self._white_focus = None
        self._black_focus = None

    def __str__(self):
        print("board")
        return f"Turn: {self._turn}, Current player: "


    