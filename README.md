# TTYKM – CLI Strategy Game

A command-line implementation of the strategy board game **TTYKM**, featuring human and AI players, undo/redo functionality, and modular software design using object-oriented design patterns.

See repository for offical **TTYKM** rulebook. 

---

## Features

- **CLI Interface**  
  Users play the game entirely through a simple command-line interface, choosing pieces, directions, and focus eras interactively.

- **Different Types of Players**  
  - Human players
  - Random AI
  - Heuristic AI based on weighted board evaluation

- **Undo/Redo Support**  
  When enabled, players can undo/redo any number of turns using the `undo`, `redo`, and `next` commands.

---

## How to Run

| Argument Position | Purpose               | Allowed Values                 | Default |
| ----------------- | --------------------- | ------------------------------ | ------- |
| `argv[1]`         | White player type     | `human`, `random`, `heuristic` | `human` |
| `argv[2]`         | Black player type     | `human`, `random`, `heuristic` | `human` |
| `argv[3]`         | Enable undo/redo      | `on`, `off`                    | `off`   |
| `argv[4]`         | Show heuristic scores | `on`, `off`                    | `off`   |

**Example: Human vs Random AI with undo/redo functionality and no heuristic score display**
```bash
python3 main.py human random on off
```

---

## Design Patterns 

### Decorator 
I used the Decorator pattern to add undo/redo/next functionality by wrapping a `GameManager` inside an `UndoRedo` class, allowing dynamic extension of behavior without modifying the base game logic. 

### Template 
The `Player` class defines a common interface, while `Human`, `RandomAI`, and `HeuristicAI` override `get_move()` and `copy()` to implement player-specific behavior.

### Command 
Each `MoveCommand` encapsulates a game move and can execute or defer it on a `Game` object, helping separate move logic from game logic.

### Memento 
I used the Memento pattern to store and restore snapshots of the `Game` state, enabling undo/redo through history and redo stacks managed by the `UndoRedo` class.
