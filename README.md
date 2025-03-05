# Game of Nim Implementation

## Project Overview
This project implements the Game of Nim as part of a programming assignment. The implementation defines the rules of the game and allows for gameplay between a computer player (using the minimax algorithm with alpha-beta pruning) and a human player.

## Game Rules
- Two players take turns removing objects from distinct heaps or rows
- In each turn, a player must remove at least one object from the same row
- The player that removes the last object loses the game

## Implementation Details
The project consists of a `GameOfNim` class that extends the `Game` class from the `games.py` module. The implementation includes:

- Representation of the game state as a list of numbers, with each number representing the count of objects in a row
- Actions represented as 2-tuples (r, n), where r is the row index and n is the number of objects to remove
- Methods for determining valid moves, computing the result of a move, and checking for game termination
- Support for the minimax algorithm with alpha-beta pruning for optimal computer play

## Usage
To play the game:

```python
from games import alpha_beta_player, query_player
from game_of_nim import GameOfNim

# Create a game with an initial board configuration
nim = GameOfNim(board=[7, 5, 3, 1])

# Play a game with the computer (alpha_beta_player) vs a human (query_player)
utility = nim.play_game(alpha_beta_player, query_player)

# Display the winner
if utility < 0:
    print("MIN won the game")
else:
    print("MAX won the game")
```

## Requirements
- Python 3.x
- The `games.py` module (provided as part of the assignment)

## Note
This project was completed as part of a programming assignment due on March 10, 2025.
