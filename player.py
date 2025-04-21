import random
from piece import Piece
from move_command import MoveCommand

class Player():
    """Abstract representation of a player in a game."""

    def __init__(self, color: str, focus=None, supply=4):
        """Initialize a player with inputted color, focus, and supply.
        A player also stores a list of their pieces."""
        self._color = color
        if focus is None:
            if color == "black":
                self._focus = 2
            elif color == "white":
                self._focus = 0
        else:
            self._focus = focus
        self._pieces: list[Piece] = []
        self._supply = supply

    def get_pieces(self):
        """Get the player's pieces."""
        return self._pieces
    
    def has_lost(self):
        """Check if the player has lost according to the rules of ttykm."""
        eras = set()
        for piece in self._pieces:
            eras.add(piece.get_era())
        return (len(eras) == 1)

    def assign_game(self, game):
        """Assign a game to the player."""
        self._game = game
        
    def set_opponent(self, opponent: 'Player'):
        """Set the player's opponent."""
        self._opponent = opponent
    
    def get_color(self):
        """Get the color of the player."""
        return self._color
    
    def change_focus_era(self, new_focus_era):
        """Change focus era to new_focus_era."""
        self._focus = new_focus_era
    
    def add_piece(self, piece: Piece):
        """Add piece to list of pieces."""
        self._pieces.append(piece)

    def remove_piece(self, piece: Piece):
        """Remove piece from list of pieces."""
        self._pieces.remove(piece)

    def decrement_supply(self):
        """Decrement supply by 1."""
        self._supply -= 1
    
    def get_supply(self):
        """Get a player's supply."""
        return self._supply
    
    def get_heuristics(self):
        """Compute desired heurstics about a player's position in a game."""
        result = []
        result.append(f"{self._color}'s score:")
        result.append(f" {self._compute_era_prescence()} eras,")
        result.append(f" {self._compute_piece_advantage()} advantage,")
        result.append(f" {self._compute_supply()} supply,")
        result.append(f" {self._compute_centrality()} centrality,")
        result.append(f" {self._compute_focus()} in focus")
        return ''.join(result)
    
    def _get_move(self):
        self._enumerate_possible_moves()

    def _enumerate_possible_moves(self):
        self._valid_moves: dict[str, list[MoveCommand]] = {}
        for piece in self._pieces:
            if piece.get_era() == self._focus:
                self._valid_moves[piece.get_name()] = piece.enumerate_possible_moves(self._focus, self._game)
            else:
                self._valid_moves[piece.get_name()] = []
        
        self._valid_moves["none"] = []
        eras = [0, 1, 2]
        for era in eras:
            if self._focus != era:
                self._valid_moves["none"].append(MoveCommand(self._game, None, None, None, era))
        self._filter_valid_moves()

    def _filter_valid_moves(self):
        self._new_valid_moves: dict[str, list[MoveCommand]] = {}
        max_moves_per_piece = self._max_moves_per_piece()
        self._move_len = max(max_moves_per_piece.values()) 
        for piece_name, moves in self._valid_moves.items():
            self._new_valid_moves[piece_name] = []
            for move in moves:
                if move.get_num_moves() == self._move_len:
                    self._new_valid_moves[piece_name].append(move)
        self._valid_moves = self._new_valid_moves

    def _max_moves_per_piece(self):
        max_moves_per_piece = {}
        for piece_name, moves in self._valid_moves.items():
            if len(moves) == 0:
                max_moves_per_piece[piece_name] = 0
            else:
                max_moves_per_piece[piece_name] = max(move.get_num_moves() for move in moves)
        return max_moves_per_piece


    def _list_valid_moves(self):
        list_valid_moves = []
        for moves in self._valid_moves.values():
            list_valid_moves += moves
        return list_valid_moves
    
    def _get_piece_names(self):
        piece_names = []
        for piece in self._pieces:
            piece_names.append(piece.get_name())
        return piece_names
    
    def _copy_pieces_from_other(self, other: 'Player'):
        for piece in other._pieces:
            self._pieces.append(piece.copy())
    
    def _heuristic_function(self):
        if self._opponent.has_lost():
            return 9999
        weight_era_prescence = 3
        weight_piece_advantage = 2
        weight_supply = 1
        weight_centrality = 4
        weight_focus = 1
        return (
            weight_era_prescence * self._compute_era_prescence() +
            weight_piece_advantage * self._compute_piece_advantage() +
            weight_supply * self._compute_supply() +
            weight_centrality * self._compute_centrality() +
            weight_focus * self._compute_focus()
        )

    def _compute_era_prescence(self):
        eras = set()
        for piece in self._pieces:
            eras.add(piece.get_era())
        return len(eras)
    
    def _compute_piece_advantage(self):
        return len(self._pieces) - len(self._opponent._pieces)

    def _compute_supply(self):
        return self._supply
    
    def _compute_centrality(self):
        num_central = 0
        for piece in self._pieces:
            num_central += Heuristic_AI._is_central(piece.get_pos(), 4)
        return num_central
    
    @staticmethod
    def _is_central(pos, size):
        return (pos[0] > 0 and pos[0] < size-1) and (pos[1] > 0 and pos[1] < size-1)
    
    def _compute_focus(self):
        num_in_focus = 0
        for piece in self._pieces:
            if piece.get_era() == self._focus:
                num_in_focus += 1
        return num_in_focus
    
    def _copy(self):
        raise NotImplementedError()
    
    @staticmethod
    def _indent_focus(focus):
        if focus == 0:
            return ' ' * 2
        elif focus == 1:
            return ' ' * 14
        elif focus == 2:
            return ' ' * 26
        
    def __str__(self):
        return Player._indent_focus(self._focus) + self._color + "  \n"
    
class Human(Player):
    """Represent a human player, one that makes moves based on human input."""

    def copy(self):
        """Generate a deep copy of a human player."""
        copy_human = Human(self._color, self._focus, self._supply)
        copy_human._copy_pieces_from_other(self)
        return copy_human
    
    def get_move(self):
        """Get a move by prompting the user and storing their choices.
        The returned move will necessarily be valid."""
        super()._get_move()
        if self._move_len == 0:
            print("No copies to move")
            new_focus = self._prompt_focus_era()
            temp_move = self._find_move("none", None, None, new_focus)
            return temp_move
        piece_to_move = self._prompt_piece_name()
        direction1, direction2 = None, None
        for move_number in range(1, self._move_len + 1):
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

    def _prompt_piece_name(self):
        piece_names_on_board = self._get_piece_names() + self._opponent._get_piece_names()
        while True:
            piece_to_move = input("Select a copy to move\n")
            if piece_to_move not in piece_names_on_board:
                print("Not a valid copy")
                continue
            if not self._check_color(piece_to_move):
                print("That is not your copy")
                continue
            if not self._check_era(piece_to_move):
                print("Cannot select a copy from an inactive era")
                continue
            if len(self._valid_moves[piece_to_move]) == 0:
                print("That copy cannot move")
                continue
            return piece_to_move
    
    def _check_era(self, piece_name: str):
        for piece in self._pieces:
            if piece.get_name() == piece_name:
                return piece.get_era() == self._focus
        return False
    
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
            moves: list[MoveCommand] = self._valid_moves[piece_to_move]
            for move in moves:
                if move_number == 1:
                    if move.directions_match((direction, other_direction), move_number):
                        return direction
                elif move_number == 2:
                    if move.directions_match((other_direction, direction), move_number):
                        return direction
            print(f"Cannot move {direction}")

    def _prompt_focus_era(self):
        focus_to_int = {"past": 0, "present": 1, "future": 2}
        while True:
            new_focus = input("Select the next era to focus on ['past', 'present', 'future']\n")
            if new_focus not in focus_to_int:
                print("Not a valid era")
                continue
            if self._focus == focus_to_int[new_focus]:
                print("Cannot select the current era")
                continue
            return focus_to_int[new_focus]
    
    def _find_move(self, piece_name, direction1, direction2, focus):
        moves: list[MoveCommand] = self._valid_moves[piece_name]
        for move in moves:
            if move.directions_match((direction1, direction2), self._move_len) and move.focus_era_match(focus):
                return move
        return None
class Random_AI(Player):
    """Represent a random_AI player. This player randomly selects a move from the valid moves."""

    def copy(self):
        """Generate a deep copy of a random_AI player."""
        copy_random_ai = Random_AI(self._color, self._focus, self._supply)
        copy_random_ai._copy_pieces_from_other(self)
        return copy_random_ai
    
    def get_move(self):
        """Get a move by selecting randomly from the valid move. The returned move
        will necessarily be valid."""
        super()._get_move()
        return random.choice(self._list_valid_moves())
class Heuristic_AI(Player):
    """Represent a heuristic_AI player. This player looks at each available move, calulates a
    total move score for each, and picks the highest one, breaking any ties randomly."""

    def copy(self):
        """Generate a deep copy of a heuristic_AI player."""
        copy_heuristic_ai = Heuristic_AI(self._color, self._focus, self._supply)
        copy_heuristic_ai._copy_pieces_from_other(self)
        return copy_heuristic_ai

    def get_move(self):
        """Get a move by selecting from the moves that give the higehst score. 
        The returned move will necessarily be valid."""
        super()._get_move()
        list_valid_moves: list[MoveCommand] = self._list_valid_moves()
        best_moves = []
        best_score = float('-inf')
        for move in list_valid_moves:
            copy_game = self._game.copy()
            copy_move = move.generate_version(copy_game)
            copy_move.execute()
            copy_other_player = copy_game.get_players()[1]
            score = copy_other_player._heuristic_function()
            if score > best_score:
                best_moves.clear()
                best_moves.append(move)
                best_score = score
            elif score == best_score:
                best_moves.append(move)
        return random.choice(best_moves)
