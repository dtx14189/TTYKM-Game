## from game import Game
from move_command import MoveCommand
class Player():
    def __init__(self, game, color: str):
        self._game = game
        self._color = color
        self._pieces = {}

    def get_color(self):
        return self._color
    
    def get_move(self):
        raise NotImplementedError()

    def _enumerate_possible_moves(self):
        pass
    
    
   

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
