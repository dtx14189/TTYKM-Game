from abc import ABC

class Memento(ABC):
    """Represent a memento abstractly."""
    pass
class Snapshot(Memento):
    """Represent a concrete version of a memento."""

    def __init__(self, state: tuple):
        """Initialize a snapshot that stores informatino in its state."""
        self._state = state
    
    def get_state(self):
        """Get the state of the snapshot."""
        return self._state

class Caretaker():
    """Represent a manager for snapshots saved from the originator."""

    def __init__(self, originator):
        """Initalize a caretaker. A caretaker stores two lists of snapshots, one to
        track the history and another to track the chain of undos."""
        self._history = []
        self._undo_chain = []
        self._originator = originator

    def backup(self, type="next"):
        """Create a snapshot, and append it to the history of snapshots. 
        If type="next", then reset the undo_chain."""
        if type == "next":
            self._undo_chain = []
        self._history.append(self._originator.save())

    def undo(self):
        """Move the originator back one snapshot, if possible."""
        if len(self._history) == 0:
            return
        self._undo_chain.append(self._originator.save())
        memento = self._history.pop()
        self._originator.restore(memento)

    def redo(self):
        """Redo any undos by moving the originator forward one snapshot, if possible."""
        if len(self._undo_chain) == 0:
            return
        self.backup(type="redo")
        memento = self._undo_chain.pop()
        self._originator.restore(memento)


