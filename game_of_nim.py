from games import Game, GameState, alpha_beta_player, query_player
from typing import List, Tuple, Optional, Dict, Any


class GameOfNim(Game):

    def __init__(self, board: List[int] = [3, 1]):

        # Generate all possible moves from this board
        moves = self._generate_moves(board)

        # Create the initial state
        self.initial = GameState(to_move='MAX', utility=0, board=board, moves=moves)

    def _generate_moves(self, board: List[int]) -> List[Tuple[int, int]]:

        moves = []
        for row, count in enumerate(board):
            for objects in range(1, count + 1):
                moves.append((row, objects))
        return moves

    def actions(self, state: GameState) -> List[Tuple[int, int]]:

        return state.moves

    def result(self, state: GameState, move: Tuple[int, int]) -> GameState:

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
        return state.utility if player == 'MAX' else -state.utility

    def terminal_test(self, state: GameState) -> bool:
        return sum(state.board) == 0

    def compute_utility(self, board: List[int], move: Tuple[int, int], player: str) -> int:
        if sum(board) == 0:
            # Player who took the last object loses
            return -1 if player == 'MAX' else 1
        return 0  # Game still in progress

    def display(self, state: GameState) -> None:
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