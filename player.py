from piece import Piece
from move_command import MoveCommand
from enum_eras import Era
class Player():
    def __init__(self, color: str, game, focus=None, supply=4):
        self._color = color
        if focus is None:
            if color == "black":
                # self._focus = Era.FUTURE
                self._focus = 2
            elif color == "white":
                # self._focus = Era.PAST
                self._focus = 0
        else:
            self._focus = focus
        self._game = game
        self._pieces: list[Piece] = []
        self._supply = supply
        self._valid_moves = None

    def copy(self):
        player_copy = Player(self._color, self._game, self._focus, self._supply)
        return player_copy

    def has_lost(self):
        eras = set()
        for piece in self._pieces:
            eras.add(piece.get_era())
        return (len(eras) == 1)
    
    def get_color(self):
        return self._color
    
    def get_move(self):
        pass
        # raise NotImplementedError()
    
    def change_focus_era(self, new_focus_era):
        self._focus = new_focus_era

    def get_piece_names(self):
        piece_names = []
        for piece in self._pieces:
            piece_names.append(piece.get_name())
        return piece_names
    
    def add_piece(self, piece: Piece):
        self._pieces.append(piece)

    def remove_piece(self, piece: Piece):
        self._pieces.remove(piece)

    def decrement_supply(self):
        self._supply -= 1
    
    def get_supply(self):
        return self._supply
    
    def _enumerate_possible_moves(self) -> dict:
        self._valid_moves = {}
        for piece in self._pieces:
            if piece.get_era() == self._focus:
                self._valid_moves[piece.get_name()] = piece.enumerate_possible_moves(self._focus, self._game)
            else:
                self._valid_moves[piece.get_name()] = None
    
    @staticmethod
    def _indent_focus(focus):
        # if focus == Era.PAST:
        #     return ' ' * 2
        # elif focus == Era.PRESENT:
        #     return ' ' * 14
        # elif focus == Era.FUTURE:
        #     return ' ' * 26
        if focus == 0:
            return ' ' * 2
        elif focus == 1:
            return ' ' * 14
        elif focus == 2:
            return ' ' * 26
        
    def __str__(self):
        return Player._indent_focus(self._focus) + self._color + "\n"
class Human(Player):
    def get_move(self):
        self._enumerate_possible_moves()
        max_moves_per_piece = self._max_moves_per_piece()
        max_moves = max(max_moves_per_piece.values())
        if max_moves == 0:
            new_focus = self._prompt_focus_era()
            return MoveCommand(self._game, None, None, None, new_focus)
        piece_to_move = self._prompt_piece_name(max_moves_per_piece, max_moves)
        direction1, direction2 = None, None
        for move_number in range(1, max_moves + 1):
            if move_number == 1:
                direction1 = self._prompt_move(piece_to_move)
            elif move_number == 2:
                direction2 = self._prompt_move(piece_to_move, direction1)
        new_focus = self._prompt_focus_era()
        temp_move = self._find_move(piece_to_move, direction1, direction2, new_focus)
        return temp_move

    def _check_color(self, piece_name: str):
        if self._color == "black":
            return not piece_name.isalpha()
        elif self._color == "white":
            return piece_name.isalpha()
    
    def _max_moves_per_piece(self):
        max_moves_per_piece = {}
        for piece_name, moves in self._valid_moves.items():
            if moves is None or len(moves) == 0:
                max_moves_per_piece[piece_name] = 0
            else:
                max_moves_per_piece[piece_name] = max(move.get_num_moves() for move in moves)
        return max_moves_per_piece

    def _prompt_piece_name(self, max_moves_per_piece: dict, max_moves: int):
        piece_names_on_board = self._game.get_piece_names()
        while True:
            piece_to_move = input("Select a copy to move\n")
            if piece_to_move not in piece_names_on_board:
                print("Not a valid copy")
                continue
            if not self._check_color(piece_to_move):
                print("That is not your copy")
                continue
            if self._valid_moves[piece_to_move] is None:
                print("Cannot select a copy from an inactive era")
                continue
            if len(self._valid_moves[piece_to_move]) == 0:
                print("That copy cannot move")
                continue
            if max_moves_per_piece[piece_to_move] < max_moves:
                print("Not a valid copy")
                continue
            return piece_to_move
    
    def _prompt_move(self, piece_to_move, other_direction=None):
        valid_directions = ['n', 'e', 's', 'w', 'f', 'b']
        if other_direction is None:
            move_number = 1
            move_number_str = "first"
        else:
            move_number = 2
            move_number_str = "second"
            
        while True:
            direction = input(f"Select the {move_number_str} direction to move ['n', 'e', 's', 'w', 'f', 'b']\n")
            if direction not in valid_directions:
                print("Not a valid direction")
                continue
            moves = self._valid_moves[piece_to_move]
            for move in moves:
                if move_number == 1:
                    if move.directions_match((direction, other_direction)):
                        return direction
                elif move_number == 2:
                    if move.directions_match((other_direction, direction)):
                        return direction
            print(f"Cannot move {direction}")

    def _prompt_focus_era(self):
        focus_to_int = {"past": 0, "present": 1, "future": 2}
        while True:
            new_focus = input("Select the next era to focus on ['past, 'present', 'future]\n")
            if new_focus not in focus_to_int:
                print("Not a valid era")
                continue
            if self._focus == focus_to_int[new_focus]:
                print("Cannot select the current era")
                continue
            return focus_to_int[new_focus]
    
    def _find_move(self, piece_name, direction1, direction2, focus):
        for move in self._valid_moves[piece_name]:
            if move.directions_match((direction1, direction2)) and move.focus_era_match(focus):
                return move
        return None
class Random_AI(Player):
    pass

class Heuristic_AI(Player):
    pass
