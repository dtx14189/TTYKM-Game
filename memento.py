from abc import ABC

class Memento(ABC):
    pass

class Snapshot(Memento):
    def __init__(self, state: tuple):
        self._state = state
    
    def get_state(self):
        return self._state


