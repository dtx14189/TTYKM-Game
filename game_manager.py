from move_command import MoveCommand
from game import Game
from player import Player

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

    def __str__(self):
        print("---------------------------------")
        return f"{self._game}"