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
        self._undo_chain = []
        self._originator = originator

    def backup(self, type="next"):
        if type == "next":
            self._undo_chain = []
        self._history.append(self._originator.save())

    def undo(self):
        if len(self._history) == 0:
            return
        self._undo_chain.append(self._originator.save())
        memento = self._history.pop()
        self._originator.restore(memento)

    def redo(self):
        if len(self._undo_chain) == 0:
            return
        self.backup(type="redo")
        memento = self._undo_chain.pop()
        self._originator.restore(memento)


