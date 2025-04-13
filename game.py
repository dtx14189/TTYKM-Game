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
    
    def play_turn(self):
        if self._turn == 2:
            pass
        move = self._current_player.get_move()
        move.execute()
        print(f"Selected move: {move}")
    
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
        
    def search_piece(self, piece_name: str):
        pieces = self._current_player.get_pieces() + self._other_player.get_pieces()
        for piece in pieces:
            if piece.get_name() == piece_name:
                return piece
        return None

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

    def _get_players_from_board(self, board: Board):
        if self._current_player.get_color() == "white":
            return board.get_player("white"), board.get_player("black")
        elif self._current_player.get_color() == "black":
            return board.get_player("black"), board.get_player("white")
        
    def copy(self):
        copy_game = Game(setup=False)
        copy_game._turn = self._turn
        copy_game._board = self._board.copy()
        copy_game._current_player, copy_game._other_player = self._get_players_from_board(copy_game._board)
        copy_game._setup_players()
        return copy_game

    def save(self):
        copy_board = self._board.copy()
        copy_current_player, copy_other_player = self._get_players_from_board(copy_board)

        copy_current_player._opponent = copy_other_player
        copy_other_player._opponent = copy_current_player

        copy_current_player.assign_game(self)
        copy_other_player.assign_game(self)

        state = (self._turn, copy_board, copy_current_player, copy_other_player)
        return Snapshot(state)

    def restore(self, snapshot: Snapshot):
        state = snapshot.get_state()
        self._turn = state[0]
        self._board = state[1]
        self._current_player = state[2]
        self._other_player = state[3]

    