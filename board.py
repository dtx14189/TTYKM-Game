from piece import Piece
from enum_eras import Era
from copy import deepcopy
from player import Player
class Board():
    def __init__(self, size: int, white_player: Player=None, black_player: Player=None, setup=True):
        self._size = size
        self._white_player: Player = white_player
        self._black_player: Player = black_player
        self._squares: list[list[list[Piece]]] = [[([None] * 3) for _ in range(size)] for _ in range(size)]
        if setup:
            self._setup()

    def _setup(self):
        for i in range(3):
            black_piece = Piece("black", f'{i+1}', (0, 0, i), self)
            self._black_player.add_piece(black_piece)
            self._squares[0][0][i] = black_piece
        # black_piece = Piece("black", "1", (0, 0, 0), self)
        # self._black_player.add_piece(black_piece)
        # self._squares[0][0][0] = black_piece
        for i in range(3):
            letter = chr(ord('A') + i)
            white_piece = Piece("white", f'{letter}', (self._size-1, self._size-1, i), self)
            self._white_player.add_piece(white_piece)
            self._squares[self._size-1][self._size-1][i] = white_piece

    @staticmethod 
    def _get_new_pos_with_direction(pos, direction):
        row, col, era = pos[0], pos[1], pos[2]
        if direction == 'n':
            return (row - 1, col, era)
        elif direction == 'e':
            return (row, col + 1, era)
        elif direction == 's':
            return (row + 1, col, era)
        elif direction == 'w':
            return (row, col - 1, era)
        elif direction == 'f':
            return (row, col, era + 1)
        elif direction == 'b':
            return (row, col, era - 1)
    
    def invalid_move(self, piece: Piece, direction):
        new_pos = Board._get_new_pos_with_direction(piece.get_pos(), direction)
        if not self._valid_pos(new_pos):
            return True
        if piece.get_color() == self.get_piece_at_pos(new_pos):
            return True
        if direction == 'f' or direction == 'b':
            if self.get_piece_at_pos(new_pos):
                return True
            if direction == 'b':
                player_to_check_supply = self._get_player_from_color(piece.get_color())
                if player_to_check_supply.get_supply() <= 0:
                    return True
        return False

    def _valid_pos(self, pos) -> bool:
        row, col, era = pos[0], pos[1], pos[2]
        if row < 0 or row >= self._size:
            return False
        if col < 0 or col >= self._size:
            return False
        if era < 0 or era > 2:
            return False
        return True
    
    def copy(self):
        board_copy = Board(self._size, setup=False)
        board_copy._squares = deepcopy(self._squares)
        board_copy._white_player = self._white_player.copy()
        board_copy._black_player = self._black_player.copy()
        for i in range(board_copy._size):
            for j in range(board_copy._size):
                for k in range(3):
                    piece = board_copy.get_piece_at_pos((i, j, k))
                    if piece is not None:
                        player = board_copy._get_player_from_color(piece.get_color())
                        player.add_piece(piece)
        return board_copy


    def update(self, piece: Piece, direction):
        if direction is None:
            return
        if direction == 'f' or direction == 'b':
            self._time_travel(piece, direction)
        else:
            self._push(piece, direction)

    def _time_travel(self, piece: Piece, direction):
        if direction == 'f':
            self._forward(piece)
        elif direction == 'b':
            self._backward(piece)

    def _forward(self, piece: Piece):
        new_pos = Board._get_new_pos_with_direction(piece.get_pos(), 'f')
        self._set_piece_at_pos(None, piece.get_pos())
        self._set_piece_at_pos(piece, new_pos)

    def _backward(self, piece: Piece):
        pos = piece.get_pos()
        new_pos = Board._get_new_pos_with_direction(pos, 'b')
        self._set_piece_at_pos(self._generate_piece(piece.get_color(), pos), pos)
        self._set_piece_at_pos(piece, new_pos)
    
    def _generate_piece(self, color, pos):
        if color == "black":
            name = str(8 - self._black_player.get_supply())
        elif color == "white":
            name = chr(ord('H') - self._white_player.get_supply())
        new_piece = Piece(color, name, pos, self)
        player_to_add_to = self._get_player_from_color(color)
        player_to_add_to.add_piece(new_piece)
        player_to_add_to.decrement_supply()
        return new_piece

    def _push(self, piece: Piece, direction):
        new_pos = Board._get_new_pos_with_direction(piece.get_pos(), direction)
        other_piece: Piece = self.get_piece_at_pos(new_pos)
        self._move(piece, new_pos)  
        if other_piece is not None:
            if piece.get_color() == other_piece.get_color():
                self._eliminate(piece)
                self._eliminate(other_piece)
            else: # colors are different
                self._push(other_piece, direction)
        
    def _move(self, piece: Piece, new_pos):
        self._set_piece_at_pos(None, piece.get_pos())
        self._set_piece_at_pos(piece, new_pos)
    
    def _eliminate(self, piece: Piece):
        self._set_piece_at_pos(None, piece.get_pos())
        player_to_remove_from = self._get_player_from_color(piece.get_color())
        player_to_remove_from.remove_piece(piece)

    def get_piece_at_pos(self, pos):
        row, col, era = pos[0], pos[1], pos[2]
        return self._squares[row][col][era]
    
    def _set_piece_at_pos(self, piece: Piece, new_pos):
        new_row, new_col, new_era = new_pos[0], new_pos[1], new_pos[2]
        self._squares[new_row][new_col][new_era] = piece
        if piece is not None:
            piece.set_pos(new_pos)

    def _get_player_from_color(self, color: str):
        if color == "black":
            return self._black_player
        elif color == "white":
            return self._white_player
        
    def __str__(self):
        result = []
        for i in range(2 * self._size + 1):
            if i % 2 == 0:
                self._print_plus_minus(result)
            else:
                self._print_board_row(result, i // 2)
        return f"{''.join(result)}"

    def _print_plus_minus(self, result: list):
        for i in range(3):
            for j in range(2 * self._size + 1):
                if j % 2 == 0:
                    result.append('+')
                else:
                    result.append('-')
            if i < 2:
                result.append("   ")
        result.append('\n')

    def _print_board_row(self, result: list, row):
        for i in range(3):
            for j in range(2 * self._size + 1):
                if j % 2 == 0:
                    result.append('|')
                else:
                    piece = self._squares[row][j // 2][i]
                    if piece == None:
                        result.append(" ")
                    else:
                        result.append(str(piece))
            if i < 2:
                result.append("   ")
        result.append("\n")


        
