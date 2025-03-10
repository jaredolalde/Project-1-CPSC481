from games import Game, GameState, alpha_beta_player, query_player
from typing import List, Tuple, Optional, Dict, Any


class GameOfNim(Game):
    """Play Game of Nim with first player 'MAX'.

    The Game of Nim Rules:
    1. Two players take turns removing objects from distinct heaps or rows.
    2. In each turn, a player must remove at least one object from the same row.
    3. The player that removes the last object loses the game.

    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (row, n) tuples where row is the row index and n is
    the number of objects to remove, and a board represented as a list with
    the number of objects in each row.
    """

    def __init__(self, board: List[int] = [3, 1]):
        """Create a Game of Nim with the given board as initial state.

        Args:
            board: A list representing the number of objects in each row.
                  For example, [7, 5, 3, 1] represents 7 objects in the first row,
                  5 in the second, 3 in the third, and 1 in the fourth.
        """
        # Generate all possible moves from this board
        moves = self._generate_moves(board)

        # Create the initial state
        self.initial = GameState(to_move='MAX', utility=0, board=board, moves=moves)

    def _generate_moves(self, board: List[int]) -> List[Tuple[int, int]]:
        """Generate all valid moves for the given board state.

        Args:
            board: Current board state as a list of integers

        Returns:
            A list of tuples (row, n) representing valid moves
        """
        moves = []
        for row, count in enumerate(board):
            for objects in range(1, count + 1):
                moves.append((row, objects))
        return moves

    def actions(self, state: GameState) -> List[Tuple[int, int]]:
        """Return all legal moves for the given state.

        A legal move is removing at least one object from a row.

        Args:
            state: Current game state

        Returns:
            List of all legal moves as (row, n) tuples
        """
        return state.moves

    def result(self, state: GameState, move: Tuple[int, int]) -> GameState:
        """Return the state that results from making a move from a state.

        Args:
            state: Current game state
            move: A tuple (row, n) representing the move to make

        Returns:
            New game state after applying the move

        Raises:
            ValueError: If the move is not in state.moves (illegal move)
        """
        if move not in state.moves:
            raise ValueError(f"Illegal move: {move}. Valid moves are {state.moves}")

        # Create a new board by removing objects at the specified row
        row, count = move
        new_board = state.board.copy()
        new_board[row] -= count

        # Generate all possible moves from this new board
        moves = self._generate_moves(new_board)

        # Calculate new player's turn
        player = 'MIN' if state.to_move == 'MAX' else 'MAX'

        # Calculate utility if game is over
        utility = self.compute_utility(new_board, move, state.to_move)

        return GameState(to_move=player, utility=utility, board=new_board, moves=moves)

    def utility(self, state: GameState, player: str) -> int:
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise.

        Args:
            state: Current game state
            player: The player for whom to calculate utility ('MAX' or 'MIN')

        Returns:
            1 if player wins, -1 if player loses, 0 if game is ongoing
        """
        return state.utility if player == 'MAX' else -state.utility

    def terminal_test(self, state: GameState) -> bool:
        """Check if the given state is terminal (game over).

        A state is terminal if there are no objects left on the board.

        Args:
            state: Current game state

        Returns:
            True if state is terminal, False otherwise
        """
        return sum(state.board) == 0

    def compute_utility(self, board: List[int], move: Tuple[int, int], player: str) -> int:
        """Calculate the utility value of a board position.

        In Nim, the player who takes the last object loses.
        Since the player argument is who just moved, they lose if the board is empty.

        Args:
            board: Current board state
            move: The move that led to this board state
            player: The player who made the move ('MAX' or 'MIN')

        Returns:
            -1 if player loses (took last object), 1 if player wins, 0 otherwise
        """
        if sum(board) == 0:
            # Player who took the last object loses
            return -1 if player == 'MAX' else 1
        return 0  # Game still in progress

    def display(self, state: GameState) -> None:
        """Display the current game state in a user-friendly format.

        Args:
            state: Current game state
        """
        board = state.board
        print("board:", board)

        # Visual representation of the board
        print("\nVisual board:")
        for row, count in enumerate(board):
            print(f"Row {row}:", "O " * count)

        print(f"Player to move: {state.to_move}")


if __name__ == "__main__":
    # Create the game instance with the board from the assignment example
    nim = GameOfNim(board=[7, 5, 3, 1])

    print("Initial state:")
    nim.display(nim.initial)
    print("Initial moves:", nim.initial.moves)

    # Example of making a move
    print("\nAfter move (0, 1):")
    new_state = nim.result(nim.initial, (0, 1))
    nim.display(new_state)

    # Play a complete game between the computer and a human
    print("\nStarting a new game...")
    utility = nim.play_game(alpha_beta_player, query_player)  # computer moves first
    if utility < 0:
        print("MIN (human player) won the game")
    else:
        print("MAX (computer) won the game")