"""
Tic Tac Toe Player
"""

from asyncio.windows_events import NULL
from itertools import chain
from copy import deepcopy
from random import randrange

X = "X"
O = "O"
EMPTY = None
BOARD_SIDE_LENGTH = 3

# Initialise a list of all possible winning combinations for current board size.
# Each combo is a list of cells. If all the cells in any combo are taken up by one player, that player wins.
# Cells are represented as tuples: (row, column), starting from (0,0) in the top left.
WINNING_COMBOS = []

# Horizontal combos
for row in range(0, BOARD_SIDE_LENGTH):
    combo = []
    for column in range(BOARD_SIDE_LENGTH):
        combo.append((row, column))
    WINNING_COMBOS.append(combo)

# Vertical combos
for column in range(BOARD_SIDE_LENGTH):
    combo = []
    for row in range(BOARD_SIDE_LENGTH):
        combo.append((row, column))
    WINNING_COMBOS.append(combo)

# Diagonal combos
combo = []
for i in range(BOARD_SIDE_LENGTH):
    combo.append((i,i))
WINNING_COMBOS.append(combo)

combo = []
for i in range(BOARD_SIDE_LENGTH):
    combo.append((i,BOARD_SIDE_LENGTH-1-i))
WINNING_COMBOS.append(combo)

def initial_state():
    """
    Returns starting state of the board.
    """
    board = []
    for i in range(BOARD_SIDE_LENGTH):
        board.append(list())
        for j in range(BOARD_SIDE_LENGTH):
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
    return sum(x != EMPTY for x in chain.from_iterable(board))
    # NOTE: removed list after chain.from_iterable - check this.


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # X always starts first, and players then alternate. If number of moves made is even, X will start next, else O.
    if number_of_moves(board) % 2 == 0:
        return X
    return O


def actions(board):
    """
    Returns set of all possible actions (row, column) available on the board i.e. all empty cells.
    """
    possible_moves = set()
    for row in range(BOARD_SIDE_LENGTH):
        for column in range(BOARD_SIDE_LENGTH):
            if board[row][column] == EMPTY:
                possible_moves.add((row,column))
    return possible_moves


def result(board, action):
    """
    Returns the board that results from making move (row, column) on the board.
    """
    # Creates a deep copy of board so as not to modify original board.
    # Since board is a list, making a regular (shallow) copy of it will only copy over the references (pointers)
    # to the original elements. There will still remain only one set of elements of board.
    # Any changes made to the shallow copy will also automatically be made on the original board. This is NOT what we want,
    # as the original board will need to be used again for subsequent calculations.
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


# Removed this function and merged with terminal
# def winner(board):
#     """
#     Returns the winner of the game, if there is one. Else returns None.

#     """
def terminal(board):
    """
    Returns (is_game_over, winner, utility). is_game_over is a boolean. winner can be X, O, or None. Utility can be 1, 0, or -1.
    If is_game_over is False, winner will be None.
    Does not contain error checking for multiple winners. In this case, will return X as winner.
    Thus, this function is checked after every move and game ends if there is a winner, to prevent there from being two winners.
    """
    # Create 2 lists with locations of all Xs and Os on current board.
    Xs = []
    Os = []
    for row in range(BOARD_SIDE_LENGTH):
        for column in range(BOARD_SIDE_LENGTH):
            if board[row][column] == X:
                Xs.append((row, column))
            if board[row][column] == O:
                Os.append((row, column))

    # Check if either of the list Xs or Os contains all the elements of any of the winning combos
    # 'all' syntax checks if all the values in the list comprehension are True
    utility = 0
    winner = None
    for combo in WINNING_COMBOS:
        if all(cell in Xs for cell in combo):
            winner = X
            utility = 1
            break
        if all(cell in Os for cell in combo):
            winner = O
            utility = -1
            break

    if number_of_moves(board) == BOARD_SIDE_LENGTH**2 or winner != None:
        return True, winner, utility
    return False, winner, utility


def minimax(board, one_level_up_minmax=None):
    """
    Recursively returns the optimal action & the utility from that action for the current player on the board.
    Utility defined in range from 1 to -1, with 1 = 100% chance of winning for X, and -1 = 100% chance of winning for O.
    Returns None, utility if game is over.
    """
    # one_level_up_minmax argument = None (i.e. it is not passed) in initial function call in runner.py module.
    # This initialises the value based on who is the player at the time.
    # For recursive function calls resulting from this, value is passed (inherited from min/max of the one-level-up function call)

    # Sets first move for computer in a random corner. Otherwise, computer will always pick the first action in the set of actions.
    # This is because optimal tic-tac-toe play leads to the same outcome for all possible first actions i.e. a draw.
    # But corner plays are better as they give the opponent more chances to make a mistake.
    # Unfortunately, the computer doesn't consider this, so we hardcode it.
    if number_of_moves(board) == 0 and BOARD_SIDE_LENGTH == 3:
        random = randrange(4)
        if random == 0:
            return ((0, 0), None)
        if random == 1:
            return ((0, 2), None)
        if random == 2:
            return ((2, 0), None)
        if random == 3:
            return ((2, 2), None)

    who_is_playing = player(board)

    # Initialise one_level_up_minmax to not be binding if it is not provided.
    # e.g. if player is X, then set it as 2, since max can never be >= 2, so no alpha-beta pruning will occur on this level.
    if one_level_up_minmax == None:
        one_level_up_minmax = 2 if who_is_playing == X else -2

    utility = 0
    game_over, _, utility = terminal(board)
    if game_over:
        return None, utility

    # If only one possible action, return that action with associated utility
    possible_actions = actions(board)
    if len(possible_actions) == 1:
        action = possible_actions.pop()
        one_level_down_utility = terminal(result(board, action))[2]
        return action, one_level_down_utility

    # Otherwise, compare the various results to see which is best
    possible_results = {action: result(board, action) for action in possible_actions}
    if who_is_playing == X:
        # Initialise max utility to -2, so that the first result checked is certain to be better (range of utility is -1 to 1)
        # It will therefore update max to a new value between -1 and 1.
        max = -2
        best_action = ()
        for action, new_board in possible_results.items():
            # If a move exists to win, make it
            new_utility = terminal(new_board)[2]
            if new_utility == 1:
                return action, 1
        for action, new_board in possible_results.items():
            # Otherwise, recursively check utility of each possible action.
            new_utility = minimax(new_board, max)[1]
            if new_utility > max:
                max = new_utility
                best_action = action
            # Implement alpha-beta pruning based on the one-level-up's min value.
            # The concept is that if your current max utility is already greater/equal to the above level's (i.e. Player O's)
            # current min, then you can stop checking the rest of your actions, since Player O wouldn't choose this branch.
            if max >= one_level_up_minmax:
                break
        return best_action, max
    if who_is_playing == O:
        min = 2
        best_action = ()
        for action, new_board in possible_results.items():
            # If move exists to win, make it
            new_utility = terminal(new_board)[2]
            if new_utility == -1:
                return action, -1
            # Otherwise, recursively check utility of each possible action.
            new_utility = minimax(new_board, min)[1]
            if new_utility < min:
                min = new_utility
                best_action = action
            # Implement alpha-beta pruning based on the one-level-up's min value.
            # The concept is that if your current min utility is already lesser/equal to the above level's (i.e. Player X's)
            # current max, then you can stop checking the rest of your actions, since Player X wouldn't choose this branch.
            if min <= one_level_up_minmax:
                break
        return best_action, min


#Testing github
