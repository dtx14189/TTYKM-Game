from board import Board
from player import Player, Human
class Game():
    def __init__(self):
        self._current_player: Player = Human("white", self)
        self._other_player: Player = Human("black", self)
        self._board = Board(4, self._current_player, self._other_player)
        self._turn = 1

    def update(self, piece, move_direction1, move_direction2, new_focus_era):
        self._board.update(piece, move_direction1)
        self._board.update(piece, move_direction2)
        self._current_player.change_focus_era(new_focus_era)
        self._swap_players()
    
    def get_move(self):
        return self._current_player.get_move()

    def get_piece_names(self):
        return self._current_player.get_piece_names() + self._other_player.get_piece_names()
    
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



    