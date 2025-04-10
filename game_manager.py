from game import Game
from player import Player
class GameManager:
    def __init__(self):
        self._game = Game()
        self._current_player: Player = Player(self._game, 'w')
        self._other_player: Player = Player(self._game, 'b')

    def is_game_end(self):
        return True

    def play_move(self):
        # make move
        self._swap_players()

    def _swap_players(self):
        temp = self._current_player
        self._current_player = self._other_player
        self._other_player = temp

    def __str__(self):
        print("---------------------------------")
        return f"{self._game}"