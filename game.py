from board import Board
from memento import Snapshot
class Game():
    def __init__(self):
        self.board = Board(4)
        self._turn = 1
        self._white_focus = None
        self._black_focus = None

    def save(self):
        return Snapshot(self._zip_state())
    
    def restore(self, snapshot: Snapshot):
        self._unzip_state(snapshot.get_state())

    def _zip_state(self) -> tuple:
        return (self.board, self._turn, self._white_focus, self._black_focus)
    
    def _unzip_state(self, state):
        self.board = state[0]
        self._turn = state[1]
        self._white_focus = state[2]
        self._black_focus = state[3]


    def __str__(self):
        print("board")
        return f"Turn: {self._turn}, Current player: "


    