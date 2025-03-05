from games import *

class GameOfNim(Game):
    """Play Game of Nim with first player 'MAX'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a list with number of objects in each row."""

    def __init__(self, board=[3, 1]):
        # Define the initial state
        moves = []
        # Generate all possible moves
        for r, row_count in enumerate(board):
            for n in range(1, row_count + 1):
                moves.append((r, n))
        
        # Create the initial state with the 'MAX' player first
        self.initial = GameState(to_move='MAX', utility=0, board=board, moves=moves)

    def actions(self, state):
        """Legal moves are at least one object, all from the same row."""
        return state.moves

    def result(self, state, move):
        """Return the state that results from taking a move."""
        if move not in state.moves:
            return state  # Illegal move has no effect
        
        # Unpack the move
        r, n = move
        
        # Create a new board with the move applied
        board = state.board.copy()
        board[r] -= n
        
        # Generate new possible moves for the new board
        moves = []
        for row, row_count in enumerate(board):
            for count in range(1, row_count + 1):
                moves.append((row, count))
        
        # Switch player
        player = 'MIN' if state.to_move == 'MAX' else 'MAX'
        
        # Return the new state
        return GameState(to_move=player, utility=self.compute_utility(board, player),
                         board=board, moves=moves)

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'MAX' else -state.utility

    def terminal_test(self, state):
        """A state is terminal if there are no objects left"""
        return sum(state.board) == 0  # Game ends when no objects remain

    def compute_utility(self, board, player):
        """If 'MAX' wins, utility = 1; if 'MIN' wins, utility = -1."""
        if sum(board) == 0:
            # The last player to move took the last object and lost
            # So the current player (who didn't move yet) wins
            return 1 if player == 'MAX' else -1
        return 0  # Game not over yet

    def display(self, state):
        board = state.board
        print("board: ", board)


if __name__ == "__main__":
    nim = GameOfNim(board=[0, 5, 3, 1])  # Creating the game instance
    # nim = GameOfNim(board=[7, 5, 3, 1])  # a much larger tree to search
    print(nim.initial.board)  # must be [0, 5, 3, 1]
    print(nim.initial.moves)  # must be [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 2), (2, 3), (3, 1)]
    print(nim.result(nim.initial, (1, 3)))
    utility = nim.play_game(alpha_beta_player, query_player)  # computer moves first 
    if utility < 0:
        print("MIN won the game")
    else:
        print("MAX won the game")
