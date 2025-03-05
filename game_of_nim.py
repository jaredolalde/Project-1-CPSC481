from games import *

class GameOfNim(Game):
    """Play Game of Nim with first player 'MAX'.
    A state has the player to move, a cached utility, a list of moves in
    the form of a list of (x, y) positions, and a board, in the form of
    a list with number of objects in each row."""

    def __init__(self, board=[3, 1]):
        """Create a Game of Nim with the given board as initial state."""
        # Generate all possible moves from this board
        moves = []
        for row, count in enumerate(board):
            for objects in range(1, count + 1):
                moves.append((row, objects))
                
        # Create the initial state
        self.initial = GameState(to_move='MAX', utility=0, board=board, moves=moves)

    def actions(self, state):
        """Legal moves are at least one object, all from the same row."""
        return state.moves

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        if move not in state.moves:
            return state  # Illegal move has no effect
            
        # Create a new board by removing objects at the specified row
        row, count = move
        new_board = state.board.copy()
        new_board[row] -= count
        
        # Generate all possible moves from this new board
        moves = []
        for r, c in enumerate(new_board):
            for objects in range(1, c + 1):
                moves.append((r, objects))
                
        # Calculate new player's turn
        player = 'MIN' if state.to_move == 'MAX' else 'MAX'
        
        # Calculate utility if game is over
        utility = self.compute_utility(new_board, move, state.to_move)
        
        return GameState(to_move=player, utility=utility, board=new_board, moves=moves)

    def utility(self, state, player):
        """Return the value to player; 1 for win, -1 for loss, 0 otherwise."""
        return state.utility if player == 'MAX' else -state.utility

    def terminal_test(self, state):
        """A state is terminal if there are no objects left"""
        return sum(state.board) == 0

    def compute_utility(self, board, move, player):
        """If all objects are removed and it's a player's turn, they lost (utility = -1)
        If all objects are removed and it's the opponent's turn, player won (utility = 1)
        Otherwise, game continues (utility = 0)"""
        if sum(board) == 0:
            return -1 if player == 'MAX' else 1
        return 0

    def display(self, state):
        board = state.board
        print("board: ", board)


if __name__ == "__main__":
    nim = GameOfNim(board=[0, 5, 3, 1])  # Creating the game instance
    #nim = GameOfNim(board=[7, 5, 3, 1])  # a much larger tree to search
    print(nim.initial.board)  # must be [0, 5, 3, 1]
    print(nim.initial.moves)  # must be [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (2, 1), (2, 2), (2, 3), (3, 1)]
    print(nim.result(nim.initial, (1, 3)))
    utility = nim.play_game(alpha_beta_player, query_player)  # computer moves first 
    if utility < 0:
        print("MIN won the game")
    else:
        print("MAX won the game")
