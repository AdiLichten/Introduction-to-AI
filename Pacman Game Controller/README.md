# Pacman Game Controller

This project is a Python implementation of a Pacman game controller. The controller uses Q-learning, a type of reinforcement learning, to determine the best actions for Pacman to take in the game.

## Files

The project consists of three main Python files:

- `ex2.py`: This file contains the `Controller` class which is responsible for controlling the Pacman game. It initializes the game board, runs the Q-learning algorithm, and chooses the next move for Pacman.

- `pacman.py`: This file contains the `Game` class which represents a Pacman game. It initializes the game, sets the locations of the ghosts and pellets, moves Pacman, and updates the game board.

- `check.py`: This file contains the `evaluate` function which runs the `Controller` on a given game and evaluates its effectiveness.

## How to Run

To run the project, execute the `check.py` file. This will run the evaluation on a given game.

```bash
python check.py
```
