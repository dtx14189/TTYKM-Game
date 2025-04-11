from memento import Caretaker
class Piece():
    def __init__(self, color: str, name: str, pos: tuple):
        self._color = color
        self._name = name
        self._pos = pos
    
    def valid_moves(self, board, supply: int):
        caretaker = Caretaker(board)
        neighbors = board.get_neighbors() # neighbors are pieces, potentially None
        # move1 =
        # for neighbor in neighbors:
        #     if neighbor  
    
    def get_color(self):
        return self._color
    
    def get_pos(self):
        return self._pos
    
    def set_pos(self, new_pos):
        self._pos = new_pos
        
    @staticmethod 
    def get_new_pos_with_direction(pos, direction):
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
        
    def __str__(self):
        return f"{self._name}"