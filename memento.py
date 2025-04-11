from abc import ABC

class Memento(ABC):
    pass

class Snapshot(Memento):
    def __init__(self, state: tuple):
        self._state = state
    
    def get_state(self):
        return self._state

class Caretaker():
    def __init__(self, originator):
        self._history = []
        self._originator = originator

    def backup(self):
        self._history.append(self._originator.save())

    def undo(self):
        if not len(self._history):
            return

        memento = self._history.pop()
        self._originator.restore(memento)


