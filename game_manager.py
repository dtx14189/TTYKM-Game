from move_command import MoveCommand
from game import Game
from player import Player
from memento import Snapshot, Caretaker
from copy import deepcopy
class GameManager():
    def __init__(self):
        self._game = Game()
        self._current_player: Player = Player(self._game, 'w')
        self._other_player: Player = Player(self._game, 'b')
        self._move: MoveCommand = None

    def is_game_end(self):
        return True

    def play_turn(self):
        self._move = self._current_player.get_move()
        self._move.execute()
        print(self._move)
        self._swap_players()

    def _swap_players(self):
        temp = self._current_player
        self._current_player = self._other_player
        self._other_player = temp

    def save(self):
        return Snapshot(self._zip_state())
    
    def restore(self, snapshot: Snapshot):
        self._unzip_state(snapshot.get_state())

    def _zip_state(self) -> tuple:
        return (deepcopy(self._game), deepcopy(self._current_player), deepcopy(self._other_player), deepcopy(self._move))
    
    def _unzip_state(self, state):
        self._game = state[0]
        self._current_player = state[1]
        self._other_player = state[2]
        self._move = state[3]

    def __str__(self):
        print("---------------------------------")
        return f"{self._game}"