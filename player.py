from board import Board
from move_command import MoveCommand
from enum_eras import Era
class Player():
    def __init__(self, color: str, board: Board):
        self._color = color
        if color == "black":
            self._focus = Era.FUTURE
        elif color == "white":
            self._focus = Era.PAST
        self._board: Board = board
        self._valid_moves = None

    def get_color(self):
        return self._color
    
    def get_move(self):
        pass
        # raise NotImplementedError()
    
    def change_focus_era(self, new_focus_era):
        self._focus = new_focus_era

    def _enumerate_possible_moves(self) -> dict:
        self._valid_moves = self._board.enumerate_possible_moves(self._color, self._focus)
    
    @staticmethod
    def _indent_focus(focus):
        if focus == Era.PAST:
            return ' ' * 2
        elif focus == Era.PRESENT:
            return ' ' * 14
        elif focus == Era.FUTURE:
            return ' ' * 26
        # if focus == 0:
        #     return ' ' * 2
        # elif focus == 1:
        #     return ' ' * 14
        # elif focus == 2:
        #     return ' ' * 26
        
    def __str__(self):
        return Player._indent_focus(self._focus) + self._color + "\n"
class Human(Player):
    def get_move(self):
        self._enumerate_possible_moves()
        max_moves_per_piece = self._max_moves_per_piece()
        max_moves = max(max_moves_per_piece.values())
        if max_moves == 0:
            new_focus = self._prompt_focus_era()
            return MoveCommand(None, None, None, new_focus)
        piece_to_move = self._prompt_piece_name(self, max_moves_per_piece, max_moves)
        for move_number in range(max_moves + 1):
            if move_number == 1:
                direction1 = self._prompt_move(piece_to_move, None)
            elif move_number == 2:
                direction2 = self._prompt_move(piece_to_move, direction1)
        new_focus = self._prompt_focus_era()
        return self._find_move(piece_to_move, direction1, direction2, new_focus)
        
    def _check_color(self, piece_name: str):
        if self._color == "black":
            return not piece_name.isalpha()
        elif self._color == "white":
            return piece_name.isalpha()
    
    def _max_moves_per_piece(self):
        max_moves_per_piece = {}
        for piece_name, moves in self._valid_moves:
            max_moves_per_piece[piece_name] = max(moves, key=lambda move: move.get_num_moves())
        return max_moves_per_piece

    def _prompt_piece_name(self, max_moves_per_piece: dict, max_moves: int):
        piece_names_on_board = self._board.get_piece_names()
        while True:
            piece_to_move = input("Select a copy to move\n")
            if piece_to_move not in piece_names_on_board:
                print("Not a valid copy")
                continue
            if self._check_color(piece_to_move):
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

    def _prompt_move(self, piece_to_move, prev_direction=None):
        valid_directions = ['n', 'e', 's', 'w', 'f', 'b']
        while True:
            direction = input("Select the first direction to move ['n', 'e', 's', 'w', 'f', 'b']\n")
            if direction not in valid_directions:
                print("Not a valid direction")
                continue
            moves = self._valid_moves[piece_to_move]
            for move in moves:
                if prev_direction is None:
                    if move.directions_match(1, (direction)):
                        return direction
                else:
                    if move.directions_match(2, (prev_direction, direction)):
                        return direction
            print(f"Cannot move {direction}\n")

    def _prompt_focus_era(self):
        valid_focuses = ["past", "present", "future"]
        while True:
            new_focus = input("Select the next era to focus on ['past, 'present', 'future]\n")
            if new_focus not in valid_focuses:
                print("Not a valid era")
                continue
            if self._focus == new_focus:
                print("Cannot select the current era")
                continue
            return new_focus
    
    def _find_move(self, piece_name, direction1, direction2, focus):
        for move in self._valid_moves[piece_name]:
            if move.direction_matches((direction1, direction2)) and move.focus_matches(focus):
                return move
        return None
class Random_AI(Player):
    pass

class Heuristic_AI(Player):
    pass
