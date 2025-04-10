from board import Board

class Player:
    def __init__(self, board: Board):
        self._color = None
        self._pieces = []
        self._board = board

    def _enumerate_possible_moves(self):
        pass

    def get_move(self):
        raise NotImplementedError()

class Human(Player):
    def get_move(self):
        pass

class Random_AI(Player):
    pass

class Heuristic_AI(Player):
    pass
