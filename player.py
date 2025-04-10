from game import Game
from move_command import MoveCommand
class Player:
    def __init__(self, game: Game, color: str):
        self._game = game
        self._color = color
        self._pieces = []

    def _enumerate_possible_moves(self):
        pass

    def get_move(self):
        raise NotImplementedError()

class Human(Player):
    def get_move(self):
        pass

    def _is_valid_move(self):
        pass

class Random_AI(Player):
    pass

class Heuristic_AI(Player):
    pass
