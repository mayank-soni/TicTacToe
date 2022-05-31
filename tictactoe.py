"""
Tic Tac Toe Player
"""

from asyncio.windows_events import NULL
import math
from itertools import chain
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None
BOARD_SIZE = 3

# Create a list of all possible winning combinations (horizontal, vertical, and diagonal)
# Each combination is a list of indexes on a flattened board
WINNING_COMBOS = []
NUMBER_OF_TILES = BOARD_SIZE**2

# Horizontal combos
for i in range(0, NUMBER_OF_TILES, BOARD_SIZE):
    combo = []
    for j in range(BOARD_SIZE):
        combo.append(i + j)
    WINNING_COMBOS.append(combo)

# Vertical combos
for i in range(BOARD_SIZE):
    combo = []
    for j in range(BOARD_SIZE):
        combo.append(i + (j * BOARD_SIZE))
    WINNING_COMBOS.append(combo)

# Diagonal combos
WINNING_COMBOS.append(list(range(0, NUMBER_OF_TILES, (BOARD_SIZE + 1))))
WINNING_COMBOS.append(list(range(BOARD_SIZE-1, NUMBER_OF_TILES-1, (BOARD_SIZE-1)))) # ends at number of tiles-1 because otherwise the bottom right cell is included in the down left diagonal winning combo

def initial_state():
    """
    Returns starting state of the board. 
    """
    board = []
    for i in range(BOARD_SIZE):
        board.append(list())
        for j in range(BOARD_SIZE):
            board[i].append(EMPTY)
    return board  
    # Below is the original implementation. Edited to have flexible board sizing. 
    # return [[EMPTY, EMPTY, EMPTY],
    #        [EMPTY, EMPTY, EMPTY],
    #        [EMPTY, EMPTY, EMPTY]]
    

def number_of_moves(board):
    """
    Returns number of moves made so far on a board
    """
    # Counts number of non-empty cells. Uses itertools.chain to flatten board. 
    return sum(x != EMPTY for x in list(chain.from_iterable(board)))


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Flatten board and count # of moves made so far
    n_moves = number_of_moves(board)
    # X always starts first, and players then alternate. If even number of moves made, X will start next, else O. 
    if n_moves % 2 == 0:
        return X
    return O
    

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_moves = set()
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == EMPTY:
                possible_moves.add((i,j))
    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Creates a deep copy of board so as not to modify original board
    new_board = deepcopy(board)
    try:
        if board[action[0]][action[1]] == EMPTY:
            # Checks which player is next and adds his piece to the selected square
            new_board[action[0]][action[1]] = player(board)
        else:
            raise ValueError(f"Duplicate move made: {action} on board {board}")
    except IndexError:
        print(f"Action {action} is out of bounds for board {board}")
        raise
    else:
        return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one. Else returns None. 
    """
    # Create 2 lists with indices of all Xs and Os in current board. Indices calculated after 
    # flattening board (merging 3 sub-lists into one list)
    flat_board = list(chain.from_iterable(board))
    number_of_tiles = BOARD_SIZE**2
    Xs = []
    Os = []
    for i in range(number_of_tiles):
        if flat_board[i] == X:
            Xs.append(i)
        if flat_board[i] == O:
            Os.append(i)
         
    # Check if either of the list Xs or Os contains all the elements of any of the winning combos
    for combo in WINNING_COMBOS:
        if all(tile in Xs for tile in combo):
            return X
        if all(tile in Os for tile in combo):
            return O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    #Game over if board is filled or there is a winner
    if number_of_moves(board) == BOARD_SIZE**2 or winner(board) != None:
        return True
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise. Can only be called if game is over. 
    """
    if terminal(board) != True:
        raise Exception("Utility called on non-terminal board")
    winning_player = winner(board)
    if winning_player == X:
        return 1
    if winning_player == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action & the utility from that action for the current player on the board. Returns None if game is over.
    Uses a second function call since CS50AI's automated checking software doesn't allow additional arguments to be passed
    """
    return minimax2(board)
    

def minimax2(board, one_level_up_minmax=None):
    """
    Returns the optimal action & the utility from that action for the current player on the board. Returns None if game is over.
    Uses a second function call since CS50AI's automated checking software doesn't allow additional arguments to be passed
    """
    # one_level_up_minmax argument = None (i.e. it is not passed) in initial function call in runner.py module. 
    # This initialises the value based on who is the player at the time. 
    # For recursive function calls resulting from this, value is passed (inherited from min/max of the one-level-up function call)
    if one_level_up_minmax == None:
        one_level_up_minmax = 2 if player(board) == X else -2
    
    if terminal(board) == True: 
        return None
    
    # If only one possible action, return that action
    possible_actions = actions(board)
    if len(possible_actions) == 1:
        action = possible_actions.pop()
        return action, utility(result(board, action))
    
    # Otherwise, compare the various results to see which is best
    possible_results = {action: result(board, action) for action in possible_actions}
    if player(board) == X:
        # Initialise max to -2, so that the first result checked is certain to be better (range is -1, 0, and 1)
        max = -2
        best_action = ()
        for action, new_board in possible_results.items():
            # If move exists to win, make it
            if winner(new_board) == X:
                return action, utility(new_board)
            # Otherwise, check if the utility of this move is higher than the current maximum. Pass in the current max
            # as the one_level_up_minmax value for alpha-beta pruning
            util = minimax2(new_board, max)[1]
            if util > max:
                max = util
                best_action = action
            # Implement alpha-beta pruning based on the next higher level's minmax. 
            if max >= one_level_up_minmax:
                break
        return best_action, max
    if player(board) == O:
        min = 2
        best_action = set()
        for action, new_board in possible_results.items():
            # If move exists to win, make it
            if winner(new_board) == O:
                return action, utility(new_board)
            # Otherwise, check if the utility of this move is lower than the current minimum. Pass in the current min
            # as the one_level_up_minmax value for alpha-beta pruning
            util = minimax2(new_board, min)[1]
            if util < min:
                min = util
                best_action = action
            # Implement alpha-beta pruning based on the next higher level's minmax 
            if min <= one_level_up_minmax:
                break
        return best_action, min