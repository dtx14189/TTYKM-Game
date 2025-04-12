from piece import Piece
from enum_eras import Era
from memento import Snapshot, Caretaker
from copy import deepcopy
from move_command import MoveCommand
class Board():
    def __init__(self, size: int):
        self._size = size
        self._black_pieces: list[Piece] = []
        self._white_pieces: list[Piece] = []
        self._squares = [[([None] * 3) for _ in range(size)] for _ in range(size)]
        self._setup()
        self._white_supply = 4
        self._black_supply = 4
        self._caretaker = Caretaker(self)

    def _setup(self):
        for i in range(3):
            black_piece = Piece("black", f'{i+1}', (0, 0, i))
            self._black_pieces.append(black_piece)
            self._squares[0][0][i] = black_piece
        for i in range(3):
            letter = chr(ord('A') + i)
            white_piece = Piece("white", f'{letter}', (self._size-1, self._size-1, i))
            self._white_pieces.append(white_piece)
            self._squares[self._size-1][self._size-1][i] = white_piece

    def enumerate_possible_moves(self, color: str, focus):
        if color == "black":
            pieces = self._black_pieces
        elif color == "white":
            pieces = self._white_pieces
        valid_moves = {}
        for piece in pieces:
            if piece.get_era() == focus:
                valid_moves[piece.get_name()] = self._piece_enumerate_possible_moves(piece, focus)
            else:
                valid_moves[piece.get_name()] = None
        return valid_moves
    
    def _piece_enumerate_possible_moves(self, piece: Piece, focus):
        valid_moves = []
        directions = ['n', 'e', 's', 'w', 'f', 'b']
        # eras = [Era.PAST, Era.PRESENT, Era.FUTURE]
        eras = [0, 1, 2]
        for direction1 in directions:
            if self._invalid_move(piece, direction1):
                continue
            self._caretaker.backup()
            self.update(piece, direction1)
            for direction2 in directions:
                if self._invalid_move(piece, direction2):
                    direction2 = None
                for era in eras:
                    if era != focus:
                        new_move = MoveCommand(piece, direction1, direction2, era)
                        valid_moves.append(new_move)
            self._caretaker.undo()
        return valid_moves

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
    
    def _invalid_move(self, piece: Piece, direction):
        new_pos = Board._get_new_pos_with_direction(piece.get_pos(), direction)
        if not self._valid_pos(new_pos):
            return False
        if piece.get_color() == self._get_piece_at_pos(new_pos):
            return False
        if direction == 'f' or direction == 'b':
            if self._get_piece_at_pos(new_pos):
                return False
            if direction == 'b':
                if piece.get_color() == "black" and self._black_supply <= 0:
                    return False
                if piece.get_color() == "white" and self._white_supply <= 0:
                    return False
        return True

    def _valid_pos(self, pos) -> bool:
        row, col, era = pos[0], pos[1], pos[2]
        if row < 0 or row >= self._size:
            return False
        if col < 0 or col >= self._size:
            return False
        if era < 0 or era >= 2:
            return False
        return True
    
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
        self._set_piece_at_pos(pos, self._generate_piece(piece.get_color(), pos))
        self._set_piece_at_pos(new_pos, piece)
    
    def _generate_piece(self, color, pos):
        if color == "black":
            name = str(8 - self._black_supply)
            black_piece = Piece(color, name, pos)
            self._black_pieces.append(black_piece)
            return black_piece
        elif color == "white":
            name = chr(ord('H') - self._white_supply)
            white_piece = Piece(color, name, pos)
            return white_piece

    def _push(self, piece: Piece, direction):
        new_pos = Board._get_new_pos_with_direction(piece.get_pos(), direction)
        other_piece: Piece = self._get_piece_at_pos(new_pos)
        self._move(piece, new_pos)  
        if other_piece is not None:
            if piece.get_color() == other_piece.get_color():
                self._remove(piece)
                self._remove(other_piece)
            else: # colors are different
                self._push(other_piece, direction)
        
    def _move(self, piece: Piece, new_pos):
        self._remove(piece)
        self._set_piece_at_pos(piece, new_pos)
    
    def _remove(self, piece: Piece):
        self._set_piece_at_pos(None, piece.get_pos())
        if piece.get_color() == "black":
            self._black_pieces.remove(piece)
        elif piece.get_color() == "white":
            self._white_pieces.remove(piece)

    def _get_piece_at_pos(self, pos):
        row, col, era = pos[0], pos[1], pos[2]
        return self._squares[row][col][era]
    
    def _set_piece_at_pos(self, piece: Piece, new_pos):
        new_row, new_col, new_era = new_pos[0], new_pos[1], new_pos[2]
        self._squares[new_row][new_col][new_era] = piece
        if piece is not None:
            piece.set_pos(new_pos)

    def get_piece_names(self):
        piece_names = []
        for piece in self._black_pieces:
            piece_names.append(piece.get_name())
        for piece in self._white_pieces:
            piece_names.append(piece.get_name())
        return piece_names
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
    
    def save(self):
        return Snapshot(self._zip_state())
    
    def restore(self, snapshot: Snapshot):
        self._unzip_state(snapshot.get_state())

    def _zip_state(self) -> tuple:
        return (deepcopy(self._squares), self._black_supply, self._white_supply)

    def _unzip_state(self, state):
        self._squares = state[0]
        self._black_supply = state[1]
        self._white_supply = state[2]

        
