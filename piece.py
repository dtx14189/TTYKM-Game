from memento import Caretaker
class Piece():
    def __init__(self, color: str, name: str, pos: tuple):
        self._color = color
        self._name = name
        self._pos = pos
    
    def valid_moves(self, board, supply: int):
        caretaker = Caretaker(board)
        neighbors = board.get_neighbors() # neighbors are pieces, potentially None
        move1 =
        for neighbor in neighbors:
            if neighbor  

        

    def __str__(self):
        return f"{self._name}"