import sys
from game import Game
from memento import Caretaker

# sys.stdin = open("commands.txt")

class GameManager():
    def __init__(self, white_player_type="human", black_player_type="human"):
        self._white_player_type = white_player_type
        self._black_player_type = black_player_type
        self._game = Game(white_player_type, black_player_type)
        self._score_display = False

    def run(self):
        while True:
            self._display_game()
            if self._game_end():
                self.run()
            self._play_turn()
    
    def turn_on_score_display(self):
        self._score_display = True
    
    def get_game(self):
        return self._game
            
    def _display_game(self):
        print("---------------------------------")
        print(self._game)
        if self._score_display:
            print(self._game.get_score())
    
    def _game_end(self):
        if self._game.is_game_end():
            response = input("Play again?\n")
            if response == "yes":
                self._reset()
                return True
            else:
                sys.exit(0)
        return False
                   
    def _reset(self):
        self._game = Game(self._white_player_type, self._black_player_type)
        
    def _play_turn(self):
        self._game.play_turn()

class UndoRedo(GameManager):
    def __init__(self, game_manager: GameManager):
        self._game_manager = game_manager
        self._caretaker = Caretaker(game_manager.get_game())
    
    def run(self):
        while True:
            self._game_manager._display_game()

            response = input("undo, redo, or next\n")
            if response == "undo":
                self._caretaker.undo()
                continue
            elif response == "redo":
                self._caretaker.redo()
                continue
            elif response == "next":
                self._caretaker.backup(type="next")
                if self._game_manager._game_end():
                    self._caretaker = Caretaker(self._game_manager.get_game())
                    self.run()
                self._game_manager._play_turn()

if __name__ == "__main__":
    if len(sys.argv) == 1:
        game_manager = GameManager()
    elif len(sys.argv) == 2:
        game_manager = GameManager(white_player_type=sys.argv[1])
    elif len(sys.argv) >= 3:
        game_manager = GameManager(white_player_type=sys.argv[1], black_player_type=sys.argv[2])
        if len(sys.argv) == 5:
            if sys.argv[4] == "on":
                game_manager.turn_on_score_display()
        if len(sys.argv) >= 4:
            if sys.argv[3] == "on":
                game_manager = UndoRedo(game_manager)
    game_manager.run()
