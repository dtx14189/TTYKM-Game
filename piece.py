class Piece():
    """Purely meant for storing attributes of a piece"""
    def __init__(self, color: str, name: str, pos: tuple):
        self._color = color
        self._name = name
        self._pos = pos
    
    def get_color(self):
        return self._color
    
    def get_name(self):
        return self._name
    
    def get_pos(self):
        return self._pos
    
    def set_pos(self, new_pos):
        self._pos = new_pos

    def get_era(self):
        return self._pos[2]
        
    def __str__(self):
        return f"{self._name}"
