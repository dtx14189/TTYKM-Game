from move_command import MoveCommand
from game import Game
from memento import Snapshot
from copy import deepcopy
class GameManager():
    def __init__(self):
        self._game = Game()
        self._move: MoveCommand = None

    def is_game_end(self):
        return self._game.is_game_end()

    def play_turn(self):
        self._move = self._game.get_move()
        self._move.execute()
        print(f"Selected move: {self._move}")

    def save(self):
        return Snapshot(self._zip_state())
    
    def restore(self, snapshot: Snapshot):
        self._unzip_state(snapshot.get_state())

    def _zip_state(self) -> tuple:
        return (deepcopy(self._game), deepcopy(self._move))
    
    def _unzip_state(self, state):
        self._game = state[0]
        self._move = state[1]

    def __str__(self):
        return f"---------------------------------\n{self._game}"