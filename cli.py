import sys
from game import Game
from memento import Caretaker

# sys.stdin = open("commands.txt")
class CLI():
    def __init__(self):
        self._undo_redo = False
        self._score_display = False

    def run(self):
        if len(sys.argv) == 1:
            self._game = Game()
        elif len(sys.argv) == 2:
            self._game = Game(white_player_type=sys.argv[1])
        elif len(sys.argv) >= 3:
            self._game = Game(white_player_type=sys.argv[1], black_player_type=sys.argv[2])
            if len(sys.argv) >= 4:
                if sys.argv[3] == "on":
                    self._undo_redo = True
            if len(sys.argv) == 5:
                if sys.argv[4] == "on":
                    self._score_display = True
        if self._undo_redo:
            self._caretaker = Caretaker(self._game)

        while True:
            self._display_game()
            self._game_end()
            self._play_turn()

    def _display_game(self):
        print("---------------------------------")
        print(self._game)
        if self._score_display:
            print(self._game.get_score())

    def _game_end(self):
        if self._game.is_game_end():
            response = input("Play again?\n")
            if response == "yes":
                self.run()
            else:
                sys.exit(0)

    def _play_turn(self):
        if self._undo_redo:
            response = input("undo, redo, or next\n")
            if response == "undo":
                self._caretaker.undo()
            elif response == "redo":
                self._caretaker.redo()
            elif response == "next":
                self._caretaker.backup(type="next")
                self._game.play_turn()
        else:
            self._game.play_turn()

if __name__ == "__main__":
    CLI().run()