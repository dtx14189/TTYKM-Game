from game import Game

class Caretaker():
    def __init__(self, game: Game):
        self._history = []
        self._game = game

    def backup(self):
        self._history.append(self._game.save())

    def undo(self):
        if not len(self._history):
            return

        memento = self._history.pop()
        self._game.restore(memento)