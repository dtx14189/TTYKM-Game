import sys
from game import Game
from memento import Caretaker

# sys.stdin = open("commands.txt")
class CLI():
    def __init__(self):
        pass

    def run(self):
        if len(sys.argv) == 1:
            self._game = Game()
        elif len(sys.argv) == 2:
            self._game = Game(white_player_type=sys.argv[1])
        elif len(sys.argv) == 3:
            self._game = Game(white_player_type=sys.argv[1], black_player_type=sys.argv[2])
        self._caretaker = Caretaker(self._game)

        while True:
            self._display_game()
            self._game_end()
            self._play_turn()

    def _display_game(self):
        print("---------------------------------")
        print(self._game)
        print(self._game.get_score())

    def _game_end(self):
        if self._game.is_game_end():
            response = input("Play again?\n")
            if response == "yes":
                self.run()
            else:
                sys.exit(0)

    def _play_turn(self):
        response = input("undo, redo, or next\n")
        if response == "undo":
            self._caretaker.undo()
        elif response == "redo":
            pass
        elif response == "next":
            self._caretaker.backup()
            self._game.play_turn()

if __name__ == "__main__":
    CLI().run()