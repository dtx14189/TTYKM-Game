from board import Board
from player import Player, Human, Random_AI, Heuristic_AI
from memento import Snapshot
class Game():
    def __init__(self, setup=True, white_player_type="human", black_player_type="human"):
        if not setup:
            return 
        self._current_player = self._create_player("white", white_player_type)
        self._other_player: Player = self._create_player("black", black_player_type)
        self._setup_players()
        # self._current_player: Player = Human("black", self)
        # self._other_player: Player = Human("white", self)
        self._board = Board(4, white_player=self._current_player, black_player=self._other_player)
        self._turn = 1

    def _create_player(self, color: str, type: str):
        if type == "human":
            return Human(color)
        elif type == "random":
            return Random_AI(color)
        elif type == "heuristic":
            return Heuristic_AI(color)
        
    def _setup_players(self):
        self._current_player.set_opponent(self._other_player)
        self._other_player.set_opponent(self._current_player)
        self._current_player.assign_game(self)
        self._other_player.assign_game(self)

    def update(self, piece, move_direction1, move_direction2, new_focus_era):
        self._board.update(piece, move_direction1)
        self._board.update(piece, move_direction2)
        self._current_player.change_focus_era(new_focus_era)
        self._swap_players()
        self._turn += 1
    
    def get_move(self):
        if self._turn == 15:
            pass
        return self._current_player.get_move()
    
    def get_score(self):
        if self._current_player.get_color() == "white":
            white_heuristics = self._current_player.get_heuristics()
            black_heuristics = self._other_player.get_heuristics()
        elif self._current_player.get_color() == "black":
            white_heuristics = self._other_player.get_heuristics()
            black_heuristics = self._current_player.get_heuristics()
        return f"{white_heuristics}\n{black_heuristics}"

    def is_game_end(self):
        lost = self._current_player.has_lost()
        if lost:
            if self._current_player.get_color() == "white":
                print("black has won")
            elif self._current_player.get_color() == "black":
                print("white has won")
        return lost
    
    def _swap_players(self):
        temp = self._current_player
        self._current_player = self._other_player
        self._other_player = temp
        
    def __str__(self):
        if self._current_player.get_color() == "black":
            black_focus = str(self._current_player)
            white_focus = str(self._other_player)
        elif self._current_player.get_color() == "white":
            black_focus = str(self._other_player)
            white_focus = str(self._current_player)
        turn_player = f"Turn: {self._turn}, Current player: {self._current_player.get_color()}"
        result = black_focus + str(self._board) + white_focus + turn_player
        return result
    
    def _copy(self):
        copy_game = Game(setup=False)
        copy_game._board = self._board.copy()
        if self._current_player.get_color() == "white":
            copy_game._current_player = copy_game._board.get_player("white")
            copy_game._other_player = copy_game._board.get_player("black")
        elif self._current_player.get_color() == "black":
            copy_game._current_player = copy_game._board.get_player("black")
            copy_game._other_player = copy_game._board.get_player("white")
        copy_game._setup_players()
        return copy_game
    
    def save(self):
        copy_game = self._copy()
        return Snapshot(copy_game._zip_state())
    
    def restore(self, snapshot: Snapshot):
        self._unzip_state(snapshot.get_state())

    def _zip_state(self) -> tuple:
        return (self._current_player, self._other_player, self._board)
    
    def _unzip_state(self, state):
        self._current_player = state[0]
        self._other_player = state[1]
        self._board = state[2]



    