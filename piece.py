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
    
    def get_pos(self):
        return self._pos
    
    def set_pos(self, new_pos):
        self._pos = new_pos

    def __str__(self):
        return f"{self._name}"