import sys
from game_manager import GameManager
class CLI():
    def __init__(self):
        self._game_manager = GameManager()

    def run(self):
        while True:
            self._display_game()
            self._game_end()
            self._play_turn()

    def _display_game(self):
        print(self._game_manager)

    def _game_end(self):
        if self._game_manager.is_game_end():
            response = input("Play again?\n")
            if response == "yes":
                self.run()
            else:
                sys.exit(0)

    def _play_turn(self):
        self._game_manager.play_turn()

if __name__ == "__main__":
    CLI().run()